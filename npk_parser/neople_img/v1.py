from util import stream
from config import Struct


def parse(npk_file, offset, size):
    npk_file.seek(offset + 24)
    index_size = stream.read_struct(npk_file, Struct['INT'])
    index_num = stream.read_struct(npk_file, Struct['INT'])

    textures = []
    for i in range(index_num):
        texture = {}
        textures.append(texture)

        texture['dw_type'] = stream.read_struct(npk_file, Struct['INT'])
        texture['dw_compress'] = stream.read_struct(npk_file, Struct['INT'])
        if texture['dw_compress'] == '\x11':
            continue

        texture['width'] = stream.read_struct(npk_file, Struct['INT'])
        texture['height'] = stream.read_struct(npk_file, Struct['INT'])
        texture['size'] = stream.read_struct(npk_file, Struct['INT'])
        texture['key_x'] = stream.read_struct(npk_file, Struct['INT'])
        texture['key_y'] = stream.read_struct(npk_file, Struct['INT'])
        texture['max_width'] = stream.read_struct(npk_file, Struct['INT'])
        texture['max_height'] = stream.read_struct(npk_file, Struct['INT'])
        texture['data'] = npk_file.read(texture['size'])
    return textures
