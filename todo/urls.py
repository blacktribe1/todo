from django.urls import path
from .views import home,loginPage,register, delete_task, update_task,logout_user

urlpatterns = [
    path('', home, name='home'),
    path('login', loginPage, name='login'),
    path('register', register, name='register'),
    path('delete-task/<str:name>', delete_task, name='delete-task'),
    path('update-task/<str:name>', update_task, name='update-task'),
    path('logout', logout_user, name='logout')
]