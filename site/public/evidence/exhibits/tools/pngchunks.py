"""Static PNG chunk lister: reads bytes only, never decodes image data."""
import struct
import sys

path = sys.argv[1]
data = open(path, 'rb').read()
assert data[:8] == b'\x89PNG\r\n\x1a\n', 'not a PNG signature'
off = 8
print(f'file_size={len(data)}')
print('offset    type  length')
while off < len(data):
    length, ctype = struct.unpack('>I4s', data[off:off + 8])
    print(f'{off:<9d} {ctype.decode("latin-1")}  {length}')
    off += 12 + length
    if ctype == b'IEND':
        break
print(f'iend_end_offset={off} trailing_bytes_after_IEND={len(data) - off}')
