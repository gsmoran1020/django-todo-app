from django.urls import path
from .views import TaskList, TaskCreate, TaskUpdate, TaskDelete, TaskLogin, LogoutView, TaskRegister

urlpatterns = [
    path('login/', TaskLogin.as_view(), name='todo-login'),
    path('logout/', LogoutView.as_view(next_page='todo-login'), name='todo-logout'),
    path('register/', TaskRegister.as_view(), name='todo-register'),
    path('', TaskList.as_view(), name='todo-list'),
    path('create/', TaskCreate.as_view(), name='todo-create'),
    path('update/task/<int:pk>/', TaskUpdate.as_view(), name='todo-update'),
    path('delete/task/<int:pk>/', TaskDelete.as_view(), name='todo-delete')
]
