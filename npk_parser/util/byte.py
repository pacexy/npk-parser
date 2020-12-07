def pad_end(raw_bytes, target_len, byte):
    raw_len = len(raw_bytes)
    len_diff = target_len - raw_len
    raw_bytes += byte * len_diff

    return raw_bytes


def xor(bytes1, bytes2):
    target_len = len(bytes2)
    padded_bytes = pad_end(bytes1, target_len, b'\x00')

    result = [0] * target_len
    for i in range(target_len):
        result[i] = padded_bytes[i] ^ bytes2[i]

    return bytes(result)


KEY = bytes(f'puchikon@neople dungeon and fighter {("DNF" * 73)}\x00', 'ascii')
# FILE_NAME = 'set01.img'.encode('euc_kr')
FILE_NAME = b"\x03\x05\x11\x01\x1d\x0e@\r(\x0f\x17\x0e\x13\x18\x00RK\x16\x06\x06\t\x03\x0bN\x06\x0bVN\x02F\x17\x1a\x1d\x00\x01Tk#/7:4!=5k=#0~wj'+#NFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNF\x00"

xorred_string = xor(FILE_NAME,
                          KEY).decode()
print(xorred_string.split('\x00')[0])
