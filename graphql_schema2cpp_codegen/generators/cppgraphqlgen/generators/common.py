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
    Any,
    Dict,
    Generic,
    Iterable,
    Mapping,
    TextIO,
    TypeVar,
)

import jinja2

from ..templates import Templates
from ..types import GenerationParameters
from ....types import VSSGraphQLIterationValue


TEntry = TypeVar('TEntry')


class CommonGeneratorSingle(Generic[TEntry]):
    params: GenerationParameters
    output: TextIO
    name: str
    entries: Iterable[TEntry]
    close_template: jinja2.Template
    entry_template: jinja2.Template
    open_template: jinja2.Template

    def __init__(
        self,
        params: GenerationParameters,
        output: TextIO,
        name: str,
        entries: Iterable[TEntry],
    ) -> None:
        self.params = params
        self.output = output
        self.name = name
        self.entries = entries
        self.close_template = getattr(Templates, f'{name}_close')
        self.entry_template = getattr(Templates, f'{name}_entry')
        self.open_template = getattr(Templates, f'{name}_open')

    def emit_open(self, extra_vars: Mapping[str, Any] = {}) -> None:
        variables = {'generator_params': self.params}
        if extra_vars:
            variables.update(extra_vars)
        self.open_template.stream(variables).dump(self.output)

    def emit_close(self, extra_vars: Mapping[str, Any] = {}) -> None:
        variables = {'generator_params': self.params}
        if extra_vars:
            variables.update(extra_vars)
        self.close_template.stream(variables).dump(self.output)

    def emit_entry(
        self,
        entry: TEntry,
        extra_vars: Mapping[str, Any] = {},
    ) -> None:
        variables = {'generator_params': self.params, 'entry': entry}
        if extra_vars:
            variables.update(extra_vars)
        self.entry_template.stream(variables).dump(self.output)

    def emit_all_entries(self, extra_vars: Mapping[str, Any] = {}) -> None:
        for entry in self.entries:
            self.emit_entry(entry, extra_vars)

    def emit_all(self, extra_vars: Mapping[str, Any] = {}) -> None:
        self.emit_open(extra_vars)
        self.emit_all_entries(extra_vars)
        self.emit_close(extra_vars)


class CommonGeneratorUmbrella(Generic[TEntry]):
    params: GenerationParameters
    name: str
    entries: Iterable[TEntry]
    generators: Mapping[str, CommonGeneratorSingle[TEntry]]

    def __init__(
        self,
        params: GenerationParameters,
        name: str,
        entries: Iterable[TEntry],
        sub_names: Mapping[str, TextIO],
    ) -> None:
        self.params = params
        self.name = name
        self.entries = tuple(entries)  # we'll iterate multiple times
        generators: Dict[str, CommonGeneratorSingle[TEntry]] = {}
        for k, io in sub_names.items():
            generators[k] = CommonGeneratorSingle(
                self.params,
                io,
                f'{name}_{k}',
                self.entries,
            )
        self.generators = generators

    def emit_open(self, extra_vars: Mapping[str, Any] = {}) -> None:
        for gen in self.generators.values():
            gen.emit_open(extra_vars)

    def emit_close(self, extra_vars: Mapping[str, Any] = {}) -> None:
        for gen in self.generators.values():
            gen.emit_close(extra_vars)

    def emit_entry(
        self,
        entry: TEntry,
        extra_vars: Mapping[str, Any] = {},
    ) -> None:
        for gen in self.generators.values():
            gen.emit_entry(entry, extra_vars)

    def emit_all_entries(self, extra_vars: Mapping[str, Any] = {}) -> None:
        for entry in self.entries:
            self.emit_entry(entry, extra_vars)

    def emit_all(self, extra_vars: Mapping[str, Any] = {}) -> None:
        self.emit_open(extra_vars)
        self.emit_all_entries(extra_vars)
        self.emit_close(extra_vars)


def generate_section_common(
    params: GenerationParameters,
    source: TextIO,
    header: TextIO,
    section: VSSGraphQLIterationValue,
) -> None:
    CommonGeneratorUmbrella(
        params,
        section[0],
        section[1],
        {'source': source, 'header': header}
    ).emit_all()
