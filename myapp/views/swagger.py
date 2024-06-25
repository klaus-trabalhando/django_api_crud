from django.shortcuts import render
from django.http import HttpResponse
import os

def swagger_ui(request):
  return render(request, 'swagger_ui.html')

def swagger_spec(request):
  swagger_file_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'swagger', 'swagger.yaml')
  with open(swagger_file_path, 'r') as file:
    spec = file.read()
  return HttpResponse(spec, content_type='application/x-yaml')
