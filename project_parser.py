import struct
import sys
from utils import hexdump, ru32, ri32, rblob, riarr, rstr, set_verbose

#T_NONE, T_FILEREF, T_DBREF, T_ENUM = range(4)

def _print(*args, **kwargs): pass

def parse(fp, basic_mode=False, _print=_print):
    type_count = ru32(fp)
    #_print('type_count = %d' % type_count)

    types = []
    for type_i in range(type_count):
        _print('[*] parsing type#%d' % type_i)
        type_info = {'index': type_i}
        types.append(type_info)
        _print('[*] parsing type#%d name' % type_i)
        type_name = rstr(fp)
        type_info['name'] = type_name
        _print('Type Name.%d: %r' % (type_i, type_name))

        _print('[*] parsing type#%d field names' % type_i)
        type_field_count = ru32(fp)
        type_fields = []
        type_info['fields'] = type_fields
        _print('type_field_count =', type_field_count)
        for i in range(type_field_count):
            field_name = rstr(fp)
            _print('- field.%d.name = %r' % (i, field_name))
            type_fields.append({'name': field_name})

        _print('[*] parsing type#%d data names' % type_i)
        data_count = ru32(fp)
        _print('data_count = %d' % data_count)
        data_names = [rstr(fp) for i in range(data_count)]
        type_info['data_names'] = data_names
        _print('data.[].name = ', data_names)
        _print('[*] parsing type#%d note' % type_i)
        type_note = rstr(fp)
        type_info['note'] = type_note
        _print('note:', repr(type_note))

        if basic_mode:
            continue

        _print('[*] parsing type#%d speicals' % type_i)
        field_data_types = rblob(fp)
        _print('field field specials:', list(field_data_types[:type_field_count]))
        for i, f in enumerate(type_fields):
            f['special'] = field_data_types[i]

        _print('[*] parsing type#%d unknown blob 2' % type_i)
        b = rblob(fp, 5)
        assert len(b) == type_field_count * 5
        assert b == (b'\x01\x00\x00\x00\x00' * (len(b) // 5))

        _print('[*] parsing type#%d field strings' % type_i)
        assert ru32(fp) == type_field_count
        for i in range(type_field_count):
            _print('[*] parsing type#%d field strings#%d' % (type_i, i))
            cnt = ru32(fp)
            field_strings = [rstr(fp) for j in range(cnt)]
            type_fields[i]['strings'] = field_strings
            _print('field.%d.strings = %r' % (i, field_strings))

        _print('[*] parsing type#%d field meta' % type_i)
        assert ru32(fp) == type_field_count
        pos = fp.tell()
        for i in range(type_field_count):
            field_meta = riarr(fp)
            type_fields[i]['meta'] = field_meta
            _print('field.%d.meta = %r' % (i, field_meta))

        _print('[*] parsing type#%d field defaults' % type_i)
        assert ru32(fp) == type_field_count
        default_values = [ ri32(fp) for i in range(type_field_count) ]
        for i, v in enumerate(default_values):
            type_fields[i]['default'] = v
            _print('field.%d.default = %r' % (i, v))
        #_print('default values:', default_values)

    assert not fp.read(1)

    return types

if __name__ == '__main__':
    BASIC_MODE = '--basic' in sys.argv
    VERBOSE = '--verbose' in sys.argv
    set_verbose(VERBOSE)
    with open(sys.argv[1], 'rb') as fp:
        parsed = parse(fp, BASIC_MODE, print if VERBOSE else _print)
        from pprint import pprint
        pprint(parsed)

        for I, T in enumerate(parsed):
            print('# Type.%d -> %r' % (I, T['name']))
            pprint(T)
            print('## Note:', repr(T['note']))
            print()
