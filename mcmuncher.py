#!/usr/bin/env python

import argparse
from datetime import datetime
import os
from pathlib import Path
import re
import sys
import amulet
from mcmuncher_utils import PathType

__version__ = 2.0

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
    parser.add_argument("--directory", type=PathType(exists=True, type='dir'), metavar='DIR', help="Path to world directory")
    parser.add_argument("--bedrock", action=argparse.BooleanOptionalAction, help="List Bedrock game worlds, and prompt for selection")
    parser.add_argument("--keep-overworld", type=argparse.FileType('r', encoding='UTF-8'), metavar="FILE")
    parser.add_argument("--keep-nether", type=argparse.FileType('r', encoding='UTF-8'), metavar="FILE")
    parser.add_argument("--keep-end", type=argparse.FileType('r', encoding='UTF-8'), metavar="FILE")
    parser.add_argument("--dryrun", action=argparse.BooleanOptionalAction, help="Print what would happen, but don't save the changes")
    parser.add_argument("--verbose", action=argparse.BooleanOptionalAction, help="Print lots of information about which chunks are being selected")
    parser.add_argument("--version", action="version", version='McMuncher ' + str(__version__))
    args = parser.parse_args()

    if not args.directory and not args.bedrock:
        warn("error: Require 1 of --directory=DIR or --bedrock")
        parser.print_help()
        sys.exit(1)

    if args.directory and args.bedrock:
        warn("error: Cannot provide both --directory=DIR and --bedrock")
        parser.print_help()
        sys.exit(1)

    if not args.keep_overworld and not args.keep_nether and not args.keep_end:
        warn("error: Require at least 1 of --keep-overworld=FILE, --keep-nether=FILE or --keep-end=FILE options\n")
        parser.print_help()
        sys.exit(1)

    return

def get_bedrock_worlds_dir():
    if sys.platform != "win32":
        raise Exception("get_bedrock_worlds_dir is only available on Windows OS")

    return os.path.join(
        os.getenv("LOCALAPPDATA"),
        "Packages",
        "Microsoft.MinecraftUWP_8wekyb3d8bbwe",
        "LocalState",
        "games",
        "com.mojang",
        "minecraftWorlds",
    )

def select_bedrock_directory():
    """
    Loosely based on amulet_map_editor/api/wx/ui/select_world.py
    in project https://github.com/Amulet-Team/Amulet-Map-Editor/

    Prompts user for an installed world in users's Bedrock worlds directory.
    Returns directory path as string.
    """
    worlds_dir = Path(get_bedrock_worlds_dir())
    world_formats = []
    for item in worlds_dir.iterdir():
        if os.path.isdir(item):
            format = None
            try:
                world_formats.append(amulet.load_format(item))
            except FormatError as e:
                warn(f"Could not find loader for {item} {e}")
            except Exception:
                warn(f"Error loading format wrapper for {item} {traceback.format_exc()}")

    world_formats = list(reversed(sorted(world_formats, key=lambda f: f.last_played)))
    counter = 0
    for item in world_formats:
        # add 1 to counter so we're not showing the user a zero-indexed list
        print("[{:d}] {:s} - {:s}".format(counter+1, datetime.utcfromtimestamp(int(item.last_played)).strftime('%Y-%m-%d %H:%M:%S'), item.level_name))
        counter+=1
    select = int(input("Enter the number of the world you want to edit: "))
    # subtract 1 from input
    world = world_formats[select-1]
    print("Selected: [{:d}] {:s}".format(select, world.level_name))

    return world.path

def select_directory():
    if args.directory:
        return args.directory
    elif args.bedrock:
        return select_bedrock_directory()
    else:
        raise Exception("Unknown type of directory to search")

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

    directory = select_directory()
    level = amulet.load_level(directory)

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
