from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View

class BaseMember(View):
  model = None
  serializer = None

  def get(self, request, id):
    obj = get_object_or_404(self.model, pk=id)
    return JsonResponse(self.serializer(obj))

  def put(self, request, id):
    obj = get_object_or_404(self.model, pk=id)
    data = request.POST
    if all(field in data for field in self.required_fields):
      for field in data:
        setattr(obj, field, data[field])
      obj.save()
      return JsonResponse(self.serializer(obj))
    else:
      return JsonResponse({'error': 'Missing required fields'}, status=400)

  def delete(self, request, id):
    obj = get_object_or_404(self.model, pk=id)
    obj.delete()
    return JsonResponse({'message': 'Object deleted successfully'}, status=204)

  @property
  def required_fields(self):
    raise NotImplementedError("You must define 'required_fields' property in your subclass.")

  def serializer(self, obj):
    raise NotImplementedError("You must define 'serializer' method in your subclass.")
