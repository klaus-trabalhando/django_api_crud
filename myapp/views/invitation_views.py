from django.views import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .session_views import require_authenticated_user
from ..models.team_invitation import TeamInvitation
from ..models.team_member import TeamMember

class Member(View):

  @require_authenticated_user
  def get(self, request, code, action, current_user):
    team_invitation = get_object_or_404(TeamInvitation, code=code, status=TeamInvitation.PENDING)
    if TeamMember.objects.filter(team=team_invitation.team, user=current_user).exists():
      return JsonResponse({'error': 'Already a member!'})
    else:
      if action == 'accept':
        TeamMember.objects.create(team=team_invitation.team, user=current_user, role=TeamMember.MEMBER)
        team_invitation.status = TeamInvitation.ACCEPTED
      else:
        team_invitation.status = TeamInvitation.REJECTED
      team_invitation.save()
    return JsonResponse(team_invitation_serialized(team_invitation))

def team_invitation_serialized(obj):
  return {'id': obj.id, 'team_id': obj.team_id, 'email': obj.email, 'status': obj.status, 'code': obj.code}