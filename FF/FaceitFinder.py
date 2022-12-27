from tkinter import *
from tkinter import messagebox
from SearchAlgo import getFaceitPlayerElo

# FACEIT STYLEGUIDE
# FONT PANTONE 
# GRAY #1f1f1f
# DARK GRAY #161616
# WHITE #EBEFF3
# ORANGE #ff5500

# TODO
# Profile anklickbar machen und mehr stats einzeigen lassen
# Spieler nach elo sortieren
# ... 

# Remove old widgets
def destroyOldWidgets():
    for widget in widgets.values():
        widget.destroy()

# Add user to friends list 
def addUser(steamID,b):
    print(steamID)
    b.config(state=DISABLED)
    with open('C:\\Program Files\\FaceitFinder\\dist\\friends.txt', 'a') as f:
        f.write("".join(steamID) + "\n")

# Generates the ouput
def generateOutput():
    # Make sure no old widgets are left over from a previouse run
    destroyOldWidgets()

    e = inp.get(1.0, "end-1c")

    if e == "deleteFriends":
        print('test')
        with open('C:\\Program Files\\FaceitFinder\\dist\\friends.txt', 'w') as f:
            f.write("")
        messagebox.showinfo('INFO','Friends list has been cleared')
        return 0

    out = getFaceitPlayerElo(e) 

    # Do nothing if the input is not corret
    if out == 0:
        messagebox.showerror('Error','Wrong input')
        return

    # Clear input box
    inp.delete('1.0',END) 


    widgets['lbl_name'] = Label(root,text='Name:',font=('PANTONE',12,'bold'),bg='#161616',fg='#EBEFF3')
    widgets['lbl_name'].grid(row=4,column=1,sticky='w')

    widgets['lbl_elo'] = Label(root,text='Elo:',font=('PANTONE',12,'bold'),bg='#161616',fg='#EBEFF3')
    widgets['lbl_elo'].grid(row=4,column=2,sticky='w')

    for i in range(len(out)):

        # Add padding for the last entry
        if i == len(out)-1:
            y = 10
        else:
            y = 0

        widgets[f"{i}" + "Name"] = Label(root,text=out[i][0],font=('PANTONE',10),bg='#161616',fg='#EBEFF3')
        widgets[f"{i}" + "Name"].grid(row=5+i,column=1,sticky='w',pady=(0,y))

        widgets[f"{i}" + "Elo"] = Label(root,text=out[i][1],font=('PANTONE',10),bg='#161616',fg='#EBEFF3')
        widgets[f"{i}" + "Elo"].grid(row=5+i,column=2,sticky='w',pady=(0,y))

        widgets[f"{i}" + "Add"] = Button(root,text='+',font=('PANTONE',10,'bold'),bg='#161616',fg='#EBEFF3')
        widgets[f"{i}" + "Add"].config(command=lambda k=out[i][2], n=widgets[f"{i}" + "Add"]: addUser(k,n))
        widgets[f"{i}" + "Add"].grid(row=5+i,column=3,sticky='nswe',pady=(0,y))


# Generate widget window
root = Tk()

# Set widget title 
root.title('  FACEIT FINDER')

# Set wiget background color
root.configure(bg='#161616')

# Set widget icon
root.iconbitmap('C:\\Program Files\\FaceitFinder\\images\\Faceit_Icon.ico')

# Create text input box
inp = Text(root, font=('PANTONE'),width=20,height=1)
inp.grid(row=0,column=0,columnspan=5,padx=10,pady=10)

widgets = {}

# Create find button
btn = Button(root,text='FIND',font=('PANTONE',10,'bold'), bg='#FF5500',fg='#EBEFF3',padx=10,pady=5,borderwidth=0, command= generateOutput)
btn.grid(row=1,column=1,columnspan=3,pady=(0,10))



root.mainloop()
