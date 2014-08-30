from django.contrib import auth
from django.http import *
import json
from cgi import parse_qs, escape

def login_view(request, username, password):
    #username = request.POST.get('username', '')
    #password = request.POST.get('password', '')
    username = escape(username)
    password = escape(password)
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        return HttpResponse(json.dumps([True]))
    else:
        # Show an error page
        return HttpResponse(json.dumps([False]))

def logout_view(request):
    try:
        auth.logout(request)
    	return HttpResponse(json.dumps([True]))
    except:
        return HttpResponse(json.dumps([False])) 
