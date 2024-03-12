from django.urls import path, include
from . import views

urlpatterns = [    
    path('index/', views.homepage, name='homepage'),
    path('send/', views.send_sms, name='send_sms'),
    path('list/', views.sms_list, name='sms_list'),
    path('filter/', views.sms_filter, name='sms_filter'),
    path('detail/<int:sms_id>/', views.sms_detail, name='sms_detail'),
    path('sms/delete/<int:sms_id>/', views.delete_sms, name='delete_sms'),
    path('sms/delete-done/<int:sms_id>/', views.delete_sms_done, name='delete_sms_done'),
   
]