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

from django import template
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.forms.utils import ErrorList
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _

from django.conf import settings
from codenerix.multiforms import MultiForm
from codenerix.views import GenList, GenCreate, GenCreateModal, GenUpdate, GenUpdateModal, GenDelete, GenDetail, GenForeignKey

from codenerix_cms.models import Slider, SliderElement, StaticheaderElement, Staticheader, StaticPage, StaticPageAuthor, TemplateStaticPage, MODELS
from codenerix_cms.forms import SliderForm, SliderElementForm, StaticheaderForm, StaticheaderElementForm, StaticPageForm, StaticPageAuthorForm, TemplateStaticPageForm

register = template.Library()

# ##################################
formsfull = {}
for info in MODELS:
    field = info[0]
    model = info[1]
    formsfull[model] = [(None, None, None)]
    for lang_code in settings.LANGUAGES_DATABASES:
        query = "from codenerix_cms.models import {}Text{}\n".format(model, lang_code.upper())
        query += "from codenerix_cms.forms import {}TextForm{}".format(model, lang_code.upper())
        exec(query)

        formsfull[model].append((eval("{}TextForm{}".format(model, lang_code.upper())), field, None))


# ##################################
# Slider group
class SliderList(GenList):
    model = Slider
    extra_context = {'menu': ['SliderGroup', 'slidergroup'], 'bread': [_('Slider Group'), _('slider group')]}
    # link_add = True
    # link_edit = True
    show_details = True


class SliderCreate(GenCreate):
    model = Slider
    show_details = True
    form_class = SliderForm


class SliderCreateModal(GenCreateModal, SliderCreate):
    pass


class SliderUpdate(GenUpdate):
    model = Slider
    show_details = True
    form_class = SliderForm


class SliderUpdateModal(GenUpdateModal, SliderUpdate):
    pass


class SliderDelete(GenDelete):
    model = Slider


class SliderDetail(GenDetail):
    model = Slider
    groups = SliderForm.__groups_details__()
    exclude_fields = []
    tabs = [
        {
            'id': 'sliders', 'name': _('Sliders'),
            'ws': 'CDNX_cms_slider_element_sublist',
            'rows': 'base'
        },
    ]


# ##################################
# Slider
class SliderElementSublist(GenList):
    model = SliderElement
    show_details = False

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(slider__pk=pk)
        return limit


# class SliderElementCreate(MultiForm, GenCreate, ImageFileView):
class SliderElementCreate(MultiForm, GenCreate):
    model = SliderElement
    form_class = SliderElementForm
    forms = formsfull["SliderElement"]
    form_ngcontroller = "CDNXCMSFormSliderCtrl"

    def form_valid(self, form, forms):
        new_forms = []
        for f in forms:
            if type(f[0]) != self.form_class:
                name_form = str(type(forms[1][0])).split('.')[-1].replace("'", '').replace('>', '')
                field_image = "{}_image".format(name_form)

                body = self.request.body
                if type(self.request.body) == bytes:
                    body = body.decode("utf-8")
                body = json.loads(body)

                if field_image in body and 'filename' in body[field_image]:
                    name_file = body[field_image]['filename']
                    self.request.name_file = name_file
                    f[0].instance.name_file = name_file
            new_forms.append(f)
        return super(SliderElementCreate, self).form_valid(form, new_forms)


class SliderElementCreateModal(GenCreateModal, SliderElementCreate):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__slider_pk = kwargs.get('tpk', None)
        return super(SliderElementCreateModal, self).dispatch(*args, **kwargs)

    def form_valid(self, form, forms):
        if self.__slider_pk:
            slider = Slider.objects.get(pk=self.__slider_pk)
            self.request.slider = slider
            form.instance.slider = slider

        return super(SliderElementCreateModal, self).form_valid(form, forms)


class SliderElementUpdate(MultiForm, GenUpdate):
    model = SliderElement
    form_class = SliderElementForm
    forms = formsfull["SliderElement"]
    form_ngcontroller = "CDNXCMSFormSliderCtrl"

    def form_valid(self, form, forms):
        new_forms = []
        for f in forms:
            if type(f[0]) != self.form_class:
                name_form = str(type(forms[1][0])).split('.')[-1].replace("'", '').replace('>', '')
                field_image = "{}_image".format(name_form)

                body = self.request.body
                if type(self.request.body) == bytes:
                    body = body.decode("utf-8")
                body = json.loads(body)
                
                if field_image in body and 'filename' in body[field_image]:
                    name_file = body[field_image]['filename']
                    self.request.name_file = name_file
                    f[0].instance.name_file = name_file
            new_forms.append(f)
        return super(SliderElementUpdate, self).form_valid(form, new_forms)


