from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
# Create your views here.
def user_login(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        password = request.GET.get('password')
        print(username+" "+password)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                user = User.objects.filter(username=username)[0]
                request.session['id'] = user.id
                request.session['name'] = user.first_name
                request.session['username'] = user.username
                # request.session['user_type'] = user.user_type
                request.session['user_type'] = 3
                return HttpResponse("done")
            else:
                return  HttpResponse("false")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("false")
    else:
        return render(request, 'index.html', {})
    return HttpResponse("true");

def main_page(request):
    if request.session:
        return render(request,"index.html",{'user_type':request.session['user_type']})
    else:
        return redirect("logout")

def logout(request):
    request.session.flush()
    return redirect('/')

def startup(request):
    return render(request,"startup/index.html",{'user_type':request.session['user_type']});

def invest(request):
    return render(request,"invest/index.html",{'user_type':request.session['user_type']});
