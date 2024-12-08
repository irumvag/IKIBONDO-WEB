from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.sessions.models import Session
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from time import sleep
from django.core.mail import send_mail

def signup(request):
    if request.method=='POST':
        forms=CustomUserCreationForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('login')
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
        info={'name':"Thank you for sending us message!!"}
        return render(request,'contactus.html',{'info':info})
    return render(request,'contactus.html')
def login_view(request):
    if request.method=='POST':
        phone_number=request.POST.get('phone_number')
        password=request.POST.get('password')
        user=authenticate(request,username=phone_number,password=password)
        if user is not None:
            login(request, user)
            if user.need_password_change:
                # Redirect to a password change page
                return redirect('change_password') 
            return redirect('useradmin')
        else:
            return render(request,'login.html',{'name':{'info':"Invalid phone number or password"}})
    else:
        messages.error(request,"Enter phone number and password")
    return render(request,'login.html')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # Update the user's session to reflect the new password
            update_session_auth_hash(request, form.user)
            # Mark that the user no longer needs to change their password
            request.user.need_password_change = False
            #console.log('the data in the database is :...........' , )
            request.user.save()
            messages.success(request, 'Your password has been changed successfully.')
            sleep(10)
            return redirect('useradmin')  # Redirect to home or desired page
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})
def logout_view(request):
    if request.method == 'POST':
        Session.objects.filter(session_key=request.session.session_key).delete()
        logout(request)
        return redirect('login')
    logout(request)
    return redirect('login')
sum1,sum2,sum3,sum4,sum5=0,0,0,0,0
for g in Myuser.objects.all():
    sum1+=1
for g in VaccinatedBaby.objects.all():
    sum3+=1
for g in Hospital.objects.all():
    sum4+=1
for k in CHW.objects.all():
    sum5+=1
total={
    'totaluser':sum1,
    'totalbabies':sum2,
    'totaltests':sum3,
    'totalhospital':sum4,
    'totalchw':sum5,
}
@login_required(login_url='/login/')
def useradmin(request):
    user=request.user
    return render(request,'admindashboard.html',{'user':user,'totals':total})
@login_required(login_url='/login/')
def adminfeedback(request):
    user=request.user
    return render(request,'adminfeedback.html',{'user':user,'totals':total})
@login_required(login_url='/login/')
def chw(request):
    user=request.user
    myuser=Myuser.objects.filter(role='Chw').order_by('-date_joined')
    return render(request,'chw.html',{'myuser':user,'user':myuser,'totals':total})
@login_required
def userprofile_view(request):
    return render(request,'userprofile.html')
@login_required
def setting_view(request):
    return render(request,'settings.html')
@login_required
def notification_view(request):
    return render(request,'notifications.html')
@login_required
def pandb_view(request):
    return render(request,'parentsandbaby.html')  
@login_required  
def vandm_view(request):
    return render(request,'vaccineandmeasure.html')
@login_required
def report_view(request):
    return render(request,'reports.html')
@login_required
def admin_view(request):
    return render(request,'admins.html')
@login_required
def babies(request):
    return render(request,'babies.html') 
@login_required
def addchw(request):
    if request.method == 'POST':
        form1 = CustomUserCreationForm(request.POST)
        if form1.is_valid():
            user = form1.save()
            #user.role = 'chw'
            user.save()
            # Notify hospital admin
            try:
                send_mail(
                    'New Comunity Health Worker User Created',
                    f'A new CHW user {user.first_name} {user.last_name} has been created. \nPlease confirm their hospital assignment.\n\nBest regards,\nIKIBONDO WEB',
                    'irumvagadanaclet@gmail.com',  # Sender email
                    ['irumvagadanaclet@gmail.com'],  # Hospital admin email
                    fail_silently=False,
                )
                return redirect('chw')
            except Exception as e:
                return redirect('chw')
    else:
        form1=CustomUserCreationForm(request.POST)
    return render(request, 'addchw.html', {'form1': form1})
@login_required
def hospital_view(request):
    return render(request,'hospitals.html')

