
# -*- coding: utf-8 -*-
"""
@author: Yi Zhang
@contact: zhangyi_aero@hotmail.com
"""
import sys
import numpy as np
from src.tools.frozen import Frozen

if './' not in sys.path:
    sys.path.append('./')


class MsePyMeshElements(Frozen):
    """"""

    def __init__(self, mesh):
        """"""
        self._mesh = mesh
        self._origin = None
        self._delta = None
        self._numbering = None
        self._num = None
        self._index_mapping = None
        self._map = None
        self._freeze()

    def _parse_origin_and_delta_from_layout(self, layouts):
        """"""
        origin = dict()
        for i in layouts:
            layout = layouts[i]
            origin[i] = list()
            for lyt in layout:
                origin[i].append([0, ])
                for ly in lyt[1:]:
                    origin[i][-1].append(ly)
                origin[i][-1] = np.array(origin[i][-1])
        delta = layouts
        return origin, delta

    def _generate_elements_from_layout(self, layouts, enm=None):
        """"""
        self._origin, self._delta = self._parse_origin_and_delta_from_layout(layouts)
        self._numbering, self._num = self._generate_element_numbering_from_layout(layouts, enm=enm)
        self._index_mapping = self._generate_indices_mapping_from_layout(layouts)

    def _generate_element_numbering_from_layout(self, layouts, enm=None):
        """"""
        regions = self._mesh.manifold.regions
        element_numbering = dict()
        if enm is None:  # a naive way of numbering elements.
            current_number = 0
            for i in regions:
                layout_of_region = layouts[i]
                element_distribution = [len(_) for _ in layout_of_region]
                number_local_elements = np.prod(element_distribution)
                element_numbering[i] = np.arange(
                    current_number, current_number+number_local_elements
                ).reshape(element_distribution, order='F')
                current_number += number_local_elements
            amount_of_elements = int(current_number)
        else:
            raise NotImplementedError()
        return element_numbering, amount_of_elements

    def _generate_indices_mapping_from_layout(self, layouts):
        """"""
        regions = self._mesh.manifold.regions
        all_unique = True
        for i in regions:
            layout_of_region = layouts[i]
            element_distribution = [len(_) for _ in layout_of_region]
            region = regions[i]
            ctm = region._ct.mtype
            indicator = ctm._indicator

            if indicator != 'unique':

                all_unique = False

                print(111)

            else:
                pass

        if all_unique:

            imp = MsePyMeshElementsIndexMapping(self._num)

        else:
            pass

        # return imp


class MsePyMeshElementsIndexMapping(Frozen):
    """"""

    def __init__(self, ci_ei_map):
        """

        Parameters
        ----------
        ci_ei_map :
            cache_index -> element_indices

        """
        if isinstance(ci_ei_map, int):  # one to one mapping; each element is unique.
            # in this case, ci_ei_map is the amount of elements.
            ci_ei_map = np.arange(ci_ei_map)[:, np.newaxis]
            ei_ci_map = ci_ei_map
        else:
            pass

        self._c2e = ci_ei_map
        self._e2c = ei_ci_map
        self._freeze()
