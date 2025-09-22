from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Task
from .serializers import TaskSerializer


class TaskView(APIView):
    def get(slef, request):
        task = Task.objects.all()
        serializer = TaskSerializer(task, many=True)
        return Response(serializer.data)
