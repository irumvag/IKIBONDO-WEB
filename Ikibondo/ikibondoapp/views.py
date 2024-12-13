from django.shortcuts import render,redirect,get_object_or_404,reverse
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
from django.core.exceptions import PermissionDenied

def returnsum(modelname):
    s=0
    for i in modelname.objects.all():
        s=s+1
    return s
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
        try:
            send_mail(
                'Your feedback has been recieved successfull!',
                f'Hello {fullname},\nYour feedback has been recieved well. \nWe will get back to you shortly!\n\nBest regards,\nIKIBONDO WEB',
                'djanaclet@gmail.com',  # Sender email
                [email],  # Hospital admin email
                fail_silently=False,
            )
            return render(request,'contactus.html',{'info':info})
        except Exception as e:
                info={'name':"failed"}
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
sum2,sum4,sum5,sum6=0,0,0,0
for g in Hospital.objects.all():
    sum4+=1
for k in Myuser.objects.filter(role='Superadmin' or 'Nurse'):
    sum5+=1
for g in Myuser.objects.filter(role='Chw'):
    sum6+=1
total={
    'totaluser':returnsum(Myuser),
    'totalbabies':sum2,
    'totaltests':returnsum(VaccinatedBaby),
    'totalhospital':sum4,
    'totalchw':sum6,
}
@login_required(login_url='/login/')
def useradmin(request):
    user=request.user
    myusers=Myuser.objects.filter(role='Chw').order_by('-date_joined')
    return render(request,'admindashboard.html',{'user':user,'totals':total,'userchws':myusers})
@login_required(login_url='/login/')
def adminfeedback(request):
    user=request.user
    return render(request,'adminfeedback.html',{'user':user,'totals':total})
@login_required(login_url='/login/')
def chw(request):
    user=request.user
    myuser=Myuser.objects.filter(role='Chw').order_by('date_joined')
    return render(request,'chw.html',{'user':user,'userss':myuser,'totals':total})
@login_required
def userprofile_view(request):
    return render(request,'userprofile.html')
@login_required
def setting_view(request):
    return render(request,'settings.html')
@login_required
def notification_view(request):
    notifications = request.user.notifications.all()
    return render(request, 'notifications.html', {'notifications': notifications})

@login_required
def pandb_view(request):
    return render(request,'parentsandbaby.html')  
@login_required  
def vandm_view(request):
    return render(request,'vaccineandmeasure.html')
@login_required
def report_view(request):
    userss=request.user.approval_approvers.all()
    userss1=Myuser.objects.filter(is_active=False,role='Chw')
    userss=Myuser.objects.filter(is_active=False,role='Nurse')
    userss2=Myuser.objects.filter(is_active=False,role='Parent')
    return render(request,'reports.html',{'userss':userss,'user':request.user,'usersschw':userss,'usernurse':userss1,'userparent':userss2})
@login_required
def admin_view(request):
    user=request.user
    myusers=Myuser.objects.filter(role='Superadmin' or 'Nurse').order_by('-date_joined')
    return render(request,'admins.html',{'userss':myusers,'totals':total,'user':user})
@login_required
def babies(request):
    return render(request,'babies.html') 
@login_required
def addchw(request):
    if request.method == 'POST':
        form1 = CustomUserCreationForm(request.POST)
        if form1.is_valid():
            user = form1.save(commit=False)
            user.is_active = False
            user.save()
            # Notify hospital admin
            try:
                send_mail(
                    'New Comunity Health Worker User Created',
                    f'A new CHW user {user.first_name} {user.last_name} has been created. \nPlease confirm their hospital assignment.\n\nBest regards,\nIKIBONDO WEB',
                    'djanaclet@gmail.com',  # Sender email
                    ['tumukundegentille001@gmail.com'],  # Hospital admin email
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
    user=request.user
    hos=Hospital.objects.all()
    return render(request,'hospitals.html',{'user':user,'totals':total,'hospitals':hos})
@login_required
def userdetail(request,phone):
    user=request.user
    editx = get_object_or_404(Myuser, phone_number=phone)
    if request.method=='POST': 
        return render(request,'userdetails.html',{'user':user,'editx':editx})
    return render(request,'userdetails.html',{'user':user,'editx':editx})
@login_required
def create_chw(request,phone,role):
    user_to_approve=get_object_or_404(Myuser,phone_number=phone,role=role)
    if request.method == 'POST':
        if role == 'Chw':
            form = CHWForm(request.POST)
        else:
            form=None
        if form.is_valid():
            form.save()  # Save the CHW instance to the database
            approval, created = Approval.objects.get_or_create()
            approval.approves.add(user_to_approve)
            approval.approvers.add(request.user)  # Assuming the logged-in user is the approver
            approval.comment = "User approved successfully."
            approval.save()
            # Update user's status
            user_to_approve.is_active = True  # Activate the user
            user_to_approve.save()

            # Create a notification for the approved user
            notification_message = f"Your account has been approved by {request.user.first_name} {request.user.last_name}."
            Notification.objects.create(
                user=user_to_approve,
                message=notification_message
            )
            approver_notification = f"You approved {user_to_approve.first_name} {user_to_approve.last_name}'s account."
            Notification.objects.create(
                user=request.user,
                message=approver_notification
            )
            messages.success(request, "User approved and notifications sent.")
        return redirect('chw')  # Redirect to a success page or list view
    else:
        if role == 'Chw':
            form = CHWForm()
            approves={
                'phone':phone,
                'role':role
            }
            return render(request, 'approve_chw.html', {'form': form,'user':request.user,'approve':approves})
        else:    
            return redirect(reverse("reports"))  # Ensure "report" exists in urls.py
@login_required
def add_vaccine(request):
    if request.method == 'POST':
        form = VacinneAndMeasureForm(request.POST)
        if form.is_valid():
            vaccine = form.save()  # Save the new vaccine record
            # Send notifications to all users
            all_users = Myuser.objects.all()
            for user in all_users:
                Notification.objects.create(
                    user=user,
                    message=f"A new vaccine '{vaccine.Vacinne_name}' has been added for age {vaccine.Age} mouths."
                )
            messages.success(request, f"Vaccine '{vaccine.Vacinne_name}' added and notifications sent.")
            return redirect('vaccine')  # Replace with the URL name of your vaccine list page
    else:
        form = VacinneAndMeasureForm()

    return render(request, 'add_vaccine.html', {'form': form,'user':request.user})
