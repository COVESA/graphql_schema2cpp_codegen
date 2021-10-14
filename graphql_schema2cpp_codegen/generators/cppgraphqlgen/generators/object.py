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

import os.path
from typing import (
    Any,
    Iterable,
    List,
    Mapping,
    TextIO,
)

from .common import CommonGeneratorSingle, CommonGeneratorUmbrella
from ..collectors.implementation import CollectImplementation
from ..types import GenerationParameters
from ....types import (
    VSSGraphQLObject,
)


class ForwardClassDeclarationsGenerator(CommonGeneratorSingle):
    def __init__(
        self,
        params: GenerationParameters,
        output: TextIO,
        entries: Iterable[VSSGraphQLObject],
    ) -> None:
        super().__init__(params, output, 'object_fwd_class', entries)


class ForwardImplementationDeclarationsGenerator(CommonGeneratorSingle):
    def __init__(
        self,
        params: GenerationParameters,
        output: TextIO,
        entries: Iterable[VSSGraphQLObject],
    ) -> None:
        super().__init__(params, output, 'object_fwd_implementation', entries)


class DeclarationsGenerator(CommonGeneratorSingle):
    def __init__(
        self,
        params: GenerationParameters,
        output: TextIO,
        entries: Iterable[VSSGraphQLObject],
    ) -> None:
        super().__init__(params, output, 'object_declare', entries)


class SourceIncludeGenerator(CommonGeneratorSingle):
    def __init__(
        self,
        params: GenerationParameters,
        output: TextIO,
        entries: Iterable[str],
    ) -> None:
        super().__init__(params, output, 'object_source_include', entries)


class ObjectGenerator(CommonGeneratorUmbrella):
    source: TextIO
    header: TextIO

    def __init__(
        self,
        params: GenerationParameters,
        source: TextIO,
        header: TextIO,
        entries: Iterable[VSSGraphQLObject],
    ) -> None:
        super().__init__(params, 'object', entries, {
            'source': source, 'header': header,
        })
        self.source = source
        self.header = header

    def emit_open(self, extra_vars: Mapping[str, Any] = {}) -> None:
        variables = {
            **extra_vars,
            'header_file': os.path.basename(self.header.name),
        }

        ForwardImplementationDeclarationsGenerator(
            self.params,
            self.header,
            self.entries,
        ).emit_all(extra_vars)

        self.emit_source_includes(variables)

        super().emit_open(variables)
        self.emit_header_forward_declarations(variables)

    def emit_header_forward_declarations(
        self,
        extra_vars: Mapping[str, Any] = {}
    ) -> None:
        ForwardClassDeclarationsGenerator(
            self.params,
            self.header,
            self.entries,
        ).emit_all(extra_vars)

    def emit_source_includes(
        self,
        extra_vars: Mapping[str, Any] = {}
    ) -> None:
        headers = self.get_implementation_headers()
        if headers:
            SourceIncludeGenerator(
                self.params,
                self.source,
                headers,
            ).emit_all(extra_vars)

    def get_implementation_headers(self) -> List[str]:
        headers: List[str] = []

        collector = CollectImplementation(self.entries)
        for c in collector.result:
            headers.append(f'implementation/{c.path}.hpp')

        return sorted(headers)


def generate_section_object(
    params: GenerationParameters,
    source: TextIO,
    header: TextIO,
    entries: Mapping[str, VSSGraphQLObject],
) -> None:
    ObjectGenerator(
        params,
        source,
        header,
        entries.values(),
    ).emit_all()
