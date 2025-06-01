# levelupapi/views/event.py
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from levelupapi.models import (
    Event,
    Game,
    Gamer,
    EventGamer,
)  # import related models needed for create


# EventView handles all event-related API endpoints, including custom actions for joining and leaving events.
# It provides CRUD operations for events and custom actions for signup/leave.
class EventView(ViewSet):
    """Level up events view"""

    def retrieve(self, request, pk):
        # GET /events/<pk>/ - Retrieve a single event by primary key.
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        # GET /events/ - Retrieve all events.
        events = Event.objects.all()

        # Get the gamer from the Authorization header (uid), handle missing gamer gracefully
        uid = request.META.get("HTTP_AUTHORIZATION")
        gamer = None
        if uid:
            try:
                gamer = Gamer.objects.get(uid=uid)
            except Gamer.DoesNotExist:
                gamer = None

        # For each event, set the joined property to True if the gamer is signed up, else False.
        for event in events:
            event.joined = (
                EventGamer.objects.filter(event=event, gamer=gamer).exists()
                if gamer
                else False
            )

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        # POST /events/ - Create a new event.
        game = Game.objects.get(pk=request.data["game"])
        organizer = Gamer.objects.get(uid=request.data["organizer"])
        event = Event.objects.create(
            game=game,
            organizer=organizer,
            description=request.data["description"],
            date=request.data["date"],
            time=request.data["time"],
        )
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        # PUT /events/<pk>/ - Update an existing event.
        event = Event.objects.get(pk=pk)
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]
        game = Game.objects.get(pk=request.data["game"])
        event.game = game
        organizer = Gamer.objects.get(uid=request.data["organizer"])
        event.organizer = organizer
        event.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        # DELETE /events/<pk>/ - Delete an event.
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=["post"], detail=True)
    def signup(self, request, pk):
        """Custom action: POST /events/<pk>/signup to sign up a gamer for an event."""
        user_id = request.data.get("user_id")
        if not user_id:
            return Response(
                {"error": "user_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            gamer = Gamer.objects.get(uid=user_id)
        except Gamer.DoesNotExist:
            return Response(
                {"error": "Gamer not found"}, status=status.HTTP_404_NOT_FOUND
            )
        event = Event.objects.get(pk=pk)
        attendee = EventGamer.objects.create(gamer=gamer, event=event)
        return Response({"message": "Gamer added"}, status=status.HTTP_201_CREATED)

    @action(methods=["delete"], detail=True)
    def leave(self, request, pk):
        """Custom action: DELETE /events/<pk>/leave to remove a gamer from an event."""
        user_id = request.data.get("user_id")
        if not user_id:
            return Response(
                {"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            gamer = Gamer.objects.get(uid=user_id)
        except Gamer.DoesNotExist:
            return Response(
                {"error": "Gamer not found"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response(
                {"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            event_gamer = EventGamer.objects.get(gamer=gamer, event=event)
            event_gamer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except EventGamer.DoesNotExist:
            return Response(
                {"error": "Signup not found"}, status=status.HTTP_404_NOT_FOUND
            )


# EventSerializer serializes Event objects for API responses.
# It includes the custom 'joined' property, which is set dynamically in the view
# to indicate if the current user (from the Authorization header) has joined the event.
class EventSerializer(serializers.ModelSerializer):
    attendees = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = (
            "id",
            "game",
            "organizer",
            "description",
            "date",
            "time",
            "joined",
            "attendees",  # List of attendees (gamers) for this event
        )
        depth = 1

    def get_attendees(self, obj):
        # Return a list of dicts with each attendee's uid and display_name
        return [
            {"uid": eg.gamer.uid, "display_name": eg.gamer.display_name}
            for eg in obj.eventgamer_set.all()
        ]
