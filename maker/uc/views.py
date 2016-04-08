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

from uc.models import Account

# This is just a HTML FORM wrapper, not related with
# django's user models or user-defined models at all
class AccountForm(forms.Form):
    user_name = forms.CharField(label='用户名/EMail:', max_length=30)
    password = forms.CharField(label='密码:', widget = forms.PasswordInput())

###################################################################################
def _save_user_code(name, code):
    try:
        obj = Account()
        obj.user_name = name;
        obj.save()
# Next try retrieve the DB's id...
        o = Account.objects.get(user_name = name)
        if o != None:
            obj_id = o.id
            print 'the %s <======> %d' %(name, obj_id)
            themd5 = hashlib.md5()
            # DO NOT change below decoration string!
            plain_data = '%d+ %s' %(obj_id, code)
            themd5.update(plain_data)
            o.password = themd5.hexdigest()
            o.save() # save it again!
    except:
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        print info

    return 0

###################################################################################
# return 0 means OK, otherwise password or name not match
def _verify_user_code(name, code):
    ok = -1
    try:
# Next try retrieve the DB's id...
        o = Account.objects.filter(user_name = name)
        if len(o) >= 1:
            obj_id = o[0].id
            print 'the %s <======> %d' %(name, obj_id)
            themd5 = hashlib.md5()
            # DO NOT change below decoration string!
            plain_data = '%d+ %s' %(obj_id, code)
            themd5.update(plain_data)
            cipher_data = themd5.hexdigest()
            if cipher_data == o[0].password:
                print 'BINGO~~'
                ok = 0
    except:
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        print info

    return ok

def _is_user_existed(name):
    existed = 0
    o = Account.objects.filter(user_name = name)
    if len(o) > 0:
        print 'Oh, this user already existed in DB'
        existed = 1

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
    return render_to_response('uc_home.html')
