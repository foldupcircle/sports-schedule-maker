from leagues import NFL_TEAMS, NBA_TEAMS, MLB_TEAMS, IPL_TEAMS, EPL_TEAMS

def main():
    league = str(input())
    teams = []
    games = 0
    if league == 'NFL':
        teams = NFL_TEAMS
        games = 17
    elif league == 'NBA':
        teams = NBA_TEAMS
        games = 82
    elif league == 'MLB':
        teams = MLB_TEAMS
        games = 162
    elif league == 'IPL':
        teams = IPL_TEAMS
        games = 14
    elif league == 'EPL':
        teams = EPL_TEAMS
        games = 38
    else:
        raise ValueError('Input must be one of: NFL, NBA, MLB, IPL, EPL')
    print(len(teams), games)

if __name__ == '__main__':
    main()