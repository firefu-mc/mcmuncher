import amulet
import argparse
import sys
import app
import app.saves
import app.coord_utils
from app import warn, verbose
from app.pathtype import PathType

def get_help():
    return "Command to trim chunks from world dimensions - deleting any chunks you don't want."

def add_arguments(parser):
    world = parser.add_mutually_exclusive_group(required=True)
    world.add_argument("--directory", type=PathType(exists=True, type='dir'), metavar='DIR', help="Path to world directory")
    world.add_argument("--bedrock", action=argparse.BooleanOptionalAction, help="List Bedrock game worlds, and prompt for selection")

    parser.add_argument("--keep-overworld", type=argparse.FileType('r', encoding='UTF-8'), metavar="FILE")
    parser.add_argument("--keep-nether", type=argparse.FileType('r', encoding='UTF-8'), metavar="FILE")
    parser.add_argument("--keep-end", type=argparse.FileType('r', encoding='UTF-8'), metavar="FILE")
    parser.add_argument("--dryrun", "--dry-run", action=argparse.BooleanOptionalAction, help="Print what would happen, but don't save the changes")
    parser.add_argument("--verbose", action=argparse.BooleanOptionalAction, help="Print lots of information about which chunks are being selected")
    return

def __validate_args():
    if not app.args.keep_overworld and not app.args.keep_nether and not app.args.keep_end:
        warn("error: Require at least 1 of --keep-overworld=FILE, --keep-nether=FILE or --keep-end=FILE options\n")
        parser.print_help()
        sys.exit(1)
    return

def __trim_chunks(level, dimension, coords_file):
    warn("Dimension: ", dimension)
    coords_from_file = app.coord_utils.get_coords_from_file(coords_file)

    verbose("Coords from file\n", coords_from_file)

    keep_chunks = app.coord_utils.convert_coord_list_to_chunk_coords(coords_from_file)

    verbose("Max possible number of chunks to keep: ", len(keep_chunks))

    world_chunks_list = level.all_chunk_coords(dimension)

    verbose("Number of chunks in world file: ", len(world_chunks_list))

    # dict of world chunks keyed on stringified coords
    world_chunks = dict()
    for i in world_chunks_list:
        world_chunks.update({app.coord_utils.key_from_coord_tuple(i): i})

    warn("Number of chunks in world file: ", len(world_chunks))

    for i in keep_chunks:
        world_chunks.pop(app.coord_utils.key_from_coord_tuple(i), None)

    # everything remaining in dict needs to be deleted
    verbose("Going to delete number of chunks: ", len(world_chunks))

    delete_counter = 0
    for i in world_chunks.values():
        level.delete_chunk(i[0], i[1], dimension)
        delete_counter+=1

    warn("Deleted number of chunks: ", delete_counter)

    warn("Number of chunks remaining in world: ", len(level.all_chunk_coords(dimension)))
    return

def run():
    __validate_args()

    directory = app.saves.select_directory(app.args.directory, app.args.bedrock)
    level = amulet.load_level(directory)

    if app.args.keep_overworld:
        __trim_chunks(level, "minecraft:overworld", app.args.keep_overworld)

    if app.args.keep_nether:
        __trim_chunks(level, "minecraft:the_nether", app.args.keep_nether)

    if app.args.keep_end:
        __trim_chunks(level, "minecraft:the_end", app.args.keep_end)

    if app.args.dryrun:
        warn("Dry Run - not saving changes")
    else:
        level.save()

    level.close()
    return
