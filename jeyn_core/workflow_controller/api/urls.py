from django.urls import path

from . import views

urlpatterns = [
    path("workflow", views.SubmitterView.as_view()),
    path("topic_name", views.SubscriberView.as_view())
]
