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

from typing import List, Literal

from . import deploy_factory
from .deploy_collection import DeployCollection
from .deploy_type import DeployType
from ...json_types import JSONValue


class DeployDispatcher(DeployType, DeployCollection):
    __slots__ = ('selector', 'options')
    kind: Literal['dispatcher'] = 'dispatcher'
    selector: str
    options: List['DeployType']

    def __init__(self, spec: JSONValue, name: str) -> None:
        super().__init__(name)
        if not isinstance(spec, dict):
            raise ValueError('Dispatcher expects a JSON object')
        self.selector = spec['selector']
        self.options = []
        for opt in spec['options']:
            for key, value in opt.items():
                factory = deploy_factory.deploy_map_factory[key]
                self.options.append(factory(value, self.name))
                break

    def get_entries(self) -> List['DeployType']:
        return self.options

    def __str__(self) -> str:
        attrs = ', '.join(f'{k}={getattr(self, k)}' for k in self.__slots__)
        return f'{self.kind}({attrs})'
