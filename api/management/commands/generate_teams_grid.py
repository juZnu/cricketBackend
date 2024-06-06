import json
import random
from django.core.management.base import BaseCommand
from api.models import PlayerTeam, Team


def check_players_played_for_both_teams(team_id_1, team_id_2):
    # Get the player IDs for each team
    players_team1 = set(PlayerTeam.objects.filter(team_id=team_id_1).values_list('player_id', flat=True))
    players_team2 = set(PlayerTeam.objects.filter(team_id=team_id_2).values_list('player_id', flat=True))

    # Check if there are any players who played for both teams
    common_players = players_team1.intersection(players_team2)

    return bool(common_players)


def select_teams_for_grid():
    # Retrieve all teams from the database
    all_teams = list(Team.objects.all())

    while True:
        # Select three random row teams
        row_teams = random.sample(all_teams, 3)

        # Remove the row teams from the available teams
        available_teams = all_teams.copy()
        for team in row_teams:
            available_teams.remove(team)

        # Select three random column teams that are not the same as the row teams
        col_teams = []
        for _ in range(3):
            while available_teams:
                column_team = random.choice(available_teams)
                available_teams.remove(column_team)
                if (check_players_played_for_both_teams(column_team.team_id, row_teams[0].team_id) and
                        check_players_played_for_both_teams(column_team.team_id, row_teams[1].team_id) and
                        check_players_played_for_both_teams(column_team.team_id, row_teams[2].team_id)):
                    col_teams.append(column_team)
                    break
            else:
                # Break out of the outer loop if no available column teams left
                break

        if len(row_teams) == 3 and len(col_teams) == 3:
            return [row_teams, col_teams]


class Command(BaseCommand):
    help = 'Generate teams grid and append it to a JSON file'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Generating teams grid...'))
        teams_json = {}

        # Read existing JSON file, if it exists
        input_file = 'teams_grid.json'
        try:
            with open(input_file, 'r') as f:
                teams_json = json.load(f)
        except FileNotFoundError:
            pass

        for _ in range(1000):
            row, col = select_teams_for_grid()
            row_str = ",".join(sorted([str(team.team_id) for team in row]))
            col_str = ",".join(sorted([str(team.team_id) for team in col]))
            if not teams_json.get(row_str):
                teams_json[row_str] = []
            teams_json[row_str].extend([str(team.team_id) for team in col])
            if not teams_json.get(col_str):
                teams_json[col_str] = []
            teams_json[col_str].extend([str(team.team_id) for team in row])

        # Write the updated dictionary to the JSON file
        with open(input_file, 'w') as f:
            json.dump(teams_json, f, indent=4)

        self.stdout.write(self.style.SUCCESS('Teams grid generated successfully and appended to teams_grid.json'))
