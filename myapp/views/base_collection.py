from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View

class BaseCollection(View):
  model = None
  serializer = None

  def get(self, request):
    objects = self.model.objects.all()
    data = [self.serializer(obj) for obj in objects]
    return JsonResponse(data, safe=False)

  def post(self, request):
    data = request.POST
    if all(field in data for field in self.required_fields):
      obj = self.model.objects.create(**data)
      return JsonResponse(self.serializer(obj), status=201)
    else:
      return JsonResponse({'error': 'Missing required fields'}, status=400)

  @property
  def required_fields(self):
    raise NotImplementedError("You must define 'required_fields' property in your subclass.")

  def serializer(self, obj):
    raise NotImplementedError("You must define 'serializer' method in your subclass.")
