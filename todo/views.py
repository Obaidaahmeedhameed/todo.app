from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView,DeleteView,UpdateView
from django.urls import reverse_lazy
#from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth.mixins import UserPassesTestMixin

from todo.forms import RegistrationForm, TaskCreateForm,TaskUpdateForm
#from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth import login
# Imports for Reordering Feature
#from django.views import View
#from django.shortcuts import redirect
#from django.db import transaction

from .models import Task


class TaskListView(ListView):
    model = Task
    template_name = 'todo/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user.id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        
        context['count'] = queryset.filter(complete=False, user=self.request.user.id).count()

        search_input = self.request.GET.get('search', None)
        if search_input:
            context['tasks'] = queryset.filter(title__contains=search_input)

        context['search_input'] = search_input

        return context

class UserCreateView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('todo:login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs) 

    def form_valid(self, form):
        # Success message 
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Registration was successful'
        ) 
        return super().form_valid(form)



class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    success_url = reverse_lazy('todo:task-list')
    form_class=TaskCreateForm
    template_name='todo/task_create.html'

    def form_valid(self, form):
        form.instance.user=self.request.user

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Task Created!'
        ) 
        return super().form_valid(form)

        
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('todo:task-list')
    template_name='todo/task_confirm_delete.html'
    context_object_name = 'task'

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.ERROR,
            'Task Deleted!'
        )         
        return super().form_valid(form)



class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    success_url = reverse_lazy('todo:task-list')
    form_class=TaskUpdateForm
    template_name='todo/task_update.html'

    def form_valid(self, form):
        #form.instance.user=self.request.user

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Task Updated!'
        ) 
        return super().form_valid(form)


    def test_func(self):
        return self.request.user == self.get_object().user