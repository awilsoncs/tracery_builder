import argparse
import collections
import json
import os
import re

VERSION = '1.0'


Module = collections.namedtuple(
    'Module',
    [
        'name',  # name of the module
        'file_path',  # location of the module
        'productions',  # tracery productions
        'variables',  # variable identifiers ([thisObject:#myrule#])
        'external',  # true if the module is not the primary module
        'links',  # True if this module should append its name to its productions
    ]
)


MODULE_CACHE = {}


def load_module(file_path, external=False):
    module_name = os.path.split(file_path)[-1].split('.')[0]

    with open(file_path) as f:
        js = json.load(f)

    variables = find_all_variables(js)

    module = Module(
        name=module_name,
        file_path=file_path,
        productions=js,
        external=external,
        variables=find_all_variables(js),
        links=find_all_links(js, variables)
    )
    MODULE_CACHE[module_name] = module

    if module.external:
        # if the module is external, we need to apply the namespace
        keys = module.productions.keys()
        for key in list(keys):
            new_key = module.name if key == 'origin' else module.name + ':' + key
            module.productions[new_key] = module.productions[key]
            del module.productions[key]

            # update entries
            for other_key, value in module.productions.items():
                module.productions[other_key] = [_replace_identifier(x, key, new_key) for x in value]
    # always apply the namespace to internal variables
    for variable in variables:
        new_variable = module.name + '->' + variable
        for key, value in module.productions.items():
            module.productions[key] = [
                _replace_identifier(
                    _replace_identifier(x, variable, new_variable),
                    variable,
                    new_variable,
                    token_pattern='[{0}:'
                ) for x in value]

    else:
        # go ahead and add the module origin as a production
        if 'origin' in module.productions:
            module.productions[module.name] = module.productions['origin']
    return module


def _replace_identifier(id_string, old_string, new_string, token_pattern='#{0}#'):
    """Return an identifier with an updated string"""
    return id_string.replace(token_pattern.format(old_string), token_pattern.format(new_string), 1000)


def find_all_variables(js: dict) -> set:
    output = set()
    for element_list in js.values():
        for element in element_list:
            matches = re.findall(r'\[([^#:]+):', element)
            for match in matches:
                output.add(match)
    return output


def find_all_links(js: dict, variables: set) -> set:
    """Return the set of symbols that do not appear on the RHS of a production."""
    rhs_symbols = set(js.keys())
    output = set()
    for element_list in js.values():
        for element in element_list:
            matches = re.findall(r'#([^#]+)#', element)
            for match in matches:
                match = match.split(':')[0].split('.')[0]
                if match not in rhs_symbols and match not in variables:
                    output.add(match)
    return output


def build_module_cache(root_file_path, external=False):
    """Manage the build."""
    root_dir = os.path.dirname(root_file_path)
    print('Building {0}'.format(root_file_path))
    module = load_module(root_file_path, external=external)
    # load unloaded submodules
    for link in module.links:
        if link not in MODULE_CACHE:
            build_module_cache(
                os.path.join(root_dir, link+'.json'),
                external=True
            )


def compile_from_module_cache():
    output = {}
    for value in MODULE_CACHE.values():
        output.update(value.productions)
    return output


def main(args):
    build_module_cache(args.root_file)
    finalized_json = compile_from_module_cache()
    print("Writing to {0}".format(args.out_file))
    with open(args.out_file, 'w') as outfile:
        if args.pretty:
            json.dump(finalized_json, outfile, indent=4)
        else:
            json.dump(finalized_json, outfile)
    print("Build success!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Tracery Builder v{0}'.format(VERSION)
    )
    parser.add_argument('root_file', type=str, help='root file for the builder')
    parser.add_argument('out_file', type=str, help='file to create or update')
    parser.add_argument('-p', '--pretty', action='store_true', help='prettify output')
    args = parser.parse_args()

    args.root_file_path = os.path.dirname(args.root_file)
    main(args)
