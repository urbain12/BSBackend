from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.base import Model
from django.db.models.fields import CharField
from django.db.models.fields.files import ImageField
from django.http import request
import datetime

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email,FirstName=None,LastName=None,Weight=None,Height=None,DOB=None, phone=None, password=None, is_active=True, is_staff=False, is_admin=False):
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
        user_obj.Weight = Weight
        user_obj.Height = Height
        user_obj.DOB = DOB
        user_obj.phone = phone
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email,FirstName=None,LastName=None,Weight=None,Height=None,DOB=None,  phone=None, password=None):
        user = self.create_user(
            email,FirstName=FirstName,LastName=LastName,Weight=Weight,Height=Height,DOB=DOB,  phone=phone, password=password, is_staff=True)
        return user

    def create_superuser(self, email,FirstName=None,LastName=None, phone=None, password=None):
        user = self.create_user(email,FirstName='0787018257',LastName='0787018257', phone='0787018287',
                                password=password, is_staff=True, is_admin=True)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    FirstName=models.CharField(max_length=255,  null=True, blank=True)
    LastName=models.CharField(max_length=255,  null=True, blank=True)
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
    
    def __str__(self):
        return self.Title


class Queries(models.Model):
    fullname = models.CharField(max_length=250,blank=True,null=True)
    email = models.EmailField(max_length=250,blank=True,null=True)
    Phone = models.CharField(max_length=250,blank=True,null=True)
    Message = models.CharField(max_length=250,blank=True,null=True)

    def __str__(self):
        return self.fullname