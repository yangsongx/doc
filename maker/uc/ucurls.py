
from django.conf.urls import include, url
from django.contrib.auth.views import login, logout

import uc.views

urlpatterns = [
    url(r'^apiListRobot/$', uc.views.uc_apiListRobot, name = 'apiListRobot'),
    url(r'^apiDelRobot/$', uc.views.uc_apiDelRobot, name = 'apiDelRobot'),
    url(r'^reg/$', uc.views.uc_reg, name = 'uc_reg'),
    url(r'^login/$', uc.views.uc_login, name = 'uc_login'),
    url(r'^logout/$', uc.views.uc_logout, name = 'uc_logout'),
    url(r'^checkExistence/$', uc.views.uc_checkExistence, name='checkExistence'), # Using Django >= 1.9 style ^_^
    url(r'^changePwd/$', uc.views.uc_changePwd, name='changePwd'),
    url(r'^personalcenter/$', uc.views.uc_pcenter, name='personalcenter'),
    url(r'^createbot/$', uc.views.uc_createbot, name='create_bot'),
    url(r'^setbot/$', uc.views.uc_setbot, name='set_bot'),
    url(r'^corpusdef/$', uc.views.uc_corpusdef, name='corpus_def'),
    url(r'^funconfig/$', uc.views.uc_funconfig, name='func_config'),
    url(r'^whitelist/$', uc.views.uc_whitelist, name='white_list'),
    url(r'^basicinfo/$', uc.views.uc_basicinfo, name='basic_info'),
    url(r'^systemnotify/$', uc.views.uc_systemnotify, name='system_notify'),
    url(r'^sitemsg/$', uc.views.uc_sitemsg, name='site_msg'),
]
