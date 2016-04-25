#coding:utf-8

import hashlib
import json
import re
import sys
import uuid
import os
import md5
from django import forms
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpRequest, HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView
from django.http import Http404, HttpResponseRedirect

from forms import EditProfileForm,CorpusForm,RobotInfoForm
import logging
from models import AccountProfile, Robot, CorpusData
from maker.views import ExtraContextTemplateView

logger = logging.getLogger('uc')

# TODO [2016-04-14 This class will be obsoleted soon, we can directly
# use the HTML's FORM data.
#
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
# return 1 means user already existed in DB
def _is_user_existed(name):
    existed = 0
    try:
        obj = User.objects.get(username = name, is_active=1)
        existed = 1
    except ObjectDoesNotExist:
        info = "+%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        print info

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
            'help@botdocker.com', # from email
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
        # return HttpResponse('TODO - UI for mail activation OK')
        return render_to_response('regfail.html',{'user': usr})
    else:
        # return HttpResponse('TODO - UI for mail activation NOT OK')
        return render_to_response('regfail.html')

###################################################################################
def create_robot(post_form, user):
    print 'TODO code, will add in the future'

#r_obj = Robot(rob_sex = post_form['robotsettings.gender'],
#           rob_alias = post_form['robotsettings.nickname'],
#           owner = user)
#   TODO - just stub code
    r_obj = Robot(rob_sex = 1,
                rob_alias = 'debug',
                owner = user)
    r_obj.save()

    return 0


###################################################################################
def set_corpus_info(post_form, user):
    print 'will add  corpus data in the DB'

    c_obj = CorpusData(
            question = post_form['corpus.question'],
            answer = post_form['corpus.answer'],
            owner = user)
    c_obj.save()

    return 0

###################################################################################
def uc_apiListRobot(request):
    ret = {}
    ret['code'] = 0

    try:
        if request.method == 'POST':
            js_data = json.loads(request.body)
            uid = js_data['userid']

            rob = Robot.objects.filter(owner_id = uid)
            print '%d ==> %d robots' %(uid, len(rob))

            i = 1
            tmp = []

            for it in rob:
                print 'go'
                item = {}
                item['index'] = i
                item['name'] = it.rob_alias
                item['create'] = str(it.rob_creation)
                tmp.append(item)
                i += 1

            ret['list'] = tmp
    except:
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        ret['code'] = -1
        ret['msg'] = info

    return HttpResponse(json.dumps(ret))

###################################################################################
def uc_apiDelRobot(request):
    ret = {}
    ret['code'] = 0

    try:
        if request.method == 'POST':
            js_data = json.loads(request.body)
            print 'need code to remove the DB entry(%d -> %d)' \
                %(js_data['userid'], js_data['robid'])
            obj = AccountProfile.objects.get(
                    user_id = js_data['userid'],
                    robot_id_id = js_data['robid']
                    )
            print 'got this one, delete it with associate robot'
            r_obj = Robot.objects.get(id=obj.robot_id_id)

            r_obj.delete()
            obj.delete()

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
            return render_to_response('regok.html', {'user':usr})
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
                    # return HttpResponse('TOOD-UI You need activate your account!')
                    return render_to_response('loginfailforneedactive.html', {'user':usr})
            else:
                print 'Failed case!'
                return render_to_response('loginfail.html', {'user':usr})
                # return HttpResponse('TODO- failed login')

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
    return render_to_response('redirect.html', {
        "title": u"退出中...",
        "url": "/",
        #"url": "http://bot.ioniconline.com/",
        }, context_instance=RequestContext(request))

###################################################################################
def uc_apiListCustCorpus(request):
    ret = {}
    ret['code'] = 0

    try:
        print 'code not completed YET, dependent on UI design'
        js_data = json.loads(request.body)
        uid = js_data['userid']

        c_obj = CorpusData.objects.filter(owner_id = uid)

        i = 1
        tmp = []
        for it in c_obj:
            item = {}
            item['index'] = i
            item['q'] = it.question
            item['a'] = it.answer
            i += 1

            tmp.append(item)

        ret['list'] = tmp


    except:
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        ret['code'] = -1
        ret['msg'] = info

    return HttpResponse(json.dumps(ret))

