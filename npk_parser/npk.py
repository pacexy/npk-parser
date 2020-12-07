from util import byte, stream

from config import Struct, NPK_SIGNATURE,  KEY
from neople_img import main as neople_img


def parse(file):
    with open(file, 'rb') as npk_file:
        file_signature = npk_file.read(16).decode()
        if file_signature != NPK_SIGNATURE:
            raise Exception('Invalid NPK file')

        img_num = stream.read_struct(npk_file, Struct['INT'])
        # parse imgs
        imgs = []
        for i in range(img_num):
            offset = stream.read_struct(npk_file, Struct['INT'])
            size = stream.read_struct(npk_file, Struct['INT'])
            name_in_bytes = byte.xor(npk_file.read(256), KEY)
            print(name_in_bytes)
            name = name_in_bytes.decode().split('\x00')[0]

            current = npk_file.tell()
            textures = neople_img.parse(npk_file, offset, size)
            npk_file.seek(current)
            
            imgs.append({
                'offset': offset,
                'size': size,
                'name': name,
                'textures': textures
            })

        return {
            'imgs': imgs
        }


parse('./npk/sprite_character_challenge2nd_swordman_darkknight.NPK')
