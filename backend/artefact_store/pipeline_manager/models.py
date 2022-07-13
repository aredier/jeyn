from django.db import models


class PipelineDefinition(models.Model):
    name = models.CharField(max_length=120)


class PipelineExecution(models.Model):
    definition = models.ForeignKey(PipelineDefinition, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
