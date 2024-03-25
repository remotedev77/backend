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


class Direction(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class User(AbstractUser):
    class AccessChoices(models.TextChoices):
        открыт = 'открыт'
        закрыт = 'закрыт'

    class RoleChoices(models.TextChoices):
        user = 'user'
        manager = 'manager'
        admin = 'admin'

    class PlanChoices(models.TextChoices):
        basic = "базовый"
        pro = "расширенный"

    username = None
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False, blank=True, null=True)
    father_name = models.CharField(max_length=50, blank=True, null=True)
    organization = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    access = models.CharField(max_length=50,choices=AccessChoices.choices, default=AccessChoices.закрыт, blank=True, null=True)
    main_test_count = models.IntegerField(default=0)
    final_test = models.BooleanField(default=False, blank=True, null=True) #delete blank and null
    role = models.CharField(max_length=20,choices=RoleChoices.choices, default=RoleChoices.user, blank=True, null=True)
    direction_type = models.ForeignKey(Direction, on_delete=models.CASCADE, blank=True, null=True)
    plan = models.CharField(max_length=20, choices=PlanChoices.choices, default=PlanChoices.basic, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'father_name']

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.RoleChoices.admin
        
        elif self.is_admin:
            self.role = self.RoleChoices.manager

        else:
            self.role = self.RoleChoices.user

        return super().save(*args, **kwargs)
    def __str__(self):
        return self.email
    

class SmsStatus(models.Model):
    DELIVERY_STATUS_CHOICES = {
        0: "в очереди",
        1: "доставлено",
        2: "не доставлено",
        3: "передано",
        4: "ожидание статуса сообщения",
        6: "сообщение отклонено",
        8: "на модерации"
    }
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sms_status')
    sms_id = models.IntegerField()
    status = models.IntegerField(choices=DELIVERY_STATUS_CHOICES.items(), default=0)
    verify_code = models.IntegerField(blank=True,null=True)

    def __str__(self) -> str:
        return self.user.phone_number
    


class AdminTable(User):
    objects = AdminManager()
    class Meta:
        proxy = True
