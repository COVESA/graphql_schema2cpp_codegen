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

from vss_deploy.model.deploy.types.deploy_dispatcher import DeployDispatcher
from vss_deploy.model.deploy.types.deploy_type import DeployType

from ...types import (
    VSSGraphQLEnum,
    VSSGraphQLList,
    VSSGraphQLNonNull,
    VSSGraphQLObject,
    VSSGraphQLScalar,
    VSSGraphQLWrapableTypes,
    get_unwrapped_type,
)


def test_vss_enum_type(
    t: VSSGraphQLWrapableTypes,
    unwrap: bool = True,
) -> bool:
    unwrapped_type = get_unwrapped_type(t) if unwrap else t
    return isinstance(unwrapped_type, VSSGraphQLEnum)


def test_vss_list_type(t: VSSGraphQLWrapableTypes) -> bool:
    return isinstance(t, VSSGraphQLList)


def test_deploy_dispatcher_type(t: Optional[DeployType]) -> bool:
    return isinstance(t, DeployDispatcher)


def test_vss_object_type(
    t: VSSGraphQLWrapableTypes,
    unwrap: bool = True,
) -> bool:
    unwrapped_type = get_unwrapped_type(t) if unwrap else t
    return isinstance(unwrapped_type, VSSGraphQLObject)


def test_vss_optional_type(t: VSSGraphQLWrapableTypes) -> bool:
    return not isinstance(t, VSSGraphQLNonNull)


def test_vss_scalar_type(
    t: VSSGraphQLWrapableTypes,
    unwrap: bool = True,
) -> bool:
    unwrapped_type = get_unwrapped_type(t) if unwrap else t
    return isinstance(unwrapped_type, VSSGraphQLScalar)


all_tests = {
    'vss_enum_type': test_vss_enum_type,
    'vss_list_type': test_vss_list_type,
    'vss_object_type': test_vss_object_type,
    'vss_optional_type': test_vss_optional_type,
    'vss_scalar_type': test_vss_scalar_type,
    'deploy_dispatcher_type': test_deploy_dispatcher_type,
}
