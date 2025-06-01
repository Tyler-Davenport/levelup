# EventGamerViewSet allows deleting a specific EventGamer row by its id (primary key).
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from levelupapi.models import EventGamer


class EventGamerViewSet(ViewSet):
    def destroy(self, request, pk=None):
        """DELETE /eventgamers/<pk>/ - Delete a specific EventGamer row by id."""
        try:
            event_gamer = EventGamer.objects.get(pk=pk)
            event_gamer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except EventGamer.DoesNotExist:
            return Response(
                {"error": "EventGamer not found"}, status=status.HTTP_404_NOT_FOUND
            )
