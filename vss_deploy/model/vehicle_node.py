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

from typing import Iterable, Optional

from anytree import Node

from vspec import VSSNode
from vspec.model.vsstree import DEFAULT_SEPARATOR

from . import Cardinality
from .deploy.deploy import deploy_from_entry
from .deploy.deploy_entry import VehicleDeployEntry
from .deploy.types.deploy_type import DeployType
from .deploy.types.deploy_with_method import DeployWithMethod
from .directives import Directives


class VehicleNode(Node):
    '''
    Node in a tree structure to associate a tree with VSSNodes used in
     vss-tools.

     :param original_node: VSSNode that originated this VehicleNode
     :param parent: Father node in this tree
     :param children: Child nodes in this tree
     :param deploy_entry: Entry from deploy file
     :param deploy_info: Values from entry (FrancaIDL | DeployConstant |
        DeployList)
     :param qualifiers: Properties as range | hasPermission
    '''

    original_node: VSSNode
    parent: Optional['VehicleNode']
    children: Iterable[Optional['VehicleNode']]
    deploy_entry: Optional[VehicleDeployEntry]
    deploy_info = Optional[DeployType]
    # TODO: Change directives to qualifiers
    qualifiers: Optional[Directives]

    def __init__(
        self,
        original_node,
        parent: 'VehicleNode' = None,
        children: Iterable['VehicleNode'] = None,
        deploy_entry=None,
    ):
        if children is None:
            children = []
        super(VehicleNode, self).__init__(
            name=original_node.name, parent=parent, children=children
        )
        self.original_node = original_node
        self.qualifiers = Directives(original_node)

        self.deploy_entry = deploy_entry
        self.deploy_info = None
        if self.deploy_entry:
            self.deploy_info = deploy_from_entry(deploy_entry)

    @staticmethod
    def supports_parameter() -> bool:
        return False

    @property
    def cardinality(self) -> Optional[Cardinality]:
        return self.deploy_entry.cardinality if self.deploy_entry else None

    @property
    def deprecation(self) -> Optional[str]:
        return self.original_node.deprecation or None

    @property
    def description(self) -> Optional[str]:
        if getattr(self.original_node, 'unit', None) is not None:
            return f'{self.original_node}\n' \
                   f'@Unit: {self.original_node.unit.value}'
        return self.original_node.description or None

    @property
    def vss_node_type(self):
        return self.original_node.type

    @property
    def vss_node_data_type(self):
        return self.original_node.data_type

    @property
    def has_write_method(self) -> bool:
        # TODO: Check if DeployList?
        if isinstance(self.deploy_info, DeployWithMethod):
            return self.deploy_info.has_write_method
        return False

    def qualified_name(self, separator=DEFAULT_SEPARATOR) -> str:
        return self.original_node.qualified_name(separator=separator)
