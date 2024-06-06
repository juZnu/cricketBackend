# serializers.py
from rest_framework import serializers
from .models import Player, Team, Competition


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['player_id', 'name', 'born_year', 'image_url', 'role', 'batting_style', 'bowling_style']


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['team_id', 'name', 'competition_id']


class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ['competition_id', 'name']
