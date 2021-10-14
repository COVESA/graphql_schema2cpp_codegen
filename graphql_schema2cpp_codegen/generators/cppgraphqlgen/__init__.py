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
import os.path

from .generators import generate
from .types import GenerationParameters
from ...types import VSSGraphQLSchema


def handle_command(
    args: argparse.Namespace,
    vss_graphql: VSSGraphQLSchema,
) -> None:
    params = GenerationParameters(
        vss_graphql=vss_graphql,
        graphql_namespace=args.graphql_namespace,
        permissions_symbols_file=os.path.basename(
            args.permissions_symbols.name),
        header_open=args.header_open.read() if args.header_open else '',
        header_close=args.header_close.read() if args.header_close else '',
        source_open=args.source_open.read() if args.source_open else '',
        source_close=args.source_close.read() if args.source_close else '',
        visibility_attribute=args.visibility_attribute,
    )
    generate(
        params,
        args.main_source,
        args.main_header,
        args.permissions_symbols,
    )


def add_arguments(subparsers: argparse._SubParsersAction) -> None:
    sp = subparsers.add_parser(
        'cppgraphqlgen',
        help='Generate resolvers for github.com/microsoft/cppgraphqlgen',
    )

    sp.add_argument(
        '--header_open',
        metavar='file.hpp',
        help='File contents to be included on each header (.hpp) file'
             ' before any content.',
        type=argparse.FileType('r'),
    )
    sp.add_argument(
        '--header_close',
        metavar='file.hpp',
        help='File contents to be included on each header (.hpp) file'
             ' after any content.',
        type=argparse.FileType('r'),
    )

    sp.add_argument(
        '--source_open',
        metavar='file.cpp',
        help='File contents to be included on each source (.cpp) file'
             ' before any content.',
        type=argparse.FileType('r'),
    )
    sp.add_argument(
        '--source_close',
        metavar='file.cpp',
        help='File contents to be included on each source (.cpp) file'
             ' after any content.',
        type=argparse.FileType('r'),
    )

    sp.add_argument(
        '--graphql_namespace',
        help='C++ namespace inside "graphql::"',
        type=str,
        default='vehicle',
    )

    sp.add_argument(
        '--visibility_attribute',
        help='Used to export symbols in dynamic libraries',
        type=str,
    )

    # TODO: --separate

    sp.add_argument(
        'main_source',
        help='Main C++ source (.cpp) file to generate',
        type=argparse.FileType('w'),
    )

    sp.add_argument(
        'main_header',
        help='Main C++ header (.hpp) file to generate',
        type=argparse.FileType('w'),
    )

    sp.add_argument(
        'permissions_symbols',
        help='Generate C++ permissions symbols and knownPermissions getter',
        type=argparse.FileType('w'),
    )

    sp.set_defaults(generator=handle_command)
