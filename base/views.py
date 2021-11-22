from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Task


class TaskLogin(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('todo-list')


class TaskRegister(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('todo-list')

    def form_valid(self, form): # This is overridden for the purpose of saving our user on creation.
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(TaskRegister, self).form_valid(form)

    def get(self, request, *args, **kwargs): # This is overridden for the purpose of redirecting a user that is already logged in
        if request.user.is_authenticated:
            return redirect('todo-list')
        return super(TaskRegister, self).get(request, *args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'base/task_list.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        # Getting all tasks for the current user
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)

        # Task Search by getting the value of 'search-area' element and filtering the already acquired users tasks.
        search_input = self.request.GET.get("search-area") or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)
        context['search_input'] = search_input
        return context


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description']
    template_name = 'base/task_create.html'
    success_url = reverse_lazy('todo-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    template_name = 'base/task_update.html'
    success_url = reverse_lazy('todo-list')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task_confirm_delete.html'
    success_url = reverse_lazy('todo-list')
