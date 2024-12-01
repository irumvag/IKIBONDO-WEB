from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Feedback,Myuser
from .forms import CustomUserCreationForm,CHWCreationForm,Addlocation
from django.contrib.sessions.models import Session

def signup(request):
    form=CustomUserCreationForm()
    if request.method=='POST':
        forms=CustomUserCreationForm(request.POST)
        if forms.is_valid():
            forms.save()
            #log the user in
            return redirect('login/')
    else:
        form=CustomUserCreationForm()
    return render(request,'signup.html',{'forms':form})

def index(request):
    return render(request,'index.html')
def about(request):
    return render(request,'about.html')
def contactus(request):
    info={}
    if request.method == 'POST':
        fullname=request.POST.get('Fullname')
        email=request.POST.get('Email')
        subject=request.POST.get('Subject')
        message=request.POST.get('message')
        if not fullname or not email or not message or not subject:
            return HttpResponse("All fields are required!", status=400)
        contact=Feedback(FUll_Name=fullname,Email=email,Subject=subject,Message=message)
        contact.save()
        info={'name':"Thank you for sending message!!"}
        return render(request,'contactus.html',{'info':info})
    return render(request,'contactus.html')

def login_view(request):
    if request.method=='POST':
        phone_number=request.POST.get('phone_number')
        password=request.POST.get('password')
        user=authenticate(request,username=phone_number,password=password)
        if user is not None:
            login(request, user)
            return redirect('useradmin')
        else:
            return render(request,'login.html',{'name':{'info':"Invalid phone number or password"}})
    else:
        messages.error(request,"Invalid phone number or password")
    return render(request,'login.html')
def logout_view(request):
    if request.method == 'POST':
        Session.objects.filter(session_key=request.session.session_key).delete()
        logout(request)
        return redirect('login')
        
@login_required(login_url='/login/')
def useradmin(request):
    user=request.user
    myuser=Myuser.objects.all()
    return render(request,'admindashboard.html',{'user':user,'myuser':myuser})

@login_required(login_url='/login/')
def adminfeedback(request):
    myuser=Myuser.objects.all()
    user=request.user
    return render(request,'adminfeedback.html',{'user':user,'myuser':myuser})
@login_required
def chw(request):
    user=request.user
    myuser=Myuser.objects.all()
    render(request,'chw.html')
    
@login_required(login_url='/login/')
def addchw(request):
    user=request.user
    myuser=Myuser.objects.all()
    if request.method =='POST':
        pass
    else:
        form1=CustomUserCreationForm()
        form2=Addlocation()
        form3=Addlocation()
    return render(request,'addchw.htm',{'form1':form1,'form2':form2,'form3':form3})

@login_required
def chw(request):
    user=request.user
    myuser=Myuser.objects.all()
    render(request,'chw.html')

