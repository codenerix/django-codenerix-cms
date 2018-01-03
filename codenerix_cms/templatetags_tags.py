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

from django.db.models import F
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

from codenerix_cms.models import Slider, Staticheader


def cdnx_slider(identifier, lang, template='codenerix_cms/slider.html', *args, **kwargs):
    slider = None
    slider_list = None
    try:
        slider = Slider.objects.get(
            identifier=identifier,
            public=True
        )
    except ObjectDoesNotExist:
        sliders = Slider.objects.filter(
            public=True,
            default=True
        )
        if sliders.count() > 0:
            slider = sliders.first()
        else:
            slider = None

    if slider is not None:
        slider_list = slider.sliderelements.filter(
            public=True
        ).values(
            'new_price',
            'old_price',
            'discount',
            'html_format',
            'show_title',
            "{}__title".format(lang),
            "{}__description".format(lang),
            "{}__button".format(lang),
            "{}__url".format(lang),
            "{}__image".format(lang),
        ).annotate(
            title=F("{}__title".format(lang)),
            description=F("{}__description".format(lang)),
            button=F("{}__button".format(lang)),
            url=F("{}__url".format(lang)),
            image=F("{}__image".format(lang)),
        ).order_by('order')

    obj = None

    try:
        obj = get_template(template)
    except TemplateDoesNotExist:
        if getattr(settings, 'DEBUG', False):
            return _('Template not found')
        else:
            obj = None

    if obj:
        if slider_list:
            context = {}
            context['slider_list'] = slider_list
            return(
                mark_safe(
                    render(
                        None, template_name=template, context=context, content_type="text/plain"
                    )._container[0].decode("utf-8").replace('\n', '').replace('\t', '')
                )
            )
        else:
            return ''
    elif getattr(settings, 'DEBUG', False):
        return _("Identifier don't found")
    else:
        return ''


_BOOTSTRAP_COLUMN_SIZES = {
    1: (12, ),
    2: (6, 6),
    3: (6, 3, 3),
    4: (3, 3, 3, 3),
}

_LEFT = 'left'
_RIGHT = 'right'

_BOOTSTRAP_COLUMN_POSITIONS = {
    1: ('', ),
    2: (_LEFT, _RIGHT),
    3: ('', '', ''),
    4: ('', '', '', ''),
}


def cdnx_staticheader(identifier, lang, template='codenerix_cms/staticheader.html', *args, **kwargs):
    staticheader = None
    staticheader_list = None
    try:
        staticheader = Staticheader.objects.get(
            identifier=identifier,
            public=True
        )
    except ObjectDoesNotExist:
        staticheaders = Staticheader.objects.filter(
            public=True,
            default=True
        )
        if staticheaders.count() > 0:
            staticheader = staticheaders.first()
        else:
            staticheader = None

    if staticheader is not None:
        staticheader_list = staticheader.staticheaderelements.filter(
            public=True
        ).values(
            'show_title',
            "{}__title".format(lang),
            "{}__description".format(lang),
            "{}__button".format(lang),
            "{}__url".format(lang),
            "{}__image".format(lang),
        ).annotate(
            title=F("{}__title".format(lang)),
            description=F("{}__description".format(lang)),
            button=F("{}__button".format(lang)),
            url=F("{}__url".format(lang)),
            image=F("{}__image".format(lang)),
        ).order_by('order')

        column_sizes = _BOOTSTRAP_COLUMN_SIZES.get(staticheader.num_elements, 1)
        column_positions = _BOOTSTRAP_COLUMN_POSITIONS.get(staticheader.num_elements, ('', '', '', ''))
        for element, column_size, column_position in zip(staticheader_list, column_sizes, column_positions):
            element['column_size'] = column_size
            element['column_position'] = column_position

    obj = None
    try:
        obj = get_template(template)
    except TemplateDoesNotExist:
        if getattr(settings, 'DEBUG', False):
            return _('Template not found')
        else:
            obj = None

    if obj:
        if staticheader_list:
            context = {}
            context['staticheader'] = {
                'column_count': staticheader.num_elements,
                'html_format': staticheader.html_format
            }

            context['staticheader_list'] = staticheader_list
            return(
                mark_safe(
                    render(
                        None, template_name=template, context=context, content_type="text/plain"
                    )._container[0].decode("utf-8").replace('\n', '').replace('\t', '')
                )
            )
        else:
            return ''
    elif getattr(settings, 'DEBUG', False):
        return _('Identifier dont found')
    else:
        return ''
