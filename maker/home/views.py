import hashlib
import json
import re
import sys
import uuid

from django import forms
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse,HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext

def aboutUs(request):
    return render_to_response('home_about.html', {
        }, context_instance=RequestContext(request))

def showService(request):
    return render_to_response('home_service.html', {
        }, context_instance=RequestContext(request))

def showBlogs(request):
    return render_to_response('home_blogs.html', {
        }, context_instance=RequestContext(request))

def showPortfolio(request):
    return render_to_response('home_portfolio.html', {
        }, context_instance=RequestContext(request))