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

from typing import Literal

from .deploy_type import DeployType
from ...json_types import JSONValue


class DeployConstant(DeployType):
    __slots__ = ('constant',)
    kind: Literal['constant'] = 'constant'
    constant: JSONValue

    def __init__(self, constant: JSONValue, name: str) -> None:
        super().__init__(name)
        self.constant = constant

    def __str__(self) -> str:
        attrs = ', '.join(f'{k}={getattr(self, k)}' for k in self.__slots__)
        return f'{self.kind}({attrs})'

    @property
    def is_iterable(self) -> bool:
        return isinstance(self.constant, (list, dict))
