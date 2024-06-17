from django.urls import path
from .views import task_views
from .views import session_views

urlpatterns = [
  path('tasks/', task_views.Collection.as_view(), name='tasks_list'),
  path('tasks/<int:id>/', task_views.Member.as_view(), name='task_detail'),
  path('login', session_views.login, name='login'),
]