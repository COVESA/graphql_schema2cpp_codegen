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

from typing import (
    TextIO,
)

from .common import generate_section_common
from .object import generate_section_object
from .permissions import generate_permissions_symbols
from ..context_managers import (
    HeaderFile,
    PermissionsSymbolsFile,
    SourceFile,
)
from ..types import GenerationParameters
from ....types import (
    VSSGraphQLIterationValue,
)


common_generator_kinds = ('scalar', 'enum', 'input')


def generate_section(
    params: GenerationParameters,
    source: TextIO,
    header: TextIO,
    section: VSSGraphQLIterationValue,
) -> None:
    if section[0] in common_generator_kinds:
        generate_section_common(params, source, header, section)
    elif section[0] == 'object':
        generate_section_object(params, source, header, section[1])


def generate(
    params: GenerationParameters,
    main_source: TextIO,
    main_header: TextIO,
    permissions_symbols: TextIO,
) -> None:
    with HeaderFile(main_header, params) as header:
        with SourceFile(main_source, params) as source:
            for section in params.vss_graphql:
                generate_section(params, source, header, section)

    with PermissionsSymbolsFile(permissions_symbols, params) as perms:
        generate_permissions_symbols(params, perms)
