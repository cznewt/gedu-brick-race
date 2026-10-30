"""Render LDraw/MPD text to PNG with three.js LDrawLoader in headless Chromium.

The part library comes from the local cache (served over HTTP), so renders do not
depend on the CDN. Usage from Python: render(mpd_text, out_png, azimuth, elevation).
"""
import asyncio
import functools
import http.server
import json
import os
import socketserver
import threading

from playwright.async_api import async_playwright

import ldr

HTML = r"""<!doctype html><html><head><meta charset="utf-8">
<style>html,body{margin:0;background:#fff}canvas{display:block}</style>
<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}</script>
</head><body><script type="module">
import * as THREE from 'three';
import { LDrawLoader } from 'three/addons/loaders/LDrawLoader.js';
window.renderModel = async (text, opts) => {
  const W = opts.width, H = opts.height;
  const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true, alpha: true });
  renderer.setPixelRatio(1); renderer.setSize(W, H); renderer.setClearColor(0xffffff, opts.transparent ? 0 : 1);
  document.body.innerHTML = ''; document.body.appendChild(renderer.domElement);
  const scene = new THREE.Scene();
  scene.add(new THREE.AmbientLight(0xffffff, 1.1));
  const key = new THREE.DirectionalLight(0xffffff, 1.6); key.position.set(-1, 2, 1.5); scene.add(key);
  const fill = new THREE.DirectionalLight(0xffffff, 0.6); fill.position.set(1, 0.5, -1); scene.add(fill);
  const loader = new LDrawLoader();
  loader.smoothNormals = true;
  if (opts.packed) {
    loader.setPartsLibraryPath('http://127.0.0.1:9/no-library/');   // a packed model must not need it
  } else {
    loader.setPartsLibraryPath(opts.lib);
    await loader.preloadMaterials(opts.lib + 'LDConfig.ldr');
  }
  const url = URL.createObjectURL(new Blob([text], { type: 'text/plain' }));
  const group = await new Promise((res, rej) => loader.load(url, res, undefined, rej));
  group.rotation.x = Math.PI;
  if (opts.maskFrom !== undefined) {
    // instruction masks: the parts from index maskFrom on in flat black, the older ones in
    // flat white (they still hide what is behind them), no lighting, no edge lines
    const white = new THREE.MeshBasicMaterial({ color: 0xffffff }), black = new THREE.MeshBasicMaterial({ color: 0x000000 });
    group.children.forEach((child, i) => child.traverse((o) => {
      if (o.isLineSegments) o.visible = false;
      else if (o.isMesh) o.material = i >= opts.maskFrom ? black : white;
    }));
    window.lastChildren = group.children.length;
  }
  scene.add(group);
  const box = new THREE.Box3().setFromObject(group);
  const c = box.getCenter(new THREE.Vector3()), s = box.getSize(new THREE.Vector3());
  const r = (opts.radius || s.length() / 2) * (opts.zoom || 1);
  const az = opts.azimuth * Math.PI / 180, el = opts.elevation * Math.PI / 180;
  const fov = 22, dist = r / Math.sin(fov * Math.PI / 360);
  const cam = new THREE.PerspectiveCamera(fov, W / H, dist / 50, dist * 10);
  const target = opts.target ? new THREE.Vector3(...opts.target) : c;
  cam.position.set(target.x + dist * Math.cos(el) * Math.sin(az), target.y + dist * Math.sin(el), target.z + dist * Math.cos(el) * Math.cos(az));
  cam.lookAt(target);
  renderer.render(scene, cam);
  return renderer.domElement.toDataURL('image/png');
};
window.ready = true;
</script></body></html>"""


class _Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


_SERVER = None


def _serve():
    global _SERVER
    if _SERVER:
        return _SERVER
    os.makedirs(ldr.CACHE, exist_ok=True)
    ldconfig = os.path.join(ldr.CACHE, "LDConfig.ldr")
    if not os.path.exists(ldconfig):
        import urllib.request
        data = urllib.request.urlopen(ldr.LIBS[0] + "LDConfig.ldr", timeout=60).read()
        ldr.write_atomic(ldconfig, data)
    ldr.write_atomic(os.path.join(ldr.CACHE, "render.html"), HTML.encode())
    handler = functools.partial(_Quiet, directory=ldr.CACHE)
    srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    _SERVER = srv
    return srv


def prefetch(mpd_text):
    """Make sure every part the model uses (and their subfiles) is in the cache."""
    names = set()
    embedded = {l[7:].strip().lower() for l in mpd_text.splitlines() if l.startswith("0 FILE ")}
    for line in mpd_text.splitlines():
        f = line.split()
        if len(f) >= 15 and f[0] == "1":
            n = " ".join(f[14:]).lower()
            if n not in embedded:
                names.add(n)
    for n in names:
        ldr.flatten(n)


async def _render_many(jobs):
    srv = _serve()
    lib = f"http://127.0.0.1:{srv.server_address[1]}/"
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"])
        pg = await b.new_page(viewport={"width": 1200, "height": 900})
        await pg.goto(lib + "render.html")
        await pg.wait_for_function("window.ready === true", timeout=60000)
        for text, out, opts in jobs:
            o = {"width": 900, "height": 640, "lib": lib, "azimuth": -45, "elevation": 30}
            o.update(opts)
            data = await pg.evaluate("([t, o]) => window.renderModel(t, o)", [text, o])
            if "maskFrom" in o and "expectChildren" in o:
                got = await pg.evaluate("window.lastChildren")
                assert got == o["expectChildren"], f"{out}: {got} children, expected {o['expectChildren']}"
            import base64
            open(out, "wb").write(base64.b64decode(data.split(",", 1)[1]))
        await b.close()


def render(jobs):
    """jobs: list of (mpd_text, out_png, opts)."""
    for text, _, _ in jobs:
        prefetch(text)
    asyncio.run(_render_many(jobs))
