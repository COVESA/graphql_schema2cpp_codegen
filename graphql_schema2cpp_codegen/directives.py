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

import json
from typing import (
    List,
    Mapping,
    NamedTuple,
    Optional,
)

from graphql.execution.values import NodeWithDirective, get_directive_values
from graphql.type.directives import GraphQLDirective


class Range(NamedTuple):
    min: Optional[float]  # noqa: 003
    max: Optional[float]  # noqa: 003

    def __repr__(self) -> str:
        s = '@range('
        if self.min is not None:
            s += f'min: {self.min}'
            if self.max is not None:
                s += ', '
        if self.max is not None:
            s += f'max: {self.max}'
        return s + ')'

    @classmethod
    def from_node(
        cls,
        ast_node: Optional[NodeWithDirective],
        directives: Mapping[str, GraphQLDirective],
    ) -> Optional['Range']:
        if ast_node is not None:
            d = directives['range']
            v = get_directive_values(d, ast_node)
            if v:
                min_v = v.get('min')
                max_v = v.get('max')
                if min_v is not None or max_v is not None:
                    return cls(min_v, max_v)
        return None


class HasPermissions(List[str]):
    def __repr__(self) -> str:
        s = '@hasPermissions(permissions: ['
        s += ', '.join(json.dumps(p) for p in self)
        return s + '])'

    @classmethod
    def from_node(
        cls,
        ast_node: Optional[NodeWithDirective],
        directives: Mapping[str, GraphQLDirective],
    ) -> Optional['HasPermissions']:
        if ast_node is not None:
            d = directives['hasPermissions']
            v = get_directive_values(d, ast_node)
            if v:
                return cls(v['permissions'])
        return None
