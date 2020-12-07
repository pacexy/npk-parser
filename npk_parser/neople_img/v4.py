from util import stream

from config import Struct
from neople_img.utils import calc_texture_offset


def parse(npk_file, offset, size):
    npk_file.seek(offset + 16)
    index_table_size = stream.read_struct(npk_file, Struct['INT'])
    stream.read_struct(npk_file, Struct['INT'])
    version = stream.read_struct(npk_file, Struct['INT'])
    index_num = stream.read_struct(npk_file, Struct['INT'])
    color_num = stream.read_struct(npk_file, Struct['INT'])
    color_data = stream.read_struct(npk_file, color_num * Struct['INT'])

    textures = []
    for i in range(index_num):
        texture = {}
        textures.append(texture)
        texture['color_model'] = stream.read_struct(npk_file, Struct['INT'])
        # 0x11 Reference
        if texture['color_model'] == 0x11:
            texture['frame_ref_num'] = stream.read_struct(npk_file,
                                                          Struct['INT'])
        # 0x0E ABGR8888
        elif texture['color_model'] == 0x0E:
            texture['compress_state'] = stream.read_struct(npk_file,
                                                           Struct['INT'])
            texture['width'] = stream.read_struct(npk_file, Struct['INT'])
            texture['height'] = stream.read_struct(npk_file, Struct['INT'])
            texture['size'] = stream.read_struct(npk_file, Struct['INT'])
            texture['key_x'] = stream.read_struct(npk_file, Struct['INT'])
            texture['key_y'] = stream.read_struct(npk_file, Struct['INT'])
            texture['max_width'] = stream.read_struct(npk_file, Struct['INT'])
            texture['max_height'] = stream.read_struct(npk_file, Struct['INT'])

            texture_offset = calc_texture_offset(textures, offset,
                                                 index_table_size)
            texture['data'] = stream.read_range(npk_file, texture_offset,
                                                texture['size'])
        else:
            raise Exception('Invalid Color Model' + texture['color_model'])

    return textures
