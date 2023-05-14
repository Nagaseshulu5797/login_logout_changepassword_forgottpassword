from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from app.forms import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')

def restration(request):
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}

    if request.method=='POST' and request.FILES:
        ufd=UserForm(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)
        if ufd.is_valid() and pfd.is_valid():
            nsud=ufd.save(commit=False)
            nsud.set_password(ufd.cleaned_data['password'])
            nsud.save()

            nspd=pfd.save(commit=False)
            nspd.username=nsud
            nspd.save()

            send_mail(
                'Mail Rigister',
                'I am sehulu you remenber me dont bother about this one my user',
                'seshulustra1234@gmail.com',
                [nsud.email],
                fail_silently=False,
            )
            return HttpResponseRedirect(reverse('user_login'))
        else:
            return HttpResponse('data is not valid')
    return render(request,'restration.html',d)



def user_login(request):
    if request.method=='POST':
        un=request.POST['un']
        ps=request.POST['ps']

        AUO=authenticate(username=un,password=ps)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=un
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('data is not correct')
    
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
@login_required
def display_profile(request):
    username=request.session.get('username')
    uo=User.objects.get(username=username)
    po=Profile.objects.get(username=uo)
    d={'uo':uo,'po':po}
    return render(request,'display_profile.html',d)
@login_required
def change_password(request):
    if request.method=='POST':
        pw=request.POST['pw']
        username=request.session.get('username')
        uo=User.objects.get(username=username)
        uo.set_password(pw)
        uo.save()
        return HttpResponse('password id change successfully')
    return render(request,'change_password.html')



