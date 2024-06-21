import json
from ..models.team import Team
from ..models.team_member import TeamMember
from ..models.team_invitation import TeamInvitation
from .base_collection import BaseCollection
from django.views import View
from .session_views import require_authenticated_user
from django.http import JsonResponse
from ..tasks import notify_invitation


class Collection(BaseCollection):
  model = Team
  folder = 'teams'
  
  @require_authenticated_user
  def get(self, request, current_user=None):
    return super().get(request, current_user)

  @require_authenticated_user
  def post(self, request, current_user=None):
    return super().post(request, current_user)

  def base_filter(self, request, current_user):
    return Team.objects.filter(team_members__user_id=current_user.id)

  @property
  def required_fields(self):
    return ['title']

  def serializer(self, obj):
    return team_serialized(obj)
  
  def after_create(self, request, current_user, obj):
    TeamMember.objects.create(user=current_user, team=obj, role=TeamMember.ADMIN)
    return obj

class Invitation(View):

  @require_authenticated_user
  def post(self, request, id, current_user=None):
    team = Team.objects.filter(id=id, team_members__user_id=current_user.id, team_members__role=TeamMember.ADMIN)
    if team:
      team = team[0]
      data = {}
      if request.content_type == 'application/x-www-form-urlencoded':
        data = request.POST.copy()
      else:
        data = json.loads(request.body)
      
      if data.get('email', None):
        team_invitation = TeamInvitation.objects.create(team= team, email=data['email'])
        context = {'code': team_invitation.code, 'team_name': team.title }
        notify_invitation.delay([team_invitation.email], context)
        return JsonResponse(team_invitation_serialized(team_invitation), status=201)
      else:
        return JsonResponse({'error': 'Missing required fields'}, status=400)
    else:
      return JsonResponse({'error': 'Not found'}, status=404)

def team_serialized(obj):
  return {'id': obj.id, 'title': obj.title, 'created_at': obj.created_at}

def team_invitation_serialized(obj):
  return {'id': obj.id, 'team_id': obj.team_id, 'email': obj.email, 'status': obj.status, 'code': obj.code}