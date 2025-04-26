from rest_framework import serializers

from config.settings import EMAIL_HOST_USER
from .models import CustomUser, User, AcademicInfo, ProfActivity, Notification
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail




class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','student_id','date_of_birth','nationality','phone','password','address','photo','cv','username']


    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])  # ✅ Hash the password
        return super().create(validated_data)

class AcademicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicInfo
        fields = ['faculty', 'year_of_admission', 'graduation_year', 'diploma_number', 'contract_type']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



class ProfActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfActivity
        fields = ['current_work','future_goal']

        def validate(self, attrs):
            print = (attrs)
            Profctivity = ProfActivity(
                current_work = attrs('current_work'),
                future_goal = attrs('future_goal'),
            )
            Profctivity.save()
            return super().validate(attrs)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone']

class PersonalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicInfo
        fields = ['faculty', "graduation_year", "contract_total", "contract_paid"]



class StudentHasDebt(serializers.ModelSerializer):
    personal_information = UserSerializer()
    debt_amount = serializers.SerializerMethodField()

    class Meta:
        model = AcademicInfo
        fields = ["personal_information", "faculty", "graduation_year", "contract_total", "contract_paid", "debt_amount"]

    def get_debt_amount(self, obj):
        debt = float(obj.contract_total - obj.contract_paid)
        print(debt)
        print(obj.personal_information.email)
        if debt < 0:
            send_mail(
                subject="Eslatma: Qarz mavjud",
                message=f"""Assalomu alaykum, {obj.personal_information.first_name}!
                            Bizning tizim bo‘yicha sizda {debt} so‘m qarz mavjud.
                            Iltimos, to‘lovni imkon qadar tezroq amalga oshiring!
                            Hurmat bilan,
                            Turin Polytechnic University in Tashkent .
                            """,
                from_email=EMAIL_HOST_USER,
                recipient_list=[obj.personal_information.email],
                fail_silently=False
            )
        return debt


