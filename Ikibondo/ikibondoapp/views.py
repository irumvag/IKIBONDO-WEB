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
from django.core.paginator import Paginator

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
    device=Device.objects.all()
    return render(request,'admindashboard.html',{'user':user,'totals':total,'userchws':myusers,'devices':device})
@login_required(login_url='/login/')
def adminfeedback(request):
    user=request.user
    return render(request,'adminfeedback.html',{'user':user,'totals':total})
@login_required(login_url='/login/')
def chw(request):
    user=request.user
    myuser=Myuser.objects.filter(role='Chw').order_by('-date_joined')
    return render(request,'chw.html',{'user':user,'userss':myuser,'totals':total})
@login_required
def userprofile_view(request):
    return render(request,'userprofile.html')
@login_required
def setting_view(request):
    return render(request,'settings.html')
@login_required
def notification_view(request):
    if request.method == 'POST':
        receiver = request.POST.get('receiver')  # Corrected typo 'reciever' to 'receiver'
        title = request.POST.get('title')
        link = request.POST.get('link', '')  # Optional link
        mes = request.POST.get('message')

        # Construct the message
        message = f"{title}\n{link}\n{mes}"

        # Handle the receiver logic
        if receiver == 'All':
            users = Myuser.objects.all()  # Get all users
        elif receiver == 'Superadmin':
            users = Myuser.objects.filter(role='Superadmin')  # Filter by role
        elif receiver == 'Chw':
            users = Myuser.objects.filter(role='Chw')
        elif receiver == 'Nurse':
            users = Myuser.objects.filter(role='Nurse')
        elif receiver == 'Parent':
            users = Myuser.objects.filter(role='Parent')
        else:
            # Handle single specific receiver (e.g., user ID or username passed)
            try:
                users = [Myuser.objects.get(phone_number=receiver)]
            except Myuser.DoesNotExist:
                return HttpResponse("Invalid receiver", status=400)
        # Create a notification for each user
        for user in users:
            Notification.objects.create(
                user=user,  # Assign the user
                message=message,  # Add the constructed message
            )
        # Redirect or return a success response
        return redirect('notification')  # Replace with your success page
            
    users=Myuser.objects.all()
    notification = request.user.notifications.all().order_by('-timestamp')
    paginator = Paginator(notification, 5)  # Show 5 notifications per page
    page_number = request.GET.get('page')
    notifications = paginator.get_page(page_number)
    return render(request, 'notifications.html', {'notifications': notifications,'users':users})
@login_required
def babies_view(request):
    return render(request,'baby.html')
@login_required
def pandb_view(request):
    parents=Myuser.objects.filter(role="Parent")
    return render(request,'parentsandbaby.html',{'parents':parents,'totalparent':returnsum(Parent)})  
@login_required  
def vandm_view(request):
    return render(request,'vaccineandmeasure.html')
@login_required
def report_view(request):
    userapproved=request.user.approval_approvers.all()
    userchw=Myuser.objects.filter(is_active=False,role='Chw')
    usernurse=Myuser.objects.filter(is_active=False,role='Nurse')
    userparent=Myuser.objects.filter(is_active=False,role='Parent')
    return render(request,'reports.html',{'userapproved':userapproved,'user':request.user,'userchw':userchw,'usernurse':usernurse,'userparent':userparent})
@login_required
def admin_view(request):
    user=request.user
    myusers=Myuser.objects.filter(role='Superadmin' or 'Nurse').order_by('-date_joined')
    return render(request,'admins.html',{'userss':myusers,'totals':total,'user':user})
@login_required
def babies(request,phone):
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
@login_required
def create_chw(request, phone, role):
    """
    Handles approval and creation logic for CHW or Parent based on user role.
    """
    # Get the user to approve or return 404
    user_to_approve = get_object_or_404(Myuser, phone_number=phone, role=role)

    # Check if request method is POST
    if request.method == 'POST':
        if  role == 'Chw':
            form = CHWForm(request.POST)
        elif role == 'Parent':
            form = ParentForm(request.POST)
        else:
            form = None

        if form and form.is_valid():
            # Save the form data (CHW or Parent instance)
            instance = form.save(commit=False)
            instance.User = user_to_approve  # Link to the approved user
            instance.save()

            # Create or update approval
            approval= Approval.objects.create()
            approval.approves.add(user_to_approve)
            approval.approvers.add(request.user)
            approval.comment = f"User approved as {role} successfully."
            approval.save()

            # Update user status
            user_to_approve.is_active = True
            user_to_approve.save()

            # Send notifications
            Notification.objects.create(
                user=user_to_approve,
                message=f"Your account has been approved by {request.user.first_name} {request.user.last_name}."
            )
            subject = "Your Account Has Been Approved 🎉"
            plain_message = (
                f"Dear {user_to_approve.last_name} {user_to_approve.first_name},\n\n"
                "We are excited to let you know that your account has been approved.\n"
                "You can now log in and enjoy all the features available.\n\n"
                "Thank you for joining us!\n\n"
                "Best Regards,\n"
                "Ikibondo Support Team"
            )

            html_message = f"""
                <div style="font-family: Arial, sans-serif; color: #333; line-height: 1.6; max-width: 600px; margin: auto;">
                    <h2 style="color: #007BFF; text-align: center;">{user_to_approve.role} Account Approved 🎉</h2>
                    <p style="font-size: 16px;">Dear <strong>{user_to_approve.last_name} {user_to_approve.first_name}</strong>,</p>
                    <p>We are excited to inform you that <strong>your account has been approved!</strong></p>
                    <p>You can now log in and start using all the amazing features available.</p>
                    <div style="text-align: center; margin: 20px;">
                        <a href="https://ikibondo.gov.rw/login" 
                        style="display: inline-block; padding: 10px 20px; font-size: 16px; 
                                color: white; background-color: #28a745; text-decoration: none; 
                                border-radius: 5px;">
                            Log In Now
                        </a>
                    </div>
                    <p>If you have any questions or need assistance, feel free to <a href="https://ikibondo.gov.rw/contact">contact us</a>.</p>
                    <p>Thank you for joining us!</p>
                    <p style="font-size: 14px; color: #777;">Best Regards,<br><strong>Ikibondo support Team</strong></p>
                </div>
            """

            send_mail(
                subject=subject,
                message=plain_message,
                from_email='djanaclet@gmail.com',
                recipient_list=[user_to_approve.email],
                html_message=html_message,
            )
            Notification.objects.create(
                user=request.user,
                message=f"You approved {user_to_approve.first_name} {user_to_approve.last_name}'s account as {role}."
            )

            messages.success(request, f"{role} approved and notifications sent.")
            return redirect('chw')  # Redirect to the CHW list or success page
    else:
        # Render form for GET requests
        if role == 'Chw':
            form = CHWForm()
        elif role == 'Parent':
            form = ParentForm()
        else:
            return redirect(reverse("reports"))  # Redirect invalid roles

        # Pass context for rendering
        context = {
            'usertoapprove':user_to_approve,
            'form': form,
            'user': request.user,
            'approve': {
                'phone': phone,
                'role': role
            }
        }
        return render(request, 'approve_chw.html', context)

