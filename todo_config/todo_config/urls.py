from django.urls import path, include
from django.contrib import admin

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),

    #apps
    path('', include('ToDoList.urls')),
    path('api/', include('todo_api.urls')),

    #external applications
    path('captcha/', include('captcha.urls')),
]

if settings.DEBUG == True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
