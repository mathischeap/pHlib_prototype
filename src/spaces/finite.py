# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 3/16/2023 5:29 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')

from src.tools.frozen import Frozen



class SpaceFiniteSetting(Frozen):
    """"""

    def __init__(self, space):
        """"""
        self._space = space
        self._degrees_form_dict = dict()  # keys are degrees of the particular finite dimensional spaces,
        # and values are forms in these particular fintie dimensional spaces.
        self._all_finite_forms = set()
        self._freeze()

    def __repr__(self):
        """customized repr"""
        return f"<SpaceFiniteSetting of {self._space}>"

    def __len__(self):
        """how many particular finite dimensional spaces?"""
        return len(self._degrees_form_dict)

    def __iter__(self):
        """Go through all degrees of particular finite dimensional spaces"""
        for degree in self._degrees_form_dict:
            yield degree

    def __contains__(self, degree):
        """if there is a particular finite dimensional space of a certain degree?"""
        return degree in self._degrees_form_dict

    def __getitem__(self, degree):
        """return the forms in the particular finite dimensional space of this a certain degree"""
        assert degree in self._degrees_form_dict, f"I have no finite dimensional space of degree {degree}."
        return self._degrees_form_dict[degree]

    def new(self, degree):
        """define a new finite dimensional space of `degree`."""
        # do not change below assertion. It is important.
        if degree in self:
            pass
        else:
            self._degrees_form_dict[degree] = list()

    def specify_form(self, f, degree):
        """specify a form `f` to be an element of a particular finite dimensional space of degree `degree`."""
        assert f not in self._all_finite_forms, f"form {f} is already in."
        if degree in self:
            pass
        else:
            self.new(degree)

        the_degree = None
        find_it = False
        for the_degree in self:
            if the_degree == degree:
                find_it = True
                break
        assert find_it, f"we must have found it."
        self[the_degree].append(f)
        self._all_finite_forms.add(f)
        return the_degree


if __name__ == '__main__':
    # python src/spaces/finite.py
    import __init__ as ph

    m = ph.manifold(3)
    m = ph.mesh(m)

    O0 = ph.space.new('Omega', 0)

    finite = O0.finite
    finite.new(3)
    finite.new(4)
    finite.new([1,2,3])
    finite.new('4')

    for s in finite:
        print(s, finite[s])
