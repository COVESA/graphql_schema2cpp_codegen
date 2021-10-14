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

from typing import Dict, Optional

import yaml


class PermissionsRegistry:
    registry: Dict[str, int]
    next_id: int

    def __init__(self, registry: Optional[Dict[str, int]]) -> None:
        if registry is None:
            registry = {}
        self.registry = registry
        self.next_id = max(registry.values()) + 1 if registry else 0
        self.changed = False

    def register(self, permission: str) -> int:
        try:
            return self.registry[permission]
        except KeyError:
            i = self.next_id
            self.next_id += 1
            self.registry[permission] = i
            self.changed = True
            return i

    def save(self, filename: str, encoding: str = 'utf-8') -> bool:
        if not self.changed:
            return False
        with open(filename, 'w', encoding=encoding) as f:
            yaml.dump(self.registry, f, encoding=encoding)
            return True

    @classmethod
    def create(
        cls,
        filename: str,
        encoding: str = 'utf-8',
    ) -> 'PermissionsRegistry':
        try:
            with open(filename, 'r', encoding=encoding) as f:
                registry = yaml.load(f, Loader=yaml.SafeLoader)
                return cls(registry)
        except FileNotFoundError:
            return cls(None)
