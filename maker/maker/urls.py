"""maker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import settings
import webviews.views
import uc.views

urlpatterns = [
    url(r'^$', webviews.views.maker_index, name='home'),
    url(r'^admin/', include(admin.site.urls)),
#url(r'^grappelli/', include('grappelli.urls')),

    # WEB HTML sections...
    url(r'^(?P<api_ver>v\d+)/$', 'webviews.views.do_index', name='do_index'),

    # NOTE - All usercenter(uc) are under uc APP...
    url(r'^uc/', include('uc.ucurls')),
     url(r'^home/', include('home.urls')),

    url(r'^wxbot/start/(?P<sid>.+)/$', webviews.views.startWxBot, name='startWxBot'),
    url(r'^wxbot/stop/(?P<sid>.+)/$', webviews.views.stopWxBot, name='stopWxBot'),
    url(r'^wxbot/restart/(?P<sid>.+)/$', webviews.views.restartWxBot, name='restartWxBot'),
    url(r'^wxbot/getlog/(?P<sid>.+)/$',webviews.views.getWxBotLog, name='getWxBotLog'),
    url(r'^wxbot/getqr/(?P<sid>.+)/$', webviews.views.getQR, name='getWxQR'),
    url(r'^wxbot/getstatus/(?P<sid>.+)/$', webviews.views.getWxBotStatus, name='getWxBotStatus'),
    url(r'^dashboard/launcher/$', webviews.views.gotoDashboard, name='gotoDashboard'),

]

if settings.DEBUG is False:
    urlpatterns += [ url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),]

handler404 = 'webviews.views.my404'
handler500 = 'webviews.views.my500'

