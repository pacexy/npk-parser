from util import stream

from config import Struct, IMAGE_SIGNATURE, IMG_SIGNATURE
from neople_img import v1, v2, v4, v5, v6


def parse(npk_file, offset, size):
    texture_signature_10 = stream.read_range(npk_file, offset, 10).decode()
    if texture_signature_10 == IMAGE_SIGNATURE[:10]:
        return v1.parse(npk_file, offset, size)
    elif texture_signature_10 == IMG_SIGNATURE[:10]:
        npk_file.seek(offset + 16)
        index_size = stream.read_struct(npk_file, Struct['INT'])
        stream.read_struct(npk_file, Struct['INT'])
        version = stream.read_struct(npk_file, Struct['INT'])
        if version == 2:
            return v2.parse(npk_file, offset, size)
        elif version == 4:
            return v4.parse(npk_file, offset, size)
        elif version == 5:
            return v5.parse(npk_file, offset, size)
        elif version == 6:
            return v6.parse(npk_file, offset, size)
        else:
            raise Exception('Invalid IMG Version')
    else:
        raise Exception('Invalid Neople IMG')