###################################################################################
# Check if the user already existed or NOT
#
def uc_apiCheckExistence(request):
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
        "user_name": request.user.username,
        "join_since":str(request.user.date_joined)
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
            "user_name": request.user.username,
            }, context_instance=RequestContext(request))

@login_required
def uc_setbot(request, theform = RobotInfoForm):
    robj = None

    try:
        robj = Robot.objects.get(owner = request.user)
    except ObjectDoesNotExist:
        # make sure exsited one robot
        robj = Robot(rob_alias = 'default', owner = request.user)
        robj.save()
    except:
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        print info


    if request.method == 'POST':
        try:
            print 'POST, get data'
            form = theform(request.POST, request.FILES,
                    instance = robj, initial={})
            if form.is_valid():
                form.save()

        except:
            info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
            print info # FIXME - currently I just log the exception

    else:
        print 'a GET'
        form = theform(instance=robj, initial={})

    return render_to_response('uc_set_bot.html', {
            "form": form,
            "user_name": request.user.username,
            }, context_instance=RequestContext(request))


@login_required
def uc_funconfig(request):
    return render_to_response('uc_func_config.html', {
        "user_name": request.user.username,
        }, context_instance=RequestContext(request))

@login_required
def uc_whitelist(request):
    return render_to_response('uc_white_list.html', {
        "user_name": request.user.username,
        }, context_instance=RequestContext(request))

@login_required
def uc_basicinfo(request, edit_profile_form=EditProfileForm):
    personal_user = None
    try:
        print request.user
        personal_user = AccountProfile.objects.get(user = request.user)

    except:
        # FIXME - I suppose exception only happen for not existed case
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        print info
        personal_user = AccountProfile(user = request.user,
                mail_act = 'blank')
        personal_user.save()

    form = edit_profile_form(instance = personal_user,initial={})

    if request.method == 'POST':
        form = edit_profile_form(request.POST, request.FILES, instance=personal_user,
                                 initial={})

        if form.is_valid():
             form.save()
        else :
             print form

    return render_to_response('uc_basic_info.html',
                { 
                    'form': form,
                     "user_name": request.user.username,
                    }, context_instance=RequestContext(request))

@login_required
def uc_systemnotify(request):
    return render_to_response('uc_system_notify.html', {
        "user_name": request.user.username,
        }, context_instance=RequestContext(request))

@login_required
def uc_sitemsg(request):
    return render_to_response('uc_site_msg.html', {
        "user_name": request.user.username,
        }, context_instance=RequestContext(request))

# TODO - below util is un-necessary
def get_account_user(user):
    personal_user = None
    try:
        logger.debug(user.id )
        # personal_user = AccountProfile.objects.get(user__exact = user.id )
        personal_user = AccountProfile.objects.get(user_id =  user.id)
    except:
         print 'personal_user.except'
         pass
    else:
         pass

    return personal_user

@login_required
def startWxBot(request):
    data = {}
    sid = request.user.id
    rc = os.system("python ./wxctl.py start %s"%sid)
    rc = rc >> 8
    if rc == 0:
        data['rc'] = 0
        data['desp'] = "sucess"
    elif rc == 1:
        data['rc'] = 1
        data['desp'] = "existing"
    else:
        data['rc'] = 2
        data['desp'] = "failed to start"

    return HttpResponse(json.dumps(data), content_type="application/json")

@login_required
def stopWxBot(request):
    data = {}
    sid = request.user.id
    rc = os.system("python ./wxctl.py stop %s"%sid)
    rc = rc >> 8
    if rc == 0:
        data['rc'] = 0
        data['desp'] = "sucess"
    elif rc == 1:
        data['rc'] = 1
        data['desp'] = "not started before"
    else:
        data['rc'] = 2
        data['desp'] = "failed to stop"

    return HttpResponse(json.dumps(data), content_type="application/json")

