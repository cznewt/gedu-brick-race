"""LDraw colour codes -> BrickLink colour ids, and BrickLink colour names/swatches."""

LDRAW_TO_BL = {
    0: 11, 1: 7, 2: 6, 3: 39, 4: 5, 5: 47, 6: 8, 7: 9, 8: 10, 9: 62,
    10: 36, 11: 41, 12: 25, 13: 23, 14: 3, 15: 1, 17: 38, 18: 33, 19: 2,
    20: 44, 22: 24, 25: 4, 26: 71, 27: 34, 28: 69, 29: 17, 36: 17,
    70: 88, 71: 86, 72: 85, 73: 42, 74: 37, 77: 100, 78: 90, 79: 60, 80: 67,
    84: 150, 85: 89, 86: 91, 92: 28, 226: 103, 272: 63, 288: 80, 308: 120,
    320: 59, 322: 156, 326: 158, 366: 29, 484: 27, 503: 49,
}

BL_COLORS = {
    0: ("(any colour)", "#cccccc"), 1: ("White", "#ffffff"), 2: ("Tan", "#e4cd9e"),
    3: ("Yellow", "#f2cd37"), 4: ("Orange", "#fe8a18"), 5: ("Red", "#c91a09"),
    6: ("Green", "#237841"), 7: ("Blue", "#0055bf"), 8: ("Brown", "#583927"),
    9: ("Light Gray", "#9ba19d"), 10: ("Dark Gray", "#6d6e5c"), 11: ("Black", "#1b2a34"),
    36: ("Bright Green", "#4b9f4a"), 42: ("Medium Blue", "#5a93db"), 63: ("Dark Blue", "#0a3463"),
    85: ("Dark Bluish Gray", "#595d60"), 86: ("Light Bluish Gray", "#afb5c7"),
    88: ("Reddish Brown", "#582a12"), 69: ("Dark Tan", "#958a73"), 59: ("Dark Red", "#720e0f"),
    103: ("Bright Light Yellow", "#fff03a"), 34: ("Lime", "#bbe90b"), 156: ("Medium Azure", "#36aebf"),
    158: ("Yellowish Green", "#dfeea5"), 25: ("Salmon", "#f2705e"), 67: ("Metallic Silver", "#a5a9b4"),
    17: ("Trans-Red", "#c91a09"),
}


def bl_color(ldraw_code):
    return LDRAW_TO_BL.get(int(ldraw_code), 0)


def color_name(bl_id):
    return BL_COLORS.get(int(bl_id or 0), (f"Colour {bl_id}", "#cccccc"))[0]


def color_hex(bl_id):
    return BL_COLORS.get(int(bl_id or 0), (f"Colour {bl_id}", "#cccccc"))[1]
