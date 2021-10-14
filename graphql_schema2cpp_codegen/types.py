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

import re
from collections import OrderedDict
from typing import (
    Any,
    ClassVar,
    Dict,
    Generic,
    Iterator,
    List,
    Literal,
    Mapping,
    MutableMapping,
    Optional,
    Tuple,
    TypeVar,
    Union,
    cast,
)

from graphql.type.definition import (
    GraphQLArgument,
    GraphQLEnumType,
    GraphQLField,
    GraphQLInputField,
    GraphQLInputObjectType,
    GraphQLInputType,
    GraphQLList,
    GraphQLNamedType,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLOutputType,
    GraphQLScalarType,
    GraphQLType,
)
from graphql.type.directives import GraphQLDirective
from graphql.type.introspection import is_introspection_type
from graphql.type.scalars import is_specified_scalar_type
from graphql.type.schema import GraphQLSchema

from vss_deploy.model.deploy.types.deploy_parent_attribute import (
    DeployParentAttribute
)
from vss_deploy.model.deploy.types.deploy_type import DeployType

from .directives import (
    HasPermissions as Permissions,
    Range,
)
from .graphql_utils import (
    check_list,
    is_int_scalar,
    is_string_scalar
)


VSSGraphQLRootTypes = Literal['mutation', 'subscription', 'query']
VSSGraphQLWrappingTypes = Union[
    'VSSGraphQLNonNull',
    'VSSGraphQLList',
]
VSSGraphQLOutputUnwrappedTypes = Union[
    'VSSGraphQLEnum',
    'VSSGraphQLObject',
    'VSSGraphQLScalar',
]
VSSGraphQLOutputTypes = Union[
    VSSGraphQLOutputUnwrappedTypes,
    VSSGraphQLWrappingTypes,
]
VSSGraphQLInputUnwrappedTypes = Union[
    'VSSGraphQLEnum',
    'VSSGraphQLInputObject',
    'VSSGraphQLScalar',
]
VSSGraphQLInputTypes = Union[
    VSSGraphQLInputUnwrappedTypes,
    VSSGraphQLWrappingTypes,
]
VSSGraphQLWrapableTypes = Union[
    VSSGraphQLOutputTypes,
    VSSGraphQLInputTypes,
]
VSSGraphQLUnwrappedTypes = Union[
    VSSGraphQLOutputUnwrappedTypes,
    VSSGraphQLInputUnwrappedTypes,
]
VSSGraphQLNamedTypeMap = Mapping[str, 'VSSGraphQLNamedTypes']


class VSSGraphQLWrappingType:
    __slots__ = ('graphql',)
    of_type: VSSGraphQLWrapableTypes

    def __init__(self, of_type: VSSGraphQLWrapableTypes) -> None:
        self.of_type = of_type


class VSSGraphQLNonNull(VSSGraphQLWrappingType):
    def __str__(self) -> str:
        return f'nonNull({self.of_type})'


class VSSGraphQLList(VSSGraphQLWrappingType):
    def __str__(self) -> str:
        return f'list({self.of_type})'


def get_wrapped_type(
    t: GraphQLType,
    named_map: VSSGraphQLNamedTypeMap,
) -> VSSGraphQLWrapableTypes:
    if isinstance(t, GraphQLNonNull):
        return VSSGraphQLNonNull(get_output_type(t.of_type, named_map))
    elif isinstance(t, GraphQLList):
        return VSSGraphQLList(get_output_type(t.of_type, named_map))
    else:
        return named_map[cast(GraphQLNamedType, t).name]


def get_unwrapped_type(
    t: VSSGraphQLWrapableTypes,
) -> VSSGraphQLUnwrappedTypes:
    while isinstance(t, (VSSGraphQLList, VSSGraphQLNonNull)):
        t = t.of_type
    return t


def get_output_type(
    t: GraphQLOutputType,
    named_map: VSSGraphQLNamedTypeMap,
) -> 'VSSGraphQLOutputTypes':
    return cast(VSSGraphQLOutputTypes, get_wrapped_type(t, named_map))


