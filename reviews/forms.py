from django.forms import ModelForm
from .models import Review


class BookReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = (
            "text",
            "book",
            "rating",
        )

    def save(self, *args, **kwargs):
        review = super().save(commit=False)
        return review


class MovieReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = (
            "text",
            "movie",
            "rating",
        )

    def save(self, *args, **kwargs):
        review = super().save(commit=False)
        return review