class SliderElementUpdateModal(GenUpdateModal, SliderElementUpdate):
    pass


class SliderElementDelete(GenDelete):
    model = SliderElement


"""
class SliderElementDetailsModal(GenDetailModal):
    model = SliderElement
    groups = SliderElementForm.__groups_details__()
    exclude_fields = []

"""


# ###########################################
# Staticheader
class StaticheaderList(GenList):
    model = Staticheader
    extra_context = {'menu': ['StaticheaderGroup', 'people'], 'bread': [_('StaticheaderGroup'), _('People')]}
    show_details = True
    default_ordering = ["-public"]


class StaticheaderCreate(GenCreate):
    model = Staticheader
    form_class = StaticheaderForm
    show_details = True


class StaticheaderCreateModal(GenCreateModal, StaticheaderCreate):
    pass


class StaticheaderUpdate(GenUpdate):
    model = Staticheader
    form_class = StaticheaderForm
    show_details = True


class StaticheaderUpdateModal(GenUpdateModal, StaticheaderUpdate):
    pass


class StaticheaderDelete(GenDelete):
    model = Staticheader


class StaticheaderDetails(GenDetail):
    model = Staticheader
    groups = StaticheaderForm.__groups_details__()

    tabs = [
        {
            'id': 'staticheader',
            'name': _('Elements'),
            'ws': 'CDNX_cms_staticheader_element_sublistlist',
            'wsbase': 'staticheader_list',
            'rows': 'base'
        },
    ]
    exclude_fields = ['columns_distribution']


# ###########################################
# StaticheaderElement

static_staticheader_formsfull = [(None, None, None)]
for lang_code in settings.LANGUAGES_DATABASES:
    static_staticheader_formsfull.append((eval("StaticheaderElementText{}".format(lang_code)), 'slider_element', None))


class StaticheaderElementSubList(GenList):
    model = StaticheaderElement
    extra_context = {'menu': ['StaticheaderElement', 'people'], 'bread': [_('StaticheaderElement'), _('People')]}
    show_details = False
    # json = False
    # template_model = "frontheader/frontheader_sublist.html"

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(frontheader__pk=pk)
        return limit


class StaticheaderElementCreate(MultiForm, GenCreate):
    model = StaticheaderElement
    form_class = StaticheaderElementForm
    forms = formsfull["StaticheaderElement"]

    def form_valid(self, form, forms):
        new_forms = []
        for f in forms:
            if type(f[0]) != self.form_class:
                name_form = str(type(forms[1][0])).split('.')[-1].replace("'", '').replace('>', '')
                field_image = "{}_image".format(name_form)

                body = self.request.body
                if type(self.request.body) == bytes:
                    body = body.decode("utf-8")
                body = json.loads(body)

                if field_image in body and 'filename' in body[field_image]:
                    name_file = body[field_image]['filename']
                    self.request.name_file = name_file
                    f[0].instance.name_file = name_file
            new_forms.append(f)

        try:
            return super(StaticheaderElementCreate, self).form_valid(form, new_forms)
        except ValidationError as e:
            errors = form._errors.setdefault("public", ErrorList())
            errors.append(e)
            return super(StaticheaderElementCreate, self).form_invalid(form, [tform[0] for tform in forms], 1, 0)


class StaticheaderElementCreateModal(GenCreateModal, StaticheaderElementCreate):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__frontheader_pk = kwargs.get('cpk', None)
        return super(StaticheaderElementCreateModal, self).dispatch(*args, **kwargs)

    def form_valid(self, form, forms):
        if self.__frontheader_pk:
            frontheader = Staticheader.objects.get(pk=self.__frontheader_pk)
            self.request.frontheader = frontheader
            form.instance.frontheader = frontheader

        return super(StaticheaderElementCreateModal, self).form_valid(form, forms)


class StaticheaderElementUpdateModal(MultiForm, GenUpdateModal):
    model = StaticheaderElement
    form_class = StaticheaderElementForm
    forms = formsfull["StaticheaderElement"]

    def form_valid(self, form, forms):
        new_forms = []
        for f in forms:
            if type(f[0]) != self.form_class:
                name_form = str(type(forms[1][0])).split('.')[-1].replace("'", '').replace('>', '')
                field_image = "{}_image".format(name_form)
                
                body = self.request.body
                if type(self.request.body) == bytes:
                    body = body.decode("utf-8")
                body = json.loads(body)

                if field_image in body and 'filename' in body[field_image]:
                    name_file = body[field_image]['filename']
                    self.request.name_file = name_file
                    f[0].instance.name_file = name_file
            new_forms.append(f)
            
        try:
            return super(StaticheaderElementUpdateModal, self).form_valid(form, new_forms)
        except ValidationError as e:
            errors = form._errors.setdefault("public", ErrorList())
            errors.append(e)
            return super(StaticheaderElementUpdateModal, self).form_invalid(form, [tform[0] for tform in forms], 1, 0)


