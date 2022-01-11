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

from typing import Literal, Tuple, Union

from ..deploy.deploy_method_read import DeployMethodRead
from ..deploy.deploy_method_subscribe import DeployMethodSubscribe
from ..deploy.deploy_method_write import DeployMethodWrite

DeployFrancaIDLMethodsIterationValue = Union[
    Tuple[Literal['subscribe'], DeployMethodSubscribe],
    Tuple[Literal['read'], DeployMethodRead],
    Tuple[Literal['write'], DeployMethodWrite]
]
