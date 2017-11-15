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

import re
import json
import unicodedata

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, IntegrityError
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _
from django.template import Context, Template
from django.conf import settings

from django.core.exceptions import ValidationError

from codenerix.models import CodenerixModel, GenInterface
from codenerix_extensions.files.models import GenImageFileNull
from codenerix_extensions.helpers import get_external_method, get_language_database

from codenerix.fields import MultiBlockWysiwygField


VALID_TYPE_TEMPLATE = ('image', 'string', 'video')

HTML_FORMAT = (
    ('a', 'A'),
    ('b', 'B'),
    ('c', 'C'),
)

HEADER_HTML_FORMAT = (
    ('a', 'A'),
    ('b', 'B'),
    ('c', 'C'),
)

CHOICE_DRAFT = 'D'
CHOICE_PENDING = 'P'
CHOICE_PUBLIC = 'R'

STATUS_CHOICES = (
    (CHOICE_DRAFT, _('Draft')),
    (CHOICE_PUBLIC, _('Public')),
    (CHOICE_PENDING, _('Pending')),
)

"""
@summary: Este modelo es un modelo genérico para gestionar slider.
@var image: Atributo obligatorio. Contiene la imagen que se va a mostrar.
@var title: Atributo obligatorio. Referencia a la cabezara que se mostrará en el slider (útil para seo).
@var active: Atributo obligatorio. Si el booleano se encuentra a verdadero, la imagen se mostrará en el slider.
        Nota: Hay una constante que indica el número máximo de imagenes activas al mismo tiempo, es recomendable usarlo.
@var button: Atributo opcional. En caso de haberlo, aquí se añade una redirección a otra url.
        Note: Teniendo en cuenta que se prevee una entrada en deprecater por parte de URLField, controlar que lo que entra
        en button es una url.

"""


def extract_regex_cdnxtiler():
    # REGEX: Head
    regex = "(?:{%\ *cdnx_tiler\ +"
    # REGEX: First argument
    regex += "\"((\ )*\w*(\ )*)\""
    # REGEX: Tail
    regex += "(\ )*%})"
    # REGEX: Compile
    return re.compile(regex)


def extract_regex_cdnxtype():
    # REGEX: Head
    regex = "(?:{%\ *cdnx_tiler_type\ +"
    # REGEX: All character until symbol %}
    regex += '''\' *\{ *'''
    # REGEX: Element with comma
    regex += '''( *(\"\w+\") *: *(\"\w+\") *,'''
    # REGEX: Element without comma
    regex += '''| *(\"\w+\") *: *(\"\w+\") *)*'''
    # REGEX: Close dictionary
    regex += ''' *\} *\''''
    # REGEX: Tail
    regex += "\ *%})"
    # REGEX: Compile
    return re.compile(regex)


class GenBaseText(CodenerixModel, GenImageFileNull):  # META: Abstract class
    title = models.CharField(_("Title"), max_length=200, blank=True, null=True)
    description = models.TextField(_("Description"), null=True, blank=True)
    button = models.CharField(_("Button"), max_length=200, blank=True, null=True)
    url = models.CharField(_("URL"), max_length=500, blank=False, null=False)
    
    class Meta(CodenerixModel.Meta):
        abstract = True

    def __str__(self):
        return u"{}".format(self.title)

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('title', _('Title'), 100))
        fields.append(('button', _('Button'), 100))
        fields.append(('url', _('URL'), 100))
        return fields


class GenMainInfo(CodenerixModel):  # META: Abstract class
    identifier = models.CharField(_("Identifier"), max_length=200, blank=True, null=True, unique=True)
    public = models.BooleanField(_("Public"), default=False)

    class Meta(CodenerixModel.Meta):
        abstract = True

    def __str__(self):
        return u"{}".format(self.identifier)

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('identifier', _('Identifier'), 100))
        fields.append(('public', _('Public'), 100))
        return fields


