BASE = 586
ORIENTATION_ID = 586

def encode_worksheet_id(n: int):
    """Return tag IDs for TR, BR, BL given worksheet_id n."""
    if n >= BASE ** 3:
        raise ValueError(f"Max worksheet_id is {BASE**3 - 1}")
    ids = []
    for _ in range(3):
        ids.append(n % BASE)
        n //= BASE
    return ids  # [TR, BR, BL]


# -------------------------------------------------
# 2️⃣  Decode TR, BR, BL  →  worksheet_id
# -------------------------------------------------
def decode_from_tags(tr: int, br: int, bl: int):
    """Return worksheet_id from three tag IDs."""
    return tr + br * BASE + bl * (BASE ** 2)


# -------------------------------------------------
# 3️⃣  Helper: rotate list clockwise
# -------------------------------------------------
def rotate(lst, n):
    """Rotate list by n positions (clockwise)."""
    return lst[-n:] + lst[:-n]


# -------------------------------------------------
# 4️⃣  Main: find orientation + decode worksheet
# -------------------------------------------------
def detect_orientation_and_decode(tag_ids):
    """
    tag_ids: list of 4 detected tag IDs in clockwise order
             starting from any corner.
    Returns (worksheet_id, rotation_degrees)
    """
    for rot, degrees in enumerate([0, 90, 180, 270]):
        rotated = rotate(tag_ids, rot)
        if rotated[0] == ORIENTATION_ID:        # TL found
            tr, br, bl = rotated[1], rotated[2], rotated[3]
            worksheet_id = decode_from_tags(tr, br, bl)
            return worksheet_id, degrees
    return None, None  # orientation tag not found

# to make sure tags are clockwise, after detecting, arrange using tag position relative to centroid 
# for rotation-independent order

if __name__ == "__main__":
    worksheet_id = 2
    print(encode_worksheet_id(2))
