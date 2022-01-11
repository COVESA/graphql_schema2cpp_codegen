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
from .deploy_with_method import DeployWithMethod
from ..deploy_methods import DeployMethods
from ...json_types import JSONValue


class DeployCustom(DeployType, DeployWithMethod):
    '''
    Custom deploy class, that holds the data declared with "custom" entry on
    the layer/deployment file. The data at the "custom" layer entry must be
    under the keys:

      - origin: Naming the origin of the information or how it will be
        obtained, for example, "http" or "MQTT";
      - shared: boolean. If 'true', then it means that the origin or attribute
        can be shared between multiple GraphQL fields. Therefore the resolver
        will use a singleton to get the value. The singleton will be named
        'originName__attributeName'.
      - methods: indicates what can be done with the data, i.e., subscribe,
        mutate or just read. Should be specified like the franca_idl methods
        keys and values.

    If "shared" is "false", it will just call a function in the implementation
    library.
    '''

    __slots__ = (
        'origin', 'shared_origin', 'shared_attribute', 'methods',
    )
    kind: Literal['custom'] = 'custom'
    origin: str
    shared_origin: bool
    shared_attribute: bool

    def __init__(self, spec: JSONValue, name: str) -> None:
        if not isinstance(spec, dict):
            raise TypeError(
                f'JSONValue is not a dict: {spec}.\n'
                'Is some layer (deploy) missing entries?'
            )
        super().__init__(name=name, methods=DeployMethods(spec['methods']))
        if not isinstance(spec, dict):
            raise ValueError('FrancaIDL expects a JSON object')
        self.origin = spec['origin']
        self.shared_origin = bool(spec['sharedOrigin'])
        self.shared_attribute = bool(spec['sharedAttribute'])

    def __str__(self) -> str:
        attrs = ', '.join(f'{k}={getattr(self, k)}' for k in self.__slots__)
        return f'{self.kind}({attrs})'

    @property
    def uses_singleton(self) -> bool:
        return self.shared_origin

    def get_include_path(self) -> str:
        include_name = '/'.join(str(self.name).lower().split('_')[:-1])
        return f'{self.origin[0].lower()}{self.origin[1:]}/{include_name}'
