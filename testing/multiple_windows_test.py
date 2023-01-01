from tkinter import *
import requests
import json
from steamid_converter import Converter
import re
import os.path

API_KEY = '5c4e1db7-f241-48fe-a334-8a17f7f81d57'
BASE_URL = 'https://open.faceit.com/data/v4'
STEAMID = "STEAM_0:1:47072726"

header = {
    'accept': 'application/json',
    'Authorization': 'Bearer {}'.format(API_KEY)
}
steamID64 = Converter.to_steamID64(STEAMID)

api_url = '{}/players'.format(BASE_URL)
api_url += '?game=csgo&game_player_id={}'.format(steamID64)

res = requests.get(api_url, headers=header)
stats = json.loads(res.content.decode('utf-8'))
csgo_stats = stats['games']['csgo']
faceit_elo = csgo_stats['faceit_elo']
print(csgo_stats)

root = Tk()
root.title("Multiple windows")

def openWindow():
    top = Toplevel()
    top.title("Second window")
    lbl = Label(top,text="Dies ist ein test").pack()

btn = Button(root,text="Open new Window", command=openWindow).pack()

root.mainloop()