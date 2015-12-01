from django.shortcuts import render
from models import Account
from django.contrib.auth.models import User
from django.http import HttpResponse

# Create your views here.
def do_reg(request):
# NOTE - can't use User(username='xx', password='yy'), which, password
# would use plain-text value
    a = User.objects.get(id=9)
    print a
    a.get_profile()
#    c = User.get_profile()
#    c = request.user.get_profile()
    print a.get_profile()
#c.user_type = 3;
    return HttpResponse('good')
