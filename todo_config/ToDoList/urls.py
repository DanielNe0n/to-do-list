from django.urls import path
from .views import *


urlpatterns = [
    path('', Index.as_view(), name='index'),
    

    #CRUD
    path('create/', CreateTask.as_view(), name='create_task'),
    path('all/', TaskList.as_view(), name='task_list'),

    path('<int:pk>/detail/', TaskDetails.as_view(), name='task_details'),
    path('<int:pk>/delete/', DeleteTask.as_view(), name='delete_task'),
    path('<int:pk>/edit/', EditTask.as_view(), name='edit_task'),

    #auth
    path('register/', UserRegister.as_view(), name='register'),
     path('activation/<uidb64>/<token>/', UserVerification.as_view(), name='activation'),
    path('login/', UserLogin.as_view(), name='login'),
     path('logout/', UserLogout.as_view(), name='logout'),

    #forgot password
    path('forgot-password/', ForgotPassword.as_view(), name='forgot_password'),
    path('reset-password/<uidb>/<token>/', ResetPassword.as_view(), name='reset_password'),

    #search
    path('searched/', Searched.as_view(), name='searched'),
    
]
