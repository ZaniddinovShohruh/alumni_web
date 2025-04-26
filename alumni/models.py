from django.urls import reverse
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    first_name = models.TextField(max_length=200, verbose_name='first_name')
    last_name = models.TextField(max_length=200, verbose_name='last_name')
    student_id = models.CharField(max_length=200)
    date_of_birth = models.IntegerField(default=0, verbose_name='Date of birth')
    nationality = models.TextField(max_length=200, verbose_name='Nationality')
    phone = models.IntegerField(default=0, verbose_name='Phone number')
    password = models.CharField(max_length=200)
    address = models.CharField(max_length=100, verbose_name='Address')
    photo = models.ImageField(upload_to='photo/', blank=True, null=True, verbose_name='Photos')
    cv = models.FileField(upload_to='cv/', blank=True, null=True, verbose_name='CV')
    email = models.EmailField(max_length=200, verbose_name='e_mail')


    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",
        blank=True
    )

    def __str__(self):
        return self.username

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]


class AcademicInfo(models.Model):
    faculty = models.TextField(max_length=100, verbose_name='Faculty')
    year_of_admission = models.IntegerField(default=0, verbose_name='Year of admission')
    graduation_year = models.IntegerField(default=0, verbose_name='Graduation year')
    diploma_number = models.IntegerField(default=0, verbose_name='Diploma number')
    contract_type = models.CharField(max_length=100, verbose_name='Contract type')
    personal_information = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User Information')
    contract_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    contract_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def __str__(self):
        return f"{self.faculty} ({self.year_of_admission} - {self.graduation_year})"

class ProfActivity(models.Model):
    current_work = models.CharField(max_length=100, verbose_name='Current work')
    future_goal = models.CharField(max_length=100, verbose_name='Future goal')
    personal_information = models.ForeignKey(AcademicInfo, on_delete=models.CASCADE, verbose_name='Prof Activity')

    def __str__(self):
        return self.current_work



class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Student')

    def __str__(self):
        return self.username

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"