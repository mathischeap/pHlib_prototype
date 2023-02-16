# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 2/16/2023 12:16 PM
"""

from abc import ABC
import matplotlib.pyplot as plt
import matplotlib
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "DejaVu Sans",
    "text.latex.preamble": r"\usepackage{amsmath}"
})
matplotlib.use('TkAgg')


class FrozenError(Exception):
    """Raise when we try to define new attribute for a frozen object."""


class Frozen(ABC):
    """"""

    def __setattr__(self, key, value):
        """"""
        if self.___is_frozen___ and key not in dir(self):
            raise FrozenError(f" <Frozen> : {self} is frozen. CANNOT define new attributes.")
        object.__setattr__(self, key, value)

    def _freeze(self):
        """Freeze self, can define no more new attributes. """
        self.___IS_FROZEN___ = True

    def _melt(self):
        """Melt self, so  we can define new attributes."""
        self.___IS_FROZEN___ = False

    @property
    def _is_frozen(self):
        """Return the status of the form, frozen (True) or melt (False)?"""
        return self.___is_frozen___

    @property
    def ___is_frozen___(self):
        """"""
        try:
            return self.___IS_FROZEN___
        except AttributeError:
            object.__setattr__(self, '___IS_FROZEN___', False)
            return self.___IS_FROZEN___


if __name__ == '__main__':
    from doctest import testmod

    testmod()
