from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import *
from rest_framework import *
from rest_framework.mixins import *

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render

from .serializers import TaskSerializer
from ToDoList.models import Task


class ApiInfo(LoginRequiredMixin, View):

    def get(self, request):
        token, created = Token.objects.get_or_create(user=request.user)
        return render(request, 'todo_api/api_info.html', {'token':token.key})



class TaskViewSet(CreateModelMixin,
                  ListModelMixin,
                  DestroyAPIView,
                  UpdateAPIView,
                  GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    authentication_classes = (TokenAuthentication, )

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


