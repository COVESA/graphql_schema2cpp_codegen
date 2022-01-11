# Copyright (C) 2021, Bayerische Motoren Werke Aktiengesellschaft (BMW AG),
#   Author: Alexander Domin (Alexander.Domin@bmw.de)
# Copyright (C) 2021, ProFUSION Sistemas e Soluções LTDA,
#   Author: Garbiel Fernandes (g7fernandes@profusion.mobi)
#
# SPDX-License-Identifier: MPL-2.0
#
# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was
# not distributed with this file, You can obtain one at
# http://mozilla.org/MPL/2.0/.

from typing import Optional

from ..deploy_methods import (DeployFrancaIDLMethodsFilter, DeployMethods)


read_keys: DeployFrancaIDLMethodsFilter = ['subscribe', 'read']
write_keys: DeployFrancaIDLMethodsFilter = ['write']


class DeployWithMethod:
    methods: DeployMethods

    def __init__(self, methods: DeployMethods):
        self.methods = methods

    def _get_any_method_attribute(
        self,
        attr: str,
        filter_keys: Optional[DeployFrancaIDLMethodsFilter] = None
    ) -> Optional[str]:
        for k, m in self.methods:
            if filter_keys and k not in filter_keys:
                continue
            v = getattr(m, attr, None)
            if v is not None:
                return v
        return None

    @property
    def attribute(self) -> Optional[str]:
        return self._get_any_method_attribute('attribute')

    @property
    def read_implementation_function(self) -> Optional[str]:
        return self._get_any_method_attribute(
            'implementation_function', read_keys)

    @property
    def write_implementation_function(self) -> Optional[str]:
        return self._get_any_method_attribute(
            'implementation_function', write_keys)

    @property
    def implementation_getter(self) -> Optional[str]:
        return self._get_any_method_attribute('implementation_getter')

    @property
    def has_implementation(self) -> bool:
        return bool(self.read_implementation_function
                    or self.write_implementation_function)

    @property
    def is_event(self) -> bool:
        if subscribe := self.methods.subscribe:
            return subscribe.is_event
        return False

    @property
    def is_attribute(self) -> bool:
        if read := self.methods.read:
            return read.attribute is not None
        elif write := self.methods.write:
            return write.attribute is not None
        elif subscribe := self.methods.subscribe:
            return subscribe.attribute is not None
        return False

    @property
    def has_write_method(self) -> bool:
        return self.methods.write is not None
