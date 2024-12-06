# Generated by Django 4.2.16 on 2024-11-22 01:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_service'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MealItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('qtd', models.CharField(max_length=255)),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='core.meal')),
            ],
        ),
        migrations.CreateModel(
            name='DietPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('meals', models.ManyToManyField(blank=True, related_name='diet_plans', to='core.meal')),
                ('nutri', models.ForeignKey(limit_choices_to={'role': 'nutri'}, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_diet_plans', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(limit_choices_to={'role': 'common'}, on_delete=django.db.models.deletion.CASCADE, related_name='user_plans', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
