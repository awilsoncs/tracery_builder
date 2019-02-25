import collections

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