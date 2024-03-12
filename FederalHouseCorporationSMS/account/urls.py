from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', include('django.contrib.auth.urls')),
    path('home/', views.homepage, name='homepage'),
    path('profile/', views.profile, name='profile'),
    path('profile/password/', views.change_password, name='change_password'),
    path('user/', views.user_list, name='user'),
    path('user/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('user/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('user/delete-done/<int:user_id>/', views.delete_user_done, name='delete_user_done'),
    path('user_register/', views.user_register, name='user_register'),
    path('user_register_csv/', views.user_register_csv, name='user_register_csv'),
]