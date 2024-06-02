from typing import List

from team import Team

def convert_teams_to_dict(teams: List[Team]):
    return [{'team_name': team.team_name, 'home_stadium_name': team.home_stadium.name, 'division': team.division} for team in teams]
