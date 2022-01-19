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

from graphql.type.scalars import (
    GraphQLBoolean,
    GraphQLFloat,
    GraphQLID,
    GraphQLInt,
    GraphQLString,
)


from vss_deploy.model.deploy.types.deploy_custom import DeployCustom
from vss_deploy.model.franca_idl.deploy_franca_idl import DeployFrancaIDL


from ...types import (
    VSSGraphQLList,
    VSSGraphQLNonNull,
    VSSGraphQLObject,
    VSSGraphQLScalar,
    VSSGraphQLWrapableTypes,
)
from ...utils import (
    upper_first_letter,
)


def franca_idl_attribute(franca: DeployFrancaIDL) -> str:
    if not franca.attribute:
        return ''

    qualifier = ''
    if franca.is_event:
        qualifier = 'Event'
    elif franca.is_attribute:
        qualifier = 'Attribute'
    return f'{upper_first_letter(franca.attribute)}{qualifier}'


def franca_idl_proxy(franca: DeployFrancaIDL) -> str:
    return '_'.join((
        f'v{franca.version.major}',
        franca.package.replace('.', '_'),
        f'{franca.interface}Proxy',
        franca.instance_id
    ))


def custom_singleton(custom: DeployCustom) -> str:
    if custom.shared_attribute:
        return f'{custom.origin}__{custom.attribute}'
    else:
        return custom.origin


def get_optional_type(cpp_type: str, is_nullable: bool) -> str:
    if not is_nullable:
        return cpp_type
    return f'std::optional<{cpp_type}>'


# TODO: we should typedef these and avoid the need for translations
cpp_type_scalar_map = {
    GraphQLString.name: 'std::string',
    GraphQLBoolean.name: 'bool',
    GraphQLFloat.name: 'double',
    GraphQLID.name: 'response::IdType',
    GraphQLInt.name: 'int',
    'Int8': 'int8_t',
    'Int16': 'int16_t',
    'Int32': 'int32_t',
    'Int64': 'int64_t',
    'UInt8': 'uint8_t',
    'UInt16': 'uint16_t',
    'UInt32': 'uint32_t',
    'UInt64': 'uint64_t',
}


def cpp_type(
    t: VSSGraphQLWrapableTypes,
    enable_optional=True,
    base_type=False,
    wrapped_custom_scalars=True,
) -> str:
    if isinstance(t, VSSGraphQLObject):
        namespace = 'object::' if base_type else ''
        return f'std::shared_ptr<{namespace}{t.name}>'
    elif isinstance(t, VSSGraphQLNonNull):
        return cpp_type(
            t.of_type,
            False,
            base_type,
            wrapped_custom_scalars,
        )
    elif isinstance(t, VSSGraphQLList):
        item_type = cpp_type(
            t.of_type,
            True,
            base_type,
            wrapped_custom_scalars,
        )
        r = f'std::vector<{item_type}>'
    elif isinstance(t, VSSGraphQLScalar):
        if t.is_custom and wrapped_custom_scalars:
            r = 'response::Value'
        else:
            r = cpp_type_scalar_map[t.name]
    else:
        r = t.name

    if not enable_optional:
        return r
    return f'std::optional<{r}>'


def _is_blank_line(s: str) -> bool:
    return not bool(len(s.strip('\t \n')))


def indent_spaces(s: str, width: int = 1, blank: bool = False) -> str:
    spaces = '    '
    res = ''
    for r in s.split('\n'):
        if blank and _is_blank_line(r):
            continue
        res = f'{res}{spaces*width}{r}\n'
    return res[:-1]


all_filters = {
    'cpp_type': cpp_type,
    'franca_idl_attribute': franca_idl_attribute,
    'franca_idl_proxy': franca_idl_proxy,
    'indent_spaces': indent_spaces,
    'upper_first_letter': upper_first_letter,
    'custom_singleton': custom_singleton,
}
