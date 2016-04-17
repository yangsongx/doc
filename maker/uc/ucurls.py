
from django.conf.urls import include, url
from django.contrib.auth.views import login, logout

import uc.views
from uc.views import CorpusListView
from uc.forms import EditProfileForm

urlpatterns = [
    url(r'^apiCheckExistence/$', uc.views.uc_apiCheckExistence, name='checkExistence'), # Using Django >= 1.9 style ^_^
    url(r'^apiListCustCorpus/$', uc.views.uc_apiListCustCorpus, name = 'apiListCustCorpus'),
    url(r'^apiListRobot/$', uc.views.uc_apiListRobot, name = 'apiListRobot'),
    url(r'^apiDelRobot/$', uc.views.uc_apiDelRobot, name = 'apiDelRobot'),
    url(r'^reg/$', uc.views.uc_reg, name = 'uc_reg'),
    url(r'^login/$', uc.views.uc_login, name = 'uc_login'),
    url(r'^logout/$', uc.views.uc_logout, name = 'uc_logout'),
    url(r'^changePwd/$', uc.views.uc_changePwd, name='changePwd'),
    url(r'^personalcenter/$', uc.views.uc_pcenter, name='personalcenter'),
    url(r'^createbot/$', uc.views.uc_createbot, name='create_bot'),
    url(r'^setbot/$', uc.views.uc_setbot, name='set_bot'),
    #url(r'^corpusdef/$', uc.views.uc_corpusdef, name='corpus_def'),
    url(r'^corpusdef/$',  CorpusListView.as_view(template_name='uc_corpus_def.html'), name='corpus_def'),
    url(r'^funconfig/$', uc.views.uc_funconfig, name='func_config'),
    url(r'^whitelist/$', uc.views.uc_whitelist, name='white_list'),
    url(r'^basicinfo/$', uc.views.uc_basicinfo, name='basic_info'),
    # url(r'^basicinfo/$', 'uc.views.uc_basicinfo',  {'edit_profile_form': EditProfileForm, \
    #     'template_name':'uc_basic_info.html','success_url':'basic_info'}, name='basic_info'),
    url(r'^systemnotify/$', uc.views.uc_systemnotify, name='system_notify'),
    url(r'^sitemsg/$', uc.views.uc_sitemsg, name='site_msg'),
    url(r'^wxbot/start/$', uc.views.startWxBot, name='startWxBot'),
    url(r'^wxbot/stop/$', uc.views.stopWxBot, name='stopWxBot'),
    url(r'^wxbot/getlog/$',uc.views.getWxBotLog, name='getWxBotLog'),
    url(r'^wxbot/getqr/$', uc.views.getQR, name='getWxQR'),
    url(r'^wxbot/getstatus/$', uc.views.getWxBotStatus, name='getWxBotStatus'),
]