class StaticheaderElementDelete(GenDelete):
    model = StaticheaderElement


"""
class StaticheaderElementDetailsModal(GenDetailModal):
    model = StaticheaderElement
    groups = StaticheaderElementForm.__groups_details__()
    exclude_fields = ['frontheader']

"""


# ###########################################
# StaticPage
class StaticPageList(GenList):
    model = StaticPage
    extra_context = {'menu': ['StaticPage', 'people'], 'bread': [_('StaticPage'), _('People')]}


class StaticPageCreate(MultiForm, GenCreate):
    model = StaticPage
    form_class = StaticPageForm
    forms = formsfull["StaticPage"]
    form_ngcontroller = "CDNXCMSFormSliderCtrl"


class StaticPageCreateModal(GenCreateModal, StaticPageCreate):
    pass


class StaticPageUpdate(MultiForm, GenUpdate):
    model = StaticPage
    form_class = StaticPageForm
    forms = formsfull["StaticPage"]


class StaticPageUpdateModal(GenUpdateModal, StaticPageUpdate):
    pass


class StaticPageDelete(GenDelete):
    model = StaticPage


# ###########################################
# StaticPageAuthor
class StaticPageAuthorList(GenList):
    model = StaticPageAuthor
    extra_context = {'menu': ['StaticPageAuthor', 'people'], 'bread': [_('StaticPageAuthor'), _('People')]}


class StaticPageAuthorCreate(GenCreate):
    model = StaticPageAuthor
    form_class = StaticPageAuthorForm
    hide_foreignkey_button = True


class StaticPageAuthorCreateModal(GenCreateModal, StaticPageAuthorCreate):
    pass


class StaticPageAuthorUpdate(GenUpdate):
    model = StaticPageAuthor
    form_class = StaticPageAuthorForm
    hide_foreignkey_button = True


class StaticPageAuthorUpdateModal(GenUpdateModal, StaticPageAuthorUpdate):
    pass


class StaticPageAuthorDelete(GenDelete):
    model = StaticPageAuthor


# ###########################################
# StaticPage
class TemplateStaticPageList(GenList):
    model = TemplateStaticPage
    extra_context = {'menu': ['StaticPage', 'people'], 'bread': [_('StaticPage'), _('People')]}


class TemplateStaticPageCreate(GenCreate):
    model = TemplateStaticPage
    form_class = TemplateStaticPageForm


class TemplateStaticPageCreateModal(GenCreateModal, TemplateStaticPageCreate):
    pass


class TemplateStaticPagePageUpdate(GenUpdate):
    model = TemplateStaticPage
    form_class = TemplateStaticPageForm


class TemplateStaticPageUpdateModal(GenUpdateModal, TemplateStaticPagePageUpdate):
    pass


class TemplateStaticPageDelete(GenDelete):
    model = TemplateStaticPage


class TemplateStaticPageForeign(GenForeignKey):
    model = TemplateStaticPage
    label = "{name}"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        # Get serach string
        search = kwargs.get('search', None)

        # Build queryset
        qs = self.model.objects.all()
        if search != '*':
            qs = qs.filter(name__icontains=search)

        # Initialize answer
        answer = {}
        answer['rows'] = []
        answer['clear'] = []
        answer['readonly'] = []

        # None
        token = {}
        token['id'] = None
        token['label'] = '---------'
        for lang_code in settings.LANGUAGES_DATABASES:
            token['StaticPageForm{}_tiles'.format(lang_code.upper())] = '{}'
        answer['rows'].append(token)

        # Entries
        for row in qs:
            # Initialize token
            token = {}
            token['id'] = row.pk
            token['label'] = row.name
            # Build tiles
            tile_base = json.loads(row.tile)
            tiles = {}
            for key in tile_base:
                tiles[key] = {'value': '', 'type': tile_base[key], 'deleted': False}

            # Set all tiles
            for lang_code in settings.LANGUAGES_DATABASES:
                token['StaticPageTextForm{}_tiles:__JSON_DATA__'.format(lang_code.upper())] = json.dumps(tiles)
            answer['rows'].append(token)

        # Dump answer
        try:
            json_answer = json.dumps(answer)
        except TypeError:
            raise TypeError("The structure can not be encoded to JSON")
        # Return the new answer
        return HttpResponse(json_answer, content_type='application/json')
