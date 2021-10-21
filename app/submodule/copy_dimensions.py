import amulet
import argparse
import sys
import app
import app.saves
import app.chunk_utils
from app import warn
from app.pathtype import PathType

def get_help():
    return "Command to copy dimensions from 1 world to another."

def add_arguments(parser):
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--source-directory", type=PathType(exists=True, type='dir'), metavar='DIR', help="Path to source world directory - containing the dimension(s) to be copied")
    source.add_argument("--source-bedrock", action=argparse.BooleanOptionalAction, help="List Bedrock game worlds, and prompt for selection for source world - containing the dimension(s) to be copied")

    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--target-directory", type=PathType(exists=True, type='dir'), metavar='DIR', help="Path to target world directory - where the dimension(s) will be copied to")
    target.add_argument("--target-bedrock", action=argparse.BooleanOptionalAction, help="List Bedrock game worlds, and prompt for selection for target world - where the dimension(s) will be copied to")

    overworld = parser.add_mutually_exclusive_group()
    overworld.add_argument("--replace-overworld", action=argparse.BooleanOptionalAction, help="Delete the Overworld in the target world before copying the Overworld from the source world")
    overworld.add_argument("--merge-overworld", action=argparse.BooleanOptionalAction, help="Copy the Overworld from the source world into the target world")

    nether = parser.add_mutually_exclusive_group()
    nether.add_argument("--replace-nether", action=argparse.BooleanOptionalAction, help="Delete the Nether in the target world before copying the Nether from the source world")
    nether.add_argument("--merge-nether", action=argparse.BooleanOptionalAction, help="Copy the Nether from the source world into the target world")

    end = parser.add_mutually_exclusive_group()
    end.add_argument("--replace-end", action=argparse.BooleanOptionalAction, help="Delete the End in the target world before copying the End from the source world")
    end.add_argument("--merge-end", action=argparse.BooleanOptionalAction, help="Copy the End from the source world into the target world")

    parser.add_argument("--dryrun", "--dry-run", action=argparse.BooleanOptionalAction, help="Print what would happen, but don't save the changes")
    parser.add_argument("--verbose", action=argparse.BooleanOptionalAction, help="Print extra information about what is happening")
    return

def __validate_args():
    if not app.args.replace_overworld and not app.args.merge_overworld and not app.args.replace_nether and not app.args.merge_nether and not app.args.replace_end and not app.args.merge_nether:
        warn("error: Require at least 1 of --replace-overworld, --merge-overworld, --replace-nether, --merge-nether, --replace-end or --merge-end options\n")
        parser.print_help()
        sys.exit(1)
    return

def run():
    __validate_args()

    source_directory = app.saves.select_directory(app.args.source_directory, app.args.source_bedrock, "Enter the number of the source world")
    target_directory = app.saves.select_directory(app.args.target_directory, app.args.target_bedrock, "Enter the number of the target world")
    source_level = amulet.load_level(source_directory)
    target_level = amulet.load_level(target_directory)

    if app.args.replace_overworld:
        app.chunk_utils.replace_dimension(source_level, target_level, "minecraft:overworld")
    elif app.args.merge_overworld:
        app.chunk_utils.merge_dimension(source_level, target_level, "minecraft:overworld")

    if app.args.replace_nether:
        app.chunk_utils.replace_dimension(source_level, target_level, "minecraft:the_nether")
    elif app.args.merge_nether:
        app.chunk_utils.merge_dimension(source_level, target_level, "minecraft:the_nether")

    if app.args.replace_end:
        app.chunk_utils.replace_dimension(source_level, target_level, "minecraft:the_end")
    elif app.args.merge_end:
        app.chunk_utils.merge_dimension(source_level, target_level, "minecraft:the_end")

    if app.args.dryrun:
        warn("Dry Run - not saving changes")
    else:
        target_level.save()

    source_level.close()
    target_level.close()
    return
