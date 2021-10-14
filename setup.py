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

# -*- coding: utf-8 -*-

from setuptools import find_packages, setup  # type: ignore

name = 'graphql_schema2cpp_codegen'
version = 1
release = 0

setup(
    name=name,
    version=f'{version}.{release}',
    description='Generate resolver code for VSS GraphQL Schema and deploy map',
    url='https://asc-repo.bmwgroup.net/gerrit/ascgit514.genivi.graphql.schema2cpp.codegen',  # noqa: 501
    python_requires='>=3.8',
    install_requires=[
        'graphql-core',
        'pyyaml-include',
        'anytree',
        'jinja2',
    ],
    keywords='graphql cpp resolver jinja vss',
    classifiers=[
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'graphql_schema2cpp_codegen=graphql_schema2cpp_codegen.graphql_schema2cpp_codegen:main',  # noqa: E501
            'vssdeploy2json=vss_deploy.deploy2json:main',
        ],
    },
    platforms='any',
    packages=find_packages(),
    package_data={
        'graphql_schema2cpp_codegen.generators.cppgraphqlgen': [
            'templates/*.jinja'
        ]
    },
)
