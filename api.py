# imported modules
from tkinter import *
from PIL import *
from PIL import Image, ImageTk
from tkinter import messagebox
import requests
import json
from io import BytesIO
import random

class Pokemon: # created a pokemon class
    # constructor with related value
    def __init__(self, name):
        self.name = name

# created main window
main = Tk()
main.title("Find Your Pokemon")
main.geometry('700x600')
main.resizable(0,0)
main.iconphoto(False, ImageTk.PhotoImage(file = 'pokeball1.png')) # changed the icon of the app
    
# function to get API data
def get_url(func):
    # assign the fetched data as a global variable that can be used outside the function
    global poke_data
    global response
    url = f"https://pokeapi.co/api/v2/pokemon/{func}" # link the API via URL
    response = requests.get(url) # request to get the data
    # write the data to the json file
    poke_data = response.json()
    with open("poke.json", "w") as file:
        json.dump(poke_data,file,indent=4)

# function to link the user's entry to the API
def get_pokemon_info():
    poke_entry = entry.get() # gathers the user's input
    pokename = Pokemon(poke_entry) # class object with assigned entry value
    get_url(pokename.name) # calls the function for the url with assigned parameter
    # a condition to call the validate_pokemon function and check the user's entry
    if response.status_code == 200:
        info_one() # displays the pokemon's information
    else:
        messagebox.showerror('ERROR','POKEMON NOT FOUND!') # an error message will appear if the function returns false

# function to generate a random pokemon
def get_random_pokemon():
    rand_poke = random.randint(1,1025) # randomizes a number from 1 to 1,025 and store in a variable
    get_url(rand_poke) # calls the function for the url with assigned parameter
    info_one() # calls the basic information function

def info_one(): # created a function for displaying the pokemon's basic information
    # gather the name from the JSON file and display it on the empty label
    name = poke_data['name'].upper()
    p_name.config(text = name)

    p_stats.config(state="normal") # allows for the data to be displayed
    p_stats.delete("1.0", END) # deletes the previous stats when generating a new pokemon
    
    # gathering data from the json file and displaying the information
    str1 = f"ID:\t\t{poke_data['id']}\n\nHeight:\t\t{poke_data['height']}\n\nWeight:\t\t{poke_data['weight']}\n\n"
    p_stats.insert(END, str1)
    
    str2 = 'Abilities:'
    p_stats.insert(END, str2)
    # goes through the pokemon's abilities and display them
    for ab in poke_data['abilities']:
        ab_name = ab['ability']['name']
        disp = f'\t\t{ab_name}'
        p_stats.insert(END, disp.title() +'\n')
    
    str3 = '\nType:'
    p_stats.insert(END, str3)
    # goes through the pokemon types and display them
    for typ in poke_data['types']:
        ab_name = typ['type']['name']
        disp = f'\t\t{ab_name}'
        p_stats.insert(END, disp.title() +'\n')
    
    p_stats.config(state="disabled") # does not allow user to enter anything in the text box
    get_pokemon_img() # calls the function to display the pokemon's image

def info_two(): # created a function for displaying the pokemon's stats
    p_stats.config(state="normal") # allows for the data to be displayed
    p_stats.delete("1.0", END) # deletes the previous stats when generating a new pokemon
    entry.delete(0, END) # deletes the entry field after searching
    
    # goes through the stats of the pokemon
    for stat in poke_data['stats']:
        # gathers the stat name
        stat_name = stat['stat']['name']
        # gathers the base stat 
        base_stat = stat['base_stat']
        # format the stats to be displayed in a specific way
        info = f"{stat_name.title()}\t\t\t{base_stat}"
        # display the stats in the textbox
        p_stats.insert(END, info + '\n\n')
    
    p_stats.config(state="disabled") # does not allow user to enter anything in the text box

# function to get the pokemon's image
def get_pokemon_img():
    # gather the image data from the json file
    image_url = poke_data['sprites']['front_default']
    image_response = requests.get(image_url)
    # condition to check if the data is true
    # resizes the image and displays it
    if image_response.status_code == 200:
        image = Image.open(BytesIO(image_response.content))
        image = image.resize((180,180))
        image = ImageTk.PhotoImage(image)
        image_label = Label(display_frame, image=image)
        image_label.image = (image)
        image_label.place(x = 110, y = 80)