def get_input_type(
    t: GraphQLInputType,
    named_map: VSSGraphQLNamedTypeMap,
) -> 'VSSGraphQLInputTypes':
    return cast(VSSGraphQLInputTypes, get_wrapped_type(t, named_map))


def get_deploy(
    deploy_map: Dict[str, DeployType],
    name: str,
) -> Optional[DeployType]:
    return deploy_map.get(name)


def get_vss_names(graphql_name: str) -> Iterator[str]:
    """ # noqa: Q002
    Get the possible VSS names of a given graphql_name

    Aims to undo the get_graphql_name(). But as it's not a single
    option, then it yields all possible results:

    >>> list(get_vss_names('isABSOn'))
    ['IsABSOn']
    >>> list(get_vss_names('ABSOn'))
    ['ABSOn']
    >>> list(get_vss_names('ABS'))
    ['ABS']
    >>> list(get_vss_names('abs'))
    ['Abs', 'ABS', 'abs']
    """
    vss_names_re = re.compile('(^[a-z]+[A-Z]|^[a-z]+$)')
    m = vss_names_re.match(graphql_name)
    if not m:
        yield graphql_name
        return

    s = m.group(0)
    if s[-1] == s[-1].upper():
        yield graphql_name[0].upper() + graphql_name[1:]
        return

    yield graphql_name[0].upper() + graphql_name[1:]
    yield graphql_name.upper()
    # all lowercase is rare, thus keep it last
    yield graphql_name


class VSSGraphQLEnum:
    __slots__ = ('graphql', 'is_list')
    graphql: GraphQLEnumType
    is_list: bool

    def __init__(self, graphql: GraphQLEnumType) -> None:
        self.graphql = graphql
        self.is_list = False

    def __repr__(self) -> str:
        return f'enum {self.name}'

    @property
    def name(self):
        return self.graphql.name


class VSSGraphQLScalar:
    __slots__ = ('graphql', 'is_custom', 'is_string', 'is_integer', 'is_list')
    graphql: GraphQLScalarType
    is_custom: bool
    is_string: bool
    is_integer: bool
    is_list: bool

    def __init__(self, graphql: GraphQLScalarType) -> None:
        self.graphql = graphql
        self.is_custom = not is_specified_scalar_type(graphql)
        self.is_string = is_string_scalar(graphql)
        self.is_integer = is_int_scalar(graphql)
        self.is_list = False

    def __repr__(self) -> str:
        qualifier = ''
        if self.is_custom:
            qualifier += ' is_custom'
        if self.is_string:
            qualifier += ' is_string'
        return f'scalar {self.name}{qualifier}'

    @property
    def name(self):
        return self.graphql.name


TUnwrapped = TypeVar('TUnwrapped', bound=VSSGraphQLUnwrappedTypes)
TGraphQLFieldType = TypeVar('TGraphQLFieldType', bound=Union[
    GraphQLInputField,
    GraphQLField,
    GraphQLArgument,
])


class _ContainerField(Generic[TUnwrapped, TGraphQLFieldType]):
    __slots__ = (
        'name', 'graphql', 'deploy', 'type', 'unwrapped_type',
        'permissions', 'range', 'is_list',
    )
    name: str
    graphql: TGraphQLFieldType
    deploy: Optional[DeployType]
    type: Union[TUnwrapped, VSSGraphQLWrappingTypes]  # noqa: A003
    unwrapped_type: TUnwrapped
    permissions: Optional[Permissions]
    range: Optional[Range]  # noqa: A003
    is_list: bool

    def __init__(
        self,
        parent: Union['_Container[Any, Any, Any]', 'VSSGraphQLField'],
        name: str,
        graphql: TGraphQLFieldType,
        named_map: VSSGraphQLNamedTypeMap,
        directives: Mapping[str, GraphQLDirective],
        deploy_map: Dict[str, DeployType],
    ) -> None:
        self.name = name
        self.graphql = graphql
        self._setup_type(named_map)
        self.unwrapped_type = cast(TUnwrapped, get_unwrapped_type(self.type))
        self._setup_deploy(parent, deploy_map)
        self._setup_directives(directives)
        self.is_list = check_list(graphql.type)

    def _setup_type(self, named_map: VSSGraphQLNamedTypeMap) -> None:
        raise NotImplementedError

    def _setup_deploy(
        self,
        parent: Union['_Container[Any, Any, Any]', 'VSSGraphQLField'],
        deploy_map: Dict[str, DeployType],
    ) -> None:
        for vss_name in get_vss_names(self.name):
            key = f'{parent.name}_{vss_name}'
            self.deploy = get_deploy(deploy_map, key)
            if self.deploy:
                break

    def _setup_directives(
        self,
        directives: Mapping[str, GraphQLDirective],
    ) -> None:
        ast_node = self.graphql.ast_node
        self.permissions = Permissions.from_node(ast_node, directives)
        type_permissions = getattr(self.type, 'permissions', None)
        if type_permissions:
            if self.permissions:
                self.permissions += type_permissions
            else:
                self.permissions = type_permissions
        self.range = Range.from_node(ast_node, directives)

    def __repr__(self) -> str:
        qualifiers = ''
        if self.is_list:
            qualifiers += ' is_list'
        if self.permissions:
            qualifiers += f' {self.permissions}'
        if self.range:
            qualifiers += f' {self.range}'
        return f'{self.name}: {self.type}{qualifiers}'


