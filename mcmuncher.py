#!/usr/bin/env python
import amulet
import mcfirefu
import mcfirefu.saves
import mcfirefu.coord_utils
from mcfirefu import warn, verbose

def trim_chunks(level, dimension, coords_file):
    warn("Dimension: ", dimension)
    coords_from_file = mcfirefu.coord_utils.get_coords_from_file(coords_file)

    verbose("Coords from file\n", coords_from_file)

    keep_chunks = mcfirefu.coord_utils.convert_coord_list_to_chunk_coords(coords_from_file)

    verbose("Max possible number of chunks to keep: ", len(keep_chunks))

    world_chunks_list = level.all_chunk_coords(dimension)

    verbose("Number of chunks in world file: ", len(world_chunks_list))

    # dict of world chunks keyed on stringified coords
    world_chunks = dict()
    for i in world_chunks_list:
        world_chunks.update({mcfirefu.coord_utils.key_from_coord_tuple(i): i})

    warn("Number of chunks in world file: ", len(world_chunks))

    for i in keep_chunks:
        world_chunks.pop(mcfirefu.coord_utils.key_from_coord_tuple(i), None)

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
    mcfirefu.parse_args();

    directory = mcfirefu.saves.select_directory()
    level = amulet.load_level(directory)

    if mcfirefu.args.keep_overworld:
        trim_chunks(level, "minecraft:overworld", mcfirefu.args.keep_overworld)

    if mcfirefu.args.keep_nether:
        trim_chunks(level, "minecraft:the_nether", mcfirefu.args.keep_nether)

    if mcfirefu.args.keep_end:
        trim_chunks(level, "minecraft:the_end", mcfirefu.args.keep_end)

    if mcfirefu.args.dryrun:
        warn("Dry Run - not saving changes")
    else:
        level.save()

    level.close()
    return

if __name__=="__main__":
    main()
