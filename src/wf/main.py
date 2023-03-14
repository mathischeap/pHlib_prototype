# -*- coding: utf-8 -*-
"""
@author: Yi Zhang
@contact: zhangyi_aero@hotmail.com
@time: 2/18/2023 10:18 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')
from src.tools.frozen import Frozen
import matplotlib.pyplot as plt
import matplotlib
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "DejaVu Sans",
    "text.latex.preamble": r"\usepackage{amsmath, amssymb}",
})
matplotlib.use('TkAgg')
from copy import deepcopy
from src.wf.td import TemporalDiscretization
from src.bc import BoundaryCondition


class WeakFormulation(Frozen):
    """Weak Formulation."""

    def __init__(self, term_sign_dict=None, test_forms=None, expression=None, weak_formulations=None):
        """

        Parameters
        ----------
        term_sign_dict
        test_forms
        expression
        """
        if term_sign_dict is not None:
            assert test_forms is not None
            assert expression is None
            assert weak_formulations is None
            self._parse_term_sign_dict(term_sign_dict, test_forms)

        elif expression is not None:
            assert term_sign_dict is None
            assert test_forms is None
            assert weak_formulations is None
            self._parse_expression(expression)

        elif weak_formulations is not None:  # merge multiple weak formulations
            assert term_sign_dict is None
            assert test_forms is None
            assert expression is None
            raise NotImplementedError(f"merge weak formulations not coded.")

        else:
            raise Exception()

        self._meshes, self._mesh = self._parse_meshes(self._term_dict)
        self._consistence_checker()
        self._unknowns = None
        self._derive = None
        self._td = None
        self._bc = None
        self._freeze()

    @classmethod
    def _parse_meshes(cls, term_dict):
        meshes = list()
        for i in term_dict:
            for terms in term_dict[i]:
                for t in terms:
                    mesh = t.mesh
                    if mesh not in meshes:
                        meshes.append(mesh)
                    else:
                        pass
        num_meshes = len(meshes)
        assert num_meshes > 0, f"we need at least one mesh."
        if num_meshes == 1:
            mesh = meshes[0]
        else:
            mesh_dim_dict = dict()
            for m in meshes:
                ndim = m.ndim
                if ndim not in mesh_dim_dict:
                    mesh_dim_dict[ndim] = list()
                else:
                    pass
                mesh_dim_dict[ndim].append(m)
            if len(mesh_dim_dict) == 2:
                larger_ndim = max(mesh_dim_dict.keys())
                lower_ndim = min(mesh_dim_dict.keys())
                if lower_ndim == larger_ndim - 1:
                    assert len(mesh_dim_dict[larger_ndim]) == 1, f"must be"
                    mesh = mesh_dim_dict[larger_ndim][0]
                else:
                    raise NotImplementedError()
            else:
                raise NotImplementedError()

        return meshes, mesh

    def _parse_term_sign_dict(self, term_sign_dict, test_forms):
        """"""
        term_dict, sign_dict = term_sign_dict
        ind_dict = dict()
        indexing = dict()
        num_eq = len(term_dict)
        for i in range(num_eq):   # ith equation
            assert i in term_dict and i in sign_dict, f"numbering of equations must be 0, 1, 2, ..."
            ind_dict[i] = ([], [])
            k = 0
            for j, terms in enumerate(term_dict[i]):
                for m in range(len(terms)):
                    if j == 0:
                        index = str(i) + '-' + str(k)
                    elif j == 1:
                        index = str(i) + '-' + str(k)
                    else:
                        raise Exception()
                    k += 1
                    indexing[index] = (sign_dict[i][j][m], term_dict[i][j][m])
                    ind_dict[i][j].append(index)

        self._test_forms = test_forms
        self._term_dict = term_dict
        self._sign_dict = sign_dict
        self._ind_dict = ind_dict
        self._indexing = indexing

    def _parse_expression(self, expression):
        """"""
        raise NotImplementedError()

    def _consistence_checker(self):
        """We do consistence check here and parse properties like mesh and so on."""
        ts = list()
        for tf in self._test_forms:
            ts.append(tf.space)
        self._test_spaces = ts

        efs = set()
        for i in self._term_dict:   # ith equation
            for terms in self._term_dict[i]:
                for term in terms:
                    efs.update(term.elementary_forms)

        self._efs = efs

    def __repr__(self):
        """Customize the __repr__."""
        super_repr = super().__repr__().split('object')[1]
        if self.unknowns is None:
            unknown_sym_repr = '[...]'
        else:
            unknown_sym_repr = [f._sym_repr for f in self.unknowns]
        return f"<WeakFormulation of {unknown_sym_repr}" + super_repr

    def __getitem__(self, item):
        """"""
        assert item in self._indexing, \
            f"index: '{item}' is illegal, do `print_representations(indexing=True)` " \
            f"to check indices of all terms."
        return self._indexing[item]

    def __iter__(self):
        """"""
        for i in self._ind_dict:
            for lri in self._ind_dict[i]:
                for index in lri:
                    yield index

    def __len__(self):
        """"""
        return len(self._term_dict)

    def __contains__(self, item):
        return item in self._indexing

    def _parse_index(self, index):
        """"""
        ith_equation, k = index.split('-')
        ith_equation = int(ith_equation)
        k = int(k)
        left_terms = self._term_dict[ith_equation][0]
        number_left_terms = len(left_terms)
        if k < number_left_terms:
            l_o_r = 0  # left
            ith_term = k
        else:
            l_o_r = 1
            ith_term = k - number_left_terms
        return ith_equation, l_o_r, ith_term

    @property
    def elementary_forms(self):
        """Return a set of root forms that this equation involves."""
        return self._efs

    @property
    def unknowns(self):
        """The unknowns of this weak formulation"""
        return self._unknowns

    @unknowns.setter
    def unknowns(self, unknowns):
        """The unknowns of this weak formulation"""
        if self._unknowns is not None:
            f"unknowns exists; not allowed to change them."

        if len(self) == 1 and not isinstance(unknowns, (list, tuple)):
            unknowns = [unknowns, ]
        assert isinstance(unknowns, (list, tuple)), \
            f"please put unknowns in a list or tuple if there are more than 1 equation."
        assert len(unknowns) == len(self), \
            f"I have {len(self)} equations but receive {len(unknowns)} unknowns."

        for i, unknown in enumerate(unknowns):
            assert unknown.__class__.__name__ == 'Form' and unknown.is_root(), \
                f"{i}th variable is not a root form."
            assert unknown in self._efs, f"{i}th variable is not an elementary form."

        self._unknowns = unknowns

    @property
    def test_forms(self):
        return self._test_forms

    def print_representations(self, indexing=True):
        """Print the representations"""
        seek_text = rf'In ${self._mesh.manifold._sym_repr}\in\mathbb' + '{R}^{' + str(self._mesh.ndim) + '}$, '
        given_text = r'given'
        for ef in self._efs:
            if ef not in self.unknowns and ef not in self._test_forms:
                given_text += rf' ${ef._sym_repr} \in {ef.space._sym_repr}$,'
        if given_text == r'Given':
            seek_text += r'Seek $\left('
        else:
            seek_text += given_text
            seek_text += r' seek $\left('
        form_sr_list = list()
        space_sr_list = list()
        for un in self.unknowns:
            form_sr_list.append(rf' {un._sym_repr}')
            space_sr_list.append(rf"{un.space._sym_repr}")
        seek_text += ','.join(form_sr_list)
        seek_text += r'\right) \in '
        seek_text += r'\times '.join(space_sr_list)
        seek_text += '$, such that\n'
        symbolic = ''
        number_equations = len(self._term_dict)
        for i in self._term_dict:
            for t, terms in enumerate(self._term_dict[i]):
                if len(terms) == 0:
                    symbolic += '0'
                else:

                    for j, term in enumerate(terms):
                        sign = self._sign_dict[i][t][j]
                        term = self._term_dict[i][t][j]

                        term_sym_repr = term._sym_repr

                        if indexing:
                            index = self._ind_dict[i][t][j].replace('-', r'\text{-}')
                            term_sym_repr = r'\underbrace{' + term_sym_repr + r'}_{' + \
                                rf"{index}" + '}'
                        else:
                            pass

                        if j == 0:
                            if sign == '+':
                                symbolic += term_sym_repr
                            elif sign == '-':
                                symbolic += '-' + term_sym_repr
                            else:
                                raise Exception()
                        else:
                            symbolic += ' ' + sign + ' ' + term_sym_repr

                if t == 0:
                    symbolic += ' &= '

            symbolic += r'\quad &&\forall ' + self._test_forms[i]._sym_repr + r'\in ' + \
                self._test_spaces[i]._sym_repr

            if i < number_equations - 1:
                symbolic += r',\\'
            else:
                symbolic += '.'

        symbolic = r"$\left\lbrace\begin{aligned}" + symbolic + r"\end{aligned}\right.$"
        if self._bc is None or len(self.bc) == 0:
            bc_text = ''
        else:
            bc_text = self.bc._bc_text()

        if indexing:
            figsize = (12, 2 * len(self._term_dict))
        else:
            figsize = (12, 1.5 * len(self._term_dict))
        plt.figure(figsize=figsize)
        plt.axis([0, 1, 0, 1])
        plt.axis('off')
        plt.text(0.05, 0.5, seek_text + symbolic + bc_text, ha='left', va='center', size=15)
        plt.tight_layout()
        plt.show()

    def pr(self, **kwargs):
        """A wrapper of print_representations"""
        return self.print_representations(**kwargs)

    @property
    def derive(self):
        """The derivations that to be applied to this current weak formulation."""
        if self._derive is None:
            self._derive = _Derive(self)
        return self._derive

    @property
    def bc(self):
        """The boundary condition of pde class."""
        if self._bc is None:
            self._bc = BoundaryCondition(self._mesh)
        return self._bc

    @property
    def td(self):
        """temporal discretization."""
        if self._td is None:
            self._td = TemporalDiscretization(self)
        return self._td


class _Derive(Frozen):
    """"""

    def __init__(self, wf):
        self._wf = wf
        self._freeze()

    def replace(self, index, terms, signs):
        """_replace the term indicated by `index` by `terms` of `signs`"""
        if isinstance(terms, (list, tuple)):
            pass
        else:
            terms = [terms, ]
            signs = [signs, ]
        assert len(terms) == len(signs), f"new terms length is not equal to the length of new signs."
        for _, sign in enumerate(signs):
            assert sign in ('+', '-'), f"{_}th sign = {sign} is wrong. Must be '+' or '-'."

        i, j, k = self._wf._parse_index(index)
        old_sign = self._wf._sign_dict[i][j][k]
        if old_sign == '+':
            signs_ = signs
        else:
            signs_ = list()
            for s_ in signs:
                signs_.append(self._switch_sign(s_))
        signs = signs_

        new_term_dict = deepcopy(self._wf._ind_dict)  # must do deepcopy, use `_ind_dict`, not a typo
        new_sign_dict = deepcopy(self._wf._ind_dict)  # must do deepcopy, use `_ind_dict`, not a typo

        new_term_dict[i][j][k] = list()
        new_sign_dict[i][j][k] = list()

        new_term_dict[i][j][k].extend(terms)
        new_sign_dict[i][j][k].extend(signs)

        new_term_dict, new_sign_dict = self._parse_new_weak_formulation_dict(new_term_dict, new_sign_dict)

        new_wf = WeakFormulation(term_sign_dict=[new_term_dict, new_sign_dict], test_forms=self._wf._test_forms)
        new_wf.unknowns = self._wf.unknowns  # pass the unknowns
        new_wf._bc = self._wf._bc   # pass the bc

        return new_wf

    def _parse_new_weak_formulation_dict(self, new_term_dict, new_sign_dict):
        term_dict = dict()
        sign_dict = dict()

        for i in self._wf._term_dict:
            term_dict[i] = ([], [])
            sign_dict[i] = ([], [])

            for j in range(2):
                for k in range(len(self._wf._term_dict[i][j])):
                    new_term = new_term_dict[i][j][k]
                    new_sign = new_sign_dict[i][j][k]

                    if isinstance(new_term, str) and new_term in self._wf:   # this term remain untouched.
                        assert new_sign in self._wf   # trivial check.
                        _t = self._wf[new_term][1]
                        if isinstance(new_sign, str) and new_sign in self._wf:
                            sign = self._wf[new_term][0]
                        else:
                            assert new_sign in ('+', '-'), f"sign must be + or -."
                            sign = new_sign
                        term_dict[i][j].append(_t)
                        sign_dict[i][j].append(sign)

                    else:
                        assert isinstance(new_term, list) and \
                               isinstance(new_sign, list) and \
                               len(new_sign) == len(new_term), f"Whenever we have a " \
                                                               f"modification to a term, pls put it in a list."

                        for term, sign in zip(new_term, new_sign):

                            if term._is_able_to_be_a_weak_term():
                                term_dict[i][j].append(term)
                                sign_dict[i][j].append(sign)

                            else:
                                raise NotImplementedError()

        return term_dict, sign_dict

    def rearrange(self, rearrangement):
        """rearrange the terms."""
        if isinstance(rearrangement, dict):
            pass
        elif isinstance(rearrangement, (list, tuple)):
            assert len(rearrangement) == len(self._wf), \
                f"When provide list (or tuple) of rearrangement, we must have a list (or tuple) of length equal to " \
                f"amount of equations."
            rag_dict = dict()
            for i, rag in enumerate(rearrangement):
                assert isinstance(rag, str) or rag is None, \
                    f"rearrangement can only be represent by str or None, {i}th rearrangement = {rag} is illegal."
                rag_dict[i] = rag
            rearrangement = rag_dict

        term_dict = dict()
        sign_dict = dict()
        for i in self._wf._term_dict:
            term_dict[i] = ([], [])
            sign_dict[i] = ([], [])

        for i in rearrangement:
            assert isinstance(i, int), f"key:{i} is not integer, pls make sure use integer as dict keys."
            assert 0 <= i < len(self._wf), f"I cannot find {i}th equation."

            ri = rearrangement[i]
            if ri is None or ri == '':
                pass

            else:
                assert isinstance(ri, str), "Use str to represent a rearrangement pls."

                # noinspection PyUnresolvedReferences
                left_terms, right_terms = ri.replace(' ', '').split('=')
                _left_terms = left_terms.replace(',', '')
                _right_terms = right_terms.replace(',', '')

                _ = _left_terms + _right_terms
                assert _.isnumeric(), \
                    f"rearrangement for {i}th equation: {ri} is illegal, using only comma to separate " \
                    f"positive indices."

                left_terms = left_terms.split(',')
                right_terms = right_terms.split(',')

                _ = list()
                if left_terms != ['', ]:
                    _.extend(left_terms)
                else:
                    left_terms = 0
                if right_terms != ['', ]:
                    _.extend(right_terms)
                else:
                    right_terms = 0
                _.sort()

                number_terms = len(self._wf._term_dict[i][0]) + len(self._wf._term_dict[i][1])
                assert _ == [str(j) for j in range(number_terms)], \
                    f'indices of rearrangement for {i}th equation: {ri} are wrong.'

                if left_terms == 0:
                    pass
                else:
                    for k in left_terms:
                        target_index = str(i) + '-' + k
                        sign, target_term = self._wf[target_index]
                        if target_term == 0:
                            continue
                        else:
                            _j = self._wf._parse_index(target_index)[1]

                            if _j == 0:  # the target term is also at left.
                                pass
                            elif _j == 1:  # the target term is at opposite side, i.e., right
                                sign = self._switch_sign(sign)
                            else:
                                raise Exception()
                            term_dict[i][0].append(target_term)
                            sign_dict[i][0].append(sign)

                if right_terms == 0:
                    pass
                else:
                    for m in right_terms:
                        target_index = str(i) + '-' + m
                        sign, target_term = self._wf[target_index]
                        if target_term == 0:
                            continue
                        else:
                            _j = self._wf._parse_index(target_index)[1]

                            if _j == 0:  # the target term is at opposite side, i.e., left
                                sign = self._switch_sign(sign)
                            elif _j == 1:  # the target term is also at right.
                                pass
                            else:
                                raise Exception()
                            term_dict[i][1].append(target_term)
                            sign_dict[i][1].append(sign)

        for _i in self._wf._term_dict:
            if _i not in rearrangement or rearrangement[_i] is None or rearrangement[_i] == '':
                term_dict[_i] = self._wf._term_dict[_i]
                sign_dict[_i] = self._wf._sign_dict[_i]
            else:
                pass

        new_wf = WeakFormulation(term_sign_dict=[term_dict, sign_dict], test_forms=self._wf._test_forms)
        new_wf.unknowns = self._wf.unknowns   # pass the unknowns
        new_wf._bc = self._wf._bc   # pass the bc
        return new_wf

    @staticmethod
    def _switch_sign(sign):
        """"""
        if sign == '+':
            return '-'
        elif sign == '-':
            return '+'
        else:
            raise Exception()

    def integration_by_parts(self, index):
        """integration by parts."""
        term = self._wf[index][1]
        assert term != 0, f"Cannot apply integration by parts to term '{index}': {term}"
        terms, signs = term._integration_by_parts()
        return self.replace(index, terms, signs)


if __name__ == '__main__':
    # python src/wf/main.py

    import __init__ as ph
    # import phlib as ph
    # ph.config.set_embedding_space_dim(3)
    manifold = ph.manifold(3)
    mesh = ph.mesh(manifold)

    ph.space.set_mesh(mesh)
    O0 = ph.space.new('Omega', 0)
    O1 = ph.space.new('Omega', 1)
    O2 = ph.space.new('Omega', 2)
    O3 = ph.space.new('Omega', 3)

    # ph.list_spaces()
    # ph.list_meshes()

    w = O1.make_form(r'\omega^1', "vorticity1")
    u = O2.make_form(r'u^2', "velocity2")
    f = O2.make_form(r'f^2', "body-force")
    P = O3.make_form(r'P^3', "total-pressure3")

    wXu = w.wedge(ph.Hodge(u))
    dsP = ph.codifferential(P)
    dsu = ph.codifferential(u)
    du = ph.d(u)
    du_dt = ph.time_derivative(u)

    # ph.list_forms(globals())

    exp = [
        'du_dt + wXu - dsP = f',
        'w = dsu',
        'du = 0',
    ]
    pde = ph.pde(exp, globals())
    pde.unknowns = [u, w, P]
    # pde.pr(indexing=True)

    wf = pde.test_with([O2, O1, O3], sym_repr=[r'v^2', r'w^1', r'q^3'])

    wf = wf.derive.integration_by_parts('0-2')
    wf = wf.derive.integration_by_parts('1-1')

    wf = wf.derive.rearrange(
        {
            0: '0, 1, 2 = 4, 3',
            1: '1, 0 = 2',
            2: ' = 0',
        }
    )

    # wf.print()

    # i = 0
    # terms = wf._term_dict[i]
    # signs = wf._sign_dict[i]
    #
    # ode_i = ph.ode(terms_and_signs=[terms, signs])
    # ode_i.print_representations()
    # ph.list_forms()

    td = wf.td
