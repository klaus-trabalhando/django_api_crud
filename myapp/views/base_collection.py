from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.shortcuts import render

class BaseCollection(View):
  model = None
  serializer = None
  folder = None

  def dispatch(self, request, current_user=None, *args, **kwargs):
    if request.path_info.endswith('/new/'):
      return self.new(request)
    else:
      return super().dispatch(request, current_user=current_user, *args, **kwargs)

  def new(self, request):
    return HttpResponse(render(request, f"{self.folder}/new.html"))

  def get(self, request, current_user=None):
    objects = self.base_filter(request, current_user)
    data = [self.serializer(obj) for obj in objects]
    return JsonResponse(data, safe=False)

  def post(self, request, current_user=None):
    data = self.assign_attributes(request, current_user, request.POST.copy())
    if all(field in data for field in self.required_fields):
      obj = self.model.objects.create(**data)
      return JsonResponse(self.serializer(obj), status=201)
    else:
      return JsonResponse({'error': 'Missing required fields'}, status=400)
  
  def assign_attributes(self, request, current_user, data):
    data_dict = {key: data.getlist(key) if len(data.getlist(key)) > 1 else data.get(key) for key in data.keys()}
    data_dict.pop('csrfmiddlewaretoken', None)
    return data_dict
  
  def base_filter(self, request, current_user):
    return self.model.objects.all()
  
  @property
  def required_fields(self):
    raise NotImplementedError("You must define 'required_fields' property in your subclass.")

  def serializer(self, obj):
    raise NotImplementedError("You must define 'serializer' method in your subclass.")
