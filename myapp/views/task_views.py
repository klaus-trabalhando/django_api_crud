from ..models.task import Task
from .base_collection import BaseCollection
from .base_member import BaseMember
from .session_views import require_authenticated_user
from django.shortcuts import get_object_or_404
from ..tasks import send_email_task
from django.http import JsonResponse

# curl -H "Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3MTg3NDA1MzQsImlhdCI6MTcxODY1NDEzNH0.t0OtcbQ-G7N1-OfqSRADk5u-kwOKt-Yjke2YE_6N3Xw" http://127.0.0.1:8000/tasks/
class Collection(BaseCollection):
  model = Task
  folder = 'tasks'

  @require_authenticated_user
  def new(self, request, current_user=None):
    return super().new(request)
  
  @require_authenticated_user
  def get(self, request, current_user=None):
    results = Task.search(query=request.GET.get('query', ''))
    result_data = {
      'total': results['hits']['total']['value'],
      'hits': [hit['_source'] for hit in results['hits']['hits']]
    }
    return JsonResponse(result_data, safe=False)

  @require_authenticated_user
  def post(self, request, current_user=None):
    return super().post(request, current_user)

  def base_filter(self, request, current_user):
    return self.model.objects.filter(user_id=current_user.id)
  
  def assign_attributes(self, request, current_user, data):
    data = super().assign_attributes(request, current_user, data)
    if current_user:
      data['user_id'] = int(current_user.id)
    return data

  @property
  def required_fields(self):
    return ['title', 'content']

  def serializer(self, obj):
    return task_serialized(obj)

class Member(BaseMember):
  model = Task
  folder = 'tasks'

  @require_authenticated_user
  def edit(self, request, current_user=None, id=None):
    return super().edit(request, current_user=current_user, id=id)

  @require_authenticated_user
  def get(self, request, id, current_user=None):
    return super().get(request, current_user, id)

  @require_authenticated_user
  def put(self, request, id, current_user=None):
    return super().put(request, current_user, id)

  @require_authenticated_user
  def delete(self, request, id, current_user=None):
    return super().delete(request, current_user, id)

  def get_object(self, request, current_user, id):
    return get_object_or_404(self.model, user_id=current_user.id, pk=id)

  def allowed_fields(self, request, current_user):
    fields = super().allowed_fields(request, current_user)
    fields['completed'] = fields.get('completed') == 'on'
    return fields
  
  def after_update(self, obj):
    if obj.completed != obj.completed_was and obj.completed:
      subject = f'Task {obj.title} has been completed'
      from_email = 'klaus.trabalhando@gmail.com'
      recipient_list = ['klaus.trabalhando@gmail.com']
      template_name = 'email_template.html'
      context = {'username': 'Klaus test', 'task': obj }
      send_email_task.delay(subject, from_email, recipient_list, template_name, context)
  
  @property
  def required_fields(self):
    return ['title', 'content']

  def serializer(self, obj):
    return task_serialized(obj)

def task_serialized(task):
  return {'id': task.id, 'title': task.title, 'content': task.content, 'user_id': task.user_id, 'completed': task.completed}