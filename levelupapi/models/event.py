# Event model represents a scheduled gaming event in the system.
# It links to a Game, an organizer (Gamer), and stores event details.
from django.db import models
from .game import Game


class Event(models.Model):
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE
    )  # The game being played at the event
    organizer = models.ForeignKey(
        "Gamer", on_delete=models.CASCADE
    )  # The user organizing the event
    description = models.CharField(max_length=255)  # Description of the event
    date = models.DateField()  # Date of the event
    time = models.TimeField()  # Time of the event

    # The 'joined' property is set dynamically in the view to indicate if the current user has joined this event.
    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value
