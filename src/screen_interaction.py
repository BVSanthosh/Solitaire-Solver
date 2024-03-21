import pyautogui
import pygetwindow as gw
import time
import json
import tkinter as tk
from tkinter import messagebox

"""
This module contains functions for scanning the game window and reading the cards.

The code for verify_cards() is written with the help of ChatGPT.
"""

NUM_OF_CARDS = 52   # Stores the total number of cards in the game
NUM_OF_PYRAMID_CARDS = 28   # Stores the number of cards in the pyramid
NUM_OF_DECK_CARDS = 24   # Stores the number of cards in the deck
PYRAMID_ROWS = 7   # Stores the number of rows in the pyramid
WINDOW_HEIGHT = 1280   # Stores the height of the game window
WINDOW_WIDTH = 720   # Stores the width of the game window
WINDOW_NAME = "Solitaire & Casual Games"   # Stores the name of the game window

img_to_card_map_data = {}   # Maps the screenshot of the card to the card value
card_to_region_map = {}  # Maps the card value to the region on the screen
deck_button_region = ()   # Stores the region of the deck button
deck_region = ()   # Stores the region of the stock
waste_region = ()   # Stores the region of the waste pile
pos_in_deck = 0   # Stores the position in the deck
pyramid_region_map_list = [None for _ in range(NUM_OF_PYRAMID_CARDS)]   # Stores the regions of the pyramid cards
verified_pyramid = [None for _ in range(NUM_OF_PYRAMID_CARDS)]   # Stores the verified pyramid cards
verified_deck = [None for _ in range(NUM_OF_DECK_CARDS)]   # Stores the verified deck cards

# Scans the game window for the Solitaire game
def scan_window():
    try:
        solitaire_window = gw.getWindowsWithTitle(WINDOW_NAME)[0]  
        
        if solitaire_window.isMinimized:
            solitaire_window.restore()
            
        solitaire_window.moveTo(0, 0)
        solitaire_window.resizeTo(WINDOW_HEIGHT, WINDOW_WIDTH)
        
        return True
    except IndexError:
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# Reads the cards from the game window
def read_cards():   #add scan_card_callback as a parameter when testing the GUI
    global img_to_card_map_data, deck_button_region, deck_region, waste_region, pyramid_region_map_list
    pyramid_cards = [None for _ in range(NUM_OF_PYRAMID_CARDS)]
    deck_cards = [None for _ in range(NUM_OF_DECK_CARDS)]
    region_data = {}
    #card_int = 0   <--- uncomment when testing the GUI
    
    with open('resources/regions.json', 'r') as file:
        region_data = json.load(file)
        
    with open('resources/image_to_card.json', 'r') as file:
        img_to_card_map_data = json.load(file) 
    
    pyramid_region_map_list = region_data["pyramid"]
    deck_region_map = region_data["deck"]
    waste_region_map = region_data["waste"]
    deck_button_region_map = region_data["deck_button"]
    undo_button_region_map = region_data["undo_button"]
    img_to_card_map = img_to_card_map_data["image_to_card"]
    
    deck_region = (deck_region_map['x'], deck_region_map['y'], deck_region_map['width'], deck_region_map['height'])
    waste_region = (waste_region_map['x'], waste_region_map['y'], waste_region_map['width'], waste_region_map['height'])
    deck_button_region = (deck_button_region_map['x'], deck_button_region_map['y'], deck_button_region_map['width'], deck_button_region_map['height'])
    undo_button_region = (undo_button_region_map['x'], undo_button_region_map['y'], undo_button_region_map['width'], undo_button_region_map['height'])

    for index, region in enumerate(pyramid_region_map_list):
        card_region = (region['x'], region['y'], region['width'], region['height'])
        pyramid_cards[index] = scan_region_for_card(card_region, img_to_card_map)
        #scan_card_callback(card_int, pyramid_cards[index])   <--- uncomment when testing the GUI
        #card_int += 1   <--- uncomment when testing the GUI

    for i in range(NUM_OF_DECK_CARDS):
        deck_cards[i] = scan_region_for_card(deck_region, img_to_card_map)
        #scan_card_callback(card_int, deck_cards[i])   <--- uncomment when testing the GUI
        #card_int += 1   <--- uncomment when testing the GUI
        pyautogui.click(deck_button_region)

    time.sleep(0.5)
    pyautogui.click(undo_button_region)
    verify_cards(pyramid_cards, deck_cards)
    initiate_maps(deck_region_map)
    create_initial_game_state()

