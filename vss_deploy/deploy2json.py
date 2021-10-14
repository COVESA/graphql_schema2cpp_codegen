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


'''
Parsers deploy files
====================

    This module parsers deploy YAML files to json and to nested dictionary.
    If excecuted as script, creates a file deploy.json containing the parsed
    information.

    Usage:
        depl_parser.py ROOT_DEPL_FILE

    Arguments:
        ROOT_DEPL_FILE: root YAML deploy file that includes other deploy nodes,
        via syntax !include: other.depl.

    End-user classes and functions:
        :func: `load_depl()`: Loads the data from the deploy files and returns
            a nested dictionary containing it.
'''

import argparse
import json
import os

from .model.deploy.deploy import load_depl


def get_arg_parse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Deploy YAML parser')

    parser.add_argument(
        '--layer',
        help='deploy yaml file',
        type=argparse.FileType('r'),
    )

    return parser


def main():
    parser = get_arg_parse()
    args = parser.parse_args()
    root_layer_file = args.layer
    base_dir = os.path.dirname(root_layer_file.name)
    depl_data = load_depl(root_layer_file, base_dir)

    with open('deploy.json', 'w+') as json_file:
        json.dump(depl_data, json_file, sort_keys=True, indent=2)
        json_file.write('\n')

    root_layer_file.close()


if __name__ == '__main__':
    main()
