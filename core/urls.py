from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'services-by-specialist', ServiceBySpecialistViewSet, basename='services-by-specialist')


urlpatterns = [
    path('', include(router.urls)),
    
    # Auth
    path('login', login_user, name='login'),
    
    # Users
    path('users/register', register_user, name='register'),
    path('users', get_user, name='get_user'),
    path('users/specialists', get_specialists, name='get_specialist'),
    path('users/<int:user_id>', manage_user, name='manage_user'),
    
    # Appointments
    path('appointments/create', create_appointment, name='create_appointment'),
    path('appointments', list_appointments, name='list_appointments'),
    path('appointments/<int:appointment_id>', manage_appointment, name='get_appointment'),
    
    path('services', list_services, name='list_services'),
    path('services/create', create_service, name='create_service'), 
    path('services/<int:service_id>', manage_service, name='manage_service'), 
    
    # ============================= DIETS ============================ #
    path('diets', list_diets, name='list-diets'),
    path('diets/create', create_diet, name='create-diet'),
    path('diets/<int:diet_id>', manage_diet, name='manage-diet'),

    # ============================= MEALS ============================ #
    path('meals', list_meals, name='list-meals'),
    path('meals/create', create_meal, name='create-meal'),
    path('meals/<int:meal_id>', manage_meal, name='manage-meal'),

    # ============================= ITEMS ============================ #
    path('items', list_items, name='list-items'),
    path('items/create', create_item, name='create-item'),
    path('items/<int:item_id>', manage_item, name='manage-item'),
    
    # ============================= WORKOUT PLANS ============================ #
    path('workout-plans', list_workout_plans, name='list-workout-plans'),
    path('workout-plans/create', create_workout_plan, name='create-workout-plan'),
    path('workout-plans/<int:workout_id>', manage_workout_plan, name='manage-workout-plan'),

    # ============================= WORKOUT ============================ #
    path('workouts', list_workouts, name='list-workout'),
    path('workouts/create', create_workout, name='create-workout'),
    path('workouts/<int:workout_id>', manage_workouts, name='manage-workout'),

    # ============================= EXERCISES ============================ #
    path('exercises', list_exercises, name='list-items'),
    path('exercises/create', create_exercise, name='create-exercise'),
    path('exercises/<int:exercise_id>', manage_exercise, name='manage-exercise'),
]

