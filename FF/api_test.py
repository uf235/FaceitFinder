import requests
import json

stmid = "STEAM_0:1:53810211"

steamid64ident = 76561197960265728

def steamid_to_steamid64(steamid):
  sid_split = steamid.split(':')
  commid = int(sid_split[2]) * 2
  
  if sid_split[1] == '1':
      commid += 1
  
  commid += steamid64ident
  return commid  


STEAM_KEY = '3C26324A5FE8534817F3568BF3BCE707'
STEAMID = '76561198202481531'
import valve.source
import valve.source.a2s
import valve.source.master_server

with valve.source.master_server.MasterServerQuerier() as msq:
    try:
        for address in msq.find(region=[u"eu", u"as"],
                                gamedir=u"tf",
                                map=u"ctf_2fort"):
            try:
                with valve.source.a2s.ServerQuerier(address) as server:
                    info = server.info()
                    players = server.players()

            except valve.source.NoResponseError:
                print("Server {}:{} timed out!".format(*address))
                continue

            print("{player_count}/{max_players} {server_name}".format(**info))
            for player in sorted(players["players"],
                                 key=lambda p: p["score"], reverse=True):
                print("{score} {name}".format(**player))

    except valve.source.NoResponseError:
        print("Master server request timed out!")
# Get ISteamUserStats
#userStats = requests.get('https://api.steampowered.com/IGameServersService/GetServerIPsBySteamID/v1/?key=3C26324A5FE8534817F3568BF3BCE707&steamid=76561198202481531')
#userStats = json.loads(userStats.content.decode('utf-8'))
#s = requests.get('https://partner.steam-api.com/ISteamGameServerStats/GetGameServerPlayerStatsForGame/v1/?key={STEAM_KEX}')
#print(userStats["playerstats"]["stats"])