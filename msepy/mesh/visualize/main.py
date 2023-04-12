# -*- coding: utf-8 -*-
"""
@author: Yi Zhang
@contact: zhangyi_aero@hotmail.com
"""
import numpy as np
import sys
if './' not in sys.path:
    sys.path.append('./')

from src.tools.frozen import Frozen
from msepy.mesh.visualize.matplot import MsePyMeshVisualizeMatplot
from msepy.mesh.visualize.vtk_ import MsePyMeshVisualizeVTK



class MsePyMeshVisualize(Frozen):
    """"""

    def __init__(self, mesh):
        self._mesh = mesh
        self._matplot = MsePyMeshVisualizeMatplot(mesh)
        self._vtk = MsePyMeshVisualizeVTK(mesh)
        self._freeze()

    def __call__(self, *args, **kwargs):
        """"""
        if self._mesh.esd in (1, 2):
            return self.matplot(*args, **kwargs)
        elif self._mesh.esd == 3:
            return self.vtk(*args, **kwargs)
        else:
            raise NotImplementedError()

    @property
    def matplot(self):
        return self._matplot

    @property
    def vtk(self):
        return self._vtk

    def _mesh_data(
            self,
            refining_factor=1,
    ):
        """"""
        if refining_factor <= 0.1:
            refining_factor = 0.1
        samples = 20000 * refining_factor
        samples = int((np.ceil(samples / self._mesh.elements._num))**(1/self._mesh.esd))
        if samples >= 200:
            samples = 200
        ndim = self._mesh.ndim
        xi_et_sg = [np.linspace(-1, 1, samples) for _ in range(ndim)]
        region_map = self._mesh.manifold.regions.map
        xi_et_sg = np.meshgrid(*xi_et_sg, indexing='ij')
        xyz = self._mesh.manifold.ct.mapping(*xi_et_sg)
        return xyz, region_map
