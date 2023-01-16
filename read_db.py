import sys
import project_parser
import data_parser
from collections import Counter
from pprint import pprint

def parse(project_fp, data_fp):
    project = project_parser.parse(project_fp)
    data_rows = data_parser.parse(data_fp)

    for schema, data_table in zip(project, data_rows):
        #pprint(schema, sort_dicts=False)
        #pprint(data_table, sort_dicts=False)
        #assert len(set(field['name'] for field in schema['fields'])) == len(schema['fields'])
        assert len(schema['data_names']) == len(data_table['rows'])

        for idx, (name, row) in enumerate(zip(schema['data_names'], data_table['rows'])):
            data = [
                {
                    'index': i,
                    'name': field['name'],
                    'value': cell,
                }
                for i, (field, cell) in enumerate(zip(schema['fields'], row))
            ]

            obj = {
                "index": idx,
                "row_name": name,
                "data": data,
            }

            pprint(obj, sort_dicts=False)

if __name__ == '__main__':
    with open(sys.argv[1], 'rb') as project_fp:
        with open(sys.argv[2], 'rb') as data_fp:
            parsed = parse(project_fp, data_fp)

