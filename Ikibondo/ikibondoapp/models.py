from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager,PermissionsMixin
from django.core.validators import RegexValidator
from django.conf import settings
from django.utils.timezone import now

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The phone number must be set')
        extra_fields.setdefault('is_active', True)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(phone_number, password, **extra_fields)
class Myuser(AbstractUser):
    ROLE_CHOICES = [
        ('Nurse', 'Nurse'),
        ('Superadmin', 'Superadmin'),
        ('Chw', 'Chw'),
        ('Parent', 'Parent'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    username=None
    phone_number=models.CharField(max_length=10,validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Phone number must be 10 digits long.",
                code='invalid_phone_number'
            )
            ],
        unique=True)
    email=models.EmailField(unique=True,blank=True)
    role=models.CharField(choices=[('Nurse','Nurse'),('Superadmin','Superadmin'),('Chw','Chw'),('Parent','Parent')],max_length=50)
    gender= models.CharField(choices=[('Male','Male'),('Female','Female')],max_length=20)
    Age= models.PositiveIntegerField(null=True,validators=[
            RegexValidator(
                regex=r'^\d{2}$',
                message="age must be 2 digits long.",
                code='invalid_age_value'
            )
            ])
    need_password_change=models.BooleanField(default=True)
    USERNAME_FIELD='phone_number'
    REQUIRED_FIELDS=['email']
    
    object=CustomUserManager()
    def __str__(self):
        return f"User:{self.first_name} {self.last_name} with: {self.phone_number}"

# #checked True
class Location(models.Model):
    LocationId= models.AutoField(primary_key=True)
    Country = models.CharField(max_length=100, default='Rwanda', blank=True)
    Provence= models.CharField(max_length=100)
    District= models.CharField(max_length=100)
    Village= models.CharField(max_length=100)
    Streetcode=models.CharField(max_length=50,blank=True)

    def __str__(self):
        return  f"{self.Country}/{self.Provence}/{self.District}/{self.Village}/{self.Streetcode}"
    class Meta:
        verbose_name_plural="Locations"
#checked True
class Parent(models.Model):
    User=models.OneToOneField(Myuser,on_delete=models.CASCADE,related_name='parent_profile')
    NID= models.PositiveIntegerField(primary_key=True,
    validators=[
            RegexValidator(
                regex=r'^\d{16}$',
                message="age must be 16 digits long.",
                code='invalid_ID_value'
            )
            ]
            )
    Location=models.ForeignKey(Location,blank=False,on_delete=models.CASCADE,related_name='location')
    def __str__(self):
        return self.Fullnames
    class Meta:
        verbose_name_plural='Parents'

# #checked True
class Hospital(models.Model):
    HID= models.PositiveBigIntegerField(primary_key=True)
    LocationId=models.ForeignKey(Location, on_delete=models.CASCADE,related_name='Hospital')
    Names= models.CharField(max_length=100)
    Hospitaltype= models.TextField()
    Recordeddate=models.IntegerField()
    def __str__(self):
        return self.Names

#checked True
class CHW(models.Model):
    User=models.OneToOneField(Myuser,on_delete=models.CASCADE)
    LocationId=models.ForeignKey(Location, on_delete=models.CASCADE, related_name='chw_profile')
    HID= models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='chw_profile')
    def __str__(self):
        return self.User.first_name
    def __str__(self):
        return f"{self.User.first_name} {self.User.last_name} ({self.HID})"
#checked True
class Device(models.Model):
    Name= models.CharField(max_length=100)
    UserGuide= models.TextField()
    Description= models.TextField()
    SerialNumber= models.PositiveBigIntegerField()
    Img=models.ImageField(default='device.png',null=True,upload_to='media/')

    def __str__(self):
        return self.Name
    
 #checked out
class Baby(models.Model):
    BID= models.PositiveBigIntegerField(primary_key=True)
    PID= models.ManyToManyField(Parent,related_name='Baby')
    Names= models.CharField(max_length=100)
    Gender= models.CharField(max_length=30,choices=[('Male','Male'),('Female','Female')])
    DOB= models.DateField()
    Photo= models.ImageField(default='default.png',blank=True)
    def __str__(self):
        return self.Names
    class Meta:
        verbose_name_plural = "Babies"

