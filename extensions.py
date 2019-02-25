import itertools

from modules import Module


def dice(d, file):
    """Output a Tracery module simulating a given dice roll using NdS notation."""
    n, s = d.split('d')
    n = int(n)
    s = int(s)
    possibility_space = itertools.product([i+1 for i in range(s)], repeat=n)
    possibility_space = [sum(x) for x in possibility_space]

    virtual_name = file + ":" + str(hash('dice({0})'.format(d)))

    return Module(
        name=virtual_name,
        file_path='!dice({0})'.format(d),
        productions={
            virtual_name: ['{0}'.format(x) for x in possibility_space]
        },
        external=True,
        variables=set(),
        links=set()
    )


DICE = (r'!dice\(([^)]+)\)', dice)
