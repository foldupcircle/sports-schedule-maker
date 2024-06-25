import pandas as pd

from collections import defaultdict

from backend.utils.debug import debug
from backend.utils.main_utils import choose_league
from backend.data.past_season_data import division_data

def determine_matchups(league: str):
    '''
    Generate all 272 games that need to happen, here's the breakdown
    1. 6 games against division opponents, home and away (Div Games)
    2. 4 games against every team in another div, same conf (rotates yearly) -> past_season_data.py (Intraconf)
    3. 4 games against every team in another div, other conf (rotates yearly) -> past_season_data.py (Interconf)
    4. 2 games against teams from the other 2 divs within same conf (based on last year's standings) (SPF)
    5. 1 game against a team from a div in the other conf (based on last year's standings) (17th Game)
        The conference that hosts this game rotates by year. 2024 is NFC
    * SPF = Same-Place Finisher (Not how good a sunscreen is)
    
    Input: league you want to generate matchups for (otu of NFL, NBA, MLB, IPL, EPL)

    Returns: 
    - matchups (List[Tuple[Team, Team]]): Each tuple in the list is a matchup that should happend at some point during the season
        - Team names are represented by Team objects
        - The first team is home and the second team in the tuple is away
    '''
    teams, games = choose_league(league)
    total_games = (len(teams) * games) / 2

    prevent_dups_dict = defaultdict(int) # Store teams we've already went through in dict, so it's easy to check for dups
    matchups = []

    for team in teams.values():
        # Add to dups dict
        prevent_dups_dict[team.team_name] = 1

        division = team.division
        conf = team.conference

        # Division Games
        other_div_teams = [t for t in teams.values() if t.division == division]
        for opp in other_div_teams:
            if prevent_dups_dict[opp.team_name]: continue
            matchups.append((team, opp)) # Home Game
            matchups.append((opp, team)) # Away Game

        # Intraconference Games
        intra_conf_teams = [t for t in teams.values() if t.division == team.intra_conference]
        for opp in intra_conf_teams:
            if prevent_dups_dict[opp.team_name]: continue
            # TODO: See if this should be home or away, it should alternate since 5 years ago (through nfl library?)
            matchups.append((team, opp)) # Home Game

        # Interconference Games
        inter_conf_teams = [t for t in teams.values() if t.division == team.inter_conference]
        for opp in inter_conf_teams:
            if prevent_dups_dict[opp.team_name]: continue
            # TODO: See if this should be home or away, it should alternate since 5 years ago (through nfl library?)
            matchups.append((team, opp)) # Home Game

        # SPF
        all_divisions = division_data['inter_conference'].keys()
        conf_divs = [div for div in all_divisions if div.startswith(conf)]
        conf_divs.remove(division)
        conf_divs.remove(team.intra_conference)

        df = pd.read_csv('backend/data/2023_NFL_Standings_by_Division.csv')
        debug(df.head(5))

        debug(df.loc[df['team'] == team.team_name])
        standing = int(df.loc[df['team'] == team.team_name]['standing'].iloc[0])

        spf_teams = df.loc[(df['standing'] == standing) & 
                           (df['division'].isin(conf_divs))]['team']
        
        for opp in spf_teams:
            if prevent_dups_dict[opp]: continue
            opp = teams[opp]
            matchups.append((team, opp)) # Assuming Home rn

        # 17th Game
        # TODO

    debug(matchups[:5])
    debug(len(matchups))
    if len(matchups) != total_games:
        raise ValueError('Total Generated Matchups do not match expected number')
    return matchups
