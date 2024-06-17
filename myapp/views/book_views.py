from ..models.book import Book
from .base_collection import BaseCollection
from .base_member import BaseMember

class Collection(BaseCollection):
  model = Book

  @property
  def required_fields(self):
    return ['title', 'content']

  def serializer(self, obj):
    return book_serialized(obj)

class Member(BaseMember):
  model = Book

  @property
  def required_fields(self):
    return ['title', 'content']

  def serializer(self, obj):
    return book_serialized(obj)

def book_serialized(book):
  return {'id': book.id, 'title': book.title, 'content': book.content}