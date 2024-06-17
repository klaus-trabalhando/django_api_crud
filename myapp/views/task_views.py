from ..models.task import Task
from .base_collection import BaseCollection
from .base_member import BaseMember
from .session_views import require_authenticated_user

# curl -H "Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3MTg3NDA1MzQsImlhdCI6MTcxODY1NDEzNH0.t0OtcbQ-G7N1-OfqSRADk5u-kwOKt-Yjke2YE_6N3Xw" http://127.0.0.1:8000/tasks/
class Collection(BaseCollection):
  model = Task

  @require_authenticated_user
  def get(self, request):
    return super().get(request)

  @require_authenticated_user
  def post(self, request):
    return super().post(request)

  @property
  def required_fields(self):
    return ['title', 'content']

  def serializer(self, obj):
    return task_serialized(obj)

class Member(BaseMember):
  model = Task

  @property
  def required_fields(self):
    return ['title', 'content']

  def serializer(self, obj):
    return task_serialized(obj)

def task_serialized(task):
  return {'id': task.id, 'title': task.title, 'content': task.content}