#checked out
class Medical_info(models.Model):
    HID= models.ManyToManyField(Hospital,related_name='bornhospital')
    BID= models.OneToOneField(Baby,on_delete=models.CASCADE,related_name='Baby')
    Age= models.PositiveIntegerField(help_text="age in mouths")
    Born_height= models.PositiveBigIntegerField()
    Born_weight= models.PositiveBigIntegerField()
    Method_Used_in_Birth= models.CharField(max_length=100)
    Midwife_name= models.CharField(max_length=100)
    def __str__(self):
        return self.Midwife_name
    class Meta:
        verbose_name_plural = "Medical Infos"
    
#checked true
class Feedback(models.Model):
    FUll_Name=models.CharField(max_length=100)
    Email= models.EmailField()
    Subject= models.CharField(max_length=100)
    Message= models.TextField()
    CreatedDate= models.DateTimeField(default=now)
    def __str__(self):
        return self.Subject
    class Meta:
        verbose_name_plural='Feedbacks'

#checked out
class Vacinne_and_measure(models.Model):
    VID= models.AutoField(primary_key=True)
    Vacinne_name= models.CharField(max_length=100)
    Age= models.PositiveIntegerField()
    Dose=models.CharField(max_length=20)
    Details= models.TextField()
    Recordeddate=models.DateTimeField(default=now)
    def __str(self):
        return self.Vacinne_name


#checked out
class Update(models.Model):
    BID=models.ForeignKey('Baby', on_delete=models.CASCADE, related_name='Update')
    VID=models.ForeignKey(Vacinne_and_measure,on_delete=models.CASCADE,related_name='Update')
    New_height= models.PositiveBigIntegerField()
    New_weight= models.PositiveBigIntegerField()
    Description=models.TextField()
    Date=models.DateField(default=now)
    def __str__():
        return self.VID
    class Meta:
        verbose_name_plural='Updates'
#checked out
class VaccinatedBaby(models.Model):
    BID=models.ForeignKey(Baby, on_delete=models.CASCADE, related_name='Gives')
    VID=models.ForeignKey(Vacinne_and_measure,on_delete=models.CASCADE,related_name='VaccinatedBabies')
    HID= models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='Gives')
    Doze=models.TextField()
    Timetaken=models.TimeField(default=now)
    def __str__(self):
        return self.Dose
    class Meta:
        verbose_name_plural='VaccinatedBabies'
class Reminder(models.Model):
    BID=models.ForeignKey(Baby,on_delete=models.CASCADE,related_name='baby_profile')
    VID=models.ForeignKey(Vacinne_and_measure,on_delete=models.CASCADE)
    Start_vaccine_date=models.DateField()
    Vaccine_reminder=models.DateField()
    def _str_(self):
        return self.Vaccine_reminder
    class Meta:
        verbose_name_plural='Reminders'
class Approval(models.Model):
    # Many-to-Many relationship to MyUser for approvers
    approvers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="approval_approvers",
        help_text="Users who approve",
    )
    # Many-to-Many relationship to MyUser for approved users
    approves = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="approved_users",
        help_text="Users being approved",
    )
    # Comment field
    comment = models.TextField(blank=True, null=True, help_text="Approval comments")
    # Time created field
    time_created = models.DateTimeField(default=now, help_text="Time approval was created")

    def __str__(self):
        return f"{', '.join([user.role for user in self.approves.all()])} {', '.join([user.last_name for user in self.approves.all()])} {', '.join([user.first_name for user in self.approves.all()])} Approved by {', '.join([user.role for user in self.approvers.all()])} : {', '.join([user.last_name for user in self.approvers.all()])} {', '.join([user.first_name for user in self.approvers.all()])}"

    class Meta:
        verbose_name = "Approval"
        verbose_name_plural = "Approvals"
        ordering = ["-time_created"]
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"

# Create your models here.
