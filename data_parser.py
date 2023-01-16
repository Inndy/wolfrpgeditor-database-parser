import struct
import sys
from utils import ru32, ri32, rblob, riarr, rstr, set_verbose

_HEADER_MAGIC = bytes.fromhex('005700004f4c00464d00')

def _print(*args, **kwargs): pass

def parse(fp, _print=_print):
    header = fp.read(11)
    _print('expect:', _HEADER_MAGIC.hex())
    _print('header:', header.hex())

    assert header[:10] == _HEADER_MAGIC

    type_count = ru32(fp)
    _print('type_count =', type_count)
    ret = []
    for type_i in range(type_count):
        table = {'index': type_i}
        ret.append(table)
        _print('# Type.%d' % type_i)
        unk1 = ri32(fp)
        db_type = ru32(fp)
        _print('unk1 = %d (0x%x)' % (unk1, unk1))
        _print('db_type = %d (0x%x)' % (db_type, db_type))

        assert unk1 == -2

        type_field_count = ru32(fp)

        fields = [ ru32(fp) for i in range(type_field_count) ]
        _print('fields:', fields)

        fields_decoded = [ divmod(f, 1000) for f in fields ]
        _print('fields (decoded):', fields_decoded)
        table['fields'] = fields_decoded

        int_type_count = sum(t == 1 for t, _ in fields_decoded)
        str_type_count = sum(t == 2 for t, _ in fields_decoded)
        _print('int_type_count:', int_type_count)
        _print('str_type_count:', str_type_count)

        assert int_type_count + str_type_count == type_field_count

        rows = []
        table['rows'] = rows
        item_count = ru32(fp)
        _print('item_count:', item_count)
        for i in range(item_count):
            row_int = []
            row_str = []
            for _ in range(int_type_count):
                row_int.append(ri32(fp))
            for _ in range(str_type_count):
                row_str.append(rstr(fp))

            mat = (None, row_int, row_str)

            row = [ mat[t][i] for t, i in fields_decoded ]
            _print(row)
            rows.append(row)

        _print('-'*80)

    assert fp.read(2) == b'\xc1'
    return ret

if __name__ == '__main__':
    BASIC_MODE = '--basic' in sys.argv
    VERBOSE = '--verbose' in sys.argv
    set_verbose(VERBOSE)
    with open(sys.argv[1], 'rb') as fp:
        parsed = parse(fp, print if VERBOSE else _print)

    from pprint import pprint
    pprint(parsed, sort_dicts=False)
