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
from typing import (
    Any,
    ClassVar,
    MutableMapping,
    Optional,
    TextIO,
)

from jinja2 import Template

from .templates import Templates
from .types import GenerationParameters


class BaseTemplateContext:
    __slots__ = ('file', 'params', 'variables')
    file: TextIO
    params: MutableMapping[str, Any]
    open_template: ClassVar[Optional[Template]] = None
    close_template: ClassVar[Optional[Template]] = None

    def __init__(self, file: TextIO, params: GenerationParameters) -> None:
        self.file = file
        self.variables = {'generator_params': params}

    def __enter__(self) -> TextIO:
        if self.open_template:
            self.open_template.stream(self.variables).dump(self.file)
        return self.file

    def __exit__(
        self,
        exc_type: Any,
        exc_value: Optional[Exception],
        exc_traceback: Any,
    ) -> None:
        if exc_value:
            try:
                os.remove(self.file.name)
            except OSError:
                pass
        elif self.close_template:
            self.close_template.stream(self.variables).dump(self.file)


class HeaderFile(BaseTemplateContext):
    open_template = Templates.header_open
    close_template = Templates.header_close


class SourceFile(BaseTemplateContext):
    open_template = Templates.source_open
    close_template = Templates.source_close


class PermissionsSymbolsFile(BaseTemplateContext):
    open_template = Templates.permissions_symbols_open
    close_template = Templates.permissions_symbols_close
