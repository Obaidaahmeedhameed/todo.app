
from django.urls import path
from django.contrib.auth import views as auth_views

from todo import views


app_name = "todo"
urlpatterns = [
    path('', views.home_page, name="home" ),
    path('login/', auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login" ),
    path('logout/', auth_views.LogoutView.as_view(), name="logout" ),
]
