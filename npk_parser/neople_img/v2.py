from random import randrange
import zlib
import cv2
import numpy as np

from util import stream
from config import Struct


def parse(npk_file, offset, size):
    npk_file.seek(offset + 16)
    index_table_size = stream.read_struct(npk_file, Struct['INT'])
    stream.read_struct(npk_file, Struct['INT'])
    version = stream.read_struct(npk_file, Struct['INT'])
    index_num = stream.read_struct(npk_file, Struct['INT'])

    textures = []
    for i in range(index_num):
        texture = {}
        textures.append(texture)
        texture['color_model'] = stream.read_struct(npk_file, Struct['INT'])
        # 0x11 Reference
        if texture['color_model'] == 0x11:
            texture['frame_ref_num'] = stream.read_struct(npk_file,
                                                          Struct['INT'])
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
            texture['frame_width'] = stream.read_struct(npk_file, Struct['INT'])
            texture['frame_height'] = stream.read_struct(npk_file,
                                                         Struct['INT'])
        else:
            raise Exception(
                'Invalid Color Model: ' + str(texture['color_model']))

    random_key = randrange(100)

    for i, texture in enumerate(textures):
        raw_data = npk_file.read(texture['size'])
        data = raw_data
        if texture['compress_state'] == 0x06:
            data = zlib.decompress(raw_data)
        elif texture['compress_state'] != 0x05:
            raise Exception('Invalid Compress State')
        bytes_in_data = [byte for byte in data]
        pixel_mat = np.array(bytes_in_data).reshape(texture['height'],
                                                    texture['width'],
                                                    4)
        cv2.imwrite(f'./img/{random_key}-{i}.png', pixel_mat)
        texture['data'] = data

    return textures
