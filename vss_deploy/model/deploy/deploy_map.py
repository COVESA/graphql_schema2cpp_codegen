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

from typing import Any, Dict, Optional, Union

from .deploy_entry import VehicleDeployEntry
from .types.deploy_factory import deploy_yaml_keys


class VehicleDeployMap:
    '''
    Deploy data flat model.

    Iterable class that contains the data of YAML deploy files in
    VehicleDeployEntry objects.

    Parameters:
    -----------
        raw_data : dict
            Nested dictionary containing deploy data. It may be generated
            by `load_depl()`.

    Methods:
    --------
        get_entry(entry_name: str)
            Returns the content of the deploy node entry_name.
    '''
    _deploy_nodes: dict = {}

    def flat_deploy_model(  # noqa: C901
        self,
        depl_dict: dict,
        path: str,
        depl_data: Union[dict, list],
        is_list_item: bool = False
    ):

        if isinstance(depl_data, dict):
            if deploy_yaml_keys['constants'] in depl_data:
                self._handle_constant(path, depl_dict, depl_data)
            for key, value in depl_data.items():
                if key in deploy_yaml_keys.values():
                    continue

                entry_name = f'{path}_{key}' if path else key

                if is_list_item:
                    self._handle_list(entry_name, depl_dict, value)
                else:
                    depl_dict[entry_name] = VehicleDeployEntry(
                        entry_name,
                        value
                    )

                if (
                    key not in deploy_yaml_keys.values()
                    and (isinstance(value, list) or isinstance(value, dict))
                ):

                    self.flat_deploy_model(depl_dict,
                                           entry_name,
                                           value,
                                           is_list_item)

        elif isinstance(depl_data, list):
            for item in depl_data:
                for key in [k for k in item.keys()
                            if k not in deploy_yaml_keys.values()]:
                    entry_name = f'{path}_{key}'
                    if not depl_dict.get(entry_name):
                        depl_dict[f'{path}_{key}'] = []
                self.flat_deploy_model(depl_dict, path, item, True)

    def _handle_constant(self,
                         entry_name: str,
                         depl_dict: Dict,
                         deploy_data: Dict) -> None:
        depl_dict[entry_name] = VehicleDeployEntry(entry_name,
                                                   deploy_data)
        constants = deploy_data[deploy_yaml_keys['constants']]
        if isinstance(constants, dict):
            for key, value in constants[next(iter(constants))].items():
                constant_entry_name = f'{entry_name}_{key}'
                depl_dict[constant_entry_name] = VehicleDeployEntry(
                    constant_entry_name,
                    value
                )
        if isinstance(constants, list):
            for key, value in constants[0]:
                constant_entry_name = f'{entry_name}_{key}'
                depl_dict[constant_entry_name] = VehicleDeployEntry(
                    constant_entry_name,
                    value
                )

    def _handle_list(self,
                     entry_name: str,
                     depl_dict: Dict,
                     value: Any):
        if entry_name not in depl_dict:
            depl_dict[entry_name] = []
        depl_dict[entry_name].append(
            VehicleDeployEntry(
                entry_name,
                value
            )
        )

    def get(self, entry_name: str) -> Optional[VehicleDeployEntry]:
        return self._deploy_nodes.get(entry_name)

    # REMOVE ME: contains + get_entry is a bad pattern, double lookup
    def get_entry(self, entry_name: str) -> VehicleDeployEntry:
        return self._deploy_nodes[f'{entry_name}']

    def contains(self, entry_name: str) -> bool:
        return entry_name in self._deploy_nodes

    def __iter__(self):
        return iter(self._deploy_nodes.items())

    def __init__(self, raw_data: dict):
        self.flat_deploy_model(self._deploy_nodes, '', raw_data)

    def __repr__(self) -> str:
        keyList = []
        for key in self._deploy_nodes.keys():
            keyList.append(key)
        keyList.sort()
        return '\n'.join(
            [f'{repr(self._deploy_nodes[key])}' for key in keyList]
        )
