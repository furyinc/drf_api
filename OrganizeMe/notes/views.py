from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Note
from .serializers import NoteSerializer


# Create your views here.

class NoteListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = NoteSerializer(many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Create a new task for the logged-in user
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Associate the task with the logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            note = Note.objects.get(pk=pk, user=request.user)
        except Note.DoesNotExist:
            return Response({'detail': 'Not found or not authorized to access this note'}, status=status.HTTP_404_NOT_FOUND)

        serializer = NoteSerializer(note)
        return Response(serializer.data)


    def put(self, request, pk):
        try:
            note = Note.objects.get(pk=pk, user=request.user)
        except Note.DoesNotExist:
            return Response({'detail': 'Not found or not authorized to update this note'})

        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        try:
            note = Note.objects.get(pk=pk, user=request.user)
        except Note.DoesNotExist:
            return Response({'response': 'Not found or not authorized to delete this note'}, status=status.HTTP_404_NOT_FOUND)

        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

