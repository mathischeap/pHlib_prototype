
import sys
if './' not in sys.path:
    sys.path.append('./')

from src.tools.frozen import Frozen
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import cm


class MsePyMeshVisualizeMatplot(Frozen):
    """"""

    def __init__(self, mesh):
        self._mesh = mesh
        self._freeze()

    def __call__(
            self,
            refining_factor=1,
            aspect='equal',
            usetex=True,
            labelsize=12,
            ticksize=12,
            xlim=None, ylim=None,
            saveto=None,
    ):
        """Default matplot method."""
        assert self._mesh.esd in (1, 2), f"matplot is not implemented for {self._mesh}."
        assert self._mesh.esd == self._mesh.ndim, f"NotImplemented."
        mesh_data, region_map = self._mesh.visualize._mesh_data(refining_factor=refining_factor)

        plt.rc('text', usetex=usetex)
        fig, ax = plt.subplots()
        ax.set_aspect(aspect)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(True)
        ax.spines['bottom'].set_visible(True)
        plt.xlabel(r"$x$", fontsize=labelsize)
        plt.ylabel(r"$y$", fontsize=labelsize)
        plt.tick_params(axis='both', which='both', labelsize=ticksize)
        if xlim is not None:
            plt.xlim(xlim)
        if ylim is not None:
            plt.ylim(ylim)

        for i in mesh_data:
            xyz = mesh_data[i]
            plt.plot(*xyz)

        plt.tight_layout()
        if saveto is not None and saveto != '':
            plt.savefig(saveto, bbox_inches='tight')
        else:
            plt.show()
        plt.close('all')
        return fig