# Scans a card region of the game window to recognize the card
def scan_region_for_card(region, img_to_card_map):
    for card_index in range(NUM_OF_CARDS):
        try:
            location = pyautogui.locateOnScreen(f'resources/cards/card{card_index}.png', region=region, confidence=0.86)
        except pyautogui.ImageNotFoundException:
            location = None

        if location:
            card = img_to_card_map[f'card{card_index}']
            print(f'{card} found in region {region}')
            return card

    print(f'No card found in region {region}')
    return 0

# Displays the verification window to verify the cards
def verify_cards(pyramid, deck):
    VALID_CARDS = {
    "1C", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "11C", "12C", "13C",
    "1D", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "11D", "12D", "13D",
    "1H", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "11H", "12H", "13H",
    "1S", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "11S", "12S", "13S"
    }
    
    def save():
        global verified_pyramid, verified_deck
        encountered_pyramid_cards = set()
        encountered_deck_cards = set()

        for entry in pyramid_entries:
            card = entry.get().strip().upper()
            if card not in VALID_CARDS:
                messagebox.showerror("Error", "One or more entries in the pyramid contain invalid cards.")
                return
            if card in encountered_pyramid_cards:
                messagebox.showerror("Error", "One or more cards in the pyramid are duplicated.")
                return
            encountered_pyramid_cards.add(card)

        for entry in deck_entries:
            card = entry.get().strip().upper()
            if card not in VALID_CARDS:
                messagebox.showerror("Error", "One or more entries in the deck contain invalid cards.")
                return
            if card in encountered_deck_cards:
                messagebox.showerror("Error", "One or more cards in the deck are duplicated.")
                return
            encountered_deck_cards.add(card)

        if (encountered_pyramid_cards.union(encountered_deck_cards)) != VALID_CARDS:
            messagebox.showerror("Error", "Not all cards from VALID_CARDS are included.")
            return

        verified_pyramid = [entry.get() for entry in pyramid_entries]
        verified_deck = [entry.get() for entry in deck_entries]
        window.destroy()
    
    window = tk.Tk()
    window.title("Verification Window")
    window.attributes("-topmost", True)
    message_label = tk.Label(window, text="Please verify that the cards below match the cards in the game window:")
    message_label.pack()
    
    pyramid_frame = tk.Frame(window)
    pyramid_frame.pack()
    pyramid_label = tk.Label(pyramid_frame, text="Pyramid")
    pyramid_label.pack()
    
    deck_frame = tk.Frame(window)
    deck_frame.pack()
    deck_label = tk.Label(deck_frame, text="Deck")
    deck_label.pack()
    
    pyramid_entries = []
    deck_entries = []
    cards_per_row = [i+1 for i in range(PYRAMID_ROWS)]

    for row_index, num_cards_in_row in enumerate(cards_per_row):
        frame = tk.Frame(pyramid_frame)

        for _ in range(PYRAMID_ROWS - num_cards_in_row):
            tk.Label(frame, text="").pack(side=tk.LEFT)

        for _ in range(num_cards_in_row):
            card = pyramid.pop(0) if pyramid else ""  
            entry = tk.Entry(frame, width=5)
            entry.insert(0, card)
            entry.pack(side=tk.LEFT)
            pyramid_entries.append(entry)

        frame.pack()
        
    frame = tk.Frame(deck_frame)
    row_count = 0
    
    for card in deck:
        entry = tk.Entry(frame, width=5)
        entry.insert(0, card)
        entry.pack(side=tk.LEFT)
        deck_entries.append(entry)
        row_count += 1
        
        if row_count == 6:
            frame.pack()
            frame = tk.Frame(deck_frame)
            row_count = 0

    tk.Button(window, text="Save", command=save).pack()
    window.mainloop()

