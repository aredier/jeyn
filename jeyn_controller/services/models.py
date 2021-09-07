import logging

from django.db import models

from . import controllers


logger = logging.getLogger(__name__)


class Service(models.Model):
    name = models.CharField(max_length=120)
    deployment_scheme = models.JSONField()
    deployed = models.BooleanField()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        service_controller = controllers.ServiceController(self)
        service_controller.deploy_all_versions()
        super().save(force_insert, force_update, using, update_fields)


class ServiceVersion(models.Model):

    model_id = models.IntegerField()
