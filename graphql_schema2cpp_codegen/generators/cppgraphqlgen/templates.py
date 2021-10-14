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

from jinja2 import ChoiceLoader, Environment, FileSystemLoader, FunctionLoader

from pkg_resources import resource_stream

from .template_filters import all_filters
from .template_tests import all_tests

templates_dir = os.path.join(os.path.dirname(__file__), 'templates')


def load_template(
    name: str,
    module: str = 'graphql_schema2cpp_codegen.generators.cppgraphqlgen'
) -> str:
    with resource_stream(module, os.path.join('templates', name)) as file:
        return file.read().decode('utf-8')


loader = ChoiceLoader([
    FunctionLoader(load_template),
    FileSystemLoader(templates_dir),
])


class Templates:
    env = Environment(
        loader=loader,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    env.filters.update(all_filters)
    env.tests.update(all_tests)

    # keep sorted! -- do not break lines, it's easier to sort
    enum_header_close = env.get_template('enum_header_close.hpp.jinja')
    enum_header_entry = env.get_template('enum_header_entry.hpp.jinja')
    enum_header_open = env.get_template('enum_header_open.hpp.jinja')
    enum_source_close = env.get_template('enum_source_close.cpp.jinja')
    enum_source_entry = env.get_template('enum_source_entry.cpp.jinja')
    enum_source_open = env.get_template('enum_source_open.cpp.jinja')
    header_close = env.get_template('header_close.hpp.jinja')
    header_open = env.get_template('header_open.hpp.jinja')
    input_header_close = env.get_template('input_header_close.hpp.jinja')
    input_header_entry = env.get_template('input_header_entry.hpp.jinja')
    input_header_open = env.get_template('input_header_open.hpp.jinja')
    input_source_close = env.get_template('input_source_close.cpp.jinja')
    input_source_entry = env.get_template('input_source_entry.cpp.jinja')
    input_source_open = env.get_template('input_source_open.cpp.jinja')
    object_fwd_class_close = env.get_template('object_fwd_class_close.hpp.jinja')  # noqa: E501
    object_fwd_class_entry = env.get_template('object_fwd_class_entry.hpp.jinja')  # noqa: E501
    object_fwd_class_open = env.get_template('object_fwd_class_open.hpp.jinja')
    object_fwd_implementation_close = env.get_template('object_fwd_implementation_close.hpp.jinja')  # noqa: E501
    object_fwd_implementation_entry = env.get_template('object_fwd_implementation_entry.hpp.jinja')  # noqa: E501
    object_fwd_implementation_open = env.get_template('object_fwd_implementation_open.hpp.jinja')  # noqa: E501
    object_header_close = env.get_template('object_header_close.hpp.jinja')
    object_header_entry = env.get_template('object_header_entry.hpp.jinja')
    object_header_open = env.get_template('object_header_open.hpp.jinja')
    object_source_close = env.get_template('object_source_close.cpp.jinja')
    object_source_entry = env.get_template('object_source_entry.cpp.jinja')
    object_source_include_close = env.get_template('object_source_include_close.cpp.jinja')  # noqa: E501
    object_source_include_entry = env.get_template('object_source_include_entry.cpp.jinja')  # noqa: E501
    object_source_include_open = env.get_template('object_source_include_open.cpp.jinja')  # noqa: E501
    object_source_open = env.get_template('object_source_open.cpp.jinja')
    permissions_symbols_close = env.get_template('permissions_symbols_close.hpp.jinja')  # noqa: E501
    permissions_symbols_entry = env.get_template('permissions_symbols_entry.hpp.jinja')  # noqa: E501
    permissions_symbols_known_symbols = env.get_template('permissions_symbols_known_symbols.hpp.jinja')  # noqa: E501
    permissions_symbols_open = env.get_template('permissions_symbols_open.hpp.jinja')  # noqa: E501
    scalar_header_close = env.get_template('scalar_header_close.hpp.jinja')
    scalar_header_entry = env.get_template('scalar_header_entry.hpp.jinja')
    scalar_header_open = env.get_template('scalar_header_open.hpp.jinja')
    scalar_source_close = env.get_template('scalar_source_close.cpp.jinja')
    scalar_source_entry = env.get_template('scalar_source_entry.cpp.jinja')
    scalar_source_open = env.get_template('scalar_source_open.cpp.jinja')
    source_close = env.get_template('source_close.cpp.jinja')
    source_open = env.get_template('source_open.cpp.jinja')
