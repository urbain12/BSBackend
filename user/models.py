from unicodedata import category
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.base import Model
from django.db.models.fields import CharField
from django.db.models.fields.files import ImageField
from django.forms import DateField
from django.http import request
import datetime

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email,FirstName=None,LastName=None,MName=None,FName=None,Weight=None,Height=None,DOB=None, phone=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('Users must have a valid email')
        if not phone:
            raise ValueError('Users must have a valid phone number')
        if not password:
            raise ValueError("You must enter a password")

        email = self.normalize_email(email)
        user_obj = self.model(email=email)
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.FirstName = FirstName
        user_obj.LastName = LastName
        user_obj.MName = MName
        user_obj.FName = FName
        user_obj.Weight = Weight
        user_obj.Height = Height
        user_obj.DOB = DOB
        user_obj.phone = phone
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email,FirstName=None,LastName=None,MName=None,FName=None,Weight=None,Height=None,DOB=None,  phone=None, password=None):
        user = self.create_user(
            email,FirstName=FirstName,LastName=LastName,MName=MName,FName=FName,Weight=Weight,Height=Height,DOB=DOB,  phone=phone, password=password, is_staff=True)
        return user

    def create_superuser(self, email,FirstName=None,LastName=None,MName=None,FName=None, phone=None, password=None):
        user = self.create_user(email,FirstName='0781269507',LastName='0781269507',MName="MName",FName="FName", phone='0787018287',
                                password=password, is_staff=True, is_admin=True)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    FirstName=models.CharField(max_length=255,  null=True, blank=True)
    LastName=models.CharField(max_length=255,  null=True, blank=True)
    MName=models.CharField(max_length=255,  null=True, blank=True)
    FName=models.CharField(max_length=255,  null=True, blank=True)
    Weight=models.CharField(max_length=255,  null=True, blank=True)
    Height=models.CharField(max_length=255,  null=True, blank=True)
    DOB = models.DateField(auto_now_add=False,null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(
        max_length=255, unique=True, null=True, blank=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def takeVax(self):
        vaccines = self.vaccines_set.all()
        vaccines_=[]
        for vax in vaccines:
            vaccines_.append(vax.Vaxtype)
        str_takeVax=", ".join(vaccines_)
        if str_takeVax=='':
            str_takeVax='0'
        return str_takeVax

    @property
    def isVaccinated(self):
        vaccines = self.vaccines_set.all()
        if len(vaccines)>0:
            hasvax=True
        else:
            hasvax=False
        return hasvax

    @property
    def remVax(self):
        vaccines = self.vaccines_set.all()
        vaccines_=[]
        for vax in vaccines:
            vaccines_.append(vax.Vaxtype)
        remVax_=list(set(['Birth','SixWeeks','TenWeeks','FourteenWeeks','NineMonths','FifteenMonths']) - set(vaccines_))
        str_remVax=", ".join(remVax_)
        if str_remVax=='':
            str_remVax='0'
        return str_remVax

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

class Guide(models.Model):
    Title = models.CharField(max_length=255, null=True, blank=True)
    SubTitle = models.CharField(max_length=255, null=True, blank=True)
    Description = models.TextField(null=True, blank=True)
    Publish = models.BooleanField(default=False)
    added_at = models.DateField(auto_now_add=True)


class Queries(models.Model):
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, null=True, blank=True)
    FirstName = models.CharField(max_length=250,blank=True,null=True)
    LastName = models.CharField(max_length=250,blank=True,null=True)
    DoB = models.DateField(blank=True,null=True)
    Phone = models.CharField(max_length=250,blank=True,null=True)
    Message = models.CharField(max_length=250,blank=True,null=True)
    category = models.CharField(max_length=250,blank=True,null=True)
    reply = models.TextField(blank=True, null=True,
                             default="Please wait for the response")
    replied = models.BooleanField(default=False)
    send_at = models.DateField(auto_now_add=True)


class Vaccines(models.Model):
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, null=True, blank=True)
    Vaxtype = models.CharField(max_length=250,blank=True,null=True)
    added_at = models.DateField(auto_now_add=True)

    