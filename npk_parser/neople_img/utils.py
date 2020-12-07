def calc_texture_offset(textures, offset, index_table_size):
    texture_offset = offset + index_table_size
    for i in range(len(textures)):
        texture_offset += textures[i]['size']
    return texture_offset
