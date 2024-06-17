from django.urls import path
from .views import book_views

urlpatterns = [
  path('books/', book_views.Collection.as_view(), name='books_list'),
  path('books/<int:id>/', book_views.Member.as_view(), name='book_detail')
]