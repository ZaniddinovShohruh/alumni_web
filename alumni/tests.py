from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from alumni.models import AcademicInfo

# @shared_task
def check_and_notify_debt_students():
    students = AcademicInfo.objects.select_related('personal_information').all()

    for student in students:
        print(student)
        debt = float(student.contract_total - student.contract_paid)

        if debt < 0:
            email = student.personal_information.email
            name = student.personal_information.first_name

            send_mail(
                subject="Eslatma: Qarz mavjud",
                message=f"""Assalomu alaykum, {name}!
Bizning tizim bo‘yicha sizda {debt:,.0f} so‘m qarz mavjud.
Iltimos, to‘lovni imkon qadar tezroq amalga oshiring!

Hurmat bilan,  
Turin Polytechnic University in Tashkent.
""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False
            )
