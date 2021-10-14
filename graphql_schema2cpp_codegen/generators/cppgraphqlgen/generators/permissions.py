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

from typing import Any, Dict, NamedTuple, TextIO

from ..templates import Templates
from ..types import GenerationParameters


class PermissionsSymbolsEntry(NamedTuple):
    permission: str
    id: int  # noqa: A003


def generate_permissions_symbols(
    params: GenerationParameters,
    output: TextIO,
) -> None:
    variables: Dict[str, Any] = {'generator_params': params}
    template = Templates.permissions_symbols_entry
    for key, value in params.vss_graphql.permissions_registry.items():
        variables['entry'] = PermissionsSymbolsEntry(key, value)
        template.stream(variables).dump(output)

    Templates.permissions_symbols_known_symbols.stream(
        gengenerator_params=params,
        permissions_registry=params.vss_graphql.permissions_registry,
    ).dump(output)
