
from django.conf.urls import include, url
from django.contrib.auth.views import login, logout

import uc.views

urlpatterns = [
    url(r'^reg/$', uc.views.uc_reg, name = 'uc_reg'),
    url(r'^login/$', uc.views.uc_login, name = 'uc_login'),
    url(r'^logout/$', uc.views.uc_logout, name = 'uc_logout'),
    url(r'^checkExistence/$', uc.views.uc_checkExistence, name='checkExistence'), # Using Django >= 1.9 style ^_^
    url(r'^changePwd/$', uc.views.uc_changePwd, name='changePwd'),
    url(r'^personalcenter/$', uc.views.uc_pcenter, name='personalcenter'),
]
