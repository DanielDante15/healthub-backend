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
        # Ensure the superuser gets a role as 'common' or any other desired role
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
    user_common = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Refere-se ao modelo de usuário definido, no seu caso seria o modelo User
        on_delete=models.CASCADE,
        related_name='common_appointments',
        limit_choices_to={'role': User.COMMON},  # Garante que o usuário seja do tipo 'common'
    )
    user_specialist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='specialist_appointments',
        limit_choices_to=models.Q(role=User.PERSONAL_TRAINER) | models.Q(role=User.NUTRITIONIST),  # Garantindo que o especialista seja 'personal' ou 'nutri'
    )
    date_time = models.DateTimeField()  # Data e hora do agendamento
    duration = models.DurationField()  # Duração do agendamento (por exemplo, 1 hora)

    def __str__(self):
        return f"Appointment with {self.user_specialist} for {self.user_common} on {self.date_time}"
