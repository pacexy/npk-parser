from util import stream
from config import Struct
from neople_img.utils import calc_texture_offset


def parse(npk_file, offset, size):
    npk_file.seek(offset + 16)
    index_table_size = stream.read_struct(npk_file, Struct['INT'])
    stream.read_struct(npk_file, Struct['INT'])
    version = stream.read_struct(npk_file, Struct['INT'])
    index_num = stream.read_struct(npk_file, Struct['INT'])
    dds_index_num = stream.read_struct(npk_file, Struct['INT'])
    size = stream.read_struct(npk_file, Struct['INT'])
    color_num = stream.read_struct(npk_file, Struct['INT'])
    color_data = stream.read_struct(npk_file, color_num * Struct['INT'])

    for i in range(dds_index_num):
        # 0x01
        dds_index_header = stream.read_struct(npk_file, Struct['INT'])
        dds_texture_compression_format = stream.read_struct(npk_file,
                                                            Struct['INT'])
        dds_serial_num = stream.read_struct(npk_file, Struct['INT'])
        dds_size_before_compression = stream.read_struct(npk_file,
                                                         Struct['INT'])
        dds_size = stream.read_struct(npk_file, Struct['INT'])
        dds_width = stream.read_struct(npk_file, Struct['INT'])
        dds_height = stream.read_struct(npk_file, Struct['INT'])

    textures = []
    for i in range(index_num):
        texture = {}
        textures.append(texture)
        texture['color_model'] = stream.read_struct(npk_file, Struct['INT'])
        # 0x11 Reference
        if texture['color_model'] == 0x11:
            texture['frame_ref_num'] = stream.read_struct(npk_file, Struct['INT'])
        # 0x10 ARGB8888
        # 0x0F ARGB4444
        # 0x0E ARGB1555
        elif texture['color_model'] in [0x10, 0x0F, 0x0E]:
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
        # 0x12 DXT1
        # 0x13 DXT3
        # 0x14 DXT5
        elif texture['color_model'] in [0x12, 0x13, 0x14]:
            texture['compress_state'] = stream.read_struct(npk_file,
                                                           Struct['INT'])
            texture['width'] = stream.read_struct(npk_file, Struct['INT'])
            texture['height'] = stream.read_struct(npk_file, Struct['INT'])
            stream.read_struct(npk_file, Struct['INT'])
            texture['key_x'] = stream.read_struct(npk_file, Struct['INT'])
            texture['key_y'] = stream.read_struct(npk_file, Struct['INT'])
            texture['frame_width'] = stream.read_struct(npk_file, Struct['INT'])
            texture['frame_height'] = stream.read_struct(npk_file,
                                                         Struct['INT'])
            stream.read_struct(npk_file, Struct['INT'])
            texture['dds_ref_num'] = stream.read_struct(npk_file,
                                                               Struct['INT'])
            texture['left'] = stream.read_struct(npk_file, Struct['INT'])
            texture['top'] = stream.read_struct(npk_file, Struct['INT'])
            texture['right'] = stream.read_struct(npk_file, Struct['INT'])
            texture['bottom'] = stream.read_struct(npk_file, Struct['INT'])
            stream.read_struct(npk_file, Struct['INT'])

            texture_offset = calc_texture_offset(textures, offset,
                                                 index_table_size)
            texture['data'] = stream.read_range(npk_file, texture_offset,
                                                texture['size'])
        else:
            raise Exception('Invalid Color Model: ' + texture['color_model'])

    return textures
