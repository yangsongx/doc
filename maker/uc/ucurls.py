
from django.conf.urls import include, url

import uc.views

urlpatterns = [
    url(r'^checkExistence/$', uc.views.uc_checkExistence, name='checkExistence'),
    url(r'^changePwd/$', uc.views.uc_changePwd, name='changePwd'),
]
