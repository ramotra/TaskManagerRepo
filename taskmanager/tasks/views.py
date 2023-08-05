from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Task
from .serializers import TaskSerializer
from .tasks import generate_csv, time_consuming_task

'''
[Description]: Class to create tasks
and return list of the available task.

[Author]: Prashant
'''
class TaskListCreate(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)

'''
[Description]: Class to delete and 
retrieve a specific taskby its id

[Author]: Prashant
'''
class TaskRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)

'''
Was planning to provide a csv generation of the user's
task and make it run in background for the case to simulate
complex task, but decided to move ahead with Complextask
'''
# class GenerateCSVView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         generate_csv.delay(request.user.id)
#         return Response({"message": "CSV generation started"}, status=status.HTTP_202_ACCEPTED)

'''
[Description]: Class to simulate the complex task
which calls the background task
which pushes some data in rabbitmq queue
which is picked by our standalone consumer service

[Author]: Prashant
'''
class ComplexTask(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            data = "Some data to be processed"
            time_consuming_task.delay(data)

            message = "Request submitted successfully, the result will be notified to you by email"
            return Response({"message":message}, status=status.HTTP_202_ACCEPTED)
        except Exception as err:
            return err