def get_md5(full_filename):
    f = file(full_filename, 'rb')
    return md5.new(f.read()).hexdigest()

@login_required
def getQR(request):
    sid = request.user.id
    data = {}
    path1 = "./out/%s/qr.png"%sid
    if os.path.exists(path1):
        val = get_md5(path1)
        os.system("cp %s ./static/images/qr/%s.png"%(path1, val))
        data['rc'] = 0
        data['url'] = "/static/images/qr/%s.png"%val
    else:
        data['rc'] = 1
        data['url'] = ""
    return HttpResponse(json.dumps(data), content_type="application/json")

@login_required
def getWxBotLog(request):
    sid = request.user.id
    rc = os.system("tail -n 20 out/%s/log.txt > out/%s/log2.txt"%(sid,sid))
    text = ""
    with open("out/%s/log2.txt"%sid) as f:
        for it in f.readlines():
            it = it.replace('\n','</br>')
            text += it

    data = {}
    data['rc'] = 0
    data['desp'] = text
    return HttpResponse(json.dumps(data), content_type="application/json")

@login_required
def getWxBotStatus(request):
    sid = request.user.id
    print sid
    data = {}
    rc = os.system("python ./wxctl.py status %s"%sid)
    rc = rc >> 8
    if int(rc) == 0:
        data['rc'] = 0
        data['desp'] = "stop"
    elif rc == 1:
        data['rc'] = 1
        data['desp'] = "wait"
    elif rc == 2:
        data['rc'] = 2
        data['desp'] = "login"
    else:
        data['rc'] = rc
        data['desp'] = "failed"

    return HttpResponse(json.dumps(data), content_type="application/json")

class CorpusListView(ListView):
    model = CorpusData
    template_name = 'uc_corpus_list.html'
    paginate_by = settings.PAGINATE_NUMBER
    context_object_name = 'obj_list'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CorpusListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CorpusListView, self).get_context_data(**kwargs)
        context['page'] = self.request.GET.get('page', '0')
        context['form'] = CorpusForm()
        context['user_name'] = self.request.user.username

        return context

    def get_queryset(self):

        obj_list =  CorpusData.objects.all().order_by('-id')
        logger.debug('get_queryset')
        return obj_list

    def post(self, request, *args, **kwargs):

        form = CorpusForm()
        extra_context = dict()
        if request.method == 'POST':
            # try:
            # TODO - how to handle the robot under a user?
            form = CorpusForm(request.POST)
            if form.is_valid():
                personal_user = get_account_user(request.user)
                if personal_user is None:
                    raise Http404("用户不存在")
                #set_corpus_info(request.POST, personal_user)
                logger.debug('form.save personal_user')
                form.save(personal_user);
                extra_context['success'] = 'yes'
                return redirect(reverse('corpus_list'))

            # except:
            #     info = "(corpusdef) %s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
            #     print info # FIXME - currently I just log the exception

        extra_context['obj_list'] = self.get_queryset()
        extra_context['form'] = CorpusForm()
        return ExtraContextTemplateView.as_view(template_name=self.template_name,
                                            extra_context=extra_context)(request)

def corpus_delete(request, next_url='corpus_list'):
    logger.debug('delete corpus ')
    if request.method == 'POST':
        idx = request.POST['id']
        result = ({'status':'ok'})
        if idx != None:
            try:
                 CorpusData.objects.get(id = int(idx)).delete()
            except Exception, e:
                logger.debug(u'%s'%e)
                result = ({'status':'error'})
        return JsonResponse(result)

    return redirect(reverse(next_url))

def corpus_edit(request,):
    logger.debug('edit corpus ')
    if request.method == 'POST':
        idx = request.POST['id']
        question = request.POST['question']
        answer = request.POST['answer']
        print question
        print answer
        result = ({'status':'ok'})
        if idx != None:
            try:
                 new_data = CorpusData.objects.get(id = int(idx))
                 new_data.question = question;
                 new_data.answer = answer;
                 new_data.save();
            except Exception, e:
                logger.debug(u'%s'%e)
                result = ({'status':'error'})
        return JsonResponse(result)