TGraphQLContainerType = TypeVar('TGraphQLContainerType', bound=Union[
    GraphQLObjectType,
    GraphQLInputType,
])
TContainerFieldType = TypeVar(
    'TContainerFieldType',
    bound=_ContainerField[Any, Any],
)


class _Container(Generic[
    TGraphQLContainerType,
    TGraphQLFieldType,
    TContainerFieldType,
]):
    __slots__ = (
        'graphql', 'deploy', 'all_deploy', 'fields', 'permissions',
        'is_list_item', 'is_list'
    )
    graphql: TGraphQLContainerType
    deploy: Optional[DeployType]
    all_deploy: Optional[List[DeployType]]
    fields: MutableMapping[str, TContainerFieldType]
    permissions: Optional[Permissions]
    is_list_item: bool
    kind: ClassVar[Literal['type', 'input']]
    is_list: bool

    def __init__(
        self,
        graphql: TGraphQLContainerType,
        deploy: Optional[DeployType],
        directives: Mapping[str, GraphQLDirective],
    ) -> None:
        self.graphql = graphql
        self.deploy = deploy
        self.is_list_item = False
        self.is_list = False
        self.fields = OrderedDict()
        self._setup_directives(directives)

    def _setup_directives(
        self,
        directives: Mapping[str, GraphQLDirective],
    ) -> None:
        ast_node = self.graphql.ast_node
        self.permissions = Permissions.from_node(ast_node, directives)

    def _populate_fields(
        self,
        named_map: VSSGraphQLNamedTypeMap,
        directives: Mapping[str, GraphQLDirective],
        deploy_map: Dict[str, DeployType],
    ) -> None:
        child_deploy: List[DeployType] = []
        for n, f in self.graphql.fields.items():
            vss_field = self._create_field(
                n, f, named_map, directives, deploy_map)
            self.fields[n] = vss_field
            if vss_field.deploy:
                child_deploy.append(vss_field.deploy)

        self._populate_all_deploy(child_deploy)
        self._fields_populated()

    def _create_field(
        self,
        name: str,
        graphql: TGraphQLFieldType,
        named_map: VSSGraphQLNamedTypeMap,
        directives: Mapping[str, GraphQLDirective],
        deploy_map: Dict[str, DeployType],
    ) -> TContainerFieldType:
        raise NotImplementedError()

    def _populate_all_deploy(self, child_deploy: List[DeployType]) -> None:
        if self.deploy and child_deploy:
            child_deploy.insert(0, self.deploy)
            self.all_deploy = child_deploy
        elif self.deploy:
            self.all_deploy = [self.deploy]
        elif child_deploy:
            self.all_deploy = child_deploy
        else:
            self.all_deploy = None

    def _fields_populated(self) -> None:
        pass

    def __repr__(self) -> str:
        qualifier = ''
        if self.is_list_item:
            qualifier += ' is_list_item'
        if self.deploy:
            qualifier = f' (deploy: {self.deploy})'
        return f'{self.kind} {self.name}{qualifier}'

    @property
    def name(self):
        return self.graphql.name

    def mark_list_item(self) -> None:
        if self.is_list_item:
            return
        self.is_list_item = True

    def mark_as_list(self) -> None:
        self.is_list = True


