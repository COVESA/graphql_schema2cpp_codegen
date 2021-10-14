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
    Iterable,
    NamedTuple,
    Set,
)

from vss_deploy.model.deploy.types.deploy_collection import DeployCollection
from vss_deploy.model.deploy.types.deploy_type import DeployType

from ....types import (
    VSSGraphQLObject,
)


class Implementation(NamedTuple):
    path: str

    def __repr__(self) -> str:
        return self.path


class CollectImplementation:
    result: Set[Implementation]

    def __init__(self, entries: Iterable[VSSGraphQLObject]) -> None:
        self.result = set()
        self._collect(entries)

    def _add(
        self,
        implementation: Implementation
    ) -> None:
        self.result.add(implementation)

    def _collect_list(
        self,
        entries: Iterable[DeployType]
    ) -> None:
        for e in entries:
            if path := e.get_include_path():
                imp = Implementation(path)
                self._add(imp)

    def _collect(self, entries: Iterable[VSSGraphQLObject]) -> None:
        for entry in entries:
            for field in entry.fields.values():
                if deploy := field.deploy:
                    if path := deploy.get_include_path():
                        imp = Implementation(path)
                        self._add(imp)
                    if isinstance(deploy, DeployCollection):
                        self._collect_list(deploy.get_entries())

                elif entry.is_list_item or field.is_list:
                    include_name = '/'.join(str(entry.name).lower().split('_'))
                    imp = Implementation(f'list/{include_name}')
                    self._add(imp)
