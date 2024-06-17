import jwt
from django.conf import settings
from datetime import datetime, timedelta, timezone

def generate_jwt(user_id):
  now = datetime.now(timezone.utc)
  payload = {
    'user_id': user_id,
    'exp': now + timedelta(days=1),
    'iat': now
  }
  token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
  return token

def decode_jwt(token):
  try:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    return payload['user_id']
  except jwt.ExpiredSignatureError:
    return None
  except jwt.InvalidTokenError:
    return None
