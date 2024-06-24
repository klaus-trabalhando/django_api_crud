from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.contrib.auth import get_user_model
from functools import wraps
from ..helpers.authentication_helper import generate_jwt, decode_jwt
import json

# curl -X POST http://127.0.0.1:8000/login -H "Content-Type: application/json" -d '{"username":"admin","password":"admin"}'
@csrf_exempt
def login(request):
  if request.method == 'GET':
    return render(request, 'login.html', { 'redirect_to': request.GET.get('redirect_to') })
  if request.method == 'POST':
    data = None
    if request.content_type == 'application/json':
      try:
        data = json.loads(request.body)
      except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")
    else:
      data = request.POST
    username = data.get('username')
    password = data.get('password')
    redirect_to = data.get('redirect_to')
    user = authenticate(username=username, password=password)
    if user is not None:
      token = generate_jwt(user.id)
      if request.content_type == 'application/json':
        return JsonResponse({'token': token })
      else:
        if redirect_to:
          response = HttpResponseRedirect(redirect_to)
        else:
          response = HttpResponseRedirect("/tasks/")
        one_day_in_seconds = 86400
        response.set_cookie('authtoken', token, max_age=one_day_in_seconds, secure=True, httponly=True, samesite='Strict')
        return response
    else:
      return JsonResponse({'error': 'Invalid credentials'}, status=400)
  return JsonResponse({'error': 'Invalid method'}, status=405)

def logout(request):
  response = HttpResponseRedirect("/login/")
  one_day_in_seconds = -1
  response.set_cookie('authtoken', '', max_age=one_day_in_seconds, secure=True, httponly=True, samesite='Strict')
  return response

def require_authenticated_user(function):
  @wraps(function)
  def wrapper(*args, **kwargs):
    request = None
    for arg in args:
      if hasattr(arg, 'META'):
        request = arg
        break
    if request is None:
      request = kwargs.get('request')

    if request is None:
      raise ValueError("Request object not found in arguments")

    token = request.COOKIES.get('authtoken')
    if token is None:
      return redirect_to_login(request)

    user_id = decode_jwt(token)
    if user_id is None:
      return redirect_to_login(request)
    User = get_user_model()
    kwargs['current_user'] = User.objects.get(pk=user_id)
    return function(*args, **kwargs)

  return wrapper

def redirect_to_login(request):
  if request.method == 'GET':
    current_url = request.build_absolute_uri()
    return HttpResponseRedirect(f'/login/?redirect_to={current_url}')
  else:
    return HttpResponseRedirect('/login/')