from django.shortcuts import render, redirect, reverse
from django.views.generic import FormView, ListView, DetailView, CreateView, UpdateView
from .forms import BookReviewForm, MovieReviewForm
from .models import Review
from movies.models import Movie
from books.models import Book


def delete_review(request, pk):
    try:
        Review.objects.filter(pk=pk).delete()
        return redirect(reverse("reviews:reviews"))
    except Review.DoesNotExist:
        return redirect(reverse("core:home"))


class ReviewFormView(FormView):

    template_name = "reviews/review_form.html"
    # form_class = MovieReviewForm

    def get_form_class(self):
        ft = self.kwargs.get("ft", None)
        if ft is not None:
            if ft == "book":
                return BookReviewForm
            elif ft == "movie":
                return MovieReviewForm

    def form_valid(self, form):
        review = form.save()
        review.created_by = self.request.user
        review.save()
        return redirect(reverse("reviews:detail", kwargs={"pk": review.pk}))


class MovieCreateView(CreateView):

    model = Review
    fields = (
        "text",
        "rating",
    )
    template_name = "reviews/review_form.html"

    def form_valid(self, form):
        review = form.save(commit=False)
        pk = self.kwargs.get("pk", None)
        if pk is not None:
            movie = Movie.objects.get(pk=pk)
            review.movie = movie
        review.created_by = self.request.user
        review.save()
        return redirect(reverse("reviews:detail", kwargs={"pk": review.pk}))

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get("pk", None)
        if pk is not None:
            movie = Movie.objects.get(pk=pk)
        context = super().get_context_data(**kwargs)
        context["title"] = movie.title
        context["type"] = "movie"
        return context


class BookCreateView(CreateView):

    model = Review
    fields = (
        "text",
        "rating",
    )
    template_name = "reviews/review_form.html"

    def form_valid(self, form):
        review = form.save(commit=False)
        pk = self.kwargs.get("pk", None)
        if pk is not None:
            book = Book.objects.get(pk=pk)
            review.book = book
        review.created_by = self.request.user
        review.save()
        return redirect(reverse("reviews:detail", kwargs={"pk": review.pk}))

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get("pk", None)
        if pk is not None:
            book = Book.objects.get(pk=pk)
        context = super().get_context_data(**kwargs)
        context["title"] = book.title
        context["type"] = "book"
        return context


class ReviewDetail(DetailView):

    model = Review


class ReviewList(ListView):

    model = Review
    paginate_by = 5
    paginate_orphans = 5
    ordering = "-created_at"
    context_object_name = "reviews"

    def get_queryset(self):
        filter_type = self.request.GET.get("filter", None)
        if filter_type is not None:
            if filter_type == "movie":
                return Review.objects.filter(book=None).order_by("-created_at")
            elif filter_type == "book":
                return Review.objects.filter(movie=None).order_by("-created_at")
        else:
            return Review.objects.all().order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_type = self.request.GET.get("filter", None)

        if filter_type is not None:
            if filter_type == "movie":
                context["filter_type"] = "movie"
            elif filter_type == "book":
                context["filter_type"] = "book"
        else:
            context["filter_type"] = "all"

        return context


class EditReview(UpdateView):

    model = Review
    fields = (
        "text",
        "rating",
    )
