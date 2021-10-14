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

from typing import Literal, Optional

from .deploy_type import DeployType
from ...json_types import JSONValue


class DeployParentAttribute(DeployType):
    __slots__ = ('attribute',)
    kind: Literal['parent_attribute'] = 'parent_attribute'
    attribute: Optional[str]

    def get_include_path(self) -> str:
        return ''

    def __init__(self, spec: JSONValue, name: str) -> None:
        super().__init__(name)
        if spec is not None and not isinstance(spec, str):
            raise ValueError('ParentAttribute expects a str or None')
        self.attribute = spec

    def __str__(self) -> str:
        attrs = ', '.join(f'{k}={getattr(self, k)}' for k in self.__slots__)
        return f'{self.kind}({attrs})'
