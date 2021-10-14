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

from typing import Optional

from ..json_types import JSONObject


class DeployFrancaIDLMethodSubscribe:
    __slots__ = (
        'source_broadcast', 'source_attribute',
        'implementation_function', 'implementation_getter',
    )
    source_broadcast: Optional[str]
    source_attribute: Optional[str]
    implementation_function: Optional[str]
    implementation_getter: Optional[str]

    def __init__(self, spec: JSONObject) -> None:
        if not isinstance(spec, dict):
            raise ValueError('FrancaIDL expects a JSON object')

        source = spec.get('source', {})
        if isinstance(source, dict):
            self.source_broadcast = spec.get('source', {}).get('broadcast')
            self.source_attribute = spec.get('source', {}).get('attribute')

        self.implementation_function = spec.get('conversionFunction')
        self.implementation_getter = spec.get('conversionGetter')

    def __str__(self) -> str:
        attribute = self.attribute or '?'
        if self.implementation_function:
            return f'{self.implementation_function}({attribute})'
        if self.implementation_getter:
            return f'{attribute}.{self.implementation_getter}()'
        return attribute

    @property
    def attribute(self) -> Optional[str]:
        if self.source_attribute:
            return self.source_attribute
        if self.source_broadcast:
            return self.source_broadcast
        return None

    @property
    def is_event(self) -> bool:
        if self.source_broadcast:
            return True
        return False

    @classmethod
    def from_spec(
        cls,
        spec: JSONObject,
    ) -> Optional['DeployFrancaIDLMethodSubscribe']:
        method = spec.get('subscribe')
        if not method:
            return None
        if not isinstance(method, dict):
            raise ValueError(
                'FrancaIDL.methods.subscribe expects a JSON object'
            )
        return cls(method)
