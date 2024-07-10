from django.urls import path
from .views import add_patient,add_health_info,about,home,chandoanBN,member,chuandoanBN2

urlpatterns = [
    path('', home,name='home'),
    path('About/', about, name='About'),
    path('PatientInformation/',add_patient,name='PatientInformation'),
    path('PatientDiagnosis/',chandoanBN,name="PatientDiagnosis"),
    path('LoadInfo/',chuandoanBN2,name='LoadInfo'),
    path('Member',member,name='Member'),
    path('AddHealthInfo/', add_health_info, name='AddHealthInfo'),
]