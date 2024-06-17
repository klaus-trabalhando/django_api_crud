from ..models.task import Task
from .base_collection import BaseCollection
from .base_member import BaseMember

class Collection(BaseCollection):
  model = Task

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