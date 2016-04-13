#coding:utf-8

import hashlib
import json
import re
import sys
import uuid

from django import forms
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse,HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext

from models import AccountProfile, RobotType


# This is just a HTML FORM wrapper, not related with
# django's user models or user-defined models at all
class AccountForm(forms.Form):
    user_name = forms.CharField(label='用户名/EMail:', max_length=30)
    password = forms.CharField(label='密码:', widget = forms.PasswordInput())

###################################################################################
# return 1 means @email is a valid text value
def is_valid_email(email):
    valid = re.match('\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*',
            email)

    if valid != None:
        return 1
    else:
        return 0

###################################################################################
# return 0 means OK, otherwise password or name not match
def _is_user_existed(name):
    existed = 1
    print 'TODO , you need implement the code here'
    return existed

###################################################################################
def send_activation_mail(httphost, email):
    ticket = uuid.uuid1()
    full_url = '%s/uc/reg/?ticket=%s&user=%s' \
               %(httphost, ticket, email)
    print 'the url:%s' %(full_url)

    if re.search(r'^http://', full_url) == None:
        full_url = 'http://%s' %(full_url)

    # NOTE - below text are stolen from doueban's registration...
    mail_title = '请激活您的帐号，完成注册'
    mail_body = '欢迎来到Robotdocker世界，请点击下面链接完成注册:\n%s\n\n如果以上链接无法点击，请将上面的地址复制到你的浏览器(如IE)的地址栏进入' \
                %(u''.join(full_url).encode('utf-8'))
    print mail_body

    print 'sending with send_mail...'
    ret = send_mail(mail_title, # Subject
            mail_body, #message
            'help@robotdocker.com', # from email
            [email], #recipient list
            fail_silently=False)
    print 'finished with'
    print ret

    return ticket

###################################################################################
def activate_email_account(ticket, email):
    ret = -1
    try:
        obj = User.objects.filter(username = email)
        if len(obj) > 0:
            uid = obj[0].id
            prof_obj = AccountProfile.objects.get(user_id = uid)
            if prof_obj.mail_act == ticket:
                print 'Wow, this is GOOD MAIL activation'
                obj[0].is_active = 1
                obj[0].save()
                ret = 0
            else:
                print 'SHIT'

    except:
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        print info


    if ret == 0:
        return HttpResponse('TODO - UI for mail activation OK')
    else:
        return HttpResponse('TODO - UI for mail activation NOT OK')

###################################################################################
def create_robot(post_form, user):
    print 'TODO code, will add in the future'
    r_obj = RobotType(rob_sex = post_form['robotsettings.gender'],
            rob_alias = post_form['robotsettings.nickname'] )
    r_obj.save()

    a_obj = AccountProfile(user_id = user.id,
            robot_id = r_obj)
    a_obj.save()

    return 0

###################################################################################
def set_robot_info(post_form, uid):
    print 'TODO code, will add in the future'
    return 0

###################################################################################
def uc_apiListRobot(request):
    ret = {}
    ret['code'] = 0

    try:
        if request.method == 'POST':
            js_data = json.loads(request.body)
            usr_profile = AccountProfile.objects.filter(user_id = js_data['userid'])
            i = 1
            tmp = []
            for it in usr_profile:
                item = {}
                print 'got the new item'
                robj = RobotType.objects.get(id=it.robot_id_id)
                item['index'] = i
                item['name'] = robj.rob_alias
                item['gender'] = robj.rob_sex
                item['create'] = str(robj.rob_creation)

                tmp.append(item)
                i += 1

            ret['list'] = tmp
    except:
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        ret['code'] = -1
        ret['msg'] = info

    return HttpResponse(json.dumps(ret))

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
            if is_valid_email(name) == 1:
                print 'This is an email, status SHOULD NOT active until user clicked ths url'
                ticket = send_activation_mail(request.META['HTTP_HOST'], name)
                obj = User.objects.create_user(
                        username = name,
                        password=passwd,
                        email = name,
                        is_active = 0)
                obj.save()
                obj = User.objects.get(username=name)
                uid = obj.id
                print 'the user id is %d' %(uid)
                prof_obj = AccountProfile(user_id = uid,
                        mail_act = ticket)
                prof_obj.save()
            else:
                print 'a normal user, can directly saving'
                # Now save the Data into DB...
                obj = User.objects.create_user(
                        username = name, password=passwd)

                obj.save()

            # TODO reg OK should NOT return below HTML UI
            return HttpResponse('TODO - UI : reg OK, you can login now.')
    else:
        ticket = request.GET.get('ticket')
        print ticket
        email = request.GET.get('user')
        print email
        if ticket != None and email != None:
            return activate_email_account(
                    ticket,
                    email)
        else:
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
                    return HttpResponse('TOOD-UI You need activate your account!')
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
                # Note - for already login, just redirect to Usercenter
                return HttpResponseRedirect('/uc/personalcenter/')

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
        "cur": u"l_09",
        }, context_instance=RequestContext(request))

@login_required
def uc_createbot(request):
    if request.method == 'POST':
        print 'Will creating...'
        try:
            create_robot(request.POST, request.user)
        except:
            info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
            print info # FIXME - currently I just log the exception

        return HttpResponse('TODO UI - Robert Creation [Successfully]- Try Start it somewhere!')

    else:
        print 'just GET'
        return render_to_response('uc_create_bot.html', {
            "cur": u"l_01",
            }, context_instance=RequestContext(request))

@login_required
def uc_setbot(request):
    if request.method == 'POST':
        try:
            print 'POST, get data'
            print request.POST
            post_data = request.POST
            print post_data['robotsettings.age'] # TODO - all FORM fields
            print 'the user are'
            print request.user
            print request.user.id
            set_robot_info(post_data, request.user.id)
        except:
            info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
            print info # FIXME - currently I just log the exception

        return HttpResponse('TODO UI - Robert Setting [Successfully]!')

    else:
        print 'a GET'
        return render_to_response('uc_set_bot.html', {
            "cur": u"l_02",
            }, context_instance=RequestContext(request))

@login_required
def uc_corpusdef(request):
    return render_to_response('uc_corpus_def.html', {
        "cur": u"l_03",
        }, context_instance=RequestContext(request))

@login_required
def uc_funconfig(request):
    return render_to_response('uc_func_config.html', {
        "cur": u"l_04",
        }, context_instance=RequestContext(request))

@login_required
def uc_whitelist(request):
    return render_to_response('uc_white_list.html', {
        "cur": u"l_05",
        }, context_instance=RequestContext(request))

@login_required
def uc_basicinfo(request):
    return render_to_response('uc_basic_info.html', {
        "cur": u"l_06",
        }, context_instance=RequestContext(request))

@login_required
def uc_systemnotify(request):
    return render_to_response('uc_system_notify.html', {
        "cur": u"l_07",
        }, context_instance=RequestContext(request))

@login_required
def uc_sitemsg(request):
    return render_to_response('uc_site_msg.html', {
        "cur": u"l_08",
        }, context_instance=RequestContext(request))
