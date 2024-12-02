from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager,PermissionsMixin
from django.core.validators import RegexValidator

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
    USERNAME_FIELD='phone_number'
    REQUIRED_FIELDS=['email']
    object=CustomUserManager()
    def __str__(self):
        return self.phone_number

#checked True
class Location(models.Model):
    LocationId= models.PositiveIntegerField(primary_key=True)
    Country = models.CharField(max_length=100, default='Rwanda', blank=True)
    Provence= models.CharField(max_length=100)
    District= models.CharField(max_length=100)
    Village= models.CharField(max_length=100)
    Streetcode=models.CharField(max_length=50,blank=True)

    def __str__(self):
        return  self.District
    class Meta:
        verbose_name_plural="Locations"
#checked True
class Parent(models.Model):
    user=models.OneToOneField(Myuser,on_delete=models.CASCADE,related_name='parent_profile')
    NID= models.PositiveIntegerField(primary_key=True)
    Gender= models.TextChoices("Male","Female")
    Age= models.PositiveIntegerField()
    Phone= models.CharField(max_length=10)
    Location=models.ForeignKey(Location,blank=False,on_delete=models.CASCADE)
    def __str__(self):
        return self.Fullnames
    class Meta:
        verbose_name_plural='Parents'

#checked True
class Hospital(models.Model):
    HID= models.PositiveBigIntegerField(primary_key=True)
    LocationId=models.ForeignKey(Location, on_delete=models.CASCADE,related_name='Hospital')
    Names= models.CharField(max_length=100)
    Hospitaltype= models.TextField()
    def __str__(self):
        return self.Names

#checked True
class CHW(models.Model):
    User=models.OneToOneField(Myuser,on_delete=models.CASCADE,related_name='chw_profile')
    NID= models.PositiveBigIntegerField(primary_key=True)
    LocationId=models.ForeignKey(Location, on_delete=models.CASCADE, related_name='CHW')
    HID= models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='CHW')
    def __str__(self):
        return self.User.first_name
    
#checked True
class Device(models.Model):
    Name= models.CharField(max_length=100)
    UserGuide= models.TextField()
    Description= models.CharField(max_length=100)
    SerialNumber= models.PositiveBigIntegerField()
    def __str__(self):
        return self.Name
    
#checked out
class Vacinne_and_measure(models.Model):
    VID= models.PositiveBigIntegerField(primary_key=True)
    Vacinne_name= models.CharField(max_length=100)
    Details= models.TextField()
    Age_Limit= models.PositiveIntegerField()
    Time_to_inject=models.PositiveIntegerField()
    def __str(self):
        return self.Vacinne_name
    
#checked out
class Medical_info(models.Model):
    HID= models.PositiveBigIntegerField()
    BID= models.PositiveBigIntegerField()
    DOB= models.DateField()
    Born_height= models.PositiveBigIntegerField()
    Born_weight= models.PositiveBigIntegerField()
    Method_Used_in_Birth= models.CharField(max_length=100)
    Midwife_name= models.CharField(max_length=100)
    def __str__(self):
        return self.Midwife_name
    class Meta:
        verbose_name_plural = "Medical Infos"
#checked out
class Baby(models.Model):
    BID= models.PositiveBigIntegerField(primary_key=True)
    PID= models.ForeignKey(CHW,on_delete=models.CASCADE,related_name='Baby')
    Names= models.CharField(max_length=100)
    Gender= models.TextChoices("Male","Female")
    Age= models.PositiveIntegerField()
    Photo= models.ImageField(default='default.png',blank=True)
    def __str__(self):
        return self.Names
    class Meta:
        verbose_name_plural = "Babies"
    
#checked true
class Feedback(models.Model):
    FUll_Name=models.CharField(max_length=100)
    Email= models.EmailField()
    Subject= models.CharField(max_length=100)
    Message= models.TextField()
    CreatedDate= models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.Subject
    class Meta:
        verbose_name_plural='Feedbacks'
#checked out
class Update(models.Model):
    BID=models.ForeignKey(Baby, on_delete=models.CASCADE, related_name='Update')
    VID=models.ForeignKey(Vacinne_and_measure,on_delete=models.CASCADE,related_name='Update')
    New_height= models.PositiveBigIntegerField()
    New_weight= models.PositiveBigIntegerField()
    Description=models.TextField()
    Date=models.DateField(auto_now=True)
    def __str__():
        return self.VID
    class Meta:
        verbose_name_plural='Updates'
#ced outheck
class VaccinatedBaby(models.Model):
    BID= models.ForeignKey(Baby, on_delete=models.CASCADE, related_name='Gives')
    VID=models.ForeignKey(Vacinne_and_measure,on_delete=models.CASCADE,related_name='VaccinatedBabies')
    HID= models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='Gives')
    Doze=models.TextField()
    Timetaken=models.TimeField(auto_now=True)
    def __str__(self):
        return self.Dose
    class Meta:
        verbose_name_plural='VaccinatedBabies'



# Create your models here.
