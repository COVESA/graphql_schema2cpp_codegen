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


class DeployFrancaIDLMethodWrite:
    __slots__ = (
        'source_method', 'source_attribute', 'implementation_function',
    )
    source_method: Optional[str]
    source_attribute: Optional[str]
    implementation_function: Optional[str]

    def __init__(self, spec: JSONObject) -> None:
        if not isinstance(spec, dict):
            raise ValueError('FrancaIDL expects a JSON object')

        source = spec.get('source', {})
        if isinstance(source, dict):
            self.source_method = source.get('method')
            self.source_attribute = source.get('attribute')

        self.implementation_function = spec.get('conversionFunction')

    def __str__(self) -> str:
        attribute = self.attribute or '?'
        if self.implementation_function:
            return f'{self.implementation_function}({attribute})'
        return attribute

    @property
    def attribute(self) -> Optional[str]:
        if self.source_attribute:
            return self.source_attribute
        if self.source_method:
            return self.source_method  # is this correct?
        return None

    @classmethod
    def from_spec(
        cls,
        spec: JSONObject,
    ) -> Optional['DeployFrancaIDLMethodWrite']:
        method = spec.get('write')
        if not method:
            return None
        if not isinstance(method, dict):
            raise ValueError('FrancaIDL.methods.write expects a JSON object')
        return cls(method)
