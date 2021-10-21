from app import warn, verbose

def delete_dimension(level, dimension):
    world_chunks_list = level.all_chunk_coords(dimension)

    verbose("Number of chunks to delete: ", len(world_chunks_list))

    for i in world_chunks_list:
        level.delete_chunk(i[0], i[1], dimension)

    return

def replace_dimension(source_level, target_level, dimension):
    warn("Dimension: ", dimension)

    delete_dimension(target_level, dimension)

    world_chunks_list = source_level.all_chunk_coords(dimension)

    verbose("Number of chunks in source world: ", len(world_chunks_list))

    for i in world_chunks_list:
        chunk = source_level.get_chunk(i[0], i[1], dimension)

        target_level.put_chunk(chunk, dimension)

    verbose("Copied chunks to %s" % dimension)

    return

def merge_dimension(source_level, target_level, dimension):
    warn("Dimension: ", dimension)

    world_chunks_list = source_level.all_chunk_coords(dimension)

    verbose("Number of chunks in source world: ", len(world_chunks_list))

    for i in world_chunks_list:
        target_level.delete_chunk(i[0], i[1], dimension)

        chunk = source_level.get_chunk(i[0], i[1], dimension)

        target_level.put_chunk(chunk, dimension)

    verbose("Copied chunks to %s" % dimension)

    return
