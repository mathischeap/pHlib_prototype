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
}
_mesh_set = dict()
_space_set = dict()


def set_mesh(mesh):
    """"""
    assert mesh.__class__.__name__ in ('StaticMesh', 'AdaptiveMesh', 'MovingMesh'), \
        f"I need a Mesh instance."
    repr = mesh.__repr__()
    if repr in _mesh_set:
        pass
    else:
        _mesh_set[repr] = mesh
        _space_set[repr] = dict()

    _config['current_mesh'] = repr


from src.spaces.scalarValuedFormSpace import ScalarValuedFormSpace

# whenever new space is implemented, add it below.
_implemented_spaces = {
    # abbr : (class                , description                 , parameters),
    'Omega': (ScalarValuedFormSpace, 'scalar valued k-form space', ['k', 'N']),
}

def list_():
    """"""
    print('{:>15} | {}'.format('abbreviation', 'description'))
    for abbr in _implemented_spaces:
        description = _implemented_spaces[abbr][1]
        print('{:>15} | {}'.format(abbr, description))


def add(abbrs, *args, **kwargs):
    """generate a space (named `abbr`) with args `kwargs` use current mesh.

    Parameters
    ----------
    abbrs
    kwargs

    Returns
    -------

    """
    if isinstance(abbrs, str):  # make only 1 space
        abbrs = [abbrs, ]
    else:
        isinstance(abbrs, (list, tuple)), f"pls put space abbreviations into a list or tuple."

    assert _config['current_mesh'] != '', f"pls set mesh firstly."

    spaces = tuple()
    for abbr in abbrs:
        assert abbr in _implemented_spaces, \
            f"space abbr.={abbr} not implemented. do `ph.space.list_()` to see all implemented spaces."
        space_class = _implemented_spaces[abbr][0]

        mesh_repr = _config['current_mesh']
        mesh = _mesh_set[mesh_repr]
        current_spaces = _space_set[mesh_repr]

        space = space_class(mesh, *args, **kwargs)
        srp = space.__repr__ ()

        if srp in current_spaces:
            pass
        else:
            current_spaces[srp] = space

        spaces += (current_spaces[srp],)

    if len(spaces) == 1:
        return spaces[0]
    else:
        return spaces


if __name__ == '__main__':
    # python src/spaces/main.py
    import __init__ as ph

    # print(_space_set)
    mesh = ph.mesh.static(None)
    ph.space.set_mesh(mesh)
    #
    O2 = ph.space.add('Omega', k=2, N=3)
