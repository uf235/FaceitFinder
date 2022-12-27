import requests
import json
from steamid_converter import Converter
import re
import os.path

STREAM_KEY = '3C26324A5FE8534817F3568BF3BCE707'
API_KEY = '5c4e1db7-f241-48fe-a334-8a17f7f81d57'
BASE_URL = 'https://open.faceit.com/data/v4'

def getFaceitPlayerElo(input):
    # Check whether an input was given
    if not input :
        return 0

    header = {
        'accept': 'application/json',
        'Authorization': 'Bearer {}'.format(API_KEY)
    }
    
    # Get all the steamID64
    steamIDS = re.findall(r'STEAM([^\s]*)',input)
    steamIDS = ['STEAM' + ID for ID in steamIDS]

    # Get all player names
    player_names = re.findall(r'"([^"]*)',input)[::2] 
    msg = []

    player_data = {}
    for idx,id in enumerate(steamIDS):
        player_data[id] = player_names[idx]
    

    # Check whether a friend was found and remove him
    if os.path.isfile('friends.txt'):
        with open('friends.txt') as f:
            lines = [line.rstrip('\n')for line in f]
            for id in steamIDS:
                if id in lines:
                    player_data.pop(id)

    # Check whether any steamID was found
    if len(player_data) == 0:
        return 0
    
    keys = list(player_data.keys())
    values = list(player_data.values())

    for i in range(len(player_data)): 
        
        steamID64 = Converter.to_steamID64(keys[i])

        #s = requests.get(' http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=3C26324A5FE8534817F3568BF3BCE707&steamids={}'.format(steamID64))
        #sc = json.loads(s.content.decode('utf-8'))

        api_url = '{}/players'.format(BASE_URL)
        api_url += '?game=csgo&game_player_id={}'.format(steamID64)

        res = requests.get(api_url, headers=header)
        stats = json.loads(res.content.decode('utf-8'))
        csgo_stats = stats['games']['csgo']
        faceit_elo = csgo_stats['faceit_elo']
        
        msg.append((values[i],faceit_elo,keys[i]))

    return msg