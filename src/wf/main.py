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
    "text.latex.preamble": r"\usepackage{amsmath}",
})
matplotlib.use('TkAgg')


class WeakFormulation(Frozen):
    """"""

    def __init__(self, term_sign_dict=None, expression=None, test_forms=None):
        """

        Parameters
        ----------
        term_sign_dict
        expression
        """
        if term_sign_dict is not None:
            assert expression is None, f"Only allow one of `term_sign_dict` and `expression` being provided."
            self._parse_term_sign_dict(term_sign_dict, test_forms)
        else:
            assert expression is not None, f"Please provide one of `term_sign_dict` and `expression`."
            self._parse_expression(expression)
        self._consistence_checker()
        self._unknowns = None
        self._derive = None
        self._freeze()

    def _parse_term_sign_dict(self, term_sign_dict, test_forms):
        """"""
        term_dict, sign_dict = term_sign_dict
        ind_dict = dict()
        indexing = dict()
        for i in term_dict:   # ith equation
            ind_dict[i] = ([], [])
            for j, terms in enumerate(term_dict[i]):
                k = 0
                for m in range(len(terms)):
                    if j == 0:
                        index = str(i) + '|' + str(k) + '='
                    elif j == 1:
                        index = str(i) + '|=' + str(k)
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
        raise Exception()

    def _consistence_checker(self):
        """We do consistence check here and parse properties like mesh and so on."""
        ts = list()
        for tf in self._test_forms:
            ts.append(tf.space)
        self._test_spaces = ts

        mesh = None
        elementary_forms = set()
        for i in self._term_dict:   # ith equation
            for terms in self._term_dict[i]:
                for term in terms:
                    if term == 0:
                        pass
                    else:
                        if mesh is None:
                            mesh = term.mesh
                        else:
                            assert mesh == term.mesh, f"mesh dis-match."
                            elementary_forms.update(term._elementary_forms)
        self._mesh = mesh
        self._elementary_forms = elementary_forms

    @property
    def mesh(self):
        return self._mesh

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

    @property
    def elementary_forms(self):
        """Return a set of root forms that this equation involves."""
        return self._elementary_forms

    @property
    def unknowns(self):
        """"""
        return self._unknowns

    @unknowns.setter
    def unknowns(self, unknowns):
        """"""
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
            assert unknown in self._elementary_forms, f"{i}th variable is not an elementary form."

        self._unknowns = unknowns

    @property
    def test_forms(self):
        return self._test_forms

    def print_representations(self, indexing=True):
        """"""
        seek_text = r'Seek $\left('
        form_sr_list = list()
        space_sr_list = list()
        for un in self.unknowns:
            form_sr_list.append(rf' {un._sym_repr}')
            space_sr_list.append(rf"{un.space._sym_repr}")
        seek_text += ','.join(form_sr_list)
        seek_text += r'\right) \in '
        seek_text += r'\times '.join(space_sr_list)
        seek_text += r'$, such that\\'
        symbolic = ''
        number_equations = len(self._term_dict)
        for i in self._term_dict:
            for t, terms in enumerate(self._term_dict[i]):
                for j, term in enumerate(terms):
                    sign = self._sign_dict[i][t][j]
                    term = self._term_dict[i][t][j]

                    if term == 0:
                        term_sym_repr = '0'
                    else:
                        term_sym_repr = term._sym_repr

                    if indexing:
                        index = self._ind_dict[i][t][j]
                        term_sym_repr = r'\underbrace{'+ term_sym_repr + r'}_{' + \
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

        if indexing:
            figsize = (14, 2 * len(self._term_dict))
        else:
            figsize = (14, len(self._term_dict))
        fig, ax = plt.subplots(figsize=figsize)
        fig.patch.set_visible(False)
        ax.axis('off')
        table = ax.table(cellText=[[seek_text + symbolic, ], ],
                         rowLabels=['symbolic', ], rowColours='gcy',
                         colLoc='left', loc='center', cellLoc='left')
        if indexing:
            table.scale(1, 5 * len(self._term_dict))
        else:
            table.scale(1, 3 * len(self._term_dict))
        table.set_fontsize(20)
        fig.tight_layout()
        plt.show()

    @property
    def derive(self):
        """The derivations that to be applied to this current weak formulation."""
        if self._derive is None:
            self._derive = _Derive(self)
        return self._derive


class _Derive(Frozen):
    """"""

    def __init__(self, wf):
        self._wf = wf
        self._derivations = dict()
        self._freeze()

    def __call__(self, *args, **kwargs):
        """Apply all derivations and return a new weak-formulation."""

    def _update_derivations(self, index, key, *args):
        """"""


    def IBP_wrt_codifferential(self, *args, **kwargs):
        """Abbr. of method `integration_by_parts_wrt_codifferential`."""
        return self.integration_by_parts_wrt_codifferential(*args, **kwargs)

    def integration_by_parts_wrt_codifferential(self, index):
        """"""
        sign, term = self._wf[index]
        assert term != 0, f"Cannot apply integration by parts to term '{index}': {term}"
        new_terms = term._integration_by_parts()



if __name__ == '__main__':
    # python src/wf/main.py
    import __init__ as ph
    # import phlib as ph
    ph.config.set_embedding_space_dim(3)
    manifold = ph.manifold(3)
    mesh = ph.mesh(manifold)

    ph.space.set_mesh(mesh)
    O0 = ph.space.new('Omega', 0, p=3)
    O1 = ph.space.new('Omega', 1, p=3)
    O2 = ph.space.new('Omega', 2, p=3)
    O3 = ph.space.new('Omega', 3, p=3)

    w = O1.make_form(r'\omega^1', "vorticity1")
    u = O2.make_form(r'u^2', r"velocity2")
    f = O2.make_form(r'f^2', r"body-force")
    P = O3.make_form(r'P^3', r"total-pressure3")

    wXu = w.wedge(ph.Hodge(u))
    dsP = ph.codifferential(P)
    dsu = ph.codifferential(u)
    du = ph.d(u)
    du_dt = ph.time_derivative(u)

    exp = [
        'du_dt + wXu - dsP = f',
        'w = dsu',
        'du = 0',
    ]
    pde = ph.pde(exp, globals())
    pde.unknowns = [u, w, P]
    wf = pde.test_with([O2, O1, O3], sym_repr=[r'v^2', r'w^1', r'q^3'])
    # wf.print_representations(indexing=True)
    # for index in wf:
    #     print(wf[index])

    wf.derive.integration_by_parts_wrt_codifferential('0|2=')

