# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 2/20/2023 11:00 AM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')
from importlib import import_module

_config = {
    'current_mesh': '',
}
_mesh_set = dict()
_space_set = dict()

# whenever new space is implemented, add it below.
_implemented_spaces = {
    # abbr : (class                                               , description                 , parameters),
    'Omega': ('src.spaces.specific.scalar : ScalarValuedFormSpace', 'scalar valued k-form space', ['k', ]),
}


def set_mesh(mesh):
    """"""
    assert mesh.__class__.__name__ == 'Mesh', \
        f"I need a Mesh instance."
    sr = mesh._sym_repr
    if sr in _mesh_set:
        pass
    else:
        _mesh_set[sr] = mesh
        _space_set[sr] = dict()

    _config['current_mesh'] = sr


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
            print('{:>15}: {}'.format(i, space._sym_repr))


def new(abbrs, *args, mesh=None, **kwargs):
    """generate a space (named `abbr`) with args `kwargs` use current mesh.

    Parameters
    ----------
    abbrs
    mesh :
        We specify a mesh here. And this does not change the global mesh setting.
    kwargs

    Returns
    -------

    """
    if _config['current_mesh'] == '' and mesh is None:
        raise Exception(f"pls set a mesh firstly by using `space.set_mesh` or specify `mesh`.")
    else:
        pass

    if isinstance(abbrs, str):  # make only 1 space
        abbrs = [abbrs, ]
    else:
        isinstance(abbrs, (list, tuple)), f"pls put space abbreviations into a list or tuple."

    mesh_sr = _config['current_mesh']

    if mesh is None:
        mesh = _mesh_set[mesh_sr]
    else:
        mesh_sr = mesh._sym_repr
        if mesh_sr in _mesh_set:
            pass
        else:
            _mesh_set[mesh_sr] = mesh
            _space_set[mesh_sr] = dict()

    current_spaces = _space_set[mesh_sr]

    spaces = tuple()
    for abbr in abbrs:
        assert abbr in _implemented_spaces, \
            f"space abbr.={abbr} not implemented. do `ph.space.list_()` to see all implemented spaces."
        space_class_path, space_class_name = _implemented_spaces[abbr][0].split(' : ')
        space_class = getattr(import_module(space_class_path), space_class_name)

        space = space_class(mesh, *args, **kwargs)
        srp = space._sym_repr  # do not use __repr__()

        if srp in current_spaces:
            pass
        else:
            current_spaces[srp] = space

        spaces += (current_spaces[srp],)

    if len(spaces) == 1:
        return spaces[0]
    else:
        return spaces
