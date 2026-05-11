from django.urls import path
from . import views

urlpatterns = [
    # redirect root to genders
    path('', views.GendersList, name='home'),

    # Gender
    path('genders/',                 views.GendersList,  name='GendersList'),
    path('genders/add/',             views.AddGender,    name='AddGender'),
    path('genders/edit/<int:pk>/',   views.EditGender,   name='EditGender'),
    path('genders/delete/<int:pk>/', views.DeleteGender, name='DeleteGender'),

    # Users
    path('users/',                   views.UsersList,    name='UsersList'),
    path('users/add/',               views.AddUser,      name='AddUser'),
    path('users/edit/<int:pk>/',     views.EditUser,     name='EditUser'),
    path('users/delete/<int:pk>/',   views.DeleteUser,   name='DeleteUser'),
]