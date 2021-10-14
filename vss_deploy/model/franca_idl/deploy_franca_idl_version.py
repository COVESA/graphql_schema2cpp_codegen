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

from ..json_types import JSONScalarValue


class DeployFrancaIDLVersion:
    __slots__ = ('major', 'minor')
    major: int
    minor: int

    def __init__(self, spec: JSONScalarValue) -> None:
        if isinstance(spec, int):
            self.major = spec
            self.minor = 0
        elif isinstance(spec, float):
            self.major = int(spec)
            self.minor = int(spec - self.major)
        elif isinstance(spec, str):
            parts = spec.split('.')
            self.major = int(parts[0])
            self.minor = int(parts[1]) if len(parts) > 1 else 0
        else:
            raise ValueError('FrancaIDL.version expects str, int or float')

    def __str__(self) -> str:
        return f'{self.major}.{self.minor}'
