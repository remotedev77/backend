from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import UserManager, AdminManager

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
    
    def get_organization_name(self):
        return self.organization.company_name

class AdminTable(User):
    objects = AdminManager()
    class Meta:
        proxy = True
