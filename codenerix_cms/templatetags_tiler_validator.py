# -*- coding: utf-8 -*-
#
# django-codenerix-cms
#
# Copyright 2017 Centrologic Computational Logistic Center S.L.
#
# Project URL : http://www.codenerix.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

from codenerix_cms.models import VALID_TYPE_TEMPLATE


def cdnx_tiler_type(context, json_tiler_type):
    response = {'code_error': 0}
    # Si existe
    # entry_dict=json.loads(args[0])
    # if exist 2 arguments, first argument is name and second it's tag

    try:
        tiler_type = json.loads(json_tiler_type)
        valid_types = True

        # Itero por los campos. Si encuentro algun campo que no tiene un tipo correcto, almaceno el error. (Solo te va a avisar una vez por error.)
        for tag in tiler_type:
            if valid_types and tiler_type[tag] not in VALID_TYPE_TEMPLATE:
                valid_types = False
                response['code_error'] = 4
                response['error_msg'] = _("Type %(tag)s  does not a allowed type. List of allowed are: %(valid)s") % {'tag': tiler_type[tag], 'valid': VALID_TYPE_TEMPLATE}
        # Actualizo el diccionario de tipos.
        if valid_types:
            if 'cdnx_tiler_types' in context:
                context['cdnx_tiler_types'].update(tiler_type)
            else:
                context['cdnx_tiler_types'] = tiler_type

            response['data'] = context['cdnx_tiler_types']
    except ValueError as e:
        response['code_error'] = 1
        response['error_msg'] = _(
            "cdnx_tiler_type has wrong format: %(error)s"
        ) % {'error': e}

    # En desarrollo
    return mark_safe(json.dumps(response))


def cdnx_tiler(context, fieldkey):
    response = {'code_error': 0}
    # Compruebo que existe un contexto previo para consultar
    if 'cdnx_tiler_types' in context:
        kinds = context['cdnx_tiler_types']
        # Si el campo está declarado, lo introduzco en el response
        if fieldkey in kinds.keys():
            response['data'] = {fieldkey: kinds[fieldkey]}
        # Si el campo no está registrado en el contexto, aviso al usuario de cuales son los campos validos.
        else:
            response['code_error'] = 2
            response['error_msg'] = _("Field %(field)s has not been declared, I can see only: %(fields)s") % {'field': fieldkey, 'fields': ", ".join(kinds.keys())}

    else:
        response['code_error'] = 3
        response['error_msg'] = _("Any type has been declared.")

    return mark_safe(json.dumps(response))
