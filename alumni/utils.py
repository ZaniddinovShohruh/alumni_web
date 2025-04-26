from django.core.mail import send_mail
from .models import User

def notify_students_about_contract_debt():
    students = User.objects.all()

    for student in students:
        remaining_debt = student.contract_total - student.contract_paid
        print(remaining_debt)

        if remaining_debt > 0:
            subject = "Shartnoma qarzi haqida eslatma"
            message = f"""Assalomu alaykum, {student.full_name}!

                Bizning tizim bo‘yicha sizda {remaining_debt} so‘m qarz mavjud.
                Iltimos, to‘lovni imkon qadar tezroq amalga oshiring!
                
                Hurmat bilan,
                Turin Polytechnic University in Tashkent .
                """
            send_mail(
                subject,
                message,
                'uniersity_email@gmail.com', # Unversitetning rasmiy emaili kerak
                [student.email],
                fail_silently=False
            )



