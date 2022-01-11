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

from typing import Callable, Mapping

from .deploy_constant import DeployConstant
from .deploy_dispatcher import DeployDispatcher
from .deploy_parent_attribute import DeployParentAttribute
from .deploy_type import DeployType
from ...franca_idl.deploy_franca_idl import DeployFrancaIDL
from .deploy_custom import DeployCustom
from ...json_types import JSONValue


deploy_map_factory: Mapping[str, Callable[[JSONValue, str], DeployType]] = {
    '_constants': DeployConstant,
    '_defaultValue': DeployConstant,
    '_dispatcher': DeployDispatcher,
    '_francaIDL': DeployFrancaIDL,
    '_parentAttribute': DeployParentAttribute,
    '_custom': DeployCustom,
}

deploy_yaml_keys = {
    'methods': 'methods',
    'proxy': '_francaIDL',
    'constants': '_constants',
    'parent_attribute': '_parentAttribute',
    'dispatcher': '_dispatcher',
    'custom': '_custom',
}
