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


from typing import ClassVar, List, Optional

from graphql import ArgumentNode, DirectiveNode, NameNode
from graphql.pyutils import FrozenList

from vspec import VSSNode

from .permissions_registry import PermissionsRegistry

IGNORED_NODE_VALUES = (None, '')


class Directives:
    '''
    Directives

    Class that creates and holds custom GraphQL directives.

    Parameters:
    -----------
        node : VSSNode
            Object inherited from anytree Node containing the vss data.

    Methods:
    --------
        get_directives()
            Returns a list of the custom directives of the node.

        get_range_directive(node: VSSNode) -> DirectiveNode
            Returns range directive node.

        get_hasPermission_directive(node: VSSNode) -> DirectiveNode
            Retuns hasPermission directive node.
    '''
    range_fields = ('min', 'max')
    range_directive: Optional[DirectiveNode]
    has_permission_directive: Optional[DirectiveNode]
    permissions_registry: ClassVar[PermissionsRegistry] = PermissionsRegistry(
        None)

    def __init__(self, node: VSSNode):
        if not node.is_leaf:
            self.range_directive = None
            self.has_permission_directive = None
        else:
            self.range_directive = self.get_range_directive(node)
            self.has_permission_directive = self.get_has_permission_directive(
                node)

    def get_directives(self) -> List[DirectiveNode]:
        return FrozenList(filter(None, [
            self.range_directive,
            self.has_permission_directive
        ])
        )

    @staticmethod
    def get_range_directive(node: VSSNode) -> Optional[DirectiveNode]:

        arguments = [
            ArgumentNode(name=NameNode(value=n),
                         value=getattr(node, n))
            for n in Directives.range_fields if
            getattr(node, n) not in IGNORED_NODE_VALUES
        ]
        return DirectiveNode(
            name=NameNode(value='range'), arguments=FrozenList(arguments)
        ) if arguments else None

    @classmethod
    def get_has_permission_directive(
            cls,
            node: VSSNode,
            operation: str = 'READ',
    ) -> Optional[DirectiveNode]:
        permission = f'{node.qualified_name(".")}_{operation}'
        Directives.permissions_registry.register(permission)
        arguments = [ArgumentNode(
            name=NameNode(value='permissions'),
            value=[permission]
        )]
        return DirectiveNode(
            name=NameNode(value='hasPermissions'),
            arguments=FrozenList(arguments))

    def __str__(self):
        directives_list = self.get_directives()
        directives = []
        for directive in directives_list:
            arguments = [
                f'{arg.name.value}: {arg.value}' for arg in directive.arguments
            ]
            directives.append(
                f' @{directive.name.value}({", ".join(arguments)})'
            )
        return ''.join(directives)
