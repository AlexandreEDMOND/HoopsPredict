import pandas as pd

# Dictionnaire de noms d'équipes et leurs abréviations
nba_teams = {
    "Atlanta Hawks": "ATL",
    "Boston Celtics": "BOS",
    "Brooklyn Nets": "BRK",
    "Charlotte Hornets": "CHO",
    "Chicago Bulls": "CHI",
    "Cleveland Cavaliers": "CLE",
    "Dallas Mavericks": "DAL",
    "Denver Nuggets": "DEN",
    "Detroit Pistons": "DET",
    "Golden State Warriors": "GSW",
    "Houston Rockets": "HOU",
    "Indiana Pacers": "IND",
    "Los Angeles Clippers": "LAC",
    "Los Angeles Lakers": "LAL",
    "Memphis Grizzlies": "MEM",
    "Miami Heat": "MIA",
    "Milwaukee Bucks": "MIL",
    "Minnesota Timberwolves": "MIN",
    "New Orleans Pelicans": "NOP",
    "New York Knicks": "NYK",
    "Oklahoma City Thunder": "OKC",
    "Orlando Magic": "ORL",
    "Philadelphia 76ers": "PHI",
    "Phoenix Suns": "PHO",
    "Portland Trail Blazers": "POR",
    "Sacramento Kings": "SAC",
    "San Antonio Spurs": "SAS",
    "Toronto Raptors": "TOR",
    "Utah Jazz": "UTA",
    "Washington Wizards": "WAS"
}




def open_csv(path_file="data_2023_2024/date_team_result/date_teams_result_match_23_24_regular_season.csv"):

    df = pd.read_csv(path_file)

    return df


def transform_list_date(list_date):
    new_list_date = []

    for date in list_date:
        new_date = date.replace('-', '')
        new_date += '0'
        new_list_date.append(new_date)
    
    return new_list_date


def transform_list_team(list_team):
    new_list_team = []

    for team in list_team:
        new_team = nba_teams[team]
        new_list_team.append(new_team)

    return new_list_team


def get_suffixe_lien(list_date_dataframe, list_team):

    suffixe_lien = []

    for i in range(len(list_date_dataframe)):
        suffixe = list_date_dataframe[i] + list_team[i]
        suffixe_lien.append(suffixe)
    
    return suffixe_lien


def get_list_lien():
    df = open_csv()

    list_date_dataframe = df['Date'].tolist()
    list_team = df['Home/Neutral'].tolist()

    list_date_dataframe = transform_list_date(list_date_dataframe)
    list_team = transform_list_team(list_team)

    suffixe_lien = get_suffixe_lien(list_date_dataframe, list_team)

    list_lien = []

    for suffixe in suffixe_lien:
        lien = f"https://www.basketball-reference.com/boxscores/{suffixe}.html"
        list_lien.append(lien)

    return list_lien
