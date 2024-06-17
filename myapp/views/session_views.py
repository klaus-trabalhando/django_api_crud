from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from ..helpers.authentication_helper import generate_jwt, decode_jwt
import json

# curl -X POST http://127.0.0.1:8000/login -H "Content-Type: application/json" -d '{"username":"admin","password":"admin"}'
@csrf_exempt
def login(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
      token = generate_jwt(user.id)
      return JsonResponse({'token': token})
    else:
      return JsonResponse({'error': 'Invalid credentials'}, status=400)
  return JsonResponse({'error': 'Invalid method'}, status=405)

def require_authenticated_user(function):
    def wrapper(self, request):
      token = request.META.get('HTTP_AUTHORIZATION')
      if token is None:
        return JsonResponse({'error': 'Token missing'}, status=403)

      user_id = decode_jwt(token)
      if user_id is None:
        return JsonResponse({'error': 'Invalid token'}, status=403)
      return function(self=self, request=request)

    return wrapper
