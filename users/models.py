from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is Required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(email, password, **extra_fields)


class Company(models.Model):
    company_name = models.CharField(max_length=100)
    legal_adress = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=60)
    def __str__(self):
        return self.company_name

class User(AbstractUser):
    class AccessChoices(models.TextChoices):
        открыт = 'открыт'
        закрыт = 'закрыт'
    username = None
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    father_name = models.CharField(max_length=50)
    organization = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    access = models.CharField(max_length=50,choices=AccessChoices.choices, default=AccessChoices.закрыт, blank=True, null=True)
    main_test_count = models.IntegerField(default=0)
    final_test = models.BooleanField(default=False, blank=True, null=True) #delete blank and null
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'father_name']

    def __str__(self):
        return self.email
    

