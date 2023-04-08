from django.urls import path, include

from rest_framework import routers

from .views import *


app_name = 'api'

router = routers.SimpleRouter(trailing_slash=False)
router.register('task', TaskViewSet)

urlpatterns = [
    path('info/', ApiInfo.as_view(), name='api-info'),
    path('v1/', include(router.urls)),
]
