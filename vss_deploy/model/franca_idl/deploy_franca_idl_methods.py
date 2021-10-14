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

from typing import Iterator, Optional, cast

from .deploy_franca_idl_method_read import DeployFrancaIDLMethodRead
from .deploy_franca_idl_method_subscribe import DeployFrancaIDLMethodSubscribe
from .deploy_franca_idl_method_write import DeployFrancaIDLMethodWrite
from .franca_types import DeployFrancaIDLMethodsIterationValue
from ..json_types import JSONValue


class DeployFrancaIDLMethods:
    __slots__ = ('subscribe', 'read', 'write')
    subscribe: Optional[DeployFrancaIDLMethodSubscribe]
    read: Optional[DeployFrancaIDLMethodRead]
    write: Optional[DeployFrancaIDLMethodWrite]

    def __init__(self, spec: JSONValue) -> None:
        if not isinstance(spec, dict):
            raise ValueError('FrancaIDL.methods expects a JSON object')
        self.subscribe = DeployFrancaIDLMethodSubscribe.from_spec(spec)
        self.read = DeployFrancaIDLMethodRead.from_spec(spec)
        self.write = DeployFrancaIDLMethodWrite.from_spec(spec)

    def __str__(self) -> str:
        itr = (f'{k}={v}' for k, v in self)
        return f'{{{", ".join(itr)}}}'

    def __iter__(self) -> Iterator[DeployFrancaIDLMethodsIterationValue]:
        for s in self.__slots__:
            v = getattr(self, s)
            if v is not None:
                yield cast(DeployFrancaIDLMethodsIterationValue, (s, v))

    @property
    def has_subscribe(self):
        return self.subscribe is not None

    @property
    def has_read(self):
        return self.read is not None

    @property
    def has_write(self):
        return self.write is not None
