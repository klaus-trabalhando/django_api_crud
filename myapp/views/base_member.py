from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.shortcuts import render

class BaseMember(View):
  model = None
  serializer = None
  folder = None

  def dispatch(self, request, current_user=None, *args, **kwargs):
    if request.method == 'POST' and request.POST.get('_method') == 'PUT':
      request.method = 'PUT'
    if request.path_info.endswith('/edit/'):
      return self.edit(request, *args, **kwargs)
    else:
      return super().dispatch(request, current_user=current_user, *args, **kwargs)

  def edit(self, request, current_user, id):
    record = self.get_object(request, current_user, id)
    context = {'current_user': current_user, 'record': record}
    return HttpResponse(render(request, f"{self.folder}/edit.html", context))

  def get(self, request, current_user, id):
    obj = self.get_object(request, current_user, id)
    return JsonResponse(self.serializer(obj))

  def put(self, request, current_user, id):
    obj = self.get_object(request, current_user, id)
    data = self.allowed_fields(request, current_user)
    if all(field in data for field in self.required_fields):
      for field in data:
        original_value = getattr(obj, field, None)
        setattr(obj, f"{field}_was", original_value)
        setattr(obj, field, data[field])
      obj.save()
      self.after_update(obj)
      return JsonResponse(self.serializer(obj))
    else:
      return JsonResponse({'error': 'Missing required fields'}, status=400)

  def delete(self, request, current_user, id):
    obj = self.get_object(request, current_user, id)
    obj.delete()
    return JsonResponse({'message': 'Object deleted successfully'}, status=204)

  def get_object(self, request, current_user, id):
    return get_object_or_404(self.model, pk=id)
  
  def allowed_fields(self, request, current_user):
    return request.POST.copy()
  
  def after_update(self, obj):
    return obj

  @property
  def required_fields(self):
    raise NotImplementedError("You must define 'required_fields' property in your subclass.")

  def serializer(self, obj):
    raise NotImplementedError("You must define 'serializer' method in your subclass.")
