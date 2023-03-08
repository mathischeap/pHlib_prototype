# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 3/8/2023 11:57 AM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')

from src.spaces.operators import wedge as space_wedge
from src.spaces.operators import Hodge as space_Hodge
from src.spaces.operators import d as space_d
from src.spaces.operators import codifferential as space_codifferential


_implemented_operators = {  # coded operators
    'wedge': r"\emph{wedge}",
    'Hodge': r'\emph{Hodge of}',
    'd': r'\emph{exterior-derivative of}',
    'codifferential': r'\emph{codifferential of}',
    'time_derivative': r'\emph{time-derivative of}',
    'trace': r'\emph{trace of}',
}


_time_derivative_related_operators = {
    'time_derivative': _implemented_operators['time_derivative'],
}


def _parse_related_time_derivative(f):
    """"""
    related = list()
    for op_name in _time_derivative_related_operators:
        op_lin_rp = _time_derivative_related_operators[op_name]
        if op_lin_rp in f._lin_repr:
            related.append(op_name)
    return related


def wedge(f1, f2):
    """f1 wedge f2"""
    s1 = f1.space
    s2 = f2.space

    wedge_space = space_wedge(s1, s2)  # if this is not possible, return NotImplementedError

    lr_term1 = f1._lin_repr
    lr_term2 = f2._lin_repr
    lr_operator = r" \emph{wedge} "

    sr_term1 = f1._sym_repr
    sr_term2 = f2._sym_repr
    sr_operator = r'\wedge '

    if f1.is_root():
        pass
    else:
        lr_term1 = '[' + lr_term1 + ']'
        sr_term1 = r'\left(' + sr_term1 + r'\right)'
    if f2.is_root():
        pass
    else:
        lr_term2 = '[' + lr_term2 + ']'
        sr_term2 = r'\left(' + sr_term2 + r'\right)'
    lin_repr = lr_term1 + lr_operator + lr_term2
    sym_repr = sr_term1 + sr_operator + sr_term2

    elementary_forms = set()
    elementary_forms.update(f1._elementary_forms)
    elementary_forms.update(f2._elementary_forms)

    if f1.orientation == f2.orientation:
        orientation = f1.orientation
    else:
        orientation = 'None'

    f = f1.__class__(
        wedge_space,  # space
        sym_repr,  # symbolic representation
        lin_repr,
        False,
        elementary_forms,
        orientation,
    )

    return f


def Hodge(f):
    """Metric Hodge of a form."""
    hs = space_Hodge(f.space)

    lr = f._lin_repr
    sr = f._sym_repr

    op_lin_repr = _implemented_operators['Hodge']

    if f.is_root():
        lr = op_lin_repr + " " + lr
    else:
        lr = op_lin_repr + " [" + lr + ']'

    if f.is_root():
        sr = r"\star " + sr
    else:
        sr = r"\star \left(" + sr + r"\right)"

    if f.orientation == 'inner':
        orientation = 'outer'
    elif f.orientation == 'outer':
        orientation = 'inner'
    else:
        orientation = 'None'
    f = f.__class__(
        hs,  # space
        sr,  # symbolic representation
        lr,
        False,
        f._elementary_forms,
        orientation,
    )

    return f


def d(f):
    """Metric Hodge of a form."""
    ds = space_d(f.space)

    lr = f._lin_repr
    sr = f._sym_repr

    op_lin_repr = _implemented_operators['d']

    if f.is_root():
        lr = op_lin_repr + " " + lr
    else:
        lr = op_lin_repr + " [" + lr + ']'

    if f.is_root():
        sr = r"\mathrm{d}" + sr
    else:
        sr = r"\mathrm{d}\left(" + sr + r"\right)"

    f = f.__class__(
        ds,  # space
        sr,  # symbolic representation
        lr,
        False,
        f._elementary_forms,
        f.orientation,
    )

    return f


def codifferential(f):
    """Metric Hodge of a form."""
    ds = space_codifferential(f.space)

    lr = f._lin_repr
    sr = f._sym_repr

    op_lin_repr = _implemented_operators['codifferential']

    if f.is_root():
        lr = op_lin_repr + " " + lr
    else:
        lr = op_lin_repr + " [" + lr + ']'

    if f.is_root():
        sr = r"\mathrm{d}^\ast " + sr
    else:
        sr = r"\mathrm{d}^\ast\left(" + sr + r"\right)"

    f = f.__class__(
        ds,  # space
        sr,  # symbolic representation
        lr,
        False,
        f._elementary_forms,
        f.orientation,
    )

    return f


def time_derivative(f):
    """The time derivative operator."""
    if f.__class__.__name__ != 'Form':
        raise NotImplementedError(f"time_derivative on {f} is not implemented or even not possible at all.")
    else:
        pass

    lr = f._lin_repr
    sr = f._sym_repr

    op_lin_repr = _implemented_operators['time_derivative']

    if f.is_root():
        lr = op_lin_repr + " " + lr
    else:
        lr = op_lin_repr + " [" + lr + ']'

    if f.is_root():
        sr = r"\partial_t " + sr
    else:
        sr = r"\partial_t\left(" + sr + r"\right)"

    tdf = f.__class__(
        f.space,
        sr,
        lr,
        False,
        f._elementary_forms,
        f.orientation,
    )

    return tdf


from src.spaces.operators import trace as space_trace


def trace(f):
    """The trace operator."""
    trf_space = space_trace(f.space)

    lr = f._lin_repr
    sr = f._sym_repr

    op_lin_repr = _implemented_operators['trace']

    if f.is_root():
        lr = op_lin_repr + " " + lr
    else:
        lr = op_lin_repr + " [" + lr + ']'

    if f.is_root():
        sr = r"\mathrm{tr}" + sr
    else:
        sr = r"\mathrm{tr}\left(" + sr + r"\right)"

    f = f.__class__(
        trf_space,  # space
        sr,  # symbolic representation
        lr,
        False,
        f._elementary_forms,
        f.orientation,
    )

    return f