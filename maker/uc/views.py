#encoding=utf-8

import hashlib
import json
import sys
from django import forms
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext


# This is just a HTML FORM wrapper, not related with
# django's user models or user-defined models at all
class AccountForm(forms.Form):
    user_name = forms.CharField(label='用户名/EMail:', max_length=30)
    password = forms.CharField(label='密码:', widget = forms.PasswordInput())

###################################################################################

###################################################################################
# return 0 means OK, otherwise password or name not match
def _is_user_existed(name):
    existed = 1
    print 'TODO , you need implement the code here'
    return existed
#
# Create your views here.

###################################################################################
# Signup(Registration)
def uc_reg(request):
    if request.method == 'POST':
        print 'POST'
        usr = AccountForm(request.POST)
        if usr.is_valid():
            name = usr.cleaned_data['user_name']
            passwd = usr.cleaned_data['password']
            print name
            print passwd
            # Now save the Data into DB...
            obj = User.objects.create_user(name, password=passwd)
            obj.save()
            # TODO reg OK should NOT return below HTML UI
            return render_to_response('uc_home.html')
    else:
        print 'GET'
        usr = AccountForm()
    return render_to_response('reg.html', {'user':usr})
###################################################################################
# Signin(Login)
def uc_login(request):

    if request.method == 'POST':
        print 'POST method'
        usr = AccountForm(request.POST)
        if usr.is_valid():
            name = usr.cleaned_data['user_name']
            passwd = usr.cleaned_data['password']
            print name
            print passwd
            ret = authenticate(username=name, password=passwd)

            if ret != None:
                print 'passwd pass'
                print ret
                if ret.is_active:
                    login(request, ret) # Note - This will auto-add session by django
                    print request.session.keys()
                    print request.session.get('_auth_user_id')
                    redirect_to = request.POST.get(REDIRECT_FIELD_NAME,
                            request.GET.get(REDIRECT_FIELD_NAME, ''))
                    print 'this is contained redirected URL, redirect_to len:%d' %(len(redirect_to))
                    if len(redirect_to) != 0:
                        return redirect(redirect_to)
                    else:
                        #FIXME - currently, login would lead user to the center panel
                        return redirect('/uc/personalcenter/')
            else:
                print 'Failed case!'
                return HttpResponse('TODO- failed login')

    else:
        print 'GET method'
        u = request.user
        if u != None:
            print u
            if u.is_authenticated():
                print 'Wow, you already logedin'
                return HttpResponse('TODO ALREADY LOGIN UI')

        usr = AccountForm()

    return render_to_response('login.html',{'user': usr})

###################################################################################
# Sign Off(Logout)
def uc_logout(request):
    logout(request) # just call django's own framework API
    return HttpResponse('TODO, need a sign off UI page here')

###################################################################################
# Check if the user already existed or NOT
#
def uc_checkExistence(request):
    ret = {}
    ret['code'] = 0

    try:
        if request.method == 'POST':
            js_data = json.loads(request.body)
            name = js_data['name']
            if _is_user_existed(name) == 1:
                ret['code'] = 1
        else:
            ret['code'] = 1
            ret['msg'] = 'Only support POST'
    except:
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        ret['code'] = -1
        ret['msg'] = info

    return HttpResponse(json.dumps(ret))
###################################################################################
def uc_changePwd(request):
    ret = {}
    ret['code'] = 0

    try:
        print 'code not completed YET, dependent on UI design'
    except:
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        ret['code'] = -1
        ret['msg'] = info

    return HttpResponse(json.dumps(ret))

    ###################################################################################
# Personalcenter(Login)
@login_required
def uc_pcenter(request):
    return render_to_response('uc_home.html', {
        "cur": u"l_08",
        }, context_instance=RequestContext(request))

@login_required
def uc_createbot(request):
    return render_to_response('uc_create_bot.html', {
        "cur": u"l_01",
        }, context_instance=RequestContext(request))

@login_required
def uc_corpusdef(request):
    return render_to_response('uc_corpus_def.html', {
        "cur": u"l_02",
        }, context_instance=RequestContext(request))

@login_required
def uc_funconfig(request):
    return render_to_response('uc_func_config.html', {
        "cur": u"l_03",
        }, context_instance=RequestContext(request))

@login_required
def uc_whitelist(request):
    return render_to_response('uc_white_list.html', {
        "cur": u"l_04",
        }, context_instance=RequestContext(request))

@login_required
def uc_basicinfo(request):
    return render_to_response('uc_basic_info.html', {
        "cur": u"l_05",
        }, context_instance=RequestContext(request))

@login_required
def uc_systemnotify(request):
    return render_to_response('uc_system_notify.html', {
        "cur": u"l_06",
        }, context_instance=RequestContext(request))

@login_required
def uc_sitemsg(request):
    return render_to_response('uc_site_msg.html', {
        "cur": u"l_07",
        }, context_instance=RequestContext(request))
