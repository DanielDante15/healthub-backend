from django.urls import path
from .views import *

urlpatterns = [
    # Auth
    path('login', login_user, name='login'),
    # Users
    path('users/register', register_user, name='register'),
    path('users', get_user, name='get_user'),
    path('users/<int:user_id>', manage_user, name='manage_user'),
    # Appointments
    
    path('appointments/create', create_appointment, name='create_appointment'),
    path('appointments', list_appointments, name='list_appointments'),
    path('appointments/<int:appointment_id>', manage_appointment, name='get_appointment'),
  
]

