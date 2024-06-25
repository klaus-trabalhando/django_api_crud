from django.urls import path
from .views import task_views
from .views import team_views
from .views import session_views
from .views import invitation_views
from .views import swagger

urlpatterns = [
  path('swagger-ui/', swagger.swagger_ui, name='swagger-ui'),
  path('swagger.yaml', swagger.swagger_spec, name='swagger-spec'),
  path('teams/', team_views.Collection.as_view(), name='teams'),
  path('teams/<int:id>/invite', team_views.Invitation.as_view(), name='team_invite'),
  path('invitation/<str:code>/<str:action>', invitation_views.Member.as_view(), name='invitation_code'),
  path('tasks/', task_views.Collection.as_view(), name='tasks'),
  path('tasks/new/', task_views.Collection.as_view(), name='tasks_new'),
  path('tasks/<int:id>/', task_views.Member.as_view(), name='task'),
  path('tasks/<int:id>/edit/', task_views.Member.as_view(), name='tasks_edit'),
  path('login/', session_views.login, name='login'),
  path('logout/', session_views.logout, name='logout'),
]