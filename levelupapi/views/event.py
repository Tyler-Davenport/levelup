# levelupapi/views/event.py
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import (Event,Game,Gamer,)  # import related models needed for create


class EventView(ViewSet):
    """Level up events view"""

    def retrieve(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        events = Event.objects.all()

        # Optional filter by game query param
        game = request.query_params.get("game", None)
        if game is not None:
            events = events.filter(game_id=game)

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        # Get related Game and Gamer instances from the request data
        game = Game.objects.get(pk=request.data["game"])
        organizer = Gamer.objects.get(uid=request.data["organizer"])

        # Create the new Event object with the data from the request
        event = Event.objects.create(
            game=game,
            organizer=organizer,
            description=request.data["description"],
            date=request.data["date"],
            time=request.data["time"],
        )

        # Serialize and return the newly created event with HTTP 201
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "id",
            "game",
            "organizer",
            "description",
            "date",
            "time",
        )
        depth = 1
