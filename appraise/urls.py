# -*- coding: utf-8 -*-
"""
Project: Appraise evaluation system
 Author: Christian Federmann <cfedermann@dfki.de>
"""
# pylint: disable-msg=W0611
from django.conf.urls.defaults import patterns, include, handler404, \
  handler500
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from appraise.settings import MEDIA_ROOT, DEBUG


admin.autodiscover()

urlpatterns = patterns('',
  (r'^appraise/$', 'appraise.views.frontpage'),

  (r'^appraise/login/$', 'appraise.views.login',
    {'template_name': 'login.html'}),

  (r'^appraise/logout/$', 'appraise.views.logout',
    {'next_page': '/appraise/'}),

  (r'^appraise/admin/', include(admin.site.urls)),

  (r'^appraise/evaluation/$', 'appraise.evaluation.views.overview'),

  (r'^appraise/evaluation/(?P<task_id>[a-f0-9]{32})/',
    'appraise.evaluation.views.task_handler'),

  (r'^appraise/status/$', 'appraise.evaluation.views.status_view'),

  (r'^appraise/status/(?P<task_id>[a-f0-9]{32})/',
    'appraise.evaluation.views.status_view'),

  (r'^appraise/export/(?P<task_id>[a-f0-9]{32})/',
    'appraise.evaluation.views.export_task_results'),

)

if DEBUG:
    urlpatterns += staticfiles_urlpatterns()