class VSSGraphQLInputField(_ContainerField[
    VSSGraphQLInputUnwrappedTypes,
    GraphQLInputField,
]):
    def _setup_type(self, named_map: VSSGraphQLNamedTypeMap) -> None:
        self.type = get_input_type(self.graphql.type, named_map)

    def _setup_deploy(
        self,
        parent: Union['_Container[Any, Any, Any]', 'VSSGraphQLField'],
        deploy_map: Dict[str, DeployType],
    ) -> None:
        prefix = parent.name
        if prefix.endswith('_Input'):
            prefix = prefix[:-len('_Input')]

        for vss_name in get_vss_names(self.name):
            key = f'{prefix}_{vss_name}'
            self.deploy = get_deploy(deploy_map, key)
            if self.deploy:
                break


class VSSGraphQLInputObject(_Container[
    GraphQLInputObjectType,
    GraphQLInputField,
    VSSGraphQLInputField,
]):
    __slots__ = ('range',)
    range: Optional[Range]  # noqa: A003
    kind: ClassVar[Literal['input']] = 'input'

    def _setup_directives(
        self,
        directives: Mapping[str, GraphQLDirective],
    ) -> None:
        ast_node = self.graphql.ast_node
        self.range = Range.from_node(ast_node, directives)
        return super()._setup_directives(directives)

    def _create_field(
        self,
        name: str,
        graphql: GraphQLInputField,
        named_map: VSSGraphQLNamedTypeMap,
        directives: Mapping[str, GraphQLDirective],
        deploy_map: Dict[str, DeployType],
    ) -> VSSGraphQLInputField:
        return VSSGraphQLInputField(
            self, name, graphql, named_map, directives, deploy_map)

    def __repr__(self) -> str:
        qualifier = ''
        if self.range:
            qualifier += f' {self.range}'
        if self.deploy:
            qualifier = f' (deploy: {self.deploy})'
        return f'{self.kind} {self.name}{qualifier}'


class VSSGraphQLArgument(_ContainerField[
    VSSGraphQLInputUnwrappedTypes,
    GraphQLArgument,
]):
    def _setup_type(self, named_map: VSSGraphQLNamedTypeMap) -> None:
        self.type = get_input_type(self.graphql.type, named_map)


class VSSGraphQLField(_ContainerField[
    VSSGraphQLOutputUnwrappedTypes,
    GraphQLField,
]):
    def __init__(
        self,
        parent: '_Container[Any, Any, Any]',
        name: str,
        graphql: GraphQLField,
        named_map: VSSGraphQLNamedTypeMap,
        directives: Mapping[str, GraphQLDirective],
        deploy_map: Dict[str, DeployType],
    ) -> None:
        super().__init__(
            parent, name, graphql, named_map, directives, deploy_map)
        self._populate_args(parent, named_map, directives, deploy_map)
        if self.is_list:
            self.unwrapped_type.is_list = True
            if isinstance(self.unwrapped_type, VSSGraphQLObject):
                self.unwrapped_type.mark_list_item()

    def _setup_type(self, named_map: VSSGraphQLNamedTypeMap) -> None:
        self.type = get_output_type(self.graphql.type, named_map)

    def _populate_args(
        self,
        parent: '_Container[Any, Any, Any]',
        named_map: VSSGraphQLNamedTypeMap,
        directives: Mapping[str, GraphQLDirective],
        deploy_map: Dict[str, DeployType],
    ) -> None:
        args = OrderedDict()
        for n, a in sorted(self.graphql.args.items()):
            args[n] = VSSGraphQLArgument(
                parent, n, a, named_map, directives, deploy_map)
        self.args = args

    def __repr__(self) -> str:
        args = ''
        if self.args:
            args = '(' + ', '.join(str(a) for a in self.args.values()) + ')'

        qualifiers = ''
        if self.is_list:
            qualifiers += ' is_list'
        if self.permissions:
            qualifiers += f' {self.permissions}'
        if self.range:
            qualifiers += f' {self.range}'
        if self.deploy:
            qualifiers += f' (deploy: {self.deploy})'
        return f'{self.name}{args}: {self.type}{qualifiers}'


