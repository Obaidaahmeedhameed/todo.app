
from django.urls import path
from django.contrib.auth import views as auth_views

from todo import views


app_name = "todo"
urlpatterns = [
    path('', views.TaskListView.as_view(), name="task-list" ),
    path('login/', auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login" ),
    path('logout/', auth_views.LogoutView.as_view(), name="logout" ),
    path('registration/', views.UserCreateView.as_view(), name="registration" ),
    path('create/', views.TaskCreateView.as_view(), name="task-create" ),
    path('delete/<int:pk>', views.TaskDeleteView.as_view(), name="task-delete" ),
    path('update/<int:pk>', views.TaskUpdateView.as_view(), name="task-update" ),

]
