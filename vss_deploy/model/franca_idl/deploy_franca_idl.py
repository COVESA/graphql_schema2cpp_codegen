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

from .deploy_franca_idl_version import DeployFrancaIDLVersion
from ..deploy.deploy_methods import DeployMethods
from ..deploy.types.deploy_type import DeployType
from ..deploy.types.deploy_with_method import DeployWithMethod
from ..json_types import JSONValue


class DeployFrancaIDL(DeployType, DeployWithMethod):
    __slots__ = (
        'package', 'interface', 'instance_id', 'version', 'methods',
    )
    kind: Literal['franca_idl'] = 'franca_idl'
    package: str
    interface: str
    instance_id: str
    version: DeployFrancaIDLVersion

    def __init__(self, spec: JSONValue, name: str) -> None:
        if not isinstance(spec, dict):
            raise TypeError(
                f'JSONValue is not a dict: {spec}.\n'
                'Is some layer (deploy) missing entries?'
            )
        super().__init__(name=name, methods=DeployMethods(spec['methods']))
        if not isinstance(spec, dict):
            raise ValueError('FrancaIDL expects a JSON object')
        self.package = spec['package']
        self.interface = spec['interface']
        self.instance_id = str(spec['instanceId'])
        self.version = DeployFrancaIDLVersion(spec['version'])

    def __str__(self) -> str:
        attrs = ', '.join(f'{k}={getattr(self, k)}' for k in self.__slots__)
        return f'{self.kind}({attrs})'
