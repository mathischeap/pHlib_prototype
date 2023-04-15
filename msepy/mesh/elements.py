# -*- coding: utf-8 -*-
"""
@author: Yi Zhang
@contact: zhangyi_aero@hotmail.com
"""
import sys
if './' not in sys.path:
    sys.path.append('./')

import numpy as np
from src.tools.frozen import Frozen
from scipy.sparse import csr_matrix


class MsePyMeshElements(Frozen):
    """"""

    def __init__(self, mesh):
        """"""
        self._mesh = mesh
        self._origin = None
        self._delta = None
        self._distribution = None   #
        self._numbering = None
        self._num = None
        self._num_accumulation = None
        self._index_mapping = None
        self._map = None
        self._freeze()

    @property
    def map(self):
        return self._map

    def _parse_origin_and_delta_from_layout(self, layouts):
        """"""
        origin = dict()
        for i in layouts:
            assert i in self._mesh.manifold.regions
            layout = layouts[i]
            origin[i] = list()
            for lyt in layout:
                origin[i].append([0, ])
                _lyt_one = lyt[0:-1]
                if len(_lyt_one) == 0:
                    pass
                else:
                    for j in range(len(_lyt_one)):
                        origin[i][-1].append(np.sum(_lyt_one[0:j+1]))

                assert round(origin[i][-1][-1] + lyt[-1], 9) == 1, f"safety check"
                origin[i][-1] = np.array(origin[i][-1])
        delta = layouts
        dis = dict()
        for i in delta:
            dis[i] = [len(_) for _ in delta[i]]
        return origin, delta, dis

    def _generate_elements_from_layout(self, layouts):
        """

        Parameters
        ----------
        layouts

        Returns
        -------

        """
        self._origin, self._delta, self._distribution = self._parse_origin_and_delta_from_layout(layouts)
        self._numbering, self._num, self._num_accumulation = self._generate_element_numbering_from_layout(layouts)
        self._index_mapping = self._generate_indices_mapping_from_layout(layouts)
        self._map = self._generate_element_map(layouts)

    def _generate_element_numbering_from_layout(self, layouts):
        """"""
        regions = self._mesh.manifold.regions
        element_numbering = dict()
        # a naive way of numbering elements.
        current_number = 0
        num_accumulation = list()
        for i in regions:
            layout_of_region = layouts[i]
            element_distribution = [len(_) for _ in layout_of_region]
            number_local_elements = np.prod(element_distribution)
            element_numbering[i] = np.arange(
                current_number, current_number+number_local_elements
            ).reshape(element_distribution, order='F')
            num_accumulation.append(current_number)
            current_number += number_local_elements
        amount_of_elements = int(current_number)
        return element_numbering, amount_of_elements, num_accumulation

    def _generate_indices_mapping_from_layout(self, layouts):
        """"""
        regions = self._mesh.manifold.regions

        existing_unique = False
        for i in regions:
            region = regions[i]
            ctm = region._ct.mtype
            indicator = ctm._indicator
            if indicator == 'Unique':
                existing_unique = True
            else:
                pass

        if existing_unique:
            mip = MsePyMeshElementsIndexMapping(self._num)
        else:

            element_mtype_dict = dict()

            for i in regions:
                layout_of_region = layouts[i]
                element_numbering_of_region = self._numbering[i]
                region = regions[i]
                ctm = region._ct.mtype
                r_emd = ctm._distribute_to_element(layout_of_region, element_numbering_of_region)
                for key in r_emd:
                    if key in element_mtype_dict:
                        element_mtype_dict[key].extend(r_emd[key])
                    else:
                        element_mtype_dict[key] = r_emd[key]

            for key in element_mtype_dict:
                element_mtype_dict[key].sort()

            mip = MsePyMeshElementsIndexMapping(element_mtype_dict, self._num)

        reference_delta = list()
        for ce in mip._reference_elements:
            in_region, local_indices = self._find_region_and_local_indices_of_element(ce)
            delta_s = self._delta[in_region]
            rd = list()
            for i, index in enumerate(local_indices):
                rd.append(delta_s[i][index])
            reference_delta.append(rd)
            mip._reference_delta = np.array(reference_delta)

        return mip

    def _find_region_and_local_indices_of_element(self, i):
        """

        Parameters
        ----------
        i

        Returns
        -------

        """
        assert 0 <= i < self._num, f"i={i} wrong, I have {self._num} elements, i must be in [0, {self._num}]."
        assert i % 1 == 0, f"i must be integer."
        in_region = -1
        num_regions = len(self._mesh.manifold.regions)
        for j, na in enumerate(self._num_accumulation):
            if j == num_regions - 1:  # the last region.
                in_region = j
                break
            else:
                if na <= i < self._mesh.manifold.regions[j+1]:
                    in_region = j
                    break
                else:
                    pass

        assert in_region != -1, f"must have found a region."

        local_numbering = i - self._num_accumulation[in_region]
        # numbering = self._numbering[in_region]
        dis = self._distribution[in_region]

        ndim = len(dis)

        indices = list()
        for _ in range(ndim-1):
            n = ndim - 1 - _

            num_layer = np.prod(dis[:n])

            indices.append(local_numbering // num_layer)

            local_numbering = local_numbering % num_layer

        indices.append(local_numbering)

        indices = indices[::-1]

        return in_region, indices

    def _generate_element_map(self, layouts):
        """"""
        regions = self._mesh.manifold.regions
        region_map = regions.map
        structured_regions = list()
        for i in regions:
            Rmap = region_map[i]
            structured_regions.append(
                isinstance(Rmap, list) and all([isinstance(_, int) or _ is None for _ in Rmap])
            )
        structured_regions = all(structured_regions)

        if structured_regions:  # `map_type = 0` region map. See `_check_map` of `regions`.

            element_map = self._generate_element_map_form_structured_regions(layouts)
            # return a 2-d array as the element-map

        else:
            raise NotImplementedError()
            # should return a 1-d data-structure of strings (which indicate the location of the element.)

        return element_map

    def _generate_element_map_form_structured_regions(self, layouts):
        """"""
        numbering = self._numbering
        total_num_elements = self._num
        ndim = self._mesh.ndim
        element_map = - np.ones((total_num_elements, 2 * ndim), dtype=int)

        for i in numbering:
            _nmb = numbering[i]
            layout = layouts[i]
            element_distribution = [len(_) for _ in layout]
            assert len(layout) == ndim, f"layout[{i}] is wrong."

            for axis in range(ndim):
                for layer in range(element_distribution[axis]):

                    for_elements = self._find_on_layer(_nmb, axis, layer)

                    plus_layer = layer + 1
                    minus_layer = layer - 1

                    if minus_layer < 0:
                        assert minus_layer == -1, f"safety check"
                        neighbor_region = self._find_region_on(i, axis, 0)
                        if neighbor_region is None:  # this side is boundary
                            minus_side_elements = None
                        else:
                            neighbor_region_numbering = numbering[neighbor_region]
                            minus_side_elements = self._find_on_layer(
                                neighbor_region_numbering, axis, -1
                            )

                    else:
                        minus_side_elements = self._find_on_layer(_nmb, axis, minus_layer)

                    if plus_layer >= element_distribution[axis]:
                        assert plus_layer == element_distribution[axis], f"safety check"
                        neighbor_region = self._find_region_on(i, axis, 1)
                        if neighbor_region is None:  # this side is boundary
                            plus_side_elements = None
                        else:
                            neighbor_region_numbering = numbering[neighbor_region]
                            plus_side_elements = self._find_on_layer(
                                neighbor_region_numbering, axis, 0
                            )

                    else:
                        plus_side_elements = self._find_on_layer(_nmb, axis, plus_layer)

                    if minus_side_elements is not None:
                        element_map[for_elements, 2*axis] = minus_side_elements
                    else:
                        pass
                    if plus_side_elements is not None:
                        element_map[for_elements, 2*axis + 1] = plus_side_elements
                    else:
                        pass

        return element_map

    def _find_region_on(self, i, axis, side):
        """"""
        rmp = self._mesh.manifold.regions.map[i]
        return rmp[2*axis + side]

    def _find_on_layer(self, numbering, axis, layer):
        """

        Parameters
        ----------
        numbering
        axis
        layer

        Returns
        -------

        """
        if axis == 0:
            return numbering[layer, ...]
        elif axis == 1:
            return numbering[:, layer, ...]
        elif axis == 2:
            return numbering[:, :, layer, ...]
        else:
            raise NotImplementedError()


class MsePyMeshElementsIndexMapping(Frozen):
    """"""

    def __init__(self, ci_ei_map, total_num_elements=None):
        """

        Parameters
        ----------
        ci_ei_map :
            cache_index -> element_indices

        """
        if isinstance(ci_ei_map, int):  # one to one mapping; each element is unique.
            # in this case, ci_ei_map is the amount of elements.
            ci_ei_map = np.arange(ci_ei_map)[:, np.newaxis]
            ei_ci_map = ci_ei_map[:, 0]

        elif isinstance(ci_ei_map, dict):
            ci_ei_map = tuple(ci_ei_map.values())
            ei_ci_map = np.zeros(total_num_elements, dtype=int)
            for i, indices in enumerate(ci_ei_map):
                ei_ci_map[indices] = i

        else:
            raise NotImplementedError()

        self._c2e = ci_ei_map
        self._e2c = csr_matrix(ei_ci_map).T

        self._reference_elements = list()
        for ce in self._c2e:
            self._reference_elements.append(ce[0])
        self._reference_elements = np.array(self._reference_elements)
        self._reference_delta = None
        self._freeze()


if __name__ == '__main__':
    # python msepy/mesh/elements.py
    import __init__ as ph
    space_dim = 2
    ph.config.set_embedding_space_dim(space_dim)

    manifold = ph.manifold(space_dim)
    mesh = ph.mesh(manifold)

    msepy, obj = ph.fem.apply('msepy', locals())

    mnf = obj['manifold']
    msh = obj['mesh']

    msepy.config(mnf)('crazy', c=0.1, periodic=False, bounds=[[0, 2] for _ in range(space_dim)])
    msepy.config(msh)([3 for _ in range(space_dim)])
    print(msh.elements.map)
