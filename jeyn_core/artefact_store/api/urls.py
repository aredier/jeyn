from django.urls import path

from . import views

urlpatterns = [
    path("dummy_view", views.DummyView.as_view()),
    path("related_view", views.DummyConnectedView.as_view()),
]