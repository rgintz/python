#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 20:54:13 2020
@author: Rodolphe Gintz
"""

# ********************* FONCTIONNEMENT DU MODULE *********************
# le module lit les données twitter contenues dans le fichier tweets.js
# Ce fichier est directement fourni par twitter
# Paramètres > Compte > Vos données twiiter
# Le fchier est parcouru ligne à ligne à la recherche des balises :
# - id : code id du tweet
# - full_text : texte du tweet
# - created_at : date de l'écriture du tweet
# - retweet_count : nombre de retweet
# - favorite_count : nombre de fav
# - in_reply_to_screen_name : alias du compte auquel il est répondu
# Il retourne les données dans un ficher au format CSV (sép : ";")
# ********************************************************************

# *********************** LIBRAIRIES UTILISEES ***********************
import time
from datetime import datetime, date, time
# ******************************************************************** 

# ************************* FONCTIONS UTILES *************************
# préfixe au format AAMMJJ-HHhMM :
# AAAA = année
# MM  mois
# JJ = jour
# HH = heure
# MM = minute
# 20200103-19h41 = 3 janvier 2020 à 19h43

def prefixe_file():
    maintenant = datetime.now()
    date = str(maintenant.year)
    
    if maintenant.month <10: date= date + "0"+ str(maintenant.month)
    else: date = date + str(maintenant.month)
    
    if maintenant.day <10: date= date + "0"+ str(maintenant.day)+ "-"
    else: date = date + str(maintenant.day)+"-"
    
    if maintenant.hour <10: date= date + "0"+ str(maintenant.hour)+"h"
    else: date = date + str(maintenant.hour)+"h"

    if maintenant.minute <10: date= date + "0"+ str(maintenant.minute)
    else: date = date + str(maintenant.minute)

    return date

# A partir d'une chaine dans tweet.js qui est au format :
# "JJJ MMM DD HH;MM:SS +0000 AAAA"
# exemple : "Sun Dec 29 13:12:07 +0000 2019"
# - extrait la date et la renvoie au format JJ/MM/AAAA
def ExtraitDate(chaine):
    list_mois = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    year = chaine[-4:]
    month = list_mois.index(chaine[4:7])+1
    day = chaine[8:10]
    return day+"/"+str(month)+"/"+year

# - extrait l'heure et la renvoie au format HH:MM
def ExtraitHeure(chaine):
    hour = chaine[11:13]
    minute = chaine[14:16]
    return hour+":"+minute

# ******************************************************************** 

def ParseTwitterJS(twitter_file):
    dic_balise = ["id", "full_text","created_at","time", "retweet_count","favorite_count", "in_reply_to_screen_name"]
    nb_balise  = len(dic_balise)
    balise_fin = [",\n","\n"]    
        
    tweet_list = list()
    tweet_properties = [''] * nb_balise
    i = 0
    suffixe = "\" : "
    
    file = open(twitter_file, 'r')  
    
    for line in file:        
        if "display_text_range" in line: 
            i +=1
            if i>1:
                tweet_list.append(tweet_properties)
                tweet_properties = [''] * nb_balise
                            
        for balise in dic_balise:
            if balise+suffixe in line: 
               valeur = line.split(balise+suffixe)[1] 
               for balisef in balise_fin:    
                   if balisef in valeur:
                       valeur= valeur.split(balisef)[0][1:-1]
                       if balise == "created_at":
                           tweet_properties[2] = ExtraitDate(valeur)
                           tweet_properties[3] = ExtraitHeure(valeur)
                       else:
                           tweet_properties[dic_balise.index(balise)] = valeur.replace(";","%%")       
    tweet_list.append(tweet_properties)
    
    header = ""
    for balise in dic_balise:
       if balise == dic_balise[-1]: header = header+balise+"\n"
       else: header = header+balise+";"
    
    filename = prefixe_file()+" tweets.csv"
    with open(filename, 'w') as f:
        f.write(header)
        for tweet in tweet_list:
            for counter, value in enumerate(tweet):
                if counter == nb_balise-1: f.write(value+"\n")
                else: f.write(value+";")
        f.close()
        
def main():    
    file = 'tweet.js' # fichier fourni par twitter
    ParseTwitterJS(file)

if __name__ == '__main__':
    main()
