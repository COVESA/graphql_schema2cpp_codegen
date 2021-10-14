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

from typing import List, Literal

from .deploy_collection import DeployCollection
from .deploy_type import DeployType


class DeployList(DeployType, DeployCollection):
    __slot__ = ('entries',)
    kind: Literal['list'] = 'list'
    entries: List['DeployType']

    def __init__(self, entries: List['DeployType'], name: str) -> None:
        super().__init__(name)
        self.entries = entries

    def get_include_path(self) -> str:
        return ''

    def get_entries(self) -> List['DeployType']:
        return self.entries

    @property
    def entry_kind(self) -> str:
        return self.entries[0].kind

    def __str__(self) -> str:
        attrs = ', '.join(str(e) for e in self.entries)
        return f'{self.kind}({attrs})'
