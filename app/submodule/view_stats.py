import amulet
import amulet.utils.world_utils
import argparse
import sys
import app
import app.saves
from app import warn
from app.pathtype import PathType

def get_help():
    return "Command to view various details about a world."

def add_arguments(parser):
    world = parser.add_mutually_exclusive_group(required=True)
    world.add_argument("--directory", type=PathType(exists=True, type='dir'), metavar='DIR', help="Path to world directory")
    world.add_argument("--bedrock", action=argparse.BooleanOptionalAction, help="List Bedrock game worlds, and prompt for selection")

    parser.add_argument("--extent", action=argparse.BooleanOptionalAction, help="Prints details on furthest explored chunks in each dimension")
    parser.add_argument("--bounds", action=argparse.BooleanOptionalAction, help="Prints info on dimension bounds - doesn't normally vary")
    parser.add_argument("--players", action=argparse.BooleanOptionalAction, help="Prints info on players - may output a lot of warnings!")
    return

def __report_max_chunks(chunks_list):
    if 0 == len(chunks_list):
        return

    min_x = None
    max_x = None
    min_z = None
    max_z = None

    for i in chunks_list:
        if min_x is None or i[0] < min_x:
            min_x = i[0]
        if max_x is None or i[0] > max_x:
            max_x = i[0]
        if min_z is None or i[1] < min_z:
            min_z = i[1]
        if max_z is None or i[1] > max_z:
            max_z = i[1]

    warn("Chunks span: East(%d), West(%d), North(%d), South(%d)" % (min_x, max_x, min_z, max_z))

    min_c_x = amulet.utils.world_utils.chunk_coords_to_block_coords(min_x, 0)[0]
    max_c_x = amulet.utils.world_utils.chunk_coords_to_block_coords(max_x, 0)[0] + 15
    min_c_z = amulet.utils.world_utils.chunk_coords_to_block_coords(0, min_z)[1]
    max_c_z = amulet.utils.world_utils.chunk_coords_to_block_coords(0, max_z)[1] + 15

    warn("Coords span: East(%d), West(%d), North(%d), South(%d)" % (min_c_x, max_c_x, min_c_z, max_c_z))
    return

def __view_stats(level):
    warn("")
    warn("level_path: %s" % level.level_path)
    warn("")

    dimensions = level.dimensions
    warn("Dimensions:")
    warn(dimensions)
    warn("")

    for i in dimensions:
        warn(i)
        world_chunks_list = level.all_chunk_coords(i)
        warn("%d chunks" % (len(world_chunks_list)))
        if app.args.extent:
            __report_max_chunks(world_chunks_list)
        if app.args.bounds:
            bounds = level.bounds(i)
            warn("bounds: %s" % bounds)
        warn("")

    if app.args.players:
        players = level.all_player_ids()
        warn("Players:")
        warn(players)
        warn("")

        for i in players:
            try:
                player = level.get_player(i)
            except:
                warn("Failed to retrieve player: %s" % i)
            else:
                warn("id: %s" % i)
                warn("dimension: %s" % str(player.dimension))
                warn("location: %s" % str(player.location))
                warn("rotation: %s" % str(player.rotation))
            warn("")

    return

def run(parser):
    directory = app.saves.select_directory(app.args.directory, app.args.bedrock)
    level = amulet.load_level(directory)

    __view_stats(level)

    level.close()
    return
