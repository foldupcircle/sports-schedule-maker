import pandas as pd
import nfl_data_py as nfl

from collections import defaultdict
from pprint import pprint

from backend.utils.debug import debug
from backend.utils.main_utils import choose_league, check_matchup
from backend.data.past_season_data import division_data

def determine_matchups(league: str, year: int):
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
    
    inter_conf_schedule = nfl.import_schedules([year - 4])
    intra_conf_schedule = nfl.import_schedules([year - 3])

    prevent_dups_dict = defaultdict(int) # Store teams we've already went through in dict, so it's easy to check for dups
    matchups = []

    # Schedules and Standings (These are used, don't delete)
    standings_2021 = pd.read_csv('backend/data/2021_NFL_Standings_by_Division.csv')
    standings_2022 = pd.read_csv('backend/data/2022_NFL_Standings_by_Division.csv')
    standings_2023 = pd.read_csv('backend/data/2023_NFL_Standings_by_Division.csv')
    schedule_2023 = nfl.import_schedules([year - 1])
    schedule_2022 = nfl.import_schedules([year - 2])

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
        home_away_check = 0
        for opp in intra_conf_teams:
            game_did_happen = check_matchup(intra_conf_schedule, team.team_name, opp.team_name)
            home_away_check += game_did_happen
            if prevent_dups_dict[opp.team_name]: continue
            if game_did_happen: matchups.append((opp, team)) # Away Game Since last one was Home
            else: matchups.append((team, opp)) # Home Game Since last one was Away
        
        if home_away_check != 2:
            debug(team.team_name)
            raise ValueError('Each team must have 2 home and 2 away games with their respective intra conference division')

        # Interconference Games
        inter_conf_teams = [t for t in teams.values() if t.division == team.inter_conference]
        home_away_check = 0
        for opp in inter_conf_teams:
            game_did_happen = check_matchup(inter_conf_schedule, team.team_name, opp.team_name)
            home_away_check += game_did_happen
            if prevent_dups_dict[opp.team_name]: continue
            if game_did_happen: matchups.append((opp, team)) # Away Game Since last one was Home
            else: matchups.append((team, opp)) # Home Game Since last one was Away
        
        if home_away_check != 2:
            debug(team.team_name)
            raise ValueError('Each team must have 2 home and 2 away games with their respective inter conference division')

        # SPF
        all_divisions = division_data['inter_conference'].keys()
        spf_divs = [div for div in all_divisions if div.startswith(conf)]
        spf_divs.remove(division)
        spf_divs.remove(team.intra_conference)

        standing = int(standings_2023.loc[standings_2023['team'] == team.team_name]['standing'].iloc[0])

        spf_teams = list(standings_2023.loc[(standings_2023['standing'] == standing) & 
                           (standings_2023['division'].isin(spf_divs))]['team'])
        
        
        for opp in spf_teams:
            if prevent_dups_dict[opp]: continue
            opp = teams[opp]

            # Check Past Standing Games to determine home/away
            opp_div = opp.division
            last_spf_year_by_div = year - 1 if opp_div != team.year_intra_conf(year - 1) else year - 2

            # 1. Get schedules
            standings_year_before = locals()[f'standings_{last_spf_year_by_div - 1}']
            year_by_div_schedule = locals()[f'schedule_{last_spf_year_by_div}']

            # 2. Check standings from year before to determine same standing teams
            same_div_team_name = standings_year_before.loc[(standings_year_before['standing'] == standing) & 
                                            (standings_year_before['division'] == division)].iloc[0]['team']
            opp_div_team_name = standings_year_before.loc[(standings_year_before['standing'] == standing) & 
                                            ((standings_year_before['division'] == opp_div))].iloc[0]['team']
            
            # 3. Check matchup in year by div schedule and add matchup
            game_did_happen = check_matchup(year_by_div_schedule, same_div_team_name, opp_div_team_name)
            if game_did_happen: matchups.append((opp, team)) # Away Game bc prev was Home
            else: matchups.append((team, opp)) # Home Game bc prev was Away
            
        # 17th Game
        # TODO


    # pprint('Home | Away')
    # for t in matchups:
    #     pprint(t[0].team_name + ' | ' + t[1].team_name)
    debug(len(matchups))
    if len(matchups) != total_games:
        raise ValueError('Total Generated Matchups do not match expected number')
    return matchups
