from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status,filters
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import PlanSerializer, HabitSerializer
from .models import Plan, Habit

class PlanViewSet(ModelViewSet):
    serializer_class = PlanSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter]
    ordering_fields = ['start_time', 'end_time']
    search_fields = ['title']
    filterset_fields = ['status']

    def get_queryset(self):
        return Plan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
       serializer.save(user=self.request.user)

    @action(methods=['PATCH'],detail=True)
    def doing(self, request, *args, **kwargs):
        plan = self.get_object()
        plan.mark_as_doing()
        serializer = PlanSerializer(plan)
        return Response(data=serializer.data)

    @action(methods=['PATCH'],detail=True)
    def done(self, request, *args, **kwargs):
        plan = self.get_object()
        plan.mark_as_done()
        serializer = PlanSerializer(plan)
        return Response(data=serializer.data)

    @action(methods=['PATCH'],detail=True)
    def pending(self, request, *args, **kwargs):
        plan = self.get_object()
        plan.mark_as_pending()
        serializer = PlanSerializer(plan)
        return Response(data=serializer.data)

    @action(methods=['PATCH'],detail=True)
    def returned(self, request, *args, **kwargs):
        plan = self.get_object()
        plan.mark_as_returned()
        serializer = PlanSerializer(plan)
        return Response(data=serializer.data)
    
# patch ishlamadi
# habit yaratishda choice ishlamayapdi, yaratilmadi habit
class HabitViewSet(ModelViewSet):
    serializer_class = HabitSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,]
    search_fields = ['name']
    filterset_fields = ['finished']
    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
       serializer.save(user=self.request.user)
    
    @action(methods=['PATCH'],detail=True)
    def finished(self, request, *args, **kwargs):
        habit = self.get_object()
        habit.mark_as_finished()
        serializer = HabitSerializer(habit)
        return Response(data=serializer.data)
    
    @action(methods=['PATCH'],detail=True)
    def unfinished(self, request, *args, **kwargs):
        habit = self.get_object()
        habit.mark_as_unfinished()
        serializer = HabitSerializer(habit)
        return Response(data=serializer.data)