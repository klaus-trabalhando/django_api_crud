from django.db import models

class ActiveRecord(models.Model):

  class Meta:
    abstract = True

  def __str__(self):
    return 'ActiveRecord'