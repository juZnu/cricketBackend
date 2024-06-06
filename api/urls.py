from django.urls import path
from . import views

urlpatterns = [
    path('players/', views.player_list),
    path('player/', views.player_detail),
    path('player_list/', views.player_list_with_name),
    path('teams/', views.team_list),
    path('team/', views.team_detail),
    path('competitions/', views.competition_list),
    path('competition/', views.competition_detail),
    path('teams-grid/', views.generate_teams_grid),
    path('check-player-teams/', views.check_player_played_for_both_teams),
    path('get-player-played-for-both-teams/', views.get_player_played_for_both_teams),

]
