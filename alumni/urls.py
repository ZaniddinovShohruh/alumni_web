from django.urls import path, include
from django.contrib import admin
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns=[
    path('user/users_create/', UserCreateView.as_view(), name='user_create'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth//token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('ProfActivities/', ProfActivityView.as_view(), name='ProfActivity'),
    path('ProfActivities/update_ProfActivities/<int:pk>', ProfActivityUpdateView.as_view(), name='ProfActivity_update'),
    path('ProfActivities/delete_ProfActivities/<int:pk>', ProfActivityDeleteView.as_view(), name='ProfActivity_delete'),
    path('ProfActivities/get_ProfActivities/', ProfActivityListView.as_view(), name='ProfActivity_get'),
    path('Academic_info/', AcademicInfoView.as_view(), name = 'Academic_info'),
    path('Academic_info/get_Academic_info/', AcademicInfoListView.as_view(), name = 'Academic_get'),
    path('Academic_info/update_Academic_info/<int:pk>', AcademicInfoUpdateView.as_view(), name = 'Academic_update'),
    path('Academic_info/delete_Academic_info/<int:pk>', AcademicInfoDeleteView.as_view(), name = 'Academic_delete'),
    path('user/get_user/', UserListView.as_view(), name = 'get_user'),
    path('user/update_user/<int:pk>', UserUpdateView.as_view(), name = 'update_user'),
    path('user/user/delete/<int:pk>', UserDeleteView.as_view(), name='delete_user'),
    path('pdf_download/', FormPDFView.as_view(), name='pdf_download'),
    path('students/debt/send-notification', StudentDebtView.as_view(), name='students-with-debt'),

]
