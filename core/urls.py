from django.urls import path, include
from .views import userView, workoutView,serviceView,appointmentView,dietView,mealView, infoView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'services-by-specialist', serviceView.ServiceBySpecialistViewSet, basename='services-by-specialist')
router.register(r'appointments-by-user', appointmentView.AppointmentsByUserEmail, basename='appointments-by-user')
router.register(r'diet-plans-by-user', dietView.DietPlanByUserEmailView, basename='diet-plans-by-user')


urlpatterns = [
    path('', include(router.urls)),
    # Auth
    path('login', userView.login_user, name='login'),
    # Users
    path('users/register', userView.register_user, name='register'),
    path('users', userView.get_user, name='get_user'),
    path('users/specialists', userView.get_specialists, name='get_specialist'),
    path('users/<int:user_id>', userView.manage_user, name='manage_user'),
    
    # Appointments
    path('appointments/create', appointmentView.create_appointment, name='create_appointment'),
    path('appointments', appointmentView.list_appointments, name='list_appointments'),
    path('appointments/<int:appointment_id>', appointmentView.manage_appointment, name='get_appointment'),
    
    path('services', serviceView.list_services, name='list_services'),
    path('services/create', serviceView.create_service, name='create_service'), 
    path('services/<int:service_id>', serviceView.manage_service, name='manage_service'), 
    
    # ============================= DIETS ============================ #
    path('diets', dietView.list_diets, name='list-diets'),
    path('diets/create', dietView.create_diet, name='create-diet'),
    path('diets/<int:diet_id>', dietView.manage_diet, name='manage-diet'),

    # ============================= MEALS ============================ #
    path('meals', mealView.list_meals, name='list-meals'),
    path('meals/create', mealView.create_meal, name='create-meal'),
    path('meals/<int:meal_id>', mealView.manage_meal, name='manage-meal'),

    # ============================= ITEMS ============================ #
    path('items', mealView.list_items, name='list-items'),
    path('items/create', mealView.create_item, name='create-item'),
    path('items/<int:item_id>',mealView.manage_item, name='manage-item'),
    # ============================= SPECIALIST INFO ============================ #
    path('infos', infoView.list_items, name='list-items'),
    path('infos/create', infoView.create_item, name='create-item'),
    path('infos/<int:item_id>',infoView.manage_item, name='manage-item'),
    
    # ============================= WORKOUT PLANS ============================ #
    path('workout-plans', workoutView.list_workout_plans, name='list-workout-plans'),
    path('workout-plans/create',  workoutView.create_workout_plan, name='create-workout-plan'),
    path('workout-plans/<int:workout_id>',  workoutView.manage_workout_plan, name='manage-workout-plan'),

    # ============================= WORKOUT ============================ #
    path('workouts',  workoutView.list_workouts, name='list-workout'),
    path('workouts/create',  workoutView.create_workout, name='create-workout'),
    path('workouts/<int:workout_id>',  workoutView.manage_workouts, name='manage-workout'),

    # ============================= EXERCISES ============================ #
    path('exercises',  workoutView.list_exercises, name='list-items'),
    path('exercises/create',workoutView.create_exercise, name='create-exercise'),
    path('exercises/<int:exercise_id>',  workoutView.manage_exercise, name='manage-exercise'),
]

