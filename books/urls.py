from django.urls import path
from books.views import BooksView, BookDetail, CreateBook, UpdateBook
from reviews.views import BookCreateView

app_name = "books"

urlpatterns = [
    path("", BooksView.as_view(), name="books"),
    path("<int:pk>", BookDetail.as_view(), name="book"),
    path("<int:pk>/update", UpdateBook.as_view(), name="update"),
    path("<int:pk>/review", BookCreateView.as_view(), name="review"),
    path("create", CreateBook.as_view(), name="create"),
]
