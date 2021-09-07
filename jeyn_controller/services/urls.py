from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"services", views.ServiceViewset)
router.register(r"service-versions", views.ServiceVerionViewset)

urlpatterns = [
    path("", include(router.urls))
]
