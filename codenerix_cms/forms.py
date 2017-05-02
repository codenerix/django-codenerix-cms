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

from django import forms
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from codenerix.forms import GenModelForm
from codenerix.widgets import WysiwygAngularInput
from codenerix_cms.models import Slider, SliderElement, StaticheaderElement, Staticheader, MODELS, StaticPage, TemplateStaticPage, extract_regex_cdnxtiler


class SliderForm(GenModelForm):
    class Meta:
        model = Slider
        exclude = []

    def __groups__(self):
        return [(_(u'Grupo'), 12,
            ['identifier', 6],
            ['public', 3],
            ['default', 3],
        )
        ]

    @staticmethod
    def __groups_details__():
        return [(_(u'Grupo'), 12,
            ['identifier', 6],
            ['public', 6],
            ['default', 6],)
        ]


class SliderElementForm(GenModelForm):
    class Meta:
        model = SliderElement
        exclude = ['slider']
    
    """
    def clean(self):
        active = self.cleaned_data['active']
        group = self.cleaned_data['group']
        if active:
            l = Slider.objects.filter(group=group, active=True)
            # ¿por que?
            if len(l) >= 6:
                raise forms.ValidationError("You only can have 6 elements active at the time.")
        self.cleaned_data['active'] = active
        self.cleaned_data['group'] = group
        return self.cleaned_data
    """
    
    def __groups__(self):
        return [(_(u'Slider'), 12,
            ['order', 6],
            ['public', 3],
            ['show_title', 3],
            ['html_format', 6],
            ['new_price', 6, None, None, None, None, None, ["ng-keypress=reset_discount()", "ng-blur=change_price()"]],
            ['old_price', 6, None, None, None, None, None, ["ng-keypress=reset_discount()", "ng-blur=change_price()"]],
            ['discount', 6, None, None, None, None, None, ["ng-keypress=reset_oldprice()", "ng-blur=change_discount()"]],
        )
        ]

    @staticmethod
    def __groups_details__():
        return [(_(u'Slider'), 12,
            ['slider', 6],
            ['order', 6],
            ['show_title', 6],
            ['public', 6],
            ['html_format', 6],
            ['new_price', 6],
            ['old_price', 6],
            ['discount', 6],)
        ]


# DynamicLanguageForm(model, "{}Text".format(model), None, "{}TextForm".format(model))

class StaticheaderForm(GenModelForm):
    class Meta:
        model = Staticheader
        exclude = []

    def __groups__(self):
        return [(_(u'Grupo'), 12,
            ['identifier', 6],
            ['public', 3],
            ['default', 3],
            ['html_format', 6],
            ['num_elements', 6],
        )
        ]

    @staticmethod
    def __groups_details__():
        return [(_(u'Grupo'), 12,
            ['identifier', 6],
            ['public', 6],
            ['default', 6],
            ['html_format', 6],
            ['num_elements', 6],
        )
        ]


class StaticheaderElementForm(GenModelForm):
    class Meta:
        model = StaticheaderElement
        exclude = ['frontheader']

    def __groups__(self):
        return [(_(u'Slider'), 12,
            ['order', 6],
            ['public', 3],
            ['show_title', 3],
        )
        ]
    
    @staticmethod
    def __groups_details__():
        return [(_('Details'), 12,
            ['order', 6],
            ['show_title', 6],
            ['public', 6],
        )
        ]


class TemplateStaticPageForm(GenModelForm):
    class Meta:
        model = TemplateStaticPage
        exclude = ['tile']

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['name', 6],
                ['template', 6],
             )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['name', 6],
                ['template', 6],
             )
        ]
        return g

    def clean_template(self):
        template = self.cleaned_data['template']
        res = TemplateStaticPage.check_template(template)
        for r in res:
            if r['code_error'] > 0:
                raise ValidationError(r['error_msg'])

        return template


class StaticPageForm(GenModelForm):
    codenerix_external_field = forms.CharField(
        label=StaticPage.foreignkey_external()['label'],
    )

    class Meta:
        model = StaticPage
        exclude = []
        autofill = {
            'StaticPageForm_template': ['select', 3, 'CDNX_cms_templatestaticpage_foreign'],
            'StaticPageForm_codenerix_external_field': ['select', 3, StaticPage.foreignkey_external()['related']],
        }

    def __groups__(self):
        g = [(_('Details'), 12,
            ['codenerix_external_field', 5],
            ['template', 5],
            ['status', 2],
        )
        ]
        return g
    
    @staticmethod
    def __groups_details__():
        g = [(_('Details'),12,
            ['codenerix_external_field', 5],
            ['template', 5],
            ['status', 2],
        )
        ]
        return g


query = ""
forms_dyn = []
for info in MODELS:
    field = info[0]
    model = info[1]
    for lang_code in settings.LANGUAGES_DATABASES:
        query = "from codenerix_cms.models import {}Text{}\n".format(model, lang_code)
        exec(query)
        query = """
class {model}TextForm{lang}(GenModelForm):\n
    class Meta:\n
        model={model}Text{lang}\n
        exclude = ['name_file', ]\n
        """
        if model not in ("StaticheaderElement", "SliderElement"):
            query += """widgets = {{\n
            'description': WysiwygAngularInput(),\n
        }}\n"""
        query += """
    def __groups__(self):\n
        return [(_('Details'),12,"""
        if model != 'StaticPage':
            if lang_code == settings.LANGUAGES_DATABASES[0]:
                query += """
                    ['title', 12, None, None, None, None, None, ["ng-blur=refresh_lang_field('title', '{model}TextForm', [{languages}])"]],
                    ['url', 12, None, None, None, None, None, ["ng-blur=refresh_lang_field('url', '{model}TextForm', [{languages}])"]],
                    ['button', 12, None, None, None, None, None, ["ng-blur=refresh_lang_field('button', '{model}TextForm', [{languages}])"]],
                    ['image', 12, None, None, None, None, None, ["ng-blur=refresh_lang_field('image', '{model}TextForm', [{languages}])"]],
                    ['description', 12, None, None, None, None, None, ["ng-blur=refresh_lang_field('description', '{model}TextForm', [{languages}])"]],
                )]\n"""
            else:
                query += """
                    ['title', 12],
                    ['url', 12],
                    ['button', 12],
                    ['image', 12],
                    ['description', 12],
                )]\n"""
        else:
            if lang_code == settings.LANGUAGES_DATABASES[0]:
                query += """
                    ['slug', 12, None, None, None, None, None, ["ng-blur=refresh_lang_field('slug', '{model}TextForm', [{languages}])"]],
                    ['tiles', 12, None, None, None, None, None, ["ng-blur=refresh_lang_field('tiles', '{model}TextForm', [{languages}])"]],
                )]\n"""
            else:
                query += """
                    ['slug', 12],
                    ['tiles', 12],
                )]\n"""

        exec(query.format(model=model, lang=lang_code, languages="'{}'".format("','".join(settings.LANGUAGES_DATABASES))))