class VSSGraphQLObject(_Container[
    GraphQLObjectType,
    GraphQLField,
    VSSGraphQLField,
]):
    __slots__ = ('is_root', 'is_entry_point', 'local_attributes')
    is_root: Optional[VSSGraphQLRootTypes]
    is_entry_point: bool
    local_attributes: Optional[Mapping[str, VSSGraphQLWrapableTypes]]
    kind: ClassVar[Literal['type']] = 'type'

    def __init__(
        self,
        graphql: GraphQLObjectType,
        deploy: Optional[DeployType],
        directives: Mapping[str, GraphQLDirective],
        is_root: Optional[VSSGraphQLRootTypes],
    ) -> None:
        super().__init__(graphql, deploy, directives)
        self.is_root = is_root
        self.is_entry_point = False
        self.is_list_item = False
        self.local_attributes = None

    def _create_field(
        self,
        name: str,
        graphql: GraphQLField,
        named_map: VSSGraphQLNamedTypeMap,
        directives: Mapping[str, GraphQLDirective],
        deploy_map: Dict[str, DeployType],
    ) -> VSSGraphQLField:
        return VSSGraphQLField(
            self, name, graphql, named_map, directives, deploy_map)

    def _fields_populated(self) -> None:
        self._mark_children_entry_point()
        self._mark_children_list_items()
        self._populate_local_attributes()

    def _populate_local_attributes(self) -> None:
        local_attributes: Dict[str, VSSGraphQLWrapableTypes] = OrderedDict()
        for n, f in self.fields.items():
            deploy = f.deploy
            if not deploy or not isinstance(deploy, DeployParentAttribute):
                continue
            if deploy.attribute is None:
                # convenience to help YAML
                deploy.attribute = tuple(get_vss_names(n))[0]
            local_attributes[n] = f.type

        if local_attributes:
            self.local_attributes = local_attributes

    def _mark_children_entry_point(self) -> None:
        if not self.is_root or self.is_root == 'mutation':
            return
        for f in self.fields.values():
            if isinstance(f.unwrapped_type, VSSGraphQLObject):
                f.unwrapped_type.is_entry_point = True

    def _mark_children_list_items(self) -> None:
        if not self.is_list_item:
            return
        for f in self.fields.values():
            if isinstance(f.unwrapped_type, VSSGraphQLObject):
                f.unwrapped_type.mark_list_item()

    def __repr__(self) -> str:
        qualifier = ''
        if self.is_root:
            qualifier += f'  root={self.is_root}'
        if self.is_entry_point:
            qualifier += ' is_entry_point'
        if self.local_attributes:
            qualifier += ' local_attributes'
        if self.is_list_item:
            qualifier += ' is_list_item'
        if self.deploy:
            qualifier = f' (deploy: {self.deploy})'
        return f'{self.kind} {self.name}{qualifier}'

    def mark_list_item(self) -> None:
        if self.is_list_item:
            return
        self.is_list_item = True
        self._mark_children_list_items()


VSSGraphQLIterationEnums = Tuple[
    Literal['enum'], Mapping[str, VSSGraphQLEnum]
]
VSSGraphQLIterationInputObjects = Tuple[
    Literal['input'], Mapping[str, VSSGraphQLInputObject]
]
VSSGraphQLIterationObjects = Tuple[
    Literal['object'], Mapping[str, VSSGraphQLObject]
]
VSSGraphQLIterationScalars = Tuple[
    Literal['scalar'], Mapping[str, VSSGraphQLScalar]
]
VSSGraphQLIterationValue = Union[
    VSSGraphQLIterationEnums,
    VSSGraphQLIterationInputObjects,
    VSSGraphQLIterationObjects,
    VSSGraphQLIterationScalars,
]

VSSGraphQLNamedTypes = Union[
    VSSGraphQLEnum,
    VSSGraphQLInputObject,
    VSSGraphQLObject,
    VSSGraphQLScalar,
]


