# -*- coding: utf-8 -*-
"""
@author: Yi Zhang
@contact: zhangyi_aero@hotmail.com
@time: 11/26/2022 2:56 PM
"""

import sys

if './' not in sys.path:
    sys.path.append('./')

from src.tools.frozen import Frozen
import traceback


class AbstractTimeSequence(Frozen):
    """"""

    def __init__(self):
        self._freeze()


class TimeSequence(Frozen):
    """"""

    def __init__(self):
        self._t_0 = None
        self._t_max = None
        self._freeze()

    @property
    def t_0(self):
        return self._t_0

    @property
    def t_max(self):
        return self._t_max



class ConstantTimeSequence(TimeSequence):
    """"""

    def __init__(self, t0_max_n, factor):
        super().__init__()
        assert len(t0_max_n) == 3, f"I need a tuple of three numbers."
        t0, t_max, n = t0_max_n
        assert t_max > t0 and n % 1 == 0 and n > 0
        assert factor % 1 == 0 and factor > 0, f"`factor` must be positive integer."

        self._t_0 = t0
        self._t_max = t_max
        self._melt()
        self._factor = factor  # in each step, we have factor - 1 intermediate time instances.
        self._dt = (t_max - t0) * factor / (n - 1)
        self._k_max = (n - 1) / (factor)
        self._n = n
        self._allowed_reminder = [round(1*i/factor, 8) for i in range(factor)]
        self._freeze()

    @property
    def dt(self):
        return self._dt
    @property
    def k_max(self):
        return self._k_max

    def __getitem__(self, k):
        """"""
        if isinstance(k, (int, float)):
            time = self.t_0 + k * self._dt
            remainder = round(k % 1, 8)
            if k <= 0 or remainder not in self._allowed_reminder:
                raise TimeInstanceError(
                    f"t[{k}] = {time} is not a valid time instance of the sequence.")
            return TimeInstance(time)
        elif isinstance(k, str):   # abstract time instance
            return AbstractTimeInstance(self, k)
        else:
            raise Exception()

    def __repr__(self):
        super_repr = super().__repr__().split('object')[1]
        return f"<ConstantTimeSequence ({self.t_0}, {self.t_max}, {self._n}) " \
               f"@ k_max={self._k_max}, dt={self._dt}, factor={self._factor}" + \
            super_repr



class TimeInstanceError(Exception):
    """Raise when we try to define new attribute for a frozen object."""


class TimeInstance(Frozen):
    """This is a time instance regardless of the sequence."""

    def __init__(self, time):
        self._t = time
        self._freeze()

    @property
    def time(self):
        return self._t

    def __call__(self):
        return self.time

    def __repr__(self):
        """"""
        super_repr = super().__repr__().split('object')[1]
        return f'< TimeInstance t={self.time}' + super_repr

    def __eq__(self, other):
        return other.__class__.__name__ == 'TimeInstance' and other.time == self.time



class AbstractTimeInstance(Frozen):
    """"""

    def __init__(self, ts, k):
        self._ts = ts
        self._k = k
        self._freeze()

    @property
    def time_sequence(self):
        return self._ts

    @property
    def k(self):
        return self._k

    def __call__(self, **kwargs):
        """

        examples
        --------
        >>> t = ConstantTimeSequence([0, 5, 6], 3)
        >>> t = t['k+1/3'](k=1)
        >>> print(t)  # doctest: +ELLIPSIS
        < TimeInstance t=4.0 at ...

        """
        assert len(kwargs) == 1, f"pls only use 1 key in abstract time instance."
        key = list(kwargs.keys())[0]
        time_instance_str = self._k.replace(key, str(kwargs[key]))
        time = eval(time_instance_str)
        try:
            ts = self._ts[time]
        except TimeInstanceError:
            tb = traceback.format_exc().split('TimeInstanceError:')[1]
            local_error_message = f"t[{self.k}] for {key}={kwargs[key]} leads to"
            raise TimeInstanceError(local_error_message + tb)
        else:
            return ts

    def __repr__(self):
        """"""
        super_repr = super().__repr__().split('object')[1]
        return f"<AbstractTimeInstance t={self.k}" + super_repr[:-1] + f' of {self.time_sequence}>'



if __name__ == '__main__':
    # python src/tools/time_sequence.py
    from doctest import testmod
    testmod()

    t = ConstantTimeSequence([0, 101, 102], 1)
    print(t)
    print(t['k'](k=0))

    # print(ts[1+1/4])