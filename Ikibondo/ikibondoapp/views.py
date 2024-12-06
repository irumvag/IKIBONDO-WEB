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
@login_required
def chw(request):
    user=request.user
    myuser=Myuser.objects.get(role='Chw')
    render(request,'chw.html',{'user':user,'chw':CHW.objects.all(),'totals':total,'loc':Location.objects.all()})    
@login_required(login_url='/login/')
def addchw(request):
    if request.method == 'POST':
        print(request.POST)
        if 'password1' not in request.POST or 'password2' not in request.POST:
            request.POST = request.POST.copy()  # Make the POST data mutable
            request.POST['password1'] = 'umwana123'  # Default password1
            request.POST['password2'] = 'umwana123'  # Default password2
        form1 = CustomUserCreationForm(request.POST)
        form3 = CHWCreationForm(request.POST)
        if form1.is_valid() and form3.is_valid():
            print("Forms are valid.")
            user = form1.save(commit=False)
            print(f"User before save: {user}")
            user.save()
            print("User saved.")
    
            chw = form3.save(commit=False)
            chw.User = user  # Associate user with CHW
            print(f"CHW before save: {chw}")
            chw.save()
            print("CHW saved.")
    
            return redirect('chw')
        else:
            print("Form1 errors:", form1.errors)
            print("Form3 errors:", form3.errors)

        # if form1.is_valid() and form3.is_valid():
        #     # Save the custom user first
        #     user = form1.save(commit=False)
        #     user.role='Chw'
        #     user.save()
        #     # Save the CHW record (with the user assigned)
        #     chw = form3.save(commit=False)
        #     chw.User = user  # Associate the user with this CHW
        #     chw.save()
        #     messages.success(request,"Saved successful")
        #     return redirect('chw')  # Redirect after successful submission
        # else:
        #     print("Form1 errors:", form1.errors)  # Debugging
        #     print("Form3 errors:", form3.errors)  # Debugging
    else:
        form1 = CustomUserCreationForm()
        form3 = CHWCreationForm()
    return render(request, 'addchw.html', {'form1': form1, 'form3': form3})
@login_required(login_url='/login/')
def chw_view(request):
    user=request.user
    return render(request,'chw.html',{'user':user,'totals':total})
