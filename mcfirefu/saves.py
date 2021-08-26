import amulet
from datetime import datetime
from pathlib import Path
import os
import sys
import mcfirefu
from mcfirefu import warn

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

def select_directory(directory, bedrock):
    if directory:
        return directory
    elif bedrock:
        return select_bedrock_directory()
    else:
        raise Exception("Unknown type of directory to search")
