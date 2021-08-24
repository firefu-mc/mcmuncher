import re
import sys
from mcfirefu import warn, verbose

def key_from_coord_tuple(coords) -> "x,z":
    """
    Returns a string usable as a dict key,
    representing a [x,z] coord tuple
    """
    return str(coords[0]) + "," + str(coords[1])

def get_coords_from_file(file) -> "[[x,z],[x,z],...]":
    """
    Takes a path to a coordinate config file for a dimension.
    Returns to the list of coordinate rectangles that shouldn't be deleted
    """
    coords = []
    valid_rectangle = re.compile("^(-?\d+),(-?\d+)\s+(-?\d+),(-?\d+)$")

    for line in file:
        line = line.lstrip()
        if line.startswith("#"):
            # ignore comments
            continue
        line = line.rstrip()
        m = valid_rectangle.match(line)
        if m:
            coords.append([
                [
                    int(m.group(1)),
                    int(m.group(2)),
                ],
                [
                    int(m.group(3)),
                    int(m.group(4)),
                ],
            ])
        else:
            warn("Line didn't match expected format: ", line)
            sys.exit(1)

    return coords

def convert_coords_to_chunk_coords(coords) -> "[x,z]":
    """
    Converts a block coordinate [x,z] tuple into a chunk coordinate tuple [x,z]
    """
    x = coords[0] >> 4
    z = coords[1] >> 4
    return[x,z]

def expand_coord_corners(coords) -> "[[x,z],[x,z],...]":
    """
    Takes a list of 2 coordinate tuples [[x1,z1],[x2,z2]] corresponding to
    any 2 opposite corners of a rectangle.
    Expands this list to include all contained coordinates within this
    rectangle.
    Returns a list of coordinate tuples
    """
    x1 = min(coords[0][0], coords[1][0])
    x2 = max(coords[0][0], coords[1][0])

    z1 = min(coords[0][1], coords[1][1])
    z2 = max(coords[0][1], coords[1][1])

    verbose("Corner coords\n", coords)

    all_coords=[]
    for x in range(x1, x2+1): # range stops 1 short!
        for z in range(z1, z2+1): # range stops 1 short!
            all_coords.append([x, z])

    verbose("Expands to\n", all_coords)

    return all_coords

def convert_coord_list_to_chunk_coords(coord_corners):
    chunk_corners = []
    for i in coord_corners:
        chunk_corners.append([
            convert_coords_to_chunk_coords(i[0]),
            convert_coords_to_chunk_coords(i[1]),
        ])

    keep_chunks = []
    for i in chunk_corners:
        keep_chunks.extend(expand_coord_corners(i))

    # remove duplicate pairs
    seen_chunk = dict()
    for i in keep_chunks:
        seen_chunk.update({key_from_coord_tuple(i): i})

    return list(seen_chunk.values())
