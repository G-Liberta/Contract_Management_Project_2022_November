# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.db.models import Sum,F

class ContractManager(BaseUserManager):
    """Manager for contracts"""

    def create_user(self, name, email, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('Please place your email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, name, email, password):
        """create and save new superuser with given details"""
        user = self.create_user(name, email, password)
        user.is_superuser = True
        user.is_staff= True
        user.save(using=self._db)

        return user



class Contract(AbstractBaseUser, PermissionsMixin):
    """Database models for the contracts in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']