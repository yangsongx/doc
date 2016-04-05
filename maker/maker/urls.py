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

urlpatterns = [
    url(r'^$', 'webviews.views.maker_index', name='home'),
    #url(r'^accounts/login/$', 'cas.views.login', name='login'),
    #url(r'^accounts/logout/$', 'cas.views.logout', name='logout'),
    #url(r'^$', 'webviews.views.test_login', name='login'),
    url(r'^login/$', 'webviews.views.test_login', name='login'),
    url(r'^start/$', 'webviews.views.maker_index', name='home'),
    url(r'^cas_response/$', 'webviews.views.cas_response', name='login'),
    url(r'^accounts/logout/$', 'cas.views.logout', name='logout'),
    url(r'^start/$', 'webviews.views.maker_index', name='home'),
    url(r'^cas_response/$', 'webviews.views.cas_response', name='login'),
    url(r'^pyb/$', 'webviews.views.pyb_index', name='pyb_test'),
    url(r'^add/$', 'webviews.views.pyb_add', name='add'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    #WEB API interface
    url(r'^(?P<api_ver>v\d+)/$', 'webviews.views.do_index', name='do_index'),
    url(r'^(?P<api_ver>v\d+)/maker/begin/$', 'webviews.views.do_begin', name='begin'),
    url(r'^(?P<api_ver>v\d+)/maker/uptoken/$', 'webviews.views.do_uptoken', name='uptoken'),
    url(r'^(?P<api_ver>v\d+)/maker/uptoken2/$', 'webviews.views.do_uptoken2', name='uptoken2'),
    url(r'^(?P<api_ver>v\d+)/maker/uploadall/$', 'webviews.views.do_upload_all', name='uploadall'),
    url(r'^(?P<api_ver>v\d+)/maker/down/$', 'webviews.views.do_down', name='down'),
    url(r'^(?P<api_ver>v\d+)/maker/finish/$', 'webviews.views.do_finish', name='finish'),
    url(r'^(?P<api_ver>v\d+)/maker/association/$', 'webviews.views.do_association', name='association'),
    url(r'^(?P<api_ver>v\d+)/maker/verifyphone/$', 'webviews.views.do_verifyphone', name='verifyphone'),
    url(r'^(?P<api_ver>v\d+)/maker/welcome/$', 'webviews.views.do_welcome', name='welcome'),
    url(r'^(?P<api_ver>v\d+)/maker/checkpackages/$', 'webviews.views.do_checkpackages', name='checkpackages'),
    url(r'^(?P<api_ver>v\d+)/maker/help/$', 'webviews.views.do_help', name='help'),
    url(r'^(?P<api_ver>v\d+)/maker/feedback/$', 'webviews.views.do_feedback', name='feedback'),
    url(r'^(?P<api_ver>v\d+)/maker/getmypackages/$', 'webviews.views.do_getmypackages', name='getmypackages'),
    url(r'^(?P<api_ver>v\d+)/maker/getappdetail/$', 'webviews.views.do_getappdetail',name='getappdetail'),
    url(r'^(?P<api_ver>v\d+)/maker/notify_result/$', 'webviews.views.do_notify_result',name='notify_result'),
    url(r'^(?P<api_ver>v\d+)/maker/retrieve/$', 'webviews.views.do_retrieve', name='retrieve'),
    url(r'^(?P<api_ver>v\d+)/maker/unlink/$', 'webviews.views.do_unlink', name='unlink'),

    #WEB API for app
    url(r'^feedback', 'webviews.views4app.feedback4app',name='feedback4app'),
    url(r'^(?P<api_ver>v\d+)/maker/preview/(?P<mid_hash>[a-z\d]{32})/$','webviews.views4app.preview_wap', name='preview_wap'),
    url(r'^(?P<api_ver>v\d+)/rom/nav/$', 'webviews.views4app.show_navigation', name='show_navigation'),
    url(r'^(?P<api_ver>v\d+)/getappinfo/(?P<package>.+)/$', 'webviews.views.getappinfo', name='getappinfo'),

    #WEB for CMS
    url(r'^cmsupload','webviews.views.cmsupload',name='cmsupload'),

    # WEB HTML sections...
    url(r'^(?P<api_ver>v\d+)/maker/cust/welcome/$', 'webviews.views.cust_welcome',name='cust_welcome'),
    url(r'^(?P<api_ver>v\d+)/maker/cust/model/$', 'webviews.views.cust_model',name='cust_model'),
    url(r'^(?P<api_ver>v\d+)/maker/cust/animation/$', 'webviews.views.cust_animation',name='cust_animation'),
    url(r'^(?P<api_ver>v\d+)/maker/cust/app/$', 'webviews.views.cust_app',name='cust_app'),
    url(r'^(?P<api_ver>v\d+)/maker/cust/ringtone_call/$', 'webviews.views.cust_ringtone_call',name='cust_ringtone_call'),
    url(r'^(?P<api_ver>v\d+)/maker/cust/wallpaper_lock/$', 'webviews.views.cust_wallpaper_lock',name='cust_wallpaper_lock'),
    url(r'^(?P<api_ver>v\d+)/maker/cust/wallpaper_head/$', 'webviews.views.cust_wallpaper_head',name='cust_wallpaper_lock'),
    url(r'^(?P<api_ver>v\d+)/maker/cust/ringtone_boot/$', 'webviews.views.cust_ringtone_boot',name='cust_ringtone_boot'),
    url(r'^(?P<api_ver>v\d+)/maker/cust/submit/$', 'webviews.views.cust_submit',name='cust_submit'),
]

if settings.DEBUG is False:
    urlpatterns += [ url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),]

#handler404 = 'webviews.views.my_404'
#handler500 = 'webviews.views.my_500'

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

