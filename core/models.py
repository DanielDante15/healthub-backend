from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings



## USER
class UserManager(BaseUserManager):
    def create_user(self, email, password, role='common', **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, role='common', **extra_fields)

class User(AbstractBaseUser):
    COMMON = 'common'
    PERSONAL_TRAINER = 'personal'
    NUTRITIONIST = 'nutri'

    ROLE_CHOICES = [
        (COMMON, 'Common User'),
        (PERSONAL_TRAINER, 'Personal Trainer'),
        (NUTRITIONIST, 'Nutritionist'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    age = models.IntegerField()
    height = models.FloatField()

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=COMMON,
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


## Appointment


class Appointment(models.Model):
    
    CANCELED = 'canceled'
    ACCEPTED = 'accepted'
    SCHEDULED = 'scheduled'

    STATUS_CHOICES = [
        (CANCELED, 'Canceled'),
        (ACCEPTED, 'Accepted'),
        (SCHEDULED, 'Scheduled'),
    ]
    
    
    user_common = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='common_appointments',
        limit_choices_to={'role': User.COMMON}, 
    )
    user_specialist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='specialist_appointments',
        limit_choices_to=models.Q(role=User.PERSONAL_TRAINER) | models.Q(role=User.NUTRITIONIST),
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=SCHEDULED,
    )
    address_or_link = models.CharField(max_length=255,blank=True,null=True)
    is_online  = models.BooleanField(default=False)
    date_time = models.DateTimeField()  
    duration = models.DurationField()

    def __str__(self):
        return f"Appointment with {self.user_specialist} for {self.user_common} on {self.date_time}"


class Service(models.Model):
    TITLE_MAX_LENGTH = 255

    ONLINE = 'online'
    IN_PERSON = 'in_person'
    
    SERVICE_TYPE_CHOICES = [
        (ONLINE, 'Online'),
        (IN_PERSON, 'In Person'),
    ]

    specialist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='services',
        limit_choices_to=models.Q(role=User.PERSONAL_TRAINER) | models.Q(role=User.NUTRITIONIST),
    )

    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    description = models.TextField()
    duration = models.DurationField() 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    service_type = models.CharField(
        max_length=20,
        choices=SERVICE_TYPE_CHOICES,
        default=ONLINE,
    )

    def __str__(self):
        return f"{self.title} - {self.specialist.name}"
    
    
class DietPlan(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='user_plans',
        limit_choices_to={'role': User.COMMON}, 
    )
    nutri = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assigned_diet_plans',
        limit_choices_to={'role': User.NUTRITIONIST},
    )
    meals = models.ManyToManyField(
        'Meal',
        related_name='diet_plans',
        blank=True 
    )

    def __str__(self):
        return f"Diet Plan: {self.name} for {self.user.name} by {self.nutri.name}"



class Meal(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class MealItem(models.Model):
    meal = models.ForeignKey(
        Meal, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    name = models.CharField(max_length=255)
    qtd = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.qtd}"


class WorkoutPlan(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='user_workout_plans',
        limit_choices_to={'role': User.COMMON}, 
    )
    personal = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assigned_workout_plans',
        limit_choices_to={'role': User.PERSONAL_TRAINER},
    )
    workouts = models.ManyToManyField(
        'Workout',
        related_name='workout_plans',
        blank=True 
    )

    def __str__(self):
        return f"Workout Plan: {self.name} for {self.user.name} by {self.personal.name}"



class Workout(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Exercise(models.Model):
    workout = models.ForeignKey(
        Workout, 
        on_delete=models.CASCADE, 
        related_name='exercises'
    )
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)

    def __str__(self):
        return f"{self.name} - {self.description}"
    

