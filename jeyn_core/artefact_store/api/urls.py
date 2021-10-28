from django.urls import path
from rest_framework import routers

from . import views

api_router = routers.DefaultRouter()
api_router.register("artefact_classes", views.ArtefactClassViewset, basename="artefact_class")
api_router.register("artefacts", views.ArtefactViewset, basename="artefact")

urlpatterns = [
    path("dummy_view", views.DummyView.as_view()),
    path("related_view", views.DummyConnectedView.as_view()),
    *api_router.urls
]
