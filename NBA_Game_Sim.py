#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import libraries 
import pandas as pd
import numpy as np
import random as rnd
import matplotlib.pyplot as plt
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder


# In[2]:


# access all games from 2021-22 regular season
games = leaguegamefinder.LeagueGameFinder(season_nullable='2021-22', league_id_nullable='00', 
                                          season_type_nullable = 'Regular Season').get_data_frames()[0]


# In[3]:


# create new field for points allowed by team
games['ALLOWED'] = games['PTS']-games['PLUS_MINUS']


# In[5]:


# select final columns and group by team for mean and standard deviation 
games_final = games[['TEAM_ID', 'TEAM_NAME', 'PTS', 'ALLOWED']]
averages = games_final.groupby(['TEAM_ID', 'TEAM_NAME']).mean()
stdv = games_final.groupby(['TEAM_ID', 'TEAM_NAME']).std()


# In[6]:


# rename columns and create final data frame 
averages.rename(columns = {'PTS':'PTS_AVG', 'ALLOWED':'ALLOWED_AVG'}, inplace = True)
stdv.rename(columns = {'PTS':'PTS_STDV', 'ALLOWED':'ALLOWED_STDV'}, inplace = True)
df_final = pd.merge(averages, stdv, on=["TEAM_NAME"])


# In[7]:


df_final = df_final.reset_index()
df_final.head()


# In[8]:


# create game class with inputs for home and away team

class Game: 
    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.home_team_pts_avg = df_final.PTS_AVG[df_final.TEAM_NAME == home_team].to_numpy()[0]
        self.home_team_pts_stdv = df_final.PTS_STDV[df_final.TEAM_NAME == home_team].to_numpy()[0]
        self.home_team_allowed_avg = df_final.ALLOWED_AVG[df_final.TEAM_NAME == home_team].to_numpy()[0]
        self.home_team_allowed_stdv = df_final.ALLOWED_STDV[df_final.TEAM_NAME == home_team].to_numpy()[0]
        self.away_team = away_team
        self.away_team_pts_avg = df_final.PTS_AVG[df_final.TEAM_NAME == away_team].to_numpy()[0]
        self.away_team_pts_stdv = df_final.PTS_STDV[df_final.TEAM_NAME == away_team].to_numpy()[0]
        self.away_team_allowed_avg = df_final.ALLOWED_AVG[df_final.TEAM_NAME == away_team].to_numpy()[0]
        self.away_team_allowed_stdv = df_final.ALLOWED_STDV[df_final.TEAM_NAME == away_team].to_numpy()[0]  


# In[15]:


# create simulation function with input for game and number of iterations 

def Sim(Game, N):
    home_scores = []
    away_scores = []
    home_team_wins = 0
    away_team_wins = 0
    counter = 0
    
    while counter < N:
        home_team_score = round((rnd.gauss(Game.home_team_pts_avg, Game.home_team_pts_stdv)+ 
                  rnd.gauss(Game.away_team_allowed_avg, Game.away_team_allowed_stdv))/2)
        home_scores.append(home_team_score)
        away_team_score = round((rnd.gauss(Game.away_team_pts_avg, Game.away_team_pts_stdv)+ 
                  rnd.gauss(Game.home_team_allowed_avg, Game.home_team_allowed_stdv))/2)
        away_scores.append(away_team_score)
        if home_team_score > away_team_score:
            home_team_wins += 1
            counter += 1            
        elif home_team_score < away_team_score:
            away_team_wins += 1
            counter += 1
              
    print(Game.home_team, home_team_wins/(home_team_wins+away_team_wins)*100,'%')
    print(Game.away_team, away_team_wins/(home_team_wins+away_team_wins)*100,'%')
    print(Game.home_team, "average points", round(sum(home_scores)/len(home_scores)))
    print(Game.away_team, "average points", round(sum(away_scores)/len(away_scores)))


# In[16]:


New_Game = Game("Orlando Magic", "Boston Celtics")      


# In[17]:


Sim(New_Game, 1000)


# In[ ]:




