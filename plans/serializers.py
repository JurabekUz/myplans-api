from dataclasses import field
from rest_framework.serializers import ModelSerializer

from .models import Plan, Habit

class PlanSerializer(ModelSerializer):
    class Meta:
        model = Plan
        fields = ('title', 'description', 'start_time', 'end_time', 'status')

class HabitSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = ('name', 'repeat', 'part_day', 'finished')
        
