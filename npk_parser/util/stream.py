import struct


def read_struct(stream, fmt):
    struct_data = stream.read(struct.calcsize(fmt))
    return struct.unpack(fmt, struct_data)[0]


def read_range(stream, offset, limit):
    stream.seek(offset)
    return stream.read(limit)

