from tkinter import *
from tkinter import messagebox
import logging
import json
import requests
import re
import os.path
import webbrowser

# FACEIT STYLEGUIDE
# FONT PANTONE 
# GRAY #1f1f1f
# DARK GRAY #161616
# WHITE #EBEFF3
# ORANGE #ff5500

# TODO
# Profile anklickbar machen und mehr stats einzeigen lassen
# Spieler name in die freinds datei packen damit man sieht wenn man löscht ?

# Constant variables
STREAM_KEY = '3C26324A5FE8534817F3568BF3BCE707'
API_KEY = '5c4e1db7-f241-48fe-a334-8a17f7f81d57'
BASE_URL = 'https://open.faceit.com/data/v4'
FACEIT_URL = 'https://www.faceit.com/de'
STEAMID64INTEND = 76561197960265728


# Convert a steamid to a steamid64
def steamid_to_steamid64(steamid):
    # Get logger
    logger = logging.getLogger('logger')
    
    try:
        logger.info('Try to convert steamid to steamid64')
        # Conversion alogrithmus
        sid_split = steamid.split(':')
        commid = int(sid_split[2]) * 2
        if sid_split[1] == '1':
            commid += 1
        commid += STEAMID64INTEND

        logger.info('Converted steamid to steamid64')
    except:
        logger.exception('Steamid could not be converted')

    return commid  

# Get the names and steamid from the input
def filterInput(input):
    # Get logger
    logger = logging.getLogger('logger')

    player_data = {}

    # Get all the steamID64
    steamIDS = re.findall(r'STEAM([^\s]*)',input)
    steamIDS = ['STEAM' + ID for ID in steamIDS]

    # Get all player names
    player_names = re.findall(r'"([^"]*)',input)[::2] 

    # If a bot was in the status remove the bot from player_names
    if len(player_names) > len(steamIDS):
        diff = len(player_names) - len(steamIDS)
        player_names = player_names[diff:]
        logger.info('Removed bots from list')
    
    # Pair the player names with their id
    for idx,id in enumerate(steamIDS):
        player_data[id] = player_names[idx]

    # Check whether a friend was found and remove him
    try:
        logger.info('Try to check whether a player is marked as friend')
        if os.path.isfile('friends.txt'):
            with open('friends.txt') as f:
                lines = [line.rstrip('\n')for line in f]
                for id in steamIDS:
                    if id in lines:
                        player_data.pop(id)
                        logger.info(f"Friend was found and removed from list")
    except:
        logger.exception('Could not check whether friend is alread in friendlist')

    # Check whether any steamID was found
    if len(player_data) == 0:
        logger.info("No player was found")
        return 0
    logger.info("Players were found")

    return player_data

# Get all necessary inforation about the player
def getFaceitPlayerElo(input):

    output = []

    # Check whether an input was given
    if not input :
        return 0

    # Header for requests
    header = {
        'accept': 'application/json',
        'Authorization': 'Bearer {}'.format(API_KEY)
    }
    
    # Get the name and steamid64
    player_data = filterInput(input)
   
    # Get lists of all keys and values from player_data
    keys = list(player_data.keys())
    values = list(player_data.values())

    # Iterate over all players and get the faceit elo
    try:
        logger.info('Try to get faceit data for each player')
        for i in range(len(player_data)): 
            
            # Convert steamid to steamid64
            steamID64 = steamid_to_steamid64(keys[i])

            # Build request link
            api_url = '{}/players'.format(BASE_URL)
            api_url += '?game=csgo&game_player_id={}'.format(steamID64)

            # Send request to the faceit api and receive the data
            res = requests.get(api_url, headers=header)
            # Ensure that programm wound fail if a player has no faceit account
            if res.status_code == requests.codes.ok:
                stats = json.loads(res.content.decode('utf-8'))
                player_profile_url = 'https://www.faceit.com/de/players/{}'.format(stats['nickname'])
                csgo_stats = stats['games']['csgo']
                faceit_elo = csgo_stats['faceit_elo']
                output.append((values[i],faceit_elo,keys[i],player_profile_url))
            else:
                logger.error("Player with no faceit account was found. Elo got set to 0")
                faceit_elo = 0
                player_profile_url = 'https://www.faceit.com/de'
                output.append((values[i],faceit_elo,keys[i],player_profile_url))
    except:
        logger.exception('Faceit data could not be accessed')

    # Sort elo from high to low
    output.sort(reverse=True,key = lambda l : l[1])

    return output

# Create logger
def initLogger():
    # Initalize the logger config
    # level = logging.NOTSET to ensure all levels off the logger 
    # are being printed into the log file
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',filename="logger.log", encoding='utf-8', level=logging.NOTSET)
    logger = logging.getLogger('logger')
    logger.info("Logger was successfully created")

# Remove old widgets
def destroyOldWidgets():
    # Get logger
    logger = logging.getLogger('logger')
    logger.info('Try to destroy previouse widgets')

    try:
        # Iterate through widget dictionary and destroy all widget on the window
        # to enusre no old widget do not get the way of the new ones
        for widget in widgets.values():
            widget.destroy()
        logger.info("Widgets from previouse run got destroyed")
    except:
        logger.exception("Widget cound not be destroyed")
        
