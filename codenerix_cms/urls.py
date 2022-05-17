# -*- coding: utf-8 -*-
#
# django-codenerix-cms
#
# Codenerix GNU
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

from django.urls import re_path as url

from codenerix_cms.views import \
    SliderList, SliderCreate, SliderCreateModal, SliderUpdate, SliderUpdateModal, SliderDelete, SliderDetail, \
    SliderElementSublist, SliderElementCreate, SliderElementCreateModal, SliderElementUpdate, SliderElementUpdateModal, SliderElementDelete, \
    StaticheaderList, StaticheaderCreate, StaticheaderCreateModal, StaticheaderUpdate, StaticheaderUpdateModal, StaticheaderDelete, StaticheaderDetails, \
    StaticheaderElementSubList, StaticheaderElementCreateModal, StaticheaderElementUpdateModal, StaticheaderElementDelete, \
    StaticPageList, StaticPageCreate, StaticPageCreateModal, StaticPageUpdate, StaticPageUpdateModal, StaticPageDelete, \
    StaticPageAuthorList, StaticPageAuthorCreate, StaticPageAuthorCreateModal, StaticPageAuthorUpdate, StaticPageAuthorUpdateModal, StaticPageAuthorDelete, \
    TemplateStaticPageList, TemplateStaticPageCreate, TemplateStaticPageCreateModal, TemplateStaticPagePageUpdate, TemplateStaticPageUpdateModal, TemplateStaticPageDelete, TemplateStaticPageForeign
# SliderElementDetailsModal, \
# StaticheaderElementDetailsModal, \
# SliderList, SliderCreate, SliderCreateModal, SliderUpdate, SliderUpdateModal, SliderDelete, SliderSublist, SliderDetail,


