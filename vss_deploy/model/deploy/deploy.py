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

import os
import re
from typing import (Dict, List, Mapping, Optional, TextIO, Union)

from graphql import GraphQLInputObjectType, GraphQLObjectType, GraphQLSchema

import yaml

import yamlinclude

from .deploy_entry import VehicleDeployEntry
from .deploy_map import VehicleDeployMap
from .types.deploy_factory import deploy_map_factory
from .types.deploy_list import DeployList
from .types.deploy_type import DeployType
from ..permissions_registry import PermissionsRegistry


READER_TABLE = [
    (re.compile(r'^.+\.depl$', re.IGNORECASE), yamlinclude.YamlReader),
]
GRAPHQL_TYPES_WITH_PERMISSION = (GraphQLObjectType, GraphQLInputObjectType)


def deploy_from_entry(
    entry: Optional[Union[List[VehicleDeployEntry], VehicleDeployEntry]]
) -> Optional[DeployType]:
    if not entry:
        return None

    if isinstance(entry, list):
        entries: List[DeployType] = []
        for e in entry:
            d = deploy_from_entry(e)
            if d:
                entries.append(d)
        if not entries:
            return None
        return DeployList(entries, entries[0].name)

    config = entry.config
    if not config:
        return None

    for key, factory in deploy_map_factory.items():
        try:
            value = config[key]
            return factory(value, entry.name)
        except KeyError:
            pass

    return None


def load_depl(root_file: TextIO, base_dir: str) -> dict:
    '''
    Parsers deploy yaml files.

    Parameters
    ----------
    root_file : TextIOWrapper
        Deploy root file.
        It should contain the other files and fields to be included with
        the sintax !include: other.depl file. The other files may be fields
        or include other depl files.

    base_dir : str
        Directory that contains the root depl file

    Returns
    -------
    depl_data : dict
        Nested dictionary with the data of the parsed deploy files.
    '''

    yamlinclude.YamlIncludeConstructor.add_to_loader_class(
        loader_class=yaml.FullLoader,
        base_dir=base_dir,
        reader_map=READER_TABLE
    )
    return yaml.load(root_file, Loader=yaml.FullLoader)


def get_depl_map(root_file: TextIO) -> VehicleDeployMap:
    base_dir = os.path.dirname(root_file.name)
    deploy_data = load_depl(root_file, base_dir)
    return VehicleDeployMap(deploy_data)


def get_depl_types_map(root_file: TextIO) -> Dict[str, DeployType]:
    deploy_types_map: Dict[str, DeployType] = {}
    vss_deploy_map = get_depl_map(root_file)
    for name, e in vss_deploy_map:
        deploy = deploy_from_entry(e)
        if deploy:
            deploy_types_map[name] = deploy
    return deploy_types_map


def get_permissions_registry(filename: str) -> Mapping[str, int]:
    return PermissionsRegistry.create(filename).registry


def update_permissions(
        permissions: PermissionsRegistry, schema: GraphQLSchema
) -> None:
    for gql_type in schema.type_map.values():
        if isinstance(gql_type, GRAPHQL_TYPES_WITH_PERMISSION):
            for field in gql_type.fields.values():
                ast_node = getattr(field, 'ast_node', None)
                if not ast_node:
                    continue
                directives = getattr(ast_node, 'directives', None)
                if not directives:
                    continue

                for directive in field.ast_node.directives:
                    if directive.name.value == 'hasPermissions':
                        gql_perms = directive.arguments[0].value.values
                        for permission in gql_perms:
                            permissions.register(permission.value)
