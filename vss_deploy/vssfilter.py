#!/usr/bin/env python3

# Copyright (C) 2021, Bayerische Motoren Werke Aktiengesellschaft (BMW AG),
#   Author: Alexander Domin (Alexander.Domin@bmw.de)
# Copyright (C) 2021, ProFUSION Sistemas e Soluções LTDA,
#   Author: Gustavo Barbieri (barbieri@profusion.mobi)
#   Author: Garbiel Fernandes (g7fernandes@profusion.mobi)
#   Author: Leandro Ferlin (leandroferlin@profusion.mobi)
#   Author: Leonardo Ramos (leo.ramos@profusion.mobi)
#
# SPDX-License-Identifier: MPL-2.0
#
# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was
# not distributed with this file, You can obtain one at
# http://mozilla.org/MPL/2.0/.

import sys
from typing import List, Optional

from vspec import VSSNode

from .model.deploy.deploy_map import VehicleDeployMap
from .model.vehicle_node import VehicleNode


def filter_vss_tree(
    vss_node: VSSNode,
    deploy_map: Optional[VehicleDeployMap] = None
) -> VehicleNode:
    '''
    Filters VSS tree using deploy data. If deploy_map is supplied, branches and
    leaves not contained in the deploy flat model are removed from vss_tree.
    As it walks the tree, custom derivatives are created.

    Parameters:
    -----------
    tree_node : VSSNode
        Root node of the VSS tree. Object inherited from anytree node that
        contains vspec data.
    deploy_map : Optional[VehicleDeployMap]
        Flat model containing deploy data.

    Returns:
    --------
    vehicle_tree : VehicleNode
        New tree of objects derived from VSSNode.
    '''

    deploy_entry = None
    if deploy_map:
        deploy_entry = deploy_map.get_entry(vss_node.qualified_name('_'))
        if isinstance(deploy_entry, list):
            deploy_entry = deploy_entry[0]

    vehicle_node = VehicleNode(vss_node, deploy_entry=deploy_entry)
    children: List[VehicleNode] = []
    for child_vss_node in vss_node.children:
        if deploy_map is None or deploy_map.contains(
                child_vss_node.qualified_name('_')
        ):
            child_vehicle_node = filter_vss_tree(child_vss_node, deploy_map)
            child_vehicle_node.parent = vehicle_node

            if child_vss_node.is_leaf == child_vehicle_node.is_leaf:
                children.append(child_vehicle_node)
            else:
                sys.stdout.write(
                    'Deploy has extra node(s) at: '
                    f'{child_vss_node.qualified_name("_")}\n'
                )

    vehicle_node.children = children

    return vehicle_node
