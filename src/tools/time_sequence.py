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
        """"""
        self._object = None
        self._freeze()

    def specify(self, obj):
        """specify to a particular time sequence."""
        assert obj._is_specific_time_sequence(), f"I need a time sequence instance."
        self._object = obj

    def __getitem__(self, k):
        """return t[k], not return t=k."""
        if isinstance(k, (int, float)):
            assert self._object is not None, \
                f"Abstract time sequence needs a object before referring to a time instance. "
            return self._object[k]
        elif isinstance(k, str):   # abstract time instance
            return AbstractTimeInstant(self, k)
        else:
            raise Exception()

    def __repr__(self):
        """customized repr."""
        super_repr = super().__repr__().split('object')[1]
        return f"<AbstractTimeSequence" + super_repr

    @staticmethod
    def _is_abstract_time_sequence():
        """A private tag."""
        return True


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

    @staticmethod
    def _is_specific_time_sequence():
        """A private tag."""
        return True

    @staticmethod
    def _is_time_sequence():
        """A private tag."""
        return True


class ConstantTimeSequence(TimeSequence):
    """Steps are all equal.

    """

    def __init__(self, t0_max_n, factor):
        """

        Parameters
        ----------
        t0_max_n
        factor
        """
        super().__init__()
        assert len(t0_max_n) == 3, f"I need a tuple of three numbers."
        t0, t_max, n = t0_max_n
        # n is equal to the number of time intervals between t0 and t_max.
        assert t_max > t0 and n % 1 == 0 and n > 0
        assert factor % 1 == 0 and factor > 0, f"`factor` needs to be a positive integer."

        self._t_0 = t0
        self._t_max = t_max
        self._melt()
        self._factor = factor  # in each step, we have factor - 1 intermediate time instances.
        self._dt = (t_max - t0) * factor / n
        self._k_max = n / factor
        self._n = n
        self._allowed_reminder = [round(1*i/factor, 8) for i in range(factor)]
        self._freeze()

    @property
    def dt(self):
        """time interval between tk and tk+1."""
        return self._dt

    @property
    def k_max(self):
        """the max valid k for t[k]."""
        return self._k_max

    def __getitem__(self, k):
        """return t[k], not return t=k."""
        if isinstance(k, (int, float)):
            time = self.t_0 + k * self._dt
            remainder = round(k % 1, 8)
            if time < self.t_0:
                raise TimeInstantError(
                    f"t[{k}] = {time} is lower than t0={self.t_0}.")
            elif time > self.t_max:
                raise TimeInstantError(
                    f"t[{k}] = {time} is higher than t_max={self.t_max}.")
            elif remainder not in self._allowed_reminder:
                raise TimeInstantError(
                    f"t[{k}] = {time} is not a valid time instance of the sequence.")
            else:
                return TimeInstant(time)
        elif isinstance(k, str):   # abstract time instance
            return AbstractTimeInstant(self, k)
        else:
            raise Exception()

    def __repr__(self):
        super_repr = super().__repr__().split('object')[1]
        return f"<ConstantTimeSequence ({self.t_0}, {self.t_max}, {self._n}) " \
               f"@ k_max={self._k_max}, dt={self._dt}, factor={self._factor}" + \
            super_repr


class TimeInstantError(Exception):
    """Raise when we try to define new attribute for a frozen object."""


class TimeInstant(Frozen):
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
        return f'<TimeInstant t={self.time}' + super_repr

    def __eq__(self, other):
        return other.__class__.__name__ == 'TimeInstant' and other.time == self.time


class AbstractTimeInstant(Frozen):
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

            >>> t = ConstantTimeSequence([0, 5, 5], 3)
            >>> t = t['k+1/3'](k=1)
            >>> print(t)  # doctest: +ELLIPSIS
            <TimeInstant t=4.0 at ...

        """
        time_instance_str = self._k
        for key in kwargs:
            time_instance_str = time_instance_str.replace(key, str(kwargs[key]))
        time = eval(time_instance_str)
        assert isinstance(time, (int, float)), f"format wrong, `eval` does not return a number."
        if self.time_sequence.__class__.__name__ == 'AbstractTimeSequence':
            assert self.time_sequence._object is not None, \
                f"The abstract time sequence has no object (particular time sequence)."
        else:
            pass
        try:
            ts = self.time_sequence[time]
        except TimeInstantError:
            tb = traceback.format_exc().split('TimeInstantError:')[1]
            key_str = ["'" + str(key) + "'" + '=' + str(kwargs[key]) for key in kwargs]
            local_error_message = f"t['{self.k}'] for {''.join(key_str)} leads to"
            raise TimeInstantError(local_error_message + tb)
        return ts

    def __repr__(self):
        """"""
        super_repr = super().__repr__().split('object')[1]
        return f"<AbstractTimeInstant t={self.k}" + super_repr[:-1] + f' of {self.time_sequence}>'


class TimeStep(Frozen):
    """"""

    def __init__(self, t_start, t_end):
        """

        Parameters
        ----------
        t_start :
            start time, the time is t[t_start], not t_start.
        t_end :
            end time, the time is t[t_end], not t_end.
        """

class AbstractTimeStep(Frozen):
    """"""

    def __init__(self, ts, t_start, t_end):
        """

        Parameters
        ----------

        Parameters
        ----------
        ts:
            The time sequence.

        t_start :
            start time, the time is t[t_start], not t_start.
        t_end :
            end time, the time is t[t_end], not t_end.
        """



if __name__ == '__main__':
    # python src/tools/time_sequence.py
    from doctest import testmod
    testmod()

    ct = ConstantTimeSequence([0, 100, 100], 2)
    t = ct['k+0.5']
    print(t)
    print(t(k=5.))

    at = AbstractTimeSequence()
    t = at['k+j']
    at.specify(ct)
    print(t(k=1.1, j=0.9))
    # print(ts[1+1/4])
