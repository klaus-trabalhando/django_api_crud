from django.db import models
from django.contrib.auth.models import User
from .team import Team

class TeamMember(models.Model):
  MEMBER = 'member'
  ADMIN = 'admin'

  ROLE_CHOICES = [
    (MEMBER, 'Member'),
    (ADMIN, 'Admin')
  ]

  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_members')
  team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_members')
  role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=MEMBER)

  class Meta:
    constraints = [
      models.UniqueConstraint(fields=['user', 'team'], name='unique_team_member')
    ]

  def __str__(self):
    return f'{self.team.title} - {self.user.username} ({self.role})'