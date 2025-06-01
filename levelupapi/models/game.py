# Game model represents a game that can be played at events.
# It links to a GameType and a Gamer (the creator/owner of the game).
from django.db import models
from .game_type import GameType
from .gamer import Gamer


class Game(models.Model):
    game_type = models.ForeignKey(
        GameType, on_delete=models.CASCADE
    )  # The type/category of the game
    title = models.CharField(max_length=50)  # Title of the game
    maker = models.CharField(max_length=50)  # Maker or publisher of the game
    gamer = models.ForeignKey(
        Gamer, on_delete=models.CASCADE
    )  # The user who created/owns the game
    number_of_players = models.PositiveBigIntegerField()  # Number of players required
    skill_level = models.IntegerField()  # Skill level required to play
