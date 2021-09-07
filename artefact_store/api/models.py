from django.db import models


class ArtefactSchema(models.Model):

    name = models.CharField(max_length=60)
    # schema = models.JSONField()


class Artefact(models.Model):

    schema = models.ForeignKey(ArtefactSchema, on_delete=models.SET_NULL, null=True, default=None, related_name="artefacts")
    value = models.JSONField()
