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

from .types.deploy_factory import deploy_yaml_keys
from ..cardinality import Cardinality
from ..json_types import JSONChildValue


class VehicleDeployEntry:
    name: str
    config: dict
    cardinality: Cardinality
    is_resolvable: bool

    def __init__(self, name: str, data: JSONChildValue):
        self.is_resolvable = (isinstance(data, dict)
                              and deploy_yaml_keys['proxy'] in data)
        self.name = name
        self.parse_deploy_config(data)

    def parse_deploy_config(self, data: JSONChildValue):
        self.config = {}
        if isinstance(data, list):
            self.cardinality = Cardinality.MANY
            # Assumes that in case the list branch node must be resolved
            # with someip, the proxy data will be the same for all items
            # therefore we take just the first.
            for subkey in data[0].keys():
                self.config[subkey] = data[0][subkey]

        elif isinstance(data, dict):
            self.cardinality = Cardinality.ONE
            if deploy_yaml_keys['constants'] in data:
                if len(data[deploy_yaml_keys['constants']]) > 1:
                    self.cardinality = Cardinality.MANY
                self.config.update(data)
            else:
                for subkey in data.keys():
                    self.config[subkey] = data[subkey]
        else:
            self.cardinality = Cardinality.ONE
            self.config['_constants'] = data

    def __repr__(self) -> str:
        return f'{self.name}: {json.dumps(self.config, indent=2)}\n'
