# GameType model represents a category or type of game (e.g., Board Game, RPG).
# Each GameType has a label describing the type.
from django.db import models


class GameType(models.Model):
    label = models.CharField(max_length=50)  # The name/label of the game type
