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

from django import template

from codenerix_cms.templatetags_tags import cdnx_slider, cdnx_staticheader


def f(x):
    return lambda identifier, lang, template='codenerix_cms/slider.html', *args, **kwargs: x(identifier, lang, template, *args, **kwargs)


def d(x):
    return lambda identifier, lang, template='codenerix_cms/staticheader.html', *args, **kwargs: x(identifier, lang, template, *args, **kwargs)


register = template.Library()

register.simple_tag(f(cdnx_slider), name="cdnx_slider")
register.simple_tag(d(cdnx_staticheader), name='cdnx_staticheader')
