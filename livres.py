#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 17:39:56 2023
@author: rodolphe
"""

# ********************* bibliothèques utilisées *********************
import pandas as pd
import datetime
from datetime import date
import matplotlib.dates as mdates
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
# *******************************************************************

# ************************* données ********************************
data_livres = "goodreads_library_export.csv"
today = today = date.today()
# *******************************************************************

arrondi = lambda x : x.floor('1d')
semaine = lambda x: "S"+ (x[1:] if x.startswith('0') else x)

def plot_target(target, année = today.year):
    # lecture du fichier créé par Goodreads
    df = pd.read_csv(data_livres, parse_dates=True)
    # transformation de 'Date Read' au format date
    df['Date Read']  = pd.to_datetime(df['Date Read']).dt.date
    # on ne retient que l'ID et la date de lecture
    df = df[(df['Date Read'] >= datetime.date(année,1,1))].loc[:,['Date Read']]
    # tri par ordre croissant de la date
    df.sort_values(by='Date Read', inplace = True)
    # création d'un indicateur du nombre de livres lus
    # si plusieurs livres lus un même jour, la somme est conservée 
    df['read']=1
    df['read']= df['read'].cumsum()
    df= df.rename(columns={'Date Read': 'date'}) 
    df = df.drop_duplicates(subset='date', keep="last")
    
    # création de la base objectif
    #bins = pd.date_range(start='2023-01-01', end='2023-12-31', periods=target+1)
    objectif = list(map(arrondi, pd.date_range(start = datetime.date(année,1,1), \
                            end=datetime.date(année,12,31), periods=target+1)))
    dg = pd.DataFrame(objectif, columns = ['date'])
    dg['date'] =  pd.to_datetime(dg['date']).dt.date
    dg['objectif']=1
    dg = dg.tail(-1)
    dg['objectif']=dg['objectif'].cumsum()
        
    # fusion et calcul de l'écart à l'objectif
    # fusion des deux bases de données
    dh = pd.concat([dg, df])
    dh.sort_values(by='date', inplace = True)
    # suppression des cellules vides et des doublons 
    dh = dh.fillna(method='ffill').drop_duplicates(subset='date', keep="last")
    dh['objectif'] = dh['objectif'].fillna(0)
    dh['to target'] = dh['read'] - dh['objectif']
    
    # création du graphique
    fig, ax = plt.subplots(figsize=(12,4))
    ax.plot([datetime.date(2023,1,1), today], [0,0], color = 'black', linewidth = .75)
    dh.plot(x='date', y = 'to target', drawstyle='steps', ax = ax, color = 'green')    
    
    # personnalisation du graphique
    plt.rcParams['font.family'] = 'cambria'
    ax.set_xlim([datetime.date(2023,1,1), today])
    ax.set_ylim([-10, 10])
    ax.xaxis.set_major_formatter(mdates.DateFormatter(semaine('%W')))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=(0)))
    ax.tick_params(axis='x', labelsize=8, color = 'none', labelcolor = 'black', rotation=0)
    ax.grid(which='major', axis='x', linewidth=0.5, linestyle='--', color='0.5')    
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.tick_params(axis='y', labelsize=8, color = 'none', labelcolor = 'black', rotation=0)
    ax.grid(which='major', axis='y', linewidth=0.5, linestyle='--', color='0.5')
    ax.legend(fontsize= 10, frameon = False)
    ax.set(xlabel=None)
    ax.set_axisbelow(True)
    
    # sauvegarde de la figure
    fig.savefig("to target "+ str(année) +" "+ today.strftime("%d%m%y")+".svg")
    
plot_target(target = 100, année = 2023)