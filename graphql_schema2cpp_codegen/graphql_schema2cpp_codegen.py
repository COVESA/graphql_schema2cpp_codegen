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

import argparse

from graphql import Source, build_schema

from vss_deploy.model.deploy import (
    get_depl_types_map, update_permissions
)
from vss_deploy.model.permissions_registry import PermissionsRegistry

from .generators import usable_generators
from .types import VSSGraphQLSchema


def get_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Generate resolvers')

    parser.add_argument(
        '--graphql',
        help='GraphQL Schema File',
        metavar='filename.graphql',
        type=argparse.FileType('r'),
        required=True,
    )

    parser.add_argument(
        '--layer',
        help='The deployment file to filter the vspec attributes',
        metavar='filename.depl',
        type=argparse.FileType('r'),
        required=True,
    )

    parser.add_argument(
        '--perms',
        help='The permissions registry YAML database to use',
        metavar='permissions.yaml',
        type=str,
        required=True,
    )

    subparsers = parser.add_subparsers(dest='generator', required=True)
    for entry in usable_generators:
        entry(subparsers)

    return parser


def main():
    parser = get_argparse()
    args = parser.parse_args()

    layer_map = get_depl_types_map(args.layer)

    schema = build_schema(Source(
        args.graphql.read(),
        args.graphql.name,
    ))

    permissions_registry = PermissionsRegistry.create(args.perms)
    update_permissions(permissions_registry, schema)
    if permissions_registry.changed:
        print('Permissions updated')  # noqa: T001
        permissions_registry.save(args.perms)

    vss_graphql = VSSGraphQLSchema(
        schema, layer_map, permissions_registry.registry
    )

    args.generator(args, vss_graphql)


if __name__ == '__main__':
    main()
