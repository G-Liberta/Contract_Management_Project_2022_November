# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.db.models import Sum,F

class UserProfileManager(BaseUserManager):
    """Manager for UserProfiles"""

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

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name for user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of user"""
        return self.email

class Contract(models.Model):
    """Table that holds the Contracts"""
    subject = models.CharField(max_length=255)
    hospital = models.ForeignKey('Contracts_api.Hospital', on_delete=models.CASCADE)
    product = models.ForeignKey('Contracts_api.ContractItem', null=True, on_delete=models.CASCADE )
    deadline = models.DateField(null=True)
    prot_nr = models.CharField(max_length=10, blank=True, null=True)
    sign_date = models.DateField(null=True)
    total_value = models.FloatField(null=True)

    def __str__(self):
        """Return the model as a string"""
        return self.hospital


class ContractItem(models.Model):
    contract_id = models.ForeignKey('Contracts_api.Contract', null=True, on_delete=models.CASCADE)
    warehouse_id = models.ForeignKey('Contracts_api.Warehouse', null=True, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    price = models.FloatField(default=0)
    discount = models.FloatField(default=0)

    @property
    def total(self):
        return self.invoiceitem_set.all().aggregate(total=Sum(F('quantity') * F('price')+F('discount')))

    def __str__(self):
        return f'{self.quantity}'

class Hospital(models.Model):
    name = models.CharField(max_length=50)
    adress = models.CharField(max_length=250)
    email = models.EmailField(max_length=255, unique=True)
    phone_nr = models.CharField(max_length=15, null=True)

    def __str__(self):
        return self.name

class Warehouse(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField(null=True)
    quantity = models.FloatField(null=True)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    client = models.ForeignKey('Contracts_api.Hospital', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        # sum = 0
        # for item in self.invoiceitem_set.all():
        #     sum += item.total
        # return sum
        return self.invoiceitems_set.all().aggregate(total=Sum(F('quantity') * F('price')))

    def __str__(self):
        return f'{self.client} / {self.date}'


class InvoiceItem(models.Model):
    warehouse_id = models.ForeignKey('Contracts_api.Warehouse', on_delete=models.CASCADE)
    quantity = models.FloatField(null=True)
    price = models.FloatField(null=True)

    def __str__(self):
        return self.warehouse_id