class GenElementInfo(CodenerixModel):  # META: Abstract class
    order = models.IntegerField(_("Order"), blank=False, null=False, unique=False)
    show_title = models.BooleanField(_("Show tittle"), default=False)
    public = models.BooleanField(_("Public"), default=False)

    class Meta(CodenerixModel.Meta):
        abstract = True

    def __str__(self):
        return u"{}".format(self.order)

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('order', _('Order'), 100))
        fields.append(('show_title', _('Show title'), 100))
        fields.append(('public', _('Public'), 100))
        return fields


class Slider(GenMainInfo):
    default = models.BooleanField(_("Default"), default=False)

    def __str__(self):
        return u"{}".format(self.identifier)

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = super(Slider, self).__fields__(info)
        fields.append(('default', _('Default'), 100))
        return fields


class SliderElement(GenElementInfo):
    html_format = models.CharField(_("HtmlFormat"), max_length=2, blank=True, null=True, choices=HTML_FORMAT)
    new_price = models.CharField(_("New price"), max_length=200, blank=True, null=True)
    old_price = models.CharField(_("Old price"), max_length=200, blank=True, null=True)
    discount = models.CharField(_("Discount"), max_length=200, blank=True, null=True)
    slider = models.ForeignKey(Slider, related_name="sliderelements", verbose_name=_("Slider"), blank=False, null=False)

    def __fields__(self, info):
        fields = super(SliderElement, self).__fields__(info)

        fields.append(('html_format', _('Html format'), 100))
        fields.append(('new_price', _('New price'), 100))
        fields.append(('old_price', _('Old price'), 100))
        fields.append(('discount', _('Discount'), 100))

        return fields


class Staticheader(GenMainInfo):
    html_format = models.CharField(_("HtmlFormat"), max_length=2, blank=True, null=True, choices=HEADER_HTML_FORMAT)
    num_elements = models.IntegerField(_("Number of columns"), blank=False, null=False, validators=[MaxValueValidator(4), MinValueValidator(1)])
    default = models.BooleanField(_("By default"), default=False)

    def __str__(self):
        return u"{}".format(self.identifier)

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = super(Staticheader, self).__fields__(info)
        fields.append(('html_format', _('Identificador'), 100))
        fields.append(('num_elements', _('Number columns'), 100))
        fields.append(('default', _('By default'), 100))
        return fields

    def save(self, *args, **kwargs):
        if self.default:
            Staticheader.objects.exclude(pk=self.pk).update(default=False)
        return super(Staticheader, self).save(*args, **kwargs)


class StaticheaderElement(GenElementInfo):
    frontheader = models.ForeignKey(Staticheader, related_name="staticheaderelements", verbose_name=_("Static Header"), blank=False, null=False)

    def save(self, *args, **kwargs):
        if self.public:
            if StaticheaderElement.objects.filter(public=True, frontheader=self.frontheader).exclude(pk=self.pk).count() >= self.frontheader.num_elements:
                raise ValidationError(_('Too many elements marked as "public". Unpublish some'))
        return super(StaticheaderElement, self).save(*args, **kwargs)


def calculate_slug(title, slug_origin, Model, pk):
    if slug_origin:
        slug_origin = slug_origin.strip()
    if not slug_origin:
        name = title.strip().replace(' ', '-')
        pattern = re.compile('[\W-]+')
        slug = pattern.sub('', name).lower()
    else:
        slug = slug_origin.lower()
    slug = ''.join((c for c in unicodedata.normalize('NFD', smart_text(slug)) if unicodedata.category(c) != 'Mn'))
    while Model.objects.filter(slug=slug).exclude(pk=pk).exists():
        slug += '_'
    return slug


# ###################################
# Static Pages


