import logging

from . import models


logger = logging.getLogger(__name__)


class ServiceController:

    def __init__(self, service_model: "models.Service"):
        self._name = service_model.name

    @property
    def name(self):
        return self._name

    def deploy_all_versions(self):
        logger.error(f"deploying service {self.name}")
