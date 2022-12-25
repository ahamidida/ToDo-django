from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import TaskList

class CustomLoginView(LoginView):
    template_name='base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name='base/register.html'
    form_class=UserCreationForm
    redirect_authenticated_user = True
    success_url=reverse_lazy('tasks')

    def form_valid(self,form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage,self).get(*args,**kwargs)

class Task(LoginRequiredMixin,ListView):
    model = TaskList
    context_object_name='tasks'
    template_name='base/tasklist.html'
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['tasks']=context['tasks'].filter(user=self.request.user)
        context['count']=context['tasks'].filter(complete_status=False).count

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        
        context['search_input']=search_input

        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    context_object_name='task'
    template_name='base/task.html'
    model=TaskList

class TaskCreate(LoginRequiredMixin,CreateView):
    model=TaskList
    fields=['title','caption','complete_status']
    success_url=reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(TaskCreate,self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model=TaskList
    fields=['title','caption','complete_status']
    success_url=reverse_lazy('tasks')
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(TaskUpdate,self).form_valid(form)

class TaskDelete(LoginRequiredMixin,DeleteView):
    model=TaskList
    success_url=reverse_lazy('tasks')