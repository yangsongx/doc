#encoding=utf-8

import hashlib
import json
import sys
from django import forms
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, render_to_response

from uc.models import Account

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
def uc_signup(request):
    if request.method == 'POST':
        print 'POST'
        usr = AccountForm(request.POST)
        if usr.is_valid():
            name = usr.cleaned_data['user_name']
            passwd = usr.cleaned_data['password']
            print name
            print passwd
            # Now save the Data into DB...
            _save_user_code(name, passwd)
            return render_to_response('regok.html')
    else:
        print 'GET'
        usr = AccountForm()
    return render_to_response('reg.html', {'user':usr})
###################################################################################
# Signin(Login)
def uc_signin(request):
    if request.method == 'POST':
        print 'POST method'
        usr = AccountForm(request.POST)
        if usr.is_valid():
            name = usr.cleaned_data['user_name']
            passwd = usr.cleaned_data['password']
            print name
            print passwd
            ret = _verify_user_code(name, passwd)
            print 'the REDIC:'
            # TODO - login OK/fail SHOULD show in the LOGIN page?
            if ret == 0:
                return render_to_response('regok.html')
            else:
                return HttpResponse('FAILED, TODO- You need do this in login UI')
    else:
        print 'GET method'
        usr = AccountForm()

    return render_to_response('login.html',{'user': usr})

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