# function for displaying the next pokemon
def go_next():
    next_p = poke_data['id'] # get pokemon's id number and store it in a variable
    next_p += 1 # increment the id number by one
    # calls the function for the url with assigned parameter
    get_url(next_p)
    # calls the basic information function
    info_one()
# function for displaying the previous pokemon
def go_back():
    prev_p = poke_data['id'] # get pokemon's id number and store it in a variable
    prev_p -= 1 # decrement the id number by one
    # calls the function for the url with assigned parameter
    get_url(prev_p)
    # calls the basic information function
    info_one() 
    
# function to display instructions to the user
def display_instruction():
    messagebox.showinfo('ABOUT', 'Enter the name/ID of the Pokemon or generate a random Pokemon to know about them!')

# created a main frame
main_frame = Frame(main, width = 700, height = 300, bg = '#D22323')
main_frame.place(x = 0)

# added an image for design
swirl = Image.open("swirls.png")
resized_swirl = swirl.resize((800,100))
new_swirl = ImageTk.PhotoImage(resized_swirl)
swirl_label = Label(main_frame, image = new_swirl, bd = -2)
swirl_label.place(x = 0, y = 50)
# created a button to display the instructions for the app
# made the button look like an image
info = PhotoImage(file = r"info.png")
resized_info = info.subsample(60,60)
dsp_info = Button(main_frame, image = resized_info, relief = FLAT, bd = 0, highlightthickness = 0, command = display_instruction)
dsp_info.place(x = 20, y = 20)
# displayed a title image and resized it
title_img = Image.open("pokemon.jpg")
resized_image1 = title_img.resize((210,170))
new_img1 = ImageTk.PhotoImage(resized_image1)
title = Label(main_frame, image = new_img1, bd = -2)
title.place(x = 240, y = 10)

# entry field for user to enter the pokemon's name
entry = Entry(main_frame, font = ('Verdana'))
entry.place(x = 260, y = 185, width = 130, height = 25)
# created a button to get the pokemons information
# made the button look like an image
imgbtn = PhotoImage(file = r"pokeball.png")
resized_btn = imgbtn.subsample(17,17)
search_btn = Button(main_frame, image = resized_btn, relief = FLAT, bd = 0, highlightthickness = 0, command = get_pokemon_info)
search_btn.place(x = 400, y = 182)

Label(main_frame, text = 'or', font = ('Lato', 15 ,'bold'), bg = '#D22323', fg = 'white').place(x = 330, y = 213)

# created a button that generates random pokemon
rand_btn = Button(main_frame, text = 'Get Random!', font = ('Verdana', 11), bg = '#ECC957', fg = '#391B00',
                  relief = 'groove',  command = get_random_pokemon)
rand_btn.place(x = 260, y = 250, width = 166)

# created a frame for the output
display_frame = Frame(main, width = 700, height = 400, bg = '#D22323')
display_frame.place(x = 0, y = 285)
# added a border image for a stylized output
bg = Image.open("border.png")
resized_bg = bg.resize((680, 315))
new_bg = ImageTk.PhotoImage(resized_bg)
bg_label = Label(display_frame, image = new_bg, bd = -2)
bg_label.place(x = 9)

# an empty label to display the pokemon's name
p_name = Label(display_frame, text = '', font = ('Verdana', 18, 'bold'), wraplength = 200)
p_name.place(x = 100, y = 47)
# empty label to display the pokemon's stats
p_stats = Text(display_frame, font = ('Verdana', 10))
p_stats.place(x = 340, y = 50, width = 250, height = 190)
# button to display the base stats of the pokemon
stat_button = Button(display_frame, text = 'Show Stats!', font = ('Verdana', 10), bg = '#ECC957', fg = '#391B00',
                     relief = 'groove', command = info_two)
stat_button.place(x = 340, y = 245)

# button for displaying the next pokemon
imgnxt = PhotoImage(file = r"arrow1.png")
resized_nxt = imgnxt.subsample(12,12)
next_button = Button(display_frame, relief = FLAT, bd = 0, highlightthickness = 0, image = resized_nxt, command = go_next)
next_button.place(x = 575, y = 245)
# button for displaying the previous pokemon
imgprev = PhotoImage(file = r"arrow2.png")
resized_prev = imgprev.subsample(12,12)
prev_button = Button(display_frame, relief = FLAT, bd = 0, highlightthickness = 0, image = resized_prev, command = go_back)
prev_button.place(x = 540, y = 245)

main.mainloop() # display the main window