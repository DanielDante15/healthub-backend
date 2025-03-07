from rest_framework import serializers
from ..models import *


class MealItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealItem
        fields = ['id', 'meal', 'name', 'qtd']


class MealSerializer(serializers.ModelSerializer):
    class MealSummaryItemSerializer(serializers.ModelSerializer):
        class Meta:
            model = MealItem
            fields = ['name', 'qtd']
            
    items = MealSummaryItemSerializer(many=True, read_only=True)

    class Meta:
        model = Meal
        fields = ['id', 'name', 'description', 'items']


class DietPlanSerializerCreate(serializers.ModelSerializer):
    user_email = serializers.EmailField(write_only=True, required=True)
    nutri_email = serializers.EmailField(write_only=True, required=True)
    meals = serializers.PrimaryKeyRelatedField(queryset=Meal.objects.all(), many=True, write_only=True)
    meals_list = MealSerializer(source='meals', many=True, read_only=True)

    class Meta:
        model = DietPlan
        fields = [
            'id', 'name', 'user_email', 'nutri_email', 'meals', 'meals_list'
        ]

    def validate_user_email(self, value):
        try:
            user = User.objects.get(email=value)
            if user.role != User.COMMON:
                raise serializers.ValidationError("The user must have the 'common' role.")
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email.")
        return value  # Retorna o email validado

    def validate_nutri_email(self, value):
        try:
            nutri = User.objects.get(email=value)
            if nutri.role != User.NUTRITIONIST:
                raise serializers.ValidationError("The nutritionist must have the 'nutri' role.")
        except User.DoesNotExist:
            raise serializers.ValidationError("No nutritionist found with this email.")
        return value  # Retorna o email validado

    def create(self, validated_data):
        user_email = validated_data.pop('user_email')
        nutri_email = validated_data.pop('nutri_email')
        meals = validated_data.pop('meals')

        # Buscar os usuários com base no email
        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"user_email": "User with this email does not exist."})

        try:
            nutri = User.objects.get(email=nutri_email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"nutri_email": "Nutritionist with this email does not exist."})

        # Criar o plano de dieta
        diet_plan = DietPlan.objects.create(user=user, nutri=nutri, **validated_data)
        diet_plan.meals.set(meals)
        return diet_plan
    
    
class DietPlanSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(write_only=True, required=True)
    nutri_email = serializers.EmailField(write_only=True, required=True)
    meals = serializers.PrimaryKeyRelatedField(queryset=Meal.objects.all(), many=True, write_only=True)
    meals_list = MealSerializer(source='meals', many=True, read_only=True)

    class Meta:
        model = DietPlan
        fields = [
            'id', 'name', 'user_email', 'nutri_email', 'meals', 'meals_list'
        ]

    def validate_user_email(self, value):
        try:
            user = User.objects.get(email=value)
            if user.role != User.COMMON:
                raise serializers.ValidationError("The user must have the 'common' role.")
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email.")
        return value  # Retorna o email validado

    def validate_nutri_email(self, value):
        try:
            nutri = User.objects.get(email=value)
            if nutri.role != User.NUTRITIONIST:
                raise serializers.ValidationError("The nutritionist must have the 'nutri' role.")
        except User.DoesNotExist:
            raise serializers.ValidationError("No nutritionist found with this email.")
        return value  # Retorna o email validado

    def create(self, validated_data):
        user_email = validated_data.pop('user_email')
        nutri_email = validated_data.pop('nutri_email')
        meals = validated_data.pop('meals')

        # Buscar os usuários com base no email
        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"user_email": "User with this email does not exist."})

        try:
            nutri = User.objects.get(email=nutri_email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"nutri_email": "Nutritionist with this email does not exist."})

        # Criar o plano de dieta
        diet_plan = DietPlan.objects.create(user=user, nutri=nutri, **validated_data)
        diet_plan.meals.set(meals)
        return diet_plan
