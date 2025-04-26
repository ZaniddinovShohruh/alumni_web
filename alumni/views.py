from django.contrib.auth.hashers import make_password
from rest_framework import generics
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import User, AcademicInfo, ProfActivity
from .permissions import UserPermission
from .serializers import (UserCreateSerializer, AcademicInfoSerializer, ProfActivitySerializer, StudentHasDebt)
from rest_framework.views import APIView
from django.http import FileResponse
import io
import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from requests import request
from reportlab.platypus import Image
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView



class FormPDFView(APIView):
    def get(self, request):
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
        textob = c.beginText()
        textob.setTextOrigin(inch, inch)

        student = User.objects.select_related("AcademicInfo", "ProfActivity").first()
        
        if not student:
            return FileResponse(buf, as_attachment=True, filename="no_student.pdf")

        user_data = [
            f"Name: {student.first_name} {student.last_name}",
            f"Student ID: {student.student_id}",
            f"Date of Birth: {student.date_of_birth}",
            f"Nationality: {student.nationality}",
            f"Phone: {student.phone}",
            f"Address: {student.address}",
            f"Email: {student.email}",
            f"Faculty: {student.faculty}",
            f"Year of Admission: {student.year_of_admission}",
            f"Graduation Year: {student.graduation_year}",
            f"Diploma Number: {student.diploma_number}",
            f"Contract Type: {student.contract_type}",
            f"Current Work: {student.current_work}",
            f"Future Goal: {student.future_goal}",
            "-" * 40
        ]

        for line in user_data:
            textob.textLine(line)

        c.drawText(textob)
        c.showPage()
        c.save()
        buf.seek(0)

        return FileResponse(buf, as_attachment=True,
                            filename=f"{student.last_name}_{student.first_name}_{student.id}.pdf")



class AcademicInfoView(generics.CreateAPIView):
    queryset = AcademicInfo.objects.all()
    serializer_class = AcademicInfoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(personal_information=self.request.user)

class AcademicInfoListView(generics.ListAPIView):
    serializer_class = AcademicInfoSerializer
    queryset = AcademicInfo.objects.all()


class AcademicInfoUpdateView(generics.UpdateAPIView):
    serializer_class = AcademicInfoSerializer
    queryset = AcademicInfo
    lookup_field = "id"

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class AcademicInfoDeleteView(generics.DestroyAPIView):
    queryset = AcademicInfo.objects.all()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)




class ProfActivityView(generics.CreateAPIView):
    '''ProfActivity View'''
    queryset = ProfActivity.objects.all()
    serializer_class = ProfActivitySerializer

class ProfActivityListView(generics.ListAPIView):
    queryset = ProfActivity.objects.all()
    serializer_class = ProfActivitySerializer

class ProfActivityUpdateView(generics.UpdateAPIView):
    serializer_class = ProfActivitySerializer
    queryset = ProfActivity.objects.all()
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class ProfActivityDeleteView(generics.DestroyAPIView):
    queryset = ProfActivity.objects.all()


    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)




class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    parser_classes = MultiPartParser, FormParser
    """User create View"""
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class UserListView(generics.ListAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [UserPermission]


class UserUpdateView(generics.UpdateAPIView):
        serializer_class = UserCreateSerializer

        def get_object(self):
            return self.request.user


        def get(self, request, *args, **kwargs):
            serializer = self.get_serializer(self.get_object())
            return Response(serializer.data)

        def perform_update(self, serializer):
            if "password" in serializer.validated_data:
                serializer.validated_data['password']=make_password(serializer.validated_data['password'])

        def patch(self, request, *args, **kwargs):
            return self.partial_update(request, *args, **kwargs)


class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

from django.db.models import F
from rest_framework import generics


class StudentDebtView(generics.ListAPIView):
    serializer_class = StudentHasDebt
    queryset = AcademicInfo.objects.filter(contract_total__lt=F('contract_paid'))


