# GameView handles API endpoints for listing, retrieving, creating, updating, and deleting games.
# It provides CRUD operations for games and uses GameSerializer for serialization.
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, GameType, Gamer


class GameView(ViewSet):
    """Level up games view"""

    def retrieve(self, request, pk):
        # GET /games/<pk>/ - Retrieve a single game by primary key.
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        # GET /games/ - Retrieve all games, optionally filtered by game_type.
        games = Game.objects.all()

        # Optional filter by game_type query param
        game_type = request.query_params.get("type", None)
        if game_type is not None:
            games = games.filter(game_type_id=game_type)

        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def create(self, request):
        # POST /games/ - Create a new game.
        gamer = Gamer.objects.get(uid=request.data["userId"])
        game_type = GameType.objects.get(pk=request.data["gameType"])

        game = Game.objects.create(
            title=request.data["title"],
            maker=request.data["maker"],
            number_of_players=request.data["numberOfPlayers"],
            skill_level=request.data["skillLevel"],
            game_type=game_type,
            gamer=gamer,
        )

        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        # PUT /games/<pk>/ - Update an existing game.
        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.maker = request.data["maker"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.skill_level = request.data["skillLevel"]

        game_type = GameType.objects.get(pk=request.data["gameType"])
        game.game_type = game_type
        game.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        # DELETE /games/<pk>/ - Delete a game.
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


# GameSerializer serializes Game objects for API responses.
class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = (
            "id",  # Game's unique identifier
            "game_type",  # ForeignKey to the GameType model
            "title",  # Title of the game
            "maker",  # Maker or publisher of the game
            "gamer",  # ForeignKey to the Gamer model (owner/creator)
            "number_of_players",  # Number of players required
            "skill_level",  # Skill level required to play
        )
        depth = 1  # Serializes related objects (game_type, gamer) with their fields
