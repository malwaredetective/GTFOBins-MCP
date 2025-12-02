import os
import glob
import frontmatter
import json
import yaml

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
GTFOBINS_PATH = os.path.join(ROOT_DIR, 'GTFOBins.github.io', '_gtfobins')
FUNCTIONS_YML_PATH = os.path.join(ROOT_DIR, 'GTFOBins.github.io', '_data', 'functions.yml')
API_OUTPUT_FILE = os.path.join(ROOT_DIR, 'api.json')
FUNCTIONS_OUTPUT_FILE = os.path.join(ROOT_DIR, 'functions.json')

with open(FUNCTIONS_YML_PATH, 'r', encoding='utf-8') as f:
    functions_yml = yaml.safe_load(f)

function_descriptions = {
    key: value['description'] for key, value in functions_yml.items()
}

data = {}
functions_data = {}

for mdfile in glob.glob(os.path.join(GTFOBINS_PATH, '*.md')):
    post = frontmatter.load(mdfile)
    binary = os.path.splitext(os.path.basename(mdfile))[0]
    functions = post.get('functions', {})
    description = post.get('description', '')

    for function_name, function_entries in functions.items():
        for i, entry in enumerate(function_entries):
            functions[function_name][i] = {
                'code': entry.get('code', ''),
                'description': function_descriptions.get(function_name, '')
            }
        if function_name not in functions_data:
            functions_data[function_name] = {
                'description': function_descriptions.get(function_name, '')
            }

    data[binary] = {
        'description': description,
        'functions': functions
    }

with open(API_OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

with open(FUNCTIONS_OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump({'functions': functions_data}, f, indent=2, ensure_ascii=False)