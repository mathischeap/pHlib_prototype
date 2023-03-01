# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 2/20/2023 11:00 AM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')

_config = {
    'current_mesh': '',
    'suppress_existing_space_warning': False,
}
_mesh_set = dict()
_space_set = dict()


def set_mesh(mesh):
    """"""
    assert mesh.__class__.__name__  == 'Mesh', \
        f"I need a Mesh instance."
    sr = mesh._symbolic_representation
    if sr in _mesh_set:
        pass
    else:
        _mesh_set[sr] = mesh
        _space_set[sr] = dict()

    _config['current_mesh'] = sr


from src.spaces.scalarValuedFormSpace import ScalarValuedFormSpace

# whenever new space is implemented, add it below.
_implemented_spaces = {
    # abbr : (class                , description                 , parameters),
    'Omega': (ScalarValuedFormSpace, 'scalar valued k-form space', ['k', 'p']),
}


def _list_spaces():
    """"""
    print('\n Implemented spaces:')
    print('{:>15} - {}'.format('abbreviation', 'description'))
    for abbr in _implemented_spaces:
        description = _implemented_spaces[abbr][1]
        print('{:>15} | {}'.format(abbr, description))

    print('\n Existing spaces:')
    for mesh in _space_set:
        spaces = _space_set[mesh]
        print('{:>15} {}'.format('On mesh', mesh))
        for i, sr in enumerate(spaces):
            space = spaces[sr]
            print('{:>15}: {}'.format(i, space._symbolic_representation))


class SpaceExistingWarning(UserWarning, ValueError):
    pass

import warnings


def _new(*args, **kwargs):
    """A private `new` function to suppress the warning."""
    _config['suppress_existing_space_warning'] = True
    spaces = new(*args, **kwargs)
    _config['suppress_existing_space_warning'] = False
    return spaces


def new(abbrs, *args, **kwargs):
    """generate a space (named `abbr`) with args `kwargs` use current mesh.

    Parameters
    ----------
    abbrs
    kwargs

    Returns
    -------

    """
    if _config['current_mesh'] == '':
        raise Exception(f"pls set a mesh firstly by using `space.set_mesh`.")
    else:
        pass

    if isinstance(abbrs, str):  # make only 1 space
        abbrs = [abbrs, ]
    else:
        isinstance(abbrs, (list, tuple)), f"pls put space abbreviations into a list or tuple."

    spaces = tuple()
    for abbr in abbrs:
        assert abbr in _implemented_spaces, \
            f"space abbr.={abbr} not implemented. do `ph.space.list_()` to see all implemented spaces."
        space_class = _implemented_spaces[abbr][0]

        mesh_sr = _config['current_mesh']
        mesh = _mesh_set[mesh_sr]
        current_spaces = _space_set[mesh_sr]

        space = space_class(mesh, *args, **kwargs)
        srp = space._symbolic_representation  # do not use __repr__()

        if srp in current_spaces:
            if _config['suppress_existing_space_warning']:
                pass
            else:
                warnings.warn(f"{srp} already exists, will return the exist one instead of making a new one.",
                              SpaceExistingWarning)
        else:
            current_spaces[srp] = space

        spaces += (current_spaces[srp],)

    if len(spaces) == 1:
        return spaces[0]
    else:
        return spaces


if __name__ == '__main__':
    # python src/spaces/main.py
    pass