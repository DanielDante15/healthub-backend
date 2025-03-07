from rest_framework import serializers
from ..models import * 

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