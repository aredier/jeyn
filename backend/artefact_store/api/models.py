from django.db import models

# Create your models here.


class ArtefactType(models.Model):
    schema = models.JSONField()
    type_name = models.CharField(max_length=120, primary_key=True)


class Artefact(models.Model):
    artefact_type_reference = models.ForeignKey(ArtefactType, on_delete=models.CASCADE, related_name="artefacts")
    artefact_data = models.JSONField()


class RelationShip(models.Model):
    parent = models.ForeignKey(Artefact, on_delete=models.CASCADE, related_name="children")
    child = models.ForeignKey(Artefact, on_delete=models.CASCADE, related_name="parents")
    relationship_type = models.CharField(max_length=120)
    creation_time = models.DateTimeField(auto_now=True)
