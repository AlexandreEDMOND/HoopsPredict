import pandas as pd

import requests
from bs4 import BeautifulSoup, Comment
import re
import os

import urllib3
# Désactiver les avertissements de sécurité
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Match():

    def __init__(self, lien):
        self.lien = lien

    # Scraping sur site + Beautiful Soup
    def generate_soup(self):
        response = requests.get(self.lien, verify=False)

        # Vérifier si la requête a réussi
        if response.status_code == 200:
            # Parser le contenu HTML avec BeautifulSoup
            self.soup = BeautifulSoup(response.content, 'html.parser')
            return True
        
        else:
            print(f"Erreur de scrapping. Status code : {response.status_code}")
            return False
    

    def get_line_score(self):
        line_score = []

        # Extraire tous les commentaires
        for comment in self.soup.find_all(string=lambda text: isinstance(text, Comment)):
            # Trouver le commentaire pour la line score
            if '<div class="table_container" id="div_line_score">' in comment:
                
                comment_soup = BeautifulSoup(comment, 'html.parser')
                for tbody in comment_soup.find_all('tbody'):
                    for row in tbody:
                        if row != "\n":
                            teams_info = []
                            for col in row:
                                if col != "\n":
                                    teams_info.append(col.text.strip())
                            line_score.append(teams_info)
                break

        #On rajoute les Overtimes dans les colonnes
        columns=['Team', 'Q1', 'Q2', 'Q3', 'Q4', 'Total']
        for i in range(len(line_score[0]) - len(columns)):
            columns.insert(5 + i, f'OT{i+1}')

        self.df_line_score = pd.DataFrame(line_score, columns=columns)


    def get_team_abbreviation(self):
        [self.away_team, self.home_team] = self.df_line_score['Team'].tolist()
    
    def get_four_factors(self):
        four_factors = []

        # Extraire tous les commentaires
        for comment in self.soup.find_all(string=lambda text: isinstance(text, Comment)):
            # Trouver le commentaire pour la line score
            if '<div class="table_container" id="div_four_factors">' in comment:

                comment_soup = BeautifulSoup(comment, 'html.parser')
                for tbody in comment_soup.find_all('tbody'):
                    for row in tbody:
                        if row != "\n":
                            teams_info = []
                            for col in row:
                                if col != "\n":
                                    teams_info.append(col.text.strip())
                            four_factors.append(teams_info)
                break

        self.df_four_factors = pd.DataFrame(four_factors, columns=['Team', 'Pace Factor', 'Effective Field Goal Percentage', 'Turnover Percentage',
                                                            'Offensive Rebound Percentage', 'FT/FGA', 'Offensive Rating'])

    def get_away_basic_stat(self):

        away_basic_stats = []

        for comment in self.soup.find_all('div', class_="table_container", id=f"div_box-{self.away_team}-game-basic"):
            for tbody in comment.find_all('tbody'):
                for row in tbody:
                    if row != "\n":
                        teams_info = []
                        for col in row:
                            if col != "\n":
                                teams_info.append(col.text.strip())
                        away_basic_stats.append(teams_info)

        # On enlève la ligne des réservistes
        away_basic_stats.pop(5)

        self.df_away_basic_stats = pd.DataFrame(away_basic_stats, columns=['Name', 'Minutes Played', 'Field Goals', 'FGA', 'Field Goal Percentage', '3-Point Field Goals',
                                                            '3-Point Field Goal Attempts', '3-Point Field Goal Percentage', 'Free Throws', 'Free Throw Attempts',
                                                            "Free Throw Percentage", "Offensive Rebounds", "Defensive Rebounds", "Total Rebounds", "Assists", "Steals",
                                                            "Blocks", "Turnovers", "Personal Fouls", "Points", "Game Score", "Plus/Minus"])
    
    def get_away_advanced_stat(self):
        away_advanced_stats = []

        for comment in self.soup.find_all('div', class_="table_container", id=f"div_box-{self.away_team}-game-advanced"):
            for tbody in comment.find_all('tbody'):
                for row in tbody:
                    if row != "\n":
                        teams_info = []
                        for col in row:
                            if col != "\n":
                                teams_info.append(col.text.strip())
                        away_advanced_stats.append(teams_info)

        # On enlève la ligne des réservistes
        away_advanced_stats.pop(5)

        self.df_away_advanced_stats = pd.DataFrame(away_advanced_stats, columns=['Name', 'Minutes Played', 'True Shooting Percentage', 'Effective Field Goal Percentage', 
                                                                        '3-Point Attempt Rate', 'Free Throw Attempt Rate', 'Offensive Rebound Percentage', 
                                                                        'Defensive Rebound Percentage', 'Total Rebound Percentage', 'Assist Percentage', 'Steal Percentage', 
                                                                        'Block Percentage', 'Turnover Percentage', 'Usage Percentage', 'Offensive Rating', 'Defensive Rating', 'BPM'])
        


    def get_home_basic_stat(self):
        home_basic_stats = []

        for comment in self.soup.find_all('div', class_="table_container", id=f"div_box-{self.home_team}-game-basic"):
            for tbody in comment.find_all('tbody'):
                for row in tbody:
                    if row != "\n":
                        teams_info = []
                        for col in row:
                            if col != "\n":
                                teams_info.append(col.text.strip())
                        home_basic_stats.append(teams_info)

        # On enlève la ligne des réservistes
        home_basic_stats.pop(5)

        self.df_home_basic_stats = pd.DataFrame(home_basic_stats, columns=['Name', 'Minutes Played', 'Field Goals', 'FGA', 'Field Goal Percentage', '3-Point Field Goals',
                                                            '3-Point Field Goal Attempts', '3-Point Field Goal Percentage', 'Free Throws', 'Free Throw Attempts',
                                                            "Free Throw Percentage", "Offensive Rebounds", "Defensive Rebounds", "Total Rebounds", "Assists", "Steals",
                                                            "Blocks", "Turnovers", "Personal Fouls", "Points", "Game Score", "Plus/Minus"])

    def get_home_advanced_stat(self):
        home_advanced_stats = []

        for comment in self.soup.find_all('div', class_="table_container", id=f"div_box-{self.home_team}-game-advanced"):
            for tbody in comment.find_all('tbody'):
                for row in tbody:
                    if row != "\n":
                        teams_info = []
                        for col in row:
                            if col != "\n":
                                teams_info.append(col.text.strip())
                        home_advanced_stats.append(teams_info)

        # # On enlève la ligne des réservistes
        home_advanced_stats.pop(5)

        self.df_home_advanced_stats = pd.DataFrame(home_advanced_stats, columns=['Name', 'Minutes Played', 'True Shooting Percentage', 'Effective Field Goal Percentage', 
                                                                        '3-Point Attempt Rate', 'Free Throw Attempt Rate', 'Offensive Rebound Percentage', 
                                                                        'Defensive Rebound Percentage', 'Total Rebound Percentage', 'Assist Percentage', 'Steal Percentage', 
                                                                        'Block Percentage', 'Turnover Percentage', 'Usage Percentage', 'Offensive Rating', 'Defensive Rating', 'BPM'])

    def get_inactive(self):
        # Trouver les sections des joueurs inactifs
        divs = self.soup.find_all('div')
        for div in divs:
            if "Inactive:" == div.text[:9]:

                inactive_text = div.text.replace('\xa0', ' ')

                away_inactive = []
                home_inactive = []

                away_part = re.search(rf'{self.away_team} (.*) {self.home_team}', inactive_text)
                if away_part:
                    away_inactive = away_part.group(1).split(', ')
                    # Nettoyer les espaces supplémentaires
                    away_inactive = [name.strip() for name in away_inactive]

                # Trouver la partie après "DEN"
                home_part = re.search(rf'{self.home_team} (.*)', inactive_text)
                if home_part:
                    home_inactive = home_part.group(1).split(', ')
                    # Nettoyer les espaces supplémentaires
                    home_inactive = [name.strip() for name in home_inactive]

        self.away_inactive = away_inactive
        self.home_inactive = home_inactive
    
    def show_all_df_head(self):
        print(self.df_line_score.head())
        print(self.df_four_factors.head())
        print(self.df_away_basic_stats.head())
        print(self.df_away_advanced_stats.head())
        print(self.df_home_basic_stats.head())
        print(self.df_home_advanced_stats.head())
        print(f"Absent {self.away_team} : {self.away_inactive}")
        print(f"Absent {self.home_team} : {self.home_inactive}")

    def scrap_information(self):

        is_scrapping_good = self.generate_soup()

        # Si le scrapping n'a pas eu lieu, on le dit
        if is_scrapping_good == False:
            return False
        
        self.get_line_score()
        self.get_team_abbreviation()
        self.get_four_factors()
        self.get_away_basic_stat()
        self.get_away_advanced_stat()
        self.get_home_basic_stat()
        self.get_home_advanced_stat()
        self.get_inactive()

        return True
    
    def save_df(self, path_dir_save="data_2023_2024/box_score_regular_season"):

        id_match = self.lien[47:55] + self.away_team + self.home_team 

        name_dir = "box_sore_" + id_match

        subfolder_path = os.path.join(path_dir_save, name_dir)

        # Crée le sous-dossier s'il n'existe pas déjà
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
            # print(f"Le sous-dossier '{name_dir}' a été créé dans '{path_dir_save}'.")
        else:
            print(f"Le sous-dossier '{name_dir}' existe déjà dans '{path_dir_save}'.")
            return

        self.df_line_score.to_csv(os.path.join(subfolder_path, "df_line_score.csv"))
        self.df_four_factors.to_csv(os.path.join(subfolder_path, "df_four_factors.csv"))
        self.df_away_basic_stats.to_csv(os.path.join(subfolder_path, "df_away_basic_stats.csv"))
        self.df_away_advanced_stats.to_csv(os.path.join(subfolder_path, "df_away_advanced_stats.csv"))
        self.df_home_basic_stats.to_csv(os.path.join(subfolder_path, "df_home_basic_stats.csv"))
        self.df_home_advanced_stats.to_csv(os.path.join(subfolder_path, "df_home_advanced_stats.csv"))

        print(f"Les informations du match {id_match} ont bien été enregistrées")
