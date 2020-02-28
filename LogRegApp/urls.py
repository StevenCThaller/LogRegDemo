from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('success', views.success),
    path('logout', views.logout),
    path('books', views.all_books),
    path('books/create', views.add_book),
    path('books/<int:book_id>/edit', views.edit_book),
    path('books/<int:book_id>/delete', views.delete_book),
    path('books/<int:book_id>/favorite', views.fav_book),
    path('books/<int:book_id>/unfavorite', views.unfav_book),
    path('books/<int:book_id>', views.one_book)
]
