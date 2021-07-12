#!/usr/bin/env python

import argparse
import math
import os
import re
import sys
import amulet
from mcmuncher_utils import PathType

__version__ = 1.0

dimensions = {
    "overworld": "minecraft:overworld",
    "nether": "minecraft:the_nether",
    "end":  "minecraft:the_end",
}

args = None

def warn(*msg):
    msg = "".join(map(str, msg))

    sys.stderr.write(msg + os.linesep)

def verbose(*msg):
    if args.verbose:
        warn(*msg)

def parse_args() -> argparse.Namespace:
    global args

    parser = argparse.ArgumentParser()
    parser.add_argument("world_directory", type=PathType(exists=True, type='dir'), metavar='world-directory', help="Path to world directory")
    parser.add_argument("--keep-overworld", type=argparse.FileType('r', encoding='UTF-8'), metavar="FILE")
    parser.add_argument("--keep-nether", type=argparse.FileType('r', encoding='UTF-8'), metavar="FILE")
    parser.add_argument("--keep-end", type=argparse.FileType('r', encoding='UTF-8'), metavar="FILE")
    parser.add_argument("--dryrun", action=argparse.BooleanOptionalAction, help="Print what would happen, but don't save the changes")
    parser.add_argument("--verbose", action=argparse.BooleanOptionalAction, help="Print lots of information about which chunks are being selected")
    parser.add_argument("--version", action="version", version='McMuncher ' + str(__version__))
    args = parser.parse_args()

    if not args.keep_overworld and not args.keep_nether and not args.keep_end:
        warn("error: Require at least 1 of --keep-overworld=FILE, --keep-nether=FILE or --keep-end=FILE options\n")
        parser.print_help()
        sys.exit(1)

    return

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
    x=math.floor(coords[0]/16)
    z=math.floor(coords[1]/16)
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

def trim_chunks(level, dimension, coords_file):
    warn("Dimension: ", dimension)
    dimension = dimensions[dimension]
    coords_from_file = get_coords_from_file(coords_file)

    verbose("Coords from file\n", coords_from_file)

    keep_chunks = convert_coord_list_to_chunk_coords(coords_from_file)

    verbose("Max possible number of chunks to keep: ", len(keep_chunks))

    world_chunks_list = level.all_chunk_coords(dimension)

    verbose("Number of chunks in world file: ", len(world_chunks_list))

    # dict of world chunks keyed on stringified coords
    world_chunks = dict()
    for i in world_chunks_list:
        world_chunks.update({key_from_coord_tuple(i): i})

    warn("Number of chunks in world file: ", len(world_chunks))

    for i in keep_chunks:
        world_chunks.pop(key_from_coord_tuple(i), None)

    # everything remaining in dict needs to be deleted
    verbose("Going to delete number of chunks: ", len(world_chunks))

    delete_counter = 0
    for i in world_chunks.values():
        level.delete_chunk(i[0], i[1], dimension)
        delete_counter+=1

    warn("Deleted number of chunks: ", delete_counter)

    warn("Number of chunks remaining in world: ", len(level.all_chunk_coords(dimension)))

    return

def main():
    parse_args();
    level = amulet.load_level(args.world_directory)

    if args.keep_overworld:
        trim_chunks(level, "overworld", args.keep_overworld)

    if args.keep_nether:
        trim_chunks(level, "nether", args.keep_nether)

    if args.keep_end:
        trim_chunks(level, "end", args.keep_end)

    if args.dryrun:
        warn("Dry Run - not saving changes")
    else:
        level.save()

    level.close()
    return

if __name__=="__main__":
    main()
