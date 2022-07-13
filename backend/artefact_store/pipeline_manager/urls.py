from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register("pipeline-definition", viewset=views.PipelineDefinitionViewset)
router.register("pipeline-execution", viewset=views.PipelineExecutionViewset)
urlpatterns = router.urls