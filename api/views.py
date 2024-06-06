import json
import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Player, Team, Competition, PlayerTeam
from .serializers import PlayerSerializer, TeamSerializer, CompetitionSerializer
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest

@api_view(['GET'])
def player_list(request):
    players = Player.objects.all()
    player_data = [{'player_id': player.player_id, 'player_name': player.name} for player in players]
    return JsonResponse({'players': player_data})

@api_view(['GET'])
def player_detail(request):
    player_id = request.headers.get('player_id')  # Retrieve player_id from request headers
    try:
        player = Player.objects.get(player_id=player_id)
        serializer = PlayerSerializer(player)
        return JsonResponse(serializer.data)
    except Player.DoesNotExist:
        return HttpResponseNotFound()


@api_view(['GET'])
def team_list(request):
    teams = Team.objects.all()
    team_data = [{'team_id': team.team_id, 'team_name': team.name} for team in teams]
    return JsonResponse({'teams': team_data})

@api_view(['GET'])
def team_detail(request):
    team_id = request.headers.get('team_id')
    try:
        team = Team.objects.get(team_id=team_id)
        serializer = TeamSerializer(team)
        return JsonResponse(serializer.data)
    except Team.DoesNotExist:
        return HttpResponseNotFound()

@api_view(['GET'])
def competition_list(request):
    competitions = Competition.objects.all()
    competition_data = [{'competition_id': competition.competition_id, 'competition_name': competition.name} for competition in competitions]
    return JsonResponse({'competitions': competition_data})

@api_view(['GET'])
def competition_detail(request):
    competition_id = request.headers.get('competition_id')
    try:
        competition = Competition.objects.get(competition_id=competition_id)
        serializer = CompetitionSerializer(competition)
        return JsonResponse(serializer.data)
    except Competition.DoesNotExist:
        return HttpResponseNotFound()

@api_view(['GET'])
def generate_teams_grid(request):
    with open('teams_grid.json', 'r') as f:
        teams_data = json.load(f)

    key = random.choice(list(teams_data.keys()))
    row_teams_ids = key.split(',')
    col_teams_ids = random.sample(teams_data[key], 3)
    grid = {'row_teams': row_teams_ids, 'col_teams': col_teams_ids}

    return JsonResponse({'grid': grid}, status=200)

@api_view(['GET'])
def get_player_played_for_both_teams(request):
    team_id_1 = request.headers.get('team_id_1')
    team_id_2 = request.headers.get('team_id_2')

    if not team_id_1 or not team_id_2:
        return JsonResponse({'error': 'Missing team_id_1 or team_id_2'}, status=400)

    player_teams_1 = PlayerTeam.objects.filter(team_id=team_id_1).values_list('player_id', flat=True)
    player_teams_2 = PlayerTeam.objects.filter(team_id=team_id_2).values_list('player_id', flat=True)
    common_players = set(player_teams_1).intersection(player_teams_2)

    if common_players:
        player_id = list(common_players)[0]  # Get the first common player
        player = Player.objects.get(player_id=player_id)
        return JsonResponse({'player_name': player.name}, status=200)
    else:
        return JsonResponse({'message': 'NOT FOUND'}, status=404)

@api_view(['GET'])
def check_player_played_for_both_teams(request):
    # Get headers from the request
    player_id = request.headers.get('player_id')
    team_id_1 = request.headers.get('team_id_1')
    team_id_2 = request.headers.get('team_id_2')

    # Check if all required parameters are present
    if not all([player_id, team_id_1, team_id_2]):
        return JsonResponse({"message": "Missing parameters"}, status=400)

    # Check if the player has played for both teams
    played_for_team_1 = PlayerTeam.objects.filter(player_id=player_id, team_id=team_id_1).exists()
    played_for_team_2 = PlayerTeam.objects.filter(player_id=player_id, team_id=team_id_2).exists()

    # Return appropriate response based on the results
    if played_for_team_1 and played_for_team_2:
        return JsonResponse({"message": "OK"}, status=200)
    else:
        return JsonResponse({"message": "NOT FOUND"}, status=404)

@api_view(['GET'])
def player_list_with_name(request):
    player_name = request.headers.get('player_name')

    if player_name:
        players = Player.objects.filter(name__icontains=player_name)
    else:
        players = Player.objects.all()

    player_data = [{'player_id': player.player_id, 'player_name': player.name} for player in players]

    return JsonResponse({'players': player_data})