class StaticPageText(CodenerixModel):  # META: Abstract class
    """
    @ivar tiles: Contiene un diccionario de diccionarios, donde la clave es el nombre del elemento, y el valor es otro diccionario con el tipo y valor asociado.
        p.e. {'nombre':{'type':'string', 'value';'Nombre dado', 'render':'vimeo'}, ...}
    """
    slug = models.CharField(_('slug'), max_length=200, blank=False, null=False, unique=True)
    tiles = MultiBlockWysiwygField(_('Tiles'), blank=True, null=False)

    class Meta(CodenerixModel.Meta):
        abstract = True

    def __str__(self):
        return u"{}".format(self.slug)

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('slug', _('Slug'), 100))
        return fields

    def update(self, tiles=None, *args, **kwargs):
        if tiles:
            if self.tiles:
                actual_tiles = json.loads(self.tiles)
            else:
                actual_tiles = {}

            for t in tiles:

                if t not in actual_tiles:
                    actual_tiles[t] = {"type": tiles[t], "value": "", "deleted": False}
                else:
                    actual_tiles[t]["type"] = tiles[t]
            for at in actual_tiles:
                if at not in tiles:
                    actual_tiles[at]["deleted"] = True

            self.tiles = json.dumps(actual_tiles)
            self.save()

    def save(self, *args, **kwargs):
        if not self.tiles:
            self.tiles = '{}'
        return super(StaticPageText, self).save(*args, **kwargs)


class TemplateStaticPage(CodenerixModel):
    """
    @ivar template: Contiene un template html, las etiquetas de mensaje se encontrarán con este patrón {+ name:type +}, type debe coincidir con un tipo valido.
    """

    name = models.CharField(_('Name'), max_length=150, blank=False, null=False)
    template = models.TextField(_('Template'), blank=False, null=False)
    # template = BootstrapWysiwygField(_('Template'), blank=False, null=False)
    tile = models.TextField(_('Tile'), blank=False, null=False)

    def __str__(self):
        return u"{}".format(smart_text(self.name))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('name', _('Title'), 100))

        return fields

    def save(self, *args, **kwargs):
        # Vars
        p = extract_regex_cdnxtiler()
        pt = extract_regex_cdnxtype()
        res = []
        ctx_type = {'cdnx_tiler_types': {}}
        tiles = {}

        # Extraction of labels
        for item in re.finditer(pt, self.template):
            res_type = json.loads(Template("{{% load cdnxcms_tiler_validator %}}{}".format(item.group(0))).render(Context(ctx_type)))
            # I extract context
            if 'data' in res_type:
                ctx_type['cdnx_tiler_types'] = res_type['data']
            res.append(res_type)
        # Si hay algúna etiqueta tiler se extrae
        if p.search(self.template):
            # Si hay algun tipo declarado, simplemente no hago nada, de esto se encarga el formulario
            if ctx_type['cdnx_tiler_types']:
                for item in re.finditer(p, self.template):

                    dict_response = json.loads(Template(
                        "{{% load cdnxcms_tiler_validator %}}{}"
                        .format(
                            item.group(0)
                        )
                    ).render(
                        Context(ctx_type))
                    )

                    if dict_response['code_error'] == 0:
                        tiles.update(dict_response['data'])
                    # If exist an error, then i send a Validation Error with message
                    elif dict_response['code_error'] > 0:
                        raise IntegrityError(dict_response['error_msg'])

        self.tile = json.dumps(tiles)

        # Update static pages
        for sp in self.staticpages.all():

            sp.update(tiles)

        return super(TemplateStaticPage, self).save(*args, **kwargs)

    @staticmethod
    def check_template(template):
        p = extract_regex_cdnxtiler()
        pt = extract_regex_cdnxtype()
        res = []
        ctx_type = {'cdnx_tiler_types': {}}

        for item in re.finditer(pt, template):
            res_type = json.loads(Template(
                "{{% load cdnxcms_tiler_validator %}}{}".format(item.group(0))
            ).render(Context(ctx_type)))
            # I extract context
            if 'data' in res_type:
                ctx_type['cdnx_tiler_types'] = res_type['data']
            res.append(res_type)
        # Si hay algúna etiqueta tiler se extrae
        if p.search(template):
            # Si hay algun tipo declarado, mando el error al formulario
            if ctx_type['cdnx_tiler_types']:
                for item in re.finditer(p, template):
                    res.append(json.loads(Template(
                        "{{% load cdnxcms_tiler_validator %}}{}"
                        .format(item.group(0)))
                        .render(Context(ctx_type))))
            else:
                res.append({'code_error': 6, 'error_msg': _(
                    "Your cdnx_tiler_type is missing or bad formed.")
                })
        return res