# Add user to friends list 
def addUser(steamID,b):
    # Get logger
    logger = logging.getLogger('logger')
    logger.info('Try to add player to friends list')

    try:
        # Disable the buttion after usage
        b.config(state=DISABLED)
        # Write steamid in friends.txt
        with open('friends.txt', 'a') as f:
            f.write("".join(steamID) + "\n")
        logger.info("Friend was added to friends.txt")
    except:
        logger.exception("Friend could not be added to friends.txt")

def callURL(url):
    webbrowser.open_new_tab(url)

# Create all widget
def CreateLabelsDynamicly(player_informations):

    # Get logger
    logger = logging.getLogger('logger')
    logger.info('Try to create all labels and buttons dynamicly')
    try:
        # Iterate over all elements and create labels for name and elo and a button 
        # for adding the players to friends list
        for i in range(len(player_informations)):
            # Add padding for the last entry
            if i == len(player_informations)-1:
                y = 10
            else:
                y = 0

            # Save the labels and button in dictonary widget to dynamicly access the widgets
            # Create label for the name
            widgets[f"{i}" + "Name"] = Label(root,text=player_informations[i][0],font=('PANTONE',10),bg='#161616',fg='#EBEFF3', cursor='hand2')
            widgets[f"{i}" + "Name"].grid(row=5+i,column=1,sticky='w',pady=(0,y))
            # Only bind if profile exits
            widgets[f"{i}" + "Name"].bind('<Button-1>', lambda event, url=player_informations[i][3]: callURL(url))

            # Create label for the elo
            widgets[f"{i}" + "Elo"] = Label(root,text=player_informations[i][1],font=('PANTONE',10),bg='#161616',fg='#EBEFF3')
            widgets[f"{i}" + "Elo"].grid(row=5+i,column=2,sticky='w',pady=(0,y))

            # Create button to add player to friendslist
            widgets[f"{i}" + "Add"] = Button(root,text='+',font=('PANTONE',10,'bold'),bg='#161616',fg='#EBEFF3')
            widgets[f"{i}" + "Add"].config(command=lambda k=player_informations[i][2], n=widgets[f"{i}" + "Add"]: addUser(k,n))
            widgets[f"{i}" + "Add"].grid(row=5+i,column=3,sticky='nswe',pady=(0,y))
        
        logger.info('All labels and buttons got successfully created')
    except:
        logger.exception('Widget cound not be created')
    
# Create the ouput       
def generateOutput():
    # Make sure no old widgets are left over from a previouse run
    destroyOldWidgets()

    # Get the input from the textbox
    e = inp.get(1.0, "end-1c")

    # Command to clear the friendslist
    try:
        if e == "deleteFriends":
            logger.info('Try to clear friendslist')

            with open('friends.txt', 'w') as f:
                f.write("")

            messagebox.showinfo('INFO','Friends list has been cleared')
            logger.info("Friendslist has been cleared")

            return 0
    except:
        logger.exception('Friendslist cound not be cleard')

    # Get a list of pair with ('name','elo','steamid')
    player_informations = getFaceitPlayerElo(e) 

    # Do nothing if the input is not corret
    if player_informations == 0:
        messagebox.showerror('Error','Wrong input')
        logger.error('Wrong input given')
        return 0

    # Clear input box
    inp.delete('1.0',END) 

    # Create headlines
    widgets['lbl_name'] = Label(root,text='Name:',font=('PANTONE',12,'bold'),bg='#161616',fg='#EBEFF3')
    widgets['lbl_name'].grid(row=4,column=1,sticky='w')

    widgets['lbl_elo'] = Label(root,text='Elo:',font=('PANTONE',12,'bold'),bg='#161616',fg='#EBEFF3')
    widgets['lbl_elo'].grid(row=4,column=2,sticky='w')

    # Create all labels and buttons
    CreateLabelsDynamicly(player_informations)

if __name__ == '__main__':

    initLogger()
   
    # Get logger
    logger = logging.getLogger('logger')

    # Generate widget window
    root = Tk()

    # Set widget title 
    root.title('  FACEIT FINDER')

    # Set wiget background color
    root.configure(bg='#161616')

    # Set widget icon
    try:
        root.iconbitmap('Faceit_Icon.ico')
    except:
        print("Icon not found")

    # Create text input box
    inp = Text(root, font=('PANTONE'),width=20,height=1)
    inp.grid(row=0,column=0,columnspan=5,padx=10,pady=10)

    widgets = {}

    # Create find button
    btn = Button(root,text='FIND',font=('PANTONE',10,'bold'), bg='#FF5500',fg='#EBEFF3',padx=10,pady=5,borderwidth=0, command= generateOutput)
    btn.grid(row=1,column=1,columnspan=3,pady=(0,10))

    logger.info("Window was successfully build")

    root.mainloop()
