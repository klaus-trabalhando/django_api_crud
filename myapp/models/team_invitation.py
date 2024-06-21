from django.db import models
from .team import Team
import secrets
import string
from django.db.models.signals import pre_save
from django.dispatch import receiver

class TeamInvitation(models.Model):
  PENDING = 'pending'
  ACCEPTED = 'accepted'
  REJECTED = 'rejected'

  STATUS_CHOICES = [
    (PENDING, 'Pending'),
    (ACCEPTED, 'Accepted'),
    (REJECTED, 'Rejected'),
  ]

  team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_invitations')
  email = models.CharField(max_length=255)
  status = models.CharField(choices=STATUS_CHOICES, default=PENDING, max_length=10)
  code = models.CharField(max_length=8)

  class Meta:
    constraints = [
      models.UniqueConstraint(fields=['team_id', 'email'], name='unique_invitation')
    ]

  def __str__(self):
    return f'Invited {self.email} {self.status}'
  
  def generate_random_code(self, length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

@receiver(pre_save, sender=TeamInvitation)
def add_code_to_invitation(sender, instance, **kwargs):
  if not instance.code:
    instance.code = instance.generate_random_code(8)