"""Static C2PA reader for a PNG caBX chunk.

Reads bytes only: walks JUMBF boxes, decodes CBOR with a minimal built-in decoder,
and parses the leaf certificate DER with `cryptography` (no network, no validation).
Usage: python3 -I c2pa_static.py <png> [labels|claims|cert]
"""
import struct
import sys
import json


def png_chunk(data, want):
    off = 8
    while off < len(data):
        length, ctype = struct.unpack('>I4s', data[off:off + 8])
        if ctype == want:
            return off + 8, data[off + 8:off + 8 + length]
        off += 12 + length
    raise SystemExit('chunk not found')


class Tag:
    def __init__(self, tag, value):
        self.tag, self.value = tag, value

    def __repr__(self):
        return f'Tag({self.tag}, {self.value!r})'


def cbor(buf, i=0):
    ib = buf[i]; major, info = ib >> 5, ib & 31; i += 1
    if info < 24:
        val = info
    elif info == 24:
        val = buf[i]; i += 1
    elif info == 25:
        val = struct.unpack('>H', buf[i:i + 2])[0]; i += 2
    elif info == 26:
        val = struct.unpack('>I', buf[i:i + 4])[0]; i += 4
    elif info == 27:
        val = struct.unpack('>Q', buf[i:i + 8])[0]; i += 8
    elif info == 31:
        val = None
    else:
        raise ValueError('bad info')
    if major == 0:
        return val, i
    if major == 1:
        return -1 - val, i
    if major in (2, 3):
        if val is None:
            parts = []
            while buf[i] != 0xff:
                p, i = cbor(buf, i); parts.append(p)
            i += 1
            out = b''.join(parts) if major == 2 else ''.join(parts)
            return out, i
        raw = buf[i:i + val]; i += val
        return (bytes(raw) if major == 2 else raw.decode('utf-8')), i
    if major == 4:
        out = []
        if val is None:
            while buf[i] != 0xff:
                v, i = cbor(buf, i); out.append(v)
            return out, i + 1
        for _ in range(val):
            v, i = cbor(buf, i); out.append(v)
        return out, i
    if major == 5:
        out = {}
        n = 0
        while (val is None and buf[i] != 0xff) or (val is not None and n < val):
            k, i = cbor(buf, i); v, i = cbor(buf, i)
            out[k if not isinstance(k, (list, dict)) else str(k)] = v; n += 1
        if val is None:
            i += 1
        return out, i
    if major == 6:
        v, i = cbor(buf, i)
        return Tag(val, v), i
    if major == 7:
        if info == 20: return False, i
        if info == 21: return True, i
        if info in (22, 23): return None, i
        if info == 25 or info == 26 or info == 27:
            fmt = {25: '>e', 26: '>f', 27: '>d'}[info]
            size = {25: 2, 26: 4, 27: 8}[info]
            return struct.unpack(fmt, buf[i - size:i])[0], i
        return val, i


def boxes(buf, start, end, depth, path, out):
    i = start
    while i + 8 <= end:
        lbox, tbox = struct.unpack('>I4s', buf[i:i + 8])
        hdr = 8
        if lbox == 1:
            lbox = struct.unpack('>Q', buf[i + 8:i + 16])[0]; hdr = 16
        if lbox == 0:
            lbox = end - i
        t = tbox.decode('latin-1')
        if t == 'jumb':
            # first child is jumd
            j = i + hdr
            dl, dt = struct.unpack('>I4s', buf[j:j + 8])
            d = buf[j + 8:j + dl]
            uuid = d[:16]; toggles = d[16]
            label = ''
            if toggles & 2:
                nul = d.index(0, 17); label = d[17:nul].decode('utf-8')
            out.append(dict(off=i, depth=depth, type='jumb', len=lbox, label=label,
                            uuid4=uuid[:4].decode('latin-1')))
            boxes(buf, j + dl, i + lbox, depth + 1, path + [label], out)
        else:
            out.append(dict(off=i, depth=depth, type=t, len=lbox, path='/'.join(path),
                            payload=(i + hdr, i + lbox)))
        i += lbox


def jsonable(o, maxbytes=24):
    if isinstance(o, Tag):
        return {'tag': o.tag, 'value': jsonable(o.value, maxbytes)}
    if isinstance(o, bytes):
        return f'<{len(o)} bytes>'
    if isinstance(o, dict):
        return {str(k): jsonable(v, maxbytes) for k, v in o.items()}
    if isinstance(o, list):
        return [jsonable(v, maxbytes) for v in o]
    return o


def main():
    path, mode = sys.argv[1], sys.argv[2]
    data = open(path, 'rb').read()
    base, chunk = png_chunk(data, b'caBX')
    out = []
    boxes(chunk, 0, len(chunk), 0, [], out)
    if mode == 'labels':
        for b in out:
            if b['type'] == 'jumb':
                print(f"{base + b['off']:>7d} {'  ' * b['depth']}jumb  {b['label']}")
            else:
                print(f"{base + b['off']:>7d} {'  ' * b['depth']}{b['type']}  len={b['len']}")
        return
    for b in out:
        if b['type'] != 'cbor':
            continue
        p = b['path']
        s, e = b['payload']
        val, _ = cbor(chunk[s:e])
        if mode == 'claims' and (p.endswith('c2pa.claim') or p.endswith('c2pa.claim.v2')
                                  or 'c2pa.actions' in p):
            print('##', p)
            print(json.dumps(jsonable(val), indent=1))
        if mode == 'ingredient' and p.endswith('c2pa.ingredient.v3'):
            print('##', p)
            print(json.dumps(jsonable(val), indent=1))
        if mode == 'protected' and p.endswith('c2pa.signature'):
            sign1 = val.value if isinstance(val, Tag) else val
            prot, _ = cbor(sign1[0])
            print('##', p, 'tag', val.tag if isinstance(val, Tag) else None,
                  'protected-keys', sorted(str(k) for k in prot),
                  'unprotected-keys', sorted(str(k) for k in sign1[1]))
        if mode == 'cert' and p.endswith('c2pa.signature'):
            from cryptography import x509
            sign1 = val.value if isinstance(val, Tag) else val
            prot, _ = cbor(sign1[0])
            unprot = sign1[1]
            chain = prot.get(33) or unprot.get(33) or prot.get('x5chain') or unprot.get('x5chain')
            if isinstance(chain, bytes):
                chain = [chain]
            print('##', p, 'protected-alg', prot.get(1))
            for n, der in enumerate(chain):
                c = x509.load_der_x509_certificate(der)
                print(f'cert[{n}] subject={c.subject.rfc4514_string()}')
                print(f'cert[{n}] issuer={c.issuer.rfc4514_string()}')
                print(f'cert[{n}] serial={c.serial_number:X}')
                print(f'cert[{n}] not_before={c.not_valid_before_utc.isoformat()}')
                print(f'cert[{n}] not_after={c.not_valid_after_utc.isoformat()}')
            print('unprotected-keys', sorted(str(k) for k in unprot))


main()
