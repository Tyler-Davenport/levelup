# levelupapi/views/game.py
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, GameType, Gamer


class GameView(ViewSet):
    """Level up games view"""

    def retrieve(self, request, pk):
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        games = Game.objects.all()

        # Optional filter by game_type query param
        game_type = request.query_params.get("type", None)
        if game_type is not None:
            games = games.filter(game_type_id=game_type)

        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def create(self, request):
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


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = (
            "id",
            "game_type",
            "title",
            "maker",
            "gamer",
            "number_of_players",
            "skill_level",
        )
        depth = 1
