from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import TaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta
from .models import Task

class TaskListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Filter tasks by the logged-in user and order by priority
        tasks = Task.objects.filter(user=request.user).order_by('priority')  # High priority tasks first
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Create a new task for the logged-in user
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Associate the task with the logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, user=request.user)  # Ensure the task belongs to the logged-in user
        except Task.DoesNotExist:
            return Response({'detail': 'Not found or not authorized to access this task.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, user=request.user)  # Ensure the task belongs to the logged-in user
        except Task.DoesNotExist:
            return Response({'detail': 'Not found or not authorized to update this task.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()  # Update the task
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, user=request.user)  # Ensure the task belongs to the logged-in user
        except Task.DoesNotExist:
            return Response({'detail': 'Not found or not authorized to delete this task.'}, status=status.HTTP_404_NOT_FOUND)

        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, user=request.user)
        except Task.DoesNotExist:
            return Response({'detail': 'Not found or not authorized to update this task.'},
                            status=status.HTTP_404_NOT_FOUND)

        # Toggle the `completed` field
        task.completed = not task.completed
        task.save()

        serializer = TaskSerializer(task)
        return Response(serializer.data)





class TaskStatisticsView(APIView):
    def get(self, request):
        period = request.query_params.get('period', 'weekly')  # Default to 'weekly'

        # Get current date
        today = datetime.today()

        # Determine the start date based on the period
        if period == 'weekly':
            start_date = today - timedelta(days=today.weekday())  # Start of the current week
        elif period == 'monthly':
            start_date = today.replace(day=1)  # First day of the current month
        elif period == 'yearly':
            start_date = today.replace(month=1, day=1)  # First day of the current year
        else:
            start_date = today

        # Filter tasks based on the time range
        tasks = Task.objects.filter(created_at__gte=start_date)

        # Get task stats
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(completed=True).count()
        pending_tasks = total_tasks - completed_tasks

        # Return the stats as JSON
        return Response({
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
        })
