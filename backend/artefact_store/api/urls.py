from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("artefact-type", views.ArtefactTypeViewset)
router.register("artefact", views.ArtefactViewset)
router.register("artefact-relationship", views.RelationshipViewset)
urlpatterns = [
    path(r"artefact/query/", views.ArtefactQueryView.as_view())
]
urlpatterns += router.urls