class ABSTRACT_GenStaticPageAuthor(models.Model):

    class Meta(CodenerixModel.Meta):
        abstract = True


class StaticPageAuthor(CodenerixModel):
    class CodenerixMeta:
        abstract = ABSTRACT_GenStaticPageAuthor

    def __str__(self):
        if hasattr(self, 'external'):
            return u"{}".format(smart_text(self.external.CDNXCMS_get_summary()))
        else:
            return _('No data!')

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        external_fields = get_external_method(StaticPageAuthor, '__fields_staticpage__', info)
        for (external_path, label) in external_fields:
            fields.append(("external__{}".format(external_path), label), )
        
        return fields

    @staticmethod
    def foreignkey_external():
        bridge = get_external_method(StaticPageAuthor, GenStaticPageAuthor.CodenerixMeta.force_methods['foreignkey_author'][0])
        if bridge is None:
            raise IOError("No bridge found with StaticPageAuthor, you should use GenStaticPageAuthor on your model to link to this one! If you are not willing to use this feature, please include in your urls.py only the URLs you need for your purpose")
        return bridge


class StaticPage(CodenerixModel):
    author = models.ForeignKey(StaticPageAuthor, related_name="staticpages", blank=True, null=True)
    status = models.CharField(_('Status'), max_length=150, blank=False, null=False, choices=STATUS_CHOICES, default=CHOICE_DRAFT)
    template = models.ForeignKey(TemplateStaticPage, related_name="staticpages", blank=False, null=False)

    def __fields__(self, info):
        lang = get_language_database()
        fields = []
        fields.append(('{}__slug'.format(lang), _('Slug'), 100))
        fields.append(('get_status_display', _('Status'), 100))
        fields.append(('author', _('Author'), 100))
        return fields

    def __str__(self):
        return u"{} ({})".format(smart_text(self.template), self.status)

    def __unicode__(self):
        return self.__str__()

    def update(self, tiles=None, *args, **kwargs):
        # I make sure to have tiles.
        if not tiles:
            tiles = json.loads(self.template.tile)

        for lang_code in settings.LANGUAGES_DATABASES:
            getattr(self, lang_code.lower()).update(tiles)


# author
class GenStaticPageAuthor(GenInterface, ABSTRACT_GenStaticPageAuthor):  # META: Abstract class
    author = models.OneToOneField(StaticPageAuthor, related_name='external', verbose_name=_("Author"), null=True, on_delete=models.SET_NULL, blank=True)

    class Meta(GenInterface.Meta, ABSTRACT_GenStaticPageAuthor.Meta):
        abstract = True

    class CodenerixMeta:
        force_methods = {
            'foreignkey_author': ('CDNXCMS_get_fk_info_author', _('---')),
            'get_name_related': ('CDNXCMS_get_name_related', _('---')),
            'get_summary': ('CDNXCMS_get_summary', ),
        }

    def save(self, *args, **kwards):
        if hasattr(self, 'author') and self.author is None:
            author = StaticPageAuthor()
            author.save()
            self.author = author

        return super(GenStaticPageAuthor, self).save(*args, **kwards)


MODELS = [
    ("slider_element", "SliderElement", "GenBaseText"),
    ("staticheader_element", "StaticheaderElement", "GenBaseText"),
    ("static_page", "StaticPage", "StaticPageText"),
]

for info in MODELS:
    field = info[0]
    model = info[1]
    base_model = info[2]
    for lang_code in settings.LANGUAGES_DATABASES:
        query = "class {}Text{}({}):\n".format(model, lang_code, base_model)
        query += "    {} = models.OneToOneField({}, blank=False, null=False, related_name='{}')\n".format(field, model, lang_code.lower())
        if model == 'StaticPage':

            query += "    def save(self, *args, **kwargs): \n"
            query += "        self.slug = calculate_slug('', self.slug, StaticPageText{}, self.pk)\n".format(lang_code)
            query += "        return super(StaticPageText{}, self).save(*args, **kwargs)\n".format(lang_code)

        exec(query)
