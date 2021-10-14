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

from graphql.type.definition import (
    GraphQLList,
    GraphQLNonNull,
    GraphQLScalarType,
    GraphQLType,
)
from graphql.type.scalars import (
    GraphQLBoolean,
    GraphQLFloat,
    GraphQLInt,
)


def check_list(t: GraphQLType) -> bool:
    if isinstance(t, GraphQLNonNull):
        return check_list(t.of_type)
    elif isinstance(t, GraphQLList):
        return True
    else:
        return False


int_scalar_names = {
    'Int8',
    'Int16',
    'Int32',
    'UInt8',
    'UInt16',
}

non_string_scalar_names = {
    GraphQLFloat.name,
    GraphQLInt.name,
    GraphQLBoolean.name,
    *int_scalar_names
}


def is_string_scalar(t: GraphQLScalarType) -> bool:
    return t.name not in non_string_scalar_names


def is_int_scalar(t: GraphQLScalarType) -> bool:
    return t.name in int_scalar_names
