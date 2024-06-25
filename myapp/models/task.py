from .searchable_record import SearchableRecord
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError

class Task(SearchableRecord):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
  title = models.CharField(max_length=100)
  content = models.TextField()
  completed = models.BooleanField()
  created_at = models.DateTimeField(auto_now_add=True)

  def clean(self):
    super().clean()
    self.clean_title()
    if not self.title:
      raise ValidationError({'title': 'Title cannot be empty'})
    
    if not self.user:
      raise ValidationError({'user': 'User cannot be blank'})
  
  def clean_title(self):
    if len(self.title.strip()) < 2:
      raise ValidationError({'title': 'title too short'})
  
  def save(self, *args, **kwargs) -> None:
    if self.completed == None:
      self.completed = False
    self.full_clean()
    return super().save(*args, **kwargs)

  def __str__(self):
    return self.title
  
  @classmethod
  def index_name(self):
    return 'tasks'

  @classmethod
  def search_config(self):
    config = super().search_config().copy()
    config['mappings'] = {
      "properties": {
        "title": {"type": "text"},
        "content": {"type": "text"},
        "completed": {'type': 'boolean'},
        "created_at": {"type": "date"}
      }
    }
    return config
  
  def index_data(self):
    return {
      'title': self.title,
      'content': self.content,
      'completed': self.completed,
      'created_at': self.created_at
    }

@receiver(post_save, sender=Task)
def save_handler(sender, instance, created, **kwargs):
  instance.index_document(created)

@receiver(post_delete, sender=Task)
def delete_handler(sender, instance, **kwargs):
  instance.delete_document()