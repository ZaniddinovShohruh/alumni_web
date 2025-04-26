from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'student_id','date_of_birth', 'nationality','phone','email','address','photo','cv')
    list_filter = ['first_name', 'last_name', 'student_id', 'phone']


@admin.register(AcademicInfo)
class AcademicInfoAdmin(admin.ModelAdmin):
    list_display = ('faculty','year_of_admission','graduation_year','diploma_number','contract_type', 'contract_paid', 'contract_total')
    list_filter = ['diploma_number']

@admin.register(ProfActivity)
class ProfActivityAdmin(admin.ModelAdmin):
    list_display = ('current_work','future_goal')