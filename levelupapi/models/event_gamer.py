# EventGamer model represents the many-to-many relationship between Gamers and Events.
# Each row links a gamer to an event they have joined.
from django.db import models
from .gamer import Gamer
from .event import Event


class EventGamer(models.Model):
    gamer = models.ForeignKey(
        Gamer, on_delete=models.CASCADE
    )  # The gamer who joined the event
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE
    )  # The event the gamer joined
