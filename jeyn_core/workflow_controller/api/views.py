from rest_framework.views import APIView, Response


class DummyView(APIView):

    def get(self, request):
        return Response(data={"message": "this is the workflow controller"})
