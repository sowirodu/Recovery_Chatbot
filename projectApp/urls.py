from django.urls import path

from . import views


app_name = "projectApp"
urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    # ex: /polls/5/
    path("<int:question_id>/", views.detail, name="details"),  # Display a single question
]