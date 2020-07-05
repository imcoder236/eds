from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Permission
from django.core.mail import EmailMessage
import string
import random
import datetime
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

                request.session['name'] = user.first_name +" "+user.last_name
                # request.session['user_type'] = user.permission_id
                userreport=user_report()
                userreport.in_time = datetime.datetime.now()
                userreport.userid_id=user.id
                userreport.save()
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

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                user = User.objects.filter(username=request.POST['Username'])[0]
                request.session['id'] = user.id
                request.session['name'] = user.first_name +" "+user.last_name
                request.session['username'] = user.username
                request.session['email'] = user.email
                userreport=user_report()
                userreport.in_time = datetime.datetime.now()
                userreport.userid_id=user.id
                userreport.save()
                request.session['user_login_id'] =userreport.id
                return redirect('../Admin/Dashboard')
            else:
                return render(request,'admin/index.html',{'inactive':'false'})
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return render(request,'admin/index.html',{'fail':'false'})
    else:
        return render(request, 'index.html', {})

def get_random_alphaNumeric_string(stringLength=8):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))

def forgot_pass(request):
    reset1=request.POST.get('reset_mail')
    userdetails = User.objects.filter(username=request.POST.get('Username'))[0]
    reset_email = userdetails.email
    uid = userdetails.id
    if reset1 == reset_email:
        random_pass=get_random_alphaNumeric_string(12)
        user_acc =User.objects.get(username=request.POST.get('Username'))
        user_acc.set_password(random_pass)
        user_acc.save()
        mail='<h3>Hello {},</h3>&emsp;&emsp;&emsp;Your new password is <b>{}</b> . <br><br> ThankYou'.format(userdetails.first_name,random_pass);
        email = EmailMessage('New Password', mail, to=[reset1])
        email.content_subtype = "html"
        email.send()
        change_passwd = passwd()
        change_passwd.user_id = uid
        change_passwd.username = request.POST.get('Username')
        change_passwd.umail = reset1
        change_passwd.date = datetime.datetime.now()
        change_passwd.save()
    else:
         return HttpResponse("<script>alert('Email ID mismatched. Enter correct email address to request new password'); windows.location.href('/');</script>")
    return redirect('/')

class passwd(models.Model):
    user_id = models.CharField(max_length = 50,null=True)
    username = models.CharField(max_length = 50,null=True)
    umail = models.CharField(max_length = 50,null=True)
    date = models.DateTimeField(null=True)

def main_page(request):
    if request.session:
        return render(request,"index.html",{'user_type':request.session['user_type']})
    else:
        return redirect("logout")

def logout(request):
    try:
        user_report.objects.filter(userid_id=request.session['id']).update(out_time= datetime.datetime.now())
        request.session.flush()
        return redirect('/')
    except:
        print("Host Machine Diconnected")
        return redirect('/')

def startup(request):
    return render(request,"startup/index.html",{'user_type':request.session['user_type']});

def invest(request):
    return render(request,"invest/index.html",{'user_type':request.session['user_type']});

def dashboard(request):
    return render(request,"admin/dashboard.html",{});