# Initializes the card to region map
def initiate_maps(deck_region_map):
    global verified_pyramid, verified_deck, card_to_region_map, pyramid_region_map_list
    
    for index, card in enumerate(verified_pyramid):
        card_to_region_map[card] = pyramid_region_map_list[index]
        
    for index, card in enumerate(verified_deck):
        card_to_region_map[card] = deck_region_map

# Writes the initial state of the game to the initial game state JSON file
def create_initial_game_state():
    global verified_pyramid, verified_deck
    pyramid_reshaped = [[None for _ in range(PYRAMID_ROWS - row)] for row in range(PYRAMID_ROWS)]
    index = 0
      
    for i in range(PYRAMID_ROWS - 1, -1, -1):
        for j in range(PYRAMID_ROWS - i):   
            pyramid_reshaped[i][j] = verified_pyramid[index]
            index += 1 
    
    game_state = {
        "pyramid": pyramid_reshaped,
        "deck": verified_deck
    }
    
    with open('game_state/initial_state.json', 'w') as file:
        json.dump(game_state, file, indent=4)

# Executes the moves on the game window
def execute_moves(moves):   #add highlight_cards_callback as a parameter when testing the GUI
    global card_to_region_map, verified_deck, verified_pyramid
    
    for move in moves:    
        if len(move) == 1:
            print(f"Click on: {move[0]}")
            #highlight_cards_callback(move[0])   <--- uncomment when testing the GUI
        else:
            print(f"Click on: {move[0]}, {move[1]}")
            #highlight_cards_callback(move[0])   <--- uncomment when testing the GUI
            #highlight_cards_callback(move[1])   <--- uncomment when testing the GUI
        
        if len(move) == 1:
            loc1 = card_to_region_map[move[0]]
            reg1 = (loc1['x'], loc1['y'], loc1['width'], loc1['height'])
            
            if move[0] in verified_deck:
                check_deck(move[0])
            else:
                pyautogui.click(reg1)
                time.sleep(0.5)
        else:
            loc1 = card_to_region_map[move[0]]
            loc2 = card_to_region_map[move[1]]
            reg1 = (loc1['x'], loc1['y'], loc1['width'], loc1['height'])
            reg2 = (loc2['x'], loc2['y'], loc2['width'], loc2['height'])
            
            if move[0] in verified_deck:
                check_deck(move[0])
            else:
                pyautogui.click(reg1)
                time.sleep(0.5)
            if move[1] in verified_deck:
                check_deck(move[1])
            else:
                pyautogui.click(reg2)
                time.sleep(0.5)

# Checks for the card in the stock or waste pile to be clicked when executing moves
def check_deck(card):
    global pos_in_deck, verified_deck, deck_button_region, deck_region, waste_region
    card_not_found = True
    
    while (card_not_found):
        if pos_in_deck != -1: 
            if verified_deck[pos_in_deck] == card:
                pyautogui.click(deck_region)
                time.sleep(0.5)
                del verified_deck[pos_in_deck]
                
                if pos_in_deck == len(verified_deck):
                    pos_in_deck = -1
                    
                card_not_found = False
            elif (pos_in_deck > 0):
                if verified_deck[pos_in_deck - 1] == card:
                    pyautogui.click(waste_region)
                    time.sleep(0.5)
                    del verified_deck[pos_in_deck - 1]
                    pos_in_deck -= 1
                    card_not_found = False
        elif pos_in_deck == -1:
            if verified_deck[len(verified_deck) - 1] == card:
                pyautogui.click(waste_region)
                time.sleep(0.5)
                del verified_deck[len(verified_deck) - 1]
                card_not_found = False
            else:
                pos_in_deck = 0
                pyautogui.click(deck_button_region)
                time.sleep(0.5)
                
        if (card_not_found):
            print("Draw")
            pyautogui.click(deck_button_region)
            time.sleep(0.5)
            pos_in_deck += 1
            check_deck_pos()

# Checks that the position in the deck is within the bounds
def check_deck_pos():
    global pos_in_deck, verified_deck,deck_button_region
    
    if pos_in_deck == len(verified_deck):
        pos_in_deck = 0
        pyautogui.click(deck_button_region)
        time.sleep(0.5)