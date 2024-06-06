from django.db import models


class Player(models.Model):
    player_id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255)
    born_year = models.IntegerField()
    image_url = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    batting_style = models.CharField(max_length=255)
    bowling_style = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'players'


class Competition(models.Model):
    competition_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'competitions'


class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'teams'


class PlayerTeam(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'player_teams'


