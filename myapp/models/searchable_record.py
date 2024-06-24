from .active_record import ActiveRecord
from ..elasticsearch_client import es

class SearchableRecord(ActiveRecord):

  class Meta:
    abstract = True

  @classmethod
  def full_index_name(self):
    return f'django_test_{self.index_name()}'

  @classmethod
  def index_name(self):
    raise NotImplementedError("You must define 'index_name' in your subclass.")

  @classmethod
  def search_config(self):
    return {
      "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
      },
      "mappings": {
        "properties": {
          "created_at": {"type": "date"}
        }
      }
    }
  
  def index_data(self):
    raise NotImplementedError("You must define 'index_name' in your subclass.")

  @classmethod
  def create_index(self):
    if not es.indices.exists(index=self.full_index_name()):
      es.indices.create(index=self.full_index_name(), body=self.search_config())
  
  def index_document(self, created):
    if created:
      es.index(index=self.full_index_name(), id=self.pk, body=self.index_data())
    else:
      es.update(index=self.full_index_name(), id=self.pk, body={'doc': self.index_data()})
  
  def delete_document(self):
    es.delete(index=self.full_index_name(), id=self.pk)

  @classmethod
  def drop_index(self):
    if es.indices.exists(index=self.full_index_name()):
      es.indices.delete(index=self.full_index_name())
  
  def document(self):
    try:
      response = es.get(index=self.full_index_name(), id=self.pk)
      return response['_source']
    except Exception as e:
      return None
  
  @classmethod
  def refresh_index(self):
    es.indices.refresh(index=self.full_index_name())
  
  @classmethod
  def search(self, query):
    search_query = query
    if isinstance(query, str):
      if len(query.strip()) == 0:
        search_query = {
          "query": {
            "match_all": {}
          }
        }
      else:
        search_query = {
          "query": {
            "match": {
              "title": query
            }
          }
        }
    try:
      response = es.search(index=self.full_index_name(), body=search_query)
      return response
    except Exception as e:
      return []

  @classmethod
  def reindex(self, recreate=False):
    if recreate:
      self.drop_index()
    self.create_index()
    all_records = self.objects.all()
    
    for record in all_records:
      record.index_document(created=True if recreate else False) 