urlpatterns = [

    url(r'^sliders$', SliderList.as_view(), name='CDNX_cms_slider_list'),
    url(r'^sliders/add$', SliderCreate.as_view(), name='CDNX_cms_slider_add'),
    url(r'^sliders/addmodal$', SliderCreateModal.as_view(), name='CDNX_cms_slider_addmodal'),
    url(r'^sliders/(?P<pk>\w+)/edit$', SliderUpdate.as_view(), name='CDNX_cms_slider_edit'),
    url(r'^sliders/(?P<pk>\w+)/editmodal$', SliderUpdateModal.as_view(), name='CDNX_cms_slider_editmodal'),
    url(r'^sliders/(?P<pk>\w+)/delete$', SliderDelete.as_view(), name='CDNX_cms_slider_delete'),
    url(r'^sliders/(?P<pk>\w+)$', SliderDetail.as_view(), name='CDNX_cms_slider_detail'),
    
    url(r'^sliderelements/(?P<pk>\w+)/sublist$', SliderElementSublist.as_view(), name='CDNX_cms_slider_element_sublist'),
    url(r'^sliderelements/(?P<tpk>\w+)/sublist/addmodal$', SliderElementCreateModal.as_view(), name='CDNX_cms_slider_element_sublist_add'),
    # url(r'^sliderelements/(?P<tpk>\w+)/sublist/(?P<pk>\w+)/modal$', SliderElementDetailsModal.as_view(), name='slider_element_sublist_detail'),
    url(r'^sliderelements/(?P<tpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', SliderElementUpdateModal.as_view(), name='CDNX_cms_slider_element_sublist_edit'),
    url(r'^sliderelements/(?P<tpk>\w+)/sublist/(?P<pk>\w+)/delete$', SliderElementDelete.as_view(), name='CDNX_cms_slider_element_sublist_delete'),
    
    
    url(r'^staticheaders$', StaticheaderList.as_view(), name='CDNX_cms_staticheader_list'),
    url(r'^staticheaders/add$', StaticheaderCreate.as_view(), name='CDNX_cms_staticheader_add'),
    url(r'^staticheaders/addmodal$', StaticheaderCreateModal.as_view(), name='CDNX_cms_staticheader_addmodal'),
    url(r'^staticheaders/(?P<pk>\w+)$', StaticheaderDetails.as_view(), name='CDNX_cms_staticheader_details'),
    url(r'^staticheaders/(?P<pk>\w+)/edit$', StaticheaderUpdate.as_view(), name='CDNX_cms_staticheader_edit'),
    url(r'^staticheaders/(?P<pk>\w+)/editmodal$', StaticheaderUpdateModal.as_view(), name='CDNX_cms_staticheader_editmodal'),
    url(r'^staticheaders/(?P<pk>\w+)/delete$', StaticheaderDelete.as_view(), name='CDNX_cms_staticheader_delete'),
    
    
    url(r'^staticheaderelements/(?P<pk>\w+)/sublist$', StaticheaderElementSubList.as_view(), name='CDNX_cms_staticheader_element_sublistlist'),
    url(r'^staticheaderelements/(?P<cpk>\w+)/sublist/addmodal$', StaticheaderElementCreateModal.as_view(), name='CDNX_cms_staticheader_element_sublistlist_add'),
    # url(r'^staticheaderelements/(?P<tpk>\w+)/sublist/(?P<pk>\w+)/modal$', StaticheaderElementDetailsModal.as_view(), name='frontheader_sublistlist_details'),
    url(r'^staticheaderelements/(?P<tpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', StaticheaderElementUpdateModal.as_view(), name='CDNX_cms_frontheader_sublistlist_edit'),
    url(r'^staticheaderelements/(?P<tpk>\w+)/sublist/(?P<pk>\w+)/delete$', StaticheaderElementDelete.as_view(), name='CDNX_cms_frontheader_sublistlist_delete'),
    

    url(r'^staticpages$', StaticPageList.as_view(), name='CDNX_cms_staticpages_list'),
    url(r'^staticpages/add$', StaticPageCreate.as_view(), name='CDNX_cms_staticpages_add'),
    url(r'^staticpages/addmodal$', StaticPageCreateModal.as_view(), name='CDNX_cms_staticpages_addmodal'),
    url(r'^staticpages/(?P<pk>\w+)/edit$', StaticPageUpdate.as_view(), name='CDNX_cms_staticpages_edit'),
    url(r'^staticpages/(?P<pk>\w+)/editmodal$', StaticPageUpdateModal.as_view(), name='CDNX_cms_staticpages_editmodal'),
    url(r'^staticpages/(?P<pk>\w+)/delete$', StaticPageDelete.as_view(), name='CDNX_cms_staticpages_delete'),

    url(r'^staticpageauthors$', StaticPageAuthorList.as_view(), name='CDNX_cms_staticpageauthors_list'),
    url(r'^staticpageauthors/add$', StaticPageAuthorCreate.as_view(), name='CDNX_cms_staticpageauthors_add'),
    url(r'^staticpageauthors/addmodal$', StaticPageAuthorCreateModal.as_view(), name='CDNX_cms_staticpageauthors_addmodal'),
    url(r'^staticpageauthors/(?P<pk>\w+)/edit$', StaticPageAuthorUpdate.as_view(), name='CDNX_cms_staticpageauthors_edit'),
    url(r'^staticpageauthors/(?P<pk>\w+)/editmodal$', StaticPageAuthorUpdateModal.as_view(), name='CDNX_cms_staticpageauthors_editmodal'),
    url(r'^staticpageauthors/(?P<pk>\w+)/delete$', StaticPageAuthorDelete.as_view(), name='CDNX_cms_staticpageauthors_delete'),

    
    url(r'^templatestaticpages$', TemplateStaticPageList.as_view(), name='CDNX_cms_templatestaticpages_list'),
    url(r'^templatestaticpages/add$', TemplateStaticPageCreate.as_view(), name='CDNX_cms_templatestaticpages_add'),
    url(r'^templatestaticpages/addmodal$', TemplateStaticPageCreateModal.as_view(), name='templatestaticpages_addmodal'),
    url(r'^templatestaticpages/(?P<pk>\w+)/edit$', TemplateStaticPagePageUpdate.as_view(), name='templatestaticpages_edit'),
    url(r'^templatestaticpages/(?P<pk>\w+)/editmodal$', TemplateStaticPageUpdateModal.as_view(), name='templatestaticpages_editmodal'),
    url(r'^templatestaticpages/(?P<pk>\w+)/delete$', TemplateStaticPageDelete.as_view(), name='templatestaticpages_delete'),
    url(r'^templatestaticpages/foreign/(?P<search>[\w\W]+|\*)$', TemplateStaticPageForeign.as_view(), name='CDNX_cms_templatestaticpage_foreign'),
]
