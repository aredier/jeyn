from django.urls import include, path

from . import views

urlpatterns = [
    path("dummy_view", views.DummyView.as_view()),
]