class VSSGraphQLSchema:
    schema: GraphQLSchema
    deploy_map: Dict[str, DeployType]
    permissions_registry: Mapping[str, int]
    root_types: Mapping[str, Optional[VSSGraphQLRootTypes]]

    enums: MutableMapping[str, VSSGraphQLEnum]
    inputs: MutableMapping[str, VSSGraphQLInputObject]
    objects: MutableMapping[str, VSSGraphQLObject]
    scalars: MutableMapping[str, VSSGraphQLScalar]

    named_types: MutableMapping[str, VSSGraphQLNamedTypes]
    directives: MutableMapping[str, GraphQLDirective]

    def __init__(
        self,
        schema: GraphQLSchema,
        deploy_map: Dict[str, DeployType],
        permissions_registry: Mapping[str, int],
    ) -> None:
        self.schema = schema
        self.deploy_map = deploy_map
        self.permissions_registry = permissions_registry
        self.enums = OrderedDict()
        self.inputs = OrderedDict()
        self.objects = OrderedDict()
        self.scalars = OrderedDict()
        self.named_types = OrderedDict()
        self.directives = {}
        self._populate_root_types()
        self._populate_graphql()

    def _populate_root_types(self) -> None:
        root_types: Dict[str, VSSGraphQLRootTypes] = {}
        if self.schema.query_type:
            root_types[self.schema.query_type.name] = 'query'
        if self.schema.mutation_type:
            root_types[self.schema.mutation_type.name] = 'mutation'
        if self.schema.subscription_type:
            root_types[self.schema.subscription_type.name] = 'subscription'
        self.root_types = root_types

    def _populate_graphql(self) -> None:
        for d in self.schema.directives:
            self.directives[d.name] = d

        for n, t in sorted(self.schema.type_map.items()):
            if is_introspection_type(t):
                continue
            if isinstance(t, GraphQLEnumType):
                self._add_enum(n, t)
            elif isinstance(t, GraphQLInputObjectType):
                self._add_input(n, t)
            elif isinstance(t, GraphQLObjectType):
                self._add_object(n, t)
            elif isinstance(t, GraphQLScalarType):
                self._add_scalar(n, t)
            else:
                # Union, Interfaces
                raise ValueError(f'Unsupported NamedType: {t}')

        self._populate_input_fields()
        self._populate_object_fields()

    def _add_enum(self, name: str, t: GraphQLEnumType) -> None:
        v = VSSGraphQLEnum(t)
        self.enums[name] = v
        self.named_types[name] = v

    def _add_input(self, name: str, t: GraphQLInputObjectType) -> None:
        deploy = get_deploy(self.deploy_map, name)
        v = VSSGraphQLInputObject(t, deploy, self.directives)
        self.inputs[name] = v
        self.named_types[name] = v

    def _add_object(self, name: str, t: GraphQLObjectType) -> None:
        deploy = get_deploy(self.deploy_map, name)
        is_root = self.root_types.get(name)
        v = VSSGraphQLObject(t, deploy, self.directives, is_root)
        self.objects[name] = v
        self.named_types[name] = v

    def _add_scalar(self, name: str, t: GraphQLScalarType) -> None:
        v = VSSGraphQLScalar(t)
        self.scalars[name] = v
        self.named_types[name] = v

    def _populate_input_fields(self) -> None:
        named_map = self.named_types
        directives = self.directives
        deploy_map = self.deploy_map
        for i in self.inputs.values():
            i._populate_fields(named_map, directives, deploy_map)

    def _populate_object_fields(self) -> None:
        named_map = self.named_types
        directives = self.directives
        deploy_map = self.deploy_map
        for o in self.objects.values():
            o._populate_fields(named_map, directives, deploy_map)

    def __iter__(self) -> Iterator[VSSGraphQLIterationValue]:
        yield cast(VSSGraphQLIterationScalars, ('scalar', self.scalars))
        yield cast(VSSGraphQLIterationEnums, ('enum', self.enums))
        yield cast(VSSGraphQLIterationInputObjects, ('input', self.inputs))
        yield cast(VSSGraphQLIterationObjects, ('object', self.objects))
