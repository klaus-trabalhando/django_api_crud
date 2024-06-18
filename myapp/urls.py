from django.urls import path
from .views import task_views
from .views import session_views

urlpatterns = [
  path('tasks/', task_views.Collection.as_view(), name='tasks'),
  path('tasks/new/', task_views.Collection.as_view(), name='tasks_new'),
  path('tasks/<int:id>/', task_views.Member.as_view(), name='task_detail'),
  path('login/', session_views.login, name='login'),
  path('logout/', session_views.logout, name='logout'),
]