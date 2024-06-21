from django.urls import path
from .views import task_views
from .views import team_views
from .views import session_views
#  path('invitation/<str:code>/<str:action>', .as_view(), name='invitation_code'),

urlpatterns = [
  path('teams/', team_views.Collection.as_view(), name='teams'),
  path('teams/<int:id>/invite', team_views.Invitation.as_view(), name='team_invite'),
  path('tasks/', task_views.Collection.as_view(), name='tasks'),
  path('tasks/new/', task_views.Collection.as_view(), name='tasks_new'),
  path('tasks/<int:id>/', task_views.Member.as_view(), name='task'),
  path('tasks/<int:id>/edit/', task_views.Member.as_view(), name='tasks_edit'),
  path('login/', session_views.login, name='login'),
  path('logout/', session_views.logout, name='logout'),
]