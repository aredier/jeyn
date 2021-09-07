from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"artefacts", views.ArtefactViewset)
router.register(r"artefact-schemas", views.ArtefactSchemaViewset)

urlpatterns = [
    path("", include(router.urls))
]
