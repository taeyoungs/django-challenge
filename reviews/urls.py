from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("", views.ReviewList.as_view(), name="reviews"),
    path("<str:ft>/create/", views.ReviewFormView.as_view(), name="create"),
    path("<int:pk>/", views.ReviewDetail.as_view(), name="detail"),
    path("<int:pk>/delete", views.delete_review, name="delete"),
    path("<int:pk>/edit", views.EditReview.as_view(), name="edit"),
]