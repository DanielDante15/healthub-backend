from rest_framework import serializers
from .models import * 
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'age', 'height','role']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)
    
class AppointmentSerializer(serializers.ModelSerializer):
    class UserSummarySerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['name', 'email']  

    user_common = UserSummarySerializer()
    user_specialist = UserSummarySerializer()

    class Meta:
        model = Appointment
        fields = [
            'id', 'user_common', 'user_specialist', 'date_time', 
            'duration', 'address_or_link', 'is_online', 'status'
        ]

    


class ServiceSerializer(serializers.ModelSerializer):
    specialist_email = serializers.EmailField(write_only=True)
    specialist = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'specialist_email', 'specialist', 'title', 'description', 'duration', 'price', 'service_type']
        read_only_fields = ['id', 'specialist']

    def validate_specialist_email(self, value):
        try:
            specialist = User.objects.get(email=value)
            if specialist.role not in [User.PERSONAL_TRAINER, User.NUTRITIONIST]:
                raise serializers.ValidationError("The specialist must be a Personal Trainer or Nutritionist.")
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email.")
        return specialist

    def create(self, validated_data):
        specialist = validated_data.pop('specialist_email')
        validated_data['specialist'] = specialist
        return super().create(validated_data)

    def get_specialist(self, obj):
        if obj.specialist:
            return obj.specialist.email 
        return None


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


class DietPlanSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField(read_only=True)
    nutri_email = serializers.SerializerMethodField(read_only=True)
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
        return user

    def validate_nutri_email(self, value):
        try:
            nutri = User.objects.get(email=value)
            if nutri.role != User.NUTRITIONIST:
                raise serializers.ValidationError("The nutritionist must have the 'nutri' role.")
        except User.DoesNotExist:
            raise serializers.ValidationError("No nutritionist found with this email.")
        return nutri

    def create(self, validated_data):
        user = validated_data.pop('user_email')
        nutri = validated_data.pop('nutri_email')
        meals = validated_data.pop('meals')
        diet_plan = DietPlan.objects.create(user=user, nutri=nutri, **validated_data)
        diet_plan.meals.set(meals)
        return diet_plan

    def get_user_email(self, obj):
        return obj.user.email if obj.user else None

    def get_nutri_email(self, obj):
        return obj.nutri.email if obj.nutri else None




class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ["id","name","description","weight","workout"]


class WorkoutSerializer(serializers.ModelSerializer):
    class ExerciseSumarySerializer(serializers.ModelSerializer):
        class Meta:
            model = Exercise
            fields = ['name', 'description','weight']
            
    exercises = ExerciseSumarySerializer(many=True, read_only=True)

    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'exercises']


class WorkoutPlanSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(write_only=True)
    personal_email = serializers.EmailField(write_only=True)
    workouts = serializers.PrimaryKeyRelatedField(queryset=Workout.objects.all(), many=True, write_only=True)
    workouts_list = WorkoutSerializer(source='workouts', many=True, read_only=True)

    class Meta:
        model = WorkoutPlan
        fields = [
            'id', 'name', 'user_email', 'personal_email', 'workouts', 'workouts_list'
        ]

    def create(self, validated_data):
        user_email = validated_data.pop('user_email')
        personal_email = validated_data.pop('personal_email')

        # Fetch user and validate roles
        try:
            user = User.objects.get(email=user_email)
            if user.role != User.COMMON:
                raise serializers.ValidationError("The user must have the 'common' role.")
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email.")

        try:
            personal = User.objects.get(email=personal_email)
            if personal.role != User.PERSONAL_TRAINER:
                raise serializers.ValidationError("The personal must have the 'personal' role.")
        except User.DoesNotExist:
            raise serializers.ValidationError("No personal found with this email.")

        # Create WorkoutPlan and associate workouts
        workouts = validated_data.pop('workouts')
        workout_plan = WorkoutPlan.objects.create(user=user, personal=personal, **validated_data)
        workout_plan.workouts.set(workouts)
        return workout_plan

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user_email'] = instance.user.email if instance.user else None
        representation['personal_email'] = instance.personal.email if instance.personal else None
        return representation
    