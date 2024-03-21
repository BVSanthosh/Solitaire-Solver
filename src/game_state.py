from card_state import CardState

"""
This module contains the GameState class, which is used to represent each state of the game.
"""

MAX_ROWS = 7   # Maximum number of rows in the pyramid
DECK_SIZE = 24   # Number of cards in the deck

class GameState:
    def __init__(self, pyramid, deck):
        self.id = 0   # Stores the unique ID of the game state 
        self.pyramid = [[None for _ in range(MAX_ROWS - row)] for row in range(MAX_ROWS)]   # Stores the cards in the pyramid
        self.deck = [None] * DECK_SIZE   # Stores the cards in the stock and waste pile
        self.valid_moves_in_pyramid = []   # Stores the valid moves within the pyramid
        self.valid_moves_between = []   # Stores the valid moves between the pyramid and the stock/waste pile
        self.valid_moves_in_deck = []   # Stores the valid moves between the stock and waste pile
        self.king_moves = []   # Stores the valid moves involving a King card
        self.moves_made = []   # Stores the moves already made in the game
        self.card_index_map = {}   # Maps each card to its position in the pyramid or deck
        self.card_moves_map = {}   # Maps each card to the cards it can be matched with
        self.freed_cards_map = {}   # Maps each move to the cards that can be freed by making the move
        self.current_deck_card = None   # Stores the current card in the stock 
        self.current_waste_card = None   # Stores the current card in the waste pile
        self.current_deck_pos = 0   # Stores the current position in the stock 
        self.current_waste_pos = -1   # Stores the current position in the waste pile
        self.deck_rounds = 0   # Stores the number of times the stock has been shuffled
        self.cards_in_pyramid = 0   # Stores the number of cards left in the pyramid
        self.count = 0   
        
        self.initialise_pyramid(pyramid)   # Initialises the pyramid using the initial game state
        self.initialise_deck(deck)   # Initialises the stock and waste pile using the initial game state
        self.initialise_card_pos_map()   # Initialises the card index map
        self.initialise_card_moves_map()   # Initialises the card moves map
        self.count_cards_in_pyramid()   # Counts the number of cards in the pyramid
    
    # Initialises the pyramid using the initial game state
    def initialise_pyramid(self, pyramid):
        for i in range(MAX_ROWS):
            for j in range(MAX_ROWS - i):
                self.pyramid[i][j] = CardState(pyramid[i][j])
                if i == 0:
                    self.pyramid[i][j].set_playable(1)
    
    # Initialises the stock and waste pile using the initial game state
    def initialise_deck(self, deck):
        for index in range(DECK_SIZE):
            self.deck[index] = CardState(deck[index])
            self.deck[index].set_playable(1)
            
        self.current_deck_card = self.deck[0]
    
    # Initialises the card index map    
    def initialise_card_pos_map(self):
        for i in range(MAX_ROWS):
            for j in range(MAX_ROWS - i):
                self.card_index_map[self.pyramid[i][j]] = (i, j)
                
        for index in range(DECK_SIZE):
            self.card_index_map[self.deck[index]] = (-1, index)
    
    # Checks if the game is over
    def is_game_over(self):
        return self.cards_in_pyramid == 0 
    
    # Checks if there are any moves left
    def has_moves(self):
        return bool(self.valid_moves_in_pyramid) or bool(self.valid_moves_between) or bool(self.valid_moves_in_deck) or bool(self.king_moves)
    
    # Counts the number of cards in the pyramid
    def count_cards_in_pyramid(self):
        self.cards_in_pyramid = sum(card.playable != 0 for row in self.pyramid for card in row)
    
    # Finds the next card in the stock and waste pile
    def next_card_in_deck(self):
        self.search_playable_deck()
        self.search_playable_waste()
    
    # Searches for the next playable card in the stock pile
    def search_playable_deck(self):
        playable_deck_card = False 
        
        while not playable_deck_card:
            self.current_deck_pos += 1
        
            if self.current_deck_pos == DECK_SIZE:
                self.current_deck_pos = 0
                self.deck_rounds += 1
                
                if self.deck_rounds == 3:
                    break
                
            if self.deck[self.current_deck_pos].playable == 1:
                playable_deck_card = True
    
    # Searches for the next playable card in the waste pile
    def search_playable_waste(self):
        if self.current_deck_pos > 0:
            playable_waste_card = False
            pos = 1
            
            while not playable_waste_card:
                if pos > self.current_deck_pos:
                    self.current_waste_pos = -1
                    break
                
                self.current_waste_pos = self.current_deck_pos - pos
                
                if self.deck[self.current_waste_pos].playable == 1:
                    playable_waste_card = True
                    
                pos += 1
        else:
            self.current_waste_pos = -1
    
    # Gets all the available moves for each valid moves list
    def get_valid_moves(self):
        playable_in_pyramid = self.get_playable_cards()
        self.current_deck_card = self.deck[self.current_deck_pos]

        for i in range(len(playable_in_pyramid)):
            card1 = playable_in_pyramid[i]
            
            if card1.card_num == 13:
                self.king_moves.append((card1,))
                continue
                
            for j in range(i+1, len(playable_in_pyramid)):
                card2 = playable_in_pyramid[j]
            
                if card1.card_num + card2.card_num == 13:
                    self.valid_moves_in_pyramid.append((card1, card2))
                    
        if self.current_deck_card.card_num == 13:
            self.king_moves.append((self.current_deck_card,))
        else:
            for i in range(len(playable_in_pyramid)):
                card = playable_in_pyramid[i]
                
                if card.card_num + self.current_deck_card.card_num == 13:
                    self.valid_moves_between.append((self.current_deck_card, card)) 
                
        if self.current_waste_pos != -1:
            self.current_waste_card = self.deck[self.current_waste_pos]
            
            if self.current_waste_card.card_num == 13:
                self.king_moves.append((self.current_waste_card,))
            else:
                for i in range(len(playable_in_pyramid)):
                    card = playable_in_pyramid[i]
                    
                    if card.card_num + self.current_waste_card.card_num == 13:
                        self.valid_moves_between.append((self.current_waste_card, card))
                  
            if self.current_waste_card.card_num + self.current_deck_card.card_num == 13:
                if not self.check_dead_end(self.current_deck_card) and not self.check_dead_end(self.current_waste_card):
                    self.valid_moves_in_deck.append((self.current_deck_card, self.current_waste_card))
    
    # Gets all the playable cards in the pyramid
    def get_playable_cards(self):
        playable_cards = []
        
        for row in range(MAX_ROWS):
            for col in range(MAX_ROWS - row):
                if self.pyramid[row][col].playable == 1:
                    playable_cards.append(self.pyramid[row][col])
                    
        return playable_cards
    
    # Updates the valid moves lists
    def update_valid_moves(self):
        self.king_moves = []
        self.valid_moves_in_pyramid = []
        self.valid_moves_between = []   
        self.valid_moves_in_deck = []
                
        while True:
            if self.deck_rounds == 3:
                break
            
            self.get_valid_moves()
            
            if self.has_moves():
                break
            
            self.next_card_in_deck()
    
    # Makes a move in the game by updating the playable status of the cards in the pyramid and stock/waste pile
    def make_move(self, move):
        if len(move) == 1:
            card = move[0]
            card_index = self.card_index_map[card]
            
            if card_index[0] == -1:
                self.deck[card_index[1]].set_playable(0)
                self.count_cards_in_pyramid()
                
                if card.card == self.current_deck_card.card:
                    self.next_card_in_deck()
                elif self.current_waste_pos != -1:
                    if card.card == self.current_waste_card.card:
                        self.search_playable_waste()
            else:
                self.pyramid[card_index[0]][card_index[1]].set_playable(0)
                self.count_cards_in_pyramid()
        else:
            card1_obj = move[0]
            card2_obj = move[1]
            card1_index = self.card_index_map[card1_obj]
            card2_index = self.card_index_map[card2_obj]
            
            if card1_index[0] == -1 and card2_index[0] == -1:
                self.deck[card1_index[1]].set_playable(0)
                self.deck[card2_index[1]].set_playable(0)
                self.count_cards_in_pyramid()
                self.next_card_in_deck()
            elif card1_index[0] == -1:
                self.deck[card1_index[1]].set_playable(0)
                self.pyramid[card2_index[0]][card2_index[1]].set_playable(0)
                self.count_cards_in_pyramid()
                
                if card1_obj.card == self.current_deck_card.card:
                    self.next_card_in_deck()
                elif self.current_waste_pos != -1:
                    if card1_obj.card == self.current_waste_card.card:
                        self.search_playable_waste()
            else:
                self.pyramid[card1_index[0]][card1_index[1]].set_playable(0)
                self.pyramid[card2_index[0]][card2_index[1]].set_playable(0)
                self.count_cards_in_pyramid()
                
        self.update_pyramid()
        
        if len(move) != 1:
            self.update_card_moves_map(move[0])
            self.update_card_moves_map(move[1])
    
    # Updates the moves made in the game
    def update_moves_made(self, move):
        self.moves_made.append(move)
    
    # Gets the list of moves made in the game
    def get_moves_made(self):
        return self.moves_made
    
    # Updates the pyramid after a move has been made
    def update_pyramid(self):
        for row in range(MAX_ROWS - 1):
            for col in range(MAX_ROWS - row - 1):
                if self.pyramid[row][col].playable == 0 and self.pyramid[row][col+1].playable == 0 and self.pyramid[row + 1][col].playable == 2:
                    self.pyramid[row + 1][col].playable = 1
    
    # Initialises the card moves map
    def initialise_card_moves_map(self):
        suits = ["S", "C", "D", "H"]
        
        for row in range(MAX_ROWS):
            for col in range(MAX_ROWS - row):
                key = self.pyramid[row][col]
                card_num1 = key.card_num
                
                if card_num1 != 13:
                    card_num2 = 13 - card_num1
                    values = []
                    
                    for j in range(4):
                        card1 = str(card_num2) + suits[j]
                        value = self.get_card_obj(card1)
                        
                        if self.check_match_validity(key, value):
                            values.append(value)
                        
                    self.card_moves_map[key] = values    
    
    # Gets the card object from the card value    
    def get_card_obj(self, card):
        for row in range(MAX_ROWS):
            for col in range(MAX_ROWS - row):
                if self.pyramid[row][col].card == card:
                    return self.pyramid[row][col]
                    
        for index in range(DECK_SIZE):
            if self.deck[index].card == card:
                return self.deck[index]
    
    # Checks the validity of a match between two cards 
    def check_match_validity(self, key, value):
        higher_card = ()
        lower_card = ()
        key_card = self.card_index_map[key]
        value_card = self.card_index_map[value]
        
        if key_card[0] == -1 and value_card[0] != -1:
            return True
        elif key_card[0] != -1 and value_card[0] == -1:
            return True
        elif key_card[0] == value_card[0]:
            return True
        
        if key_card[0] > value_card[0]:
            higher_card = key_card
            lower_card = value_card
        else:
            higher_card = value_card
            lower_card = key_card
            
        if (lower_card[1] < higher_card[1]):
            return True 

        if lower_card[1] >= 2:
            if lower_card[0] == 0 and higher_card[0] >= 1 and higher_card[0] <= 5:
                if lower_card[1] == 2 and higher_card[0] == 1 and higher_card[1] == 0:
                    return True
                elif lower_card[1] == 3 and ((higher_card[0] == 1 and higher_card[1] <= 1) or (higher_card[0] == 2 and higher_card[1] == 0)):
                    return True
                elif lower_card[1] == 4 and ((higher_card[0] == 1 and higher_card[1] <= 2) or (higher_card[0] == 2 and higher_card[1] <= 1) or (higher_card[0] == 3 and higher_card[1] == 0)):
                    return True
                elif lower_card[1] == 5 and ((higher_card[0] == 1 and higher_card[1] <= 3) or (higher_card[0] == 2 and higher_card[1] <= 2) or (higher_card[0] == 3 and higher_card[1] <= 1) or (higher_card[0] == 4 and higher_card[1] == 0)):
                    return True
                elif lower_card[1] == 6 and ((higher_card[0] == 1 and higher_card[1] <= 4) or (higher_card[0] == 2 and higher_card[1] <= 3) or (higher_card[0] == 3 and higher_card[1] <= 2) or (higher_card[0] == 4 and higher_card[1] <= 1) or (higher_card[0] == 5 and higher_card[1] == 0)):
                    return True
            elif lower_card[0] == 1 and higher_card[0] >= 2 and higher_card[0] <= 5:
                if lower_card[1] == 2 and higher_card[0] == 2 and higher_card[1] == 0:
                    return True
                elif lower_card[1] == 3 and ((higher_card[0] == 2 and higher_card[1] <= 1) or (higher_card[0] == 3 and higher_card[1] == 0)):
                    return True
                elif lower_card[1] == 4 and ((higher_card[0] == 2 and higher_card[1] <= 2) or (higher_card[0] == 3 and higher_card[1] <= 1) or (higher_card[0] == 4 and higher_card[1] == 0)):
                    return True
                elif lower_card[1] == 5 and ((higher_card[0] == 2 and higher_card[1] <= 3) or (higher_card[0] == 3 and higher_card[1] <= 2) or (higher_card[0] == 4 and higher_card[1] <= 1) or (higher_card[0] == 5 and higher_card[1] == 0)):
                    return True
            elif lower_card[0] == 2 and higher_card[0] >= 3 and higher_card[0] <= 5:
                if lower_card[1] == 2 and higher_card[0] == 3 and higher_card[1] == 0:
                    return True
                elif lower_card[1] == 3 and ((higher_card[0] == 3 and higher_card[1] <= 1) or (higher_card[0] == 4 and higher_card[1] == 0)):
                    return True
                elif lower_card[1] == 4 and ((higher_card[0] == 3 and higher_card[1] <= 2) or (higher_card[0] == 4 and higher_card[1] <= 1) or (higher_card[0] == 5 and higher_card[1] == 0)):
                    return True
            elif lower_card[0] == 3 and higher_card[0] >= 4 and higher_card[0] <= 5:
                if lower_card[1] == 2 and higher_card[0] == 4 and higher_card[1] == 0:
                    return True
                elif lower_card[1] == 3 and ((higher_card[0] == 4 and higher_card[1] <= 1) or (higher_card[0] == 5 and higher_card[1] == 0)):
                    return True
            elif lower_card[0] == 4 and higher_card[0] == 5:
                if lower_card[1] == 2 and higher_card[0] == 5 and higher_card[1] == 0:
                    return True
            
        return False
    
    # Updates the card moves map after a move has been made    
    def update_card_moves_map(self, card):
        if card in self.card_moves_map:
            del self.card_moves_map[card]
        
        for key, values in self.card_moves_map.items():
            if card in values:
                values.remove(card)
    
    # Checks if a move between the stock and waste pile leads to a dead end
    def check_dead_end(self, card):
        key_list = []
        
        for key, values in self.card_moves_map.items():
            if card in values:  
                key_list.append(key)
                
                if len(values) == 1:
                    return True
        
        if len(key_list) != 0:
            if len(key_list) == 1:
                return False
            
            for key in key_list:
                self.card_moves_map[key].remove(card)
            
            for i in range(len(key_list)):
                first_list = self.card_moves_map[key_list[i]]
                
                for j in range(i+1, len(key_list)):
                    second_list = self.card_moves_map[key_list[j]]
                    
                    if len(first_list) == len(second_list) and all(element in first_list for element in second_list):
                        if len(first_list) < len(key_list):
                            self.undo_deletion(key_list, card)
                            return True
                    
            self.undo_deletion(key_list, card)
            
        return False
    
    # Undoes the deletion of a card from the card moves map
    def undo_deletion(self, key_list, card):
        for key in key_list:
            self.card_moves_map[key].append(card)
   
   # Updates the cards freed map
    def update_cards_freed_map(self):
        for move in self.valid_moves_between:
            self.freed_cards_map[move] = self.cards_freed(move[1])
        
        for move in self.valid_moves_in_pyramid:
            cards2 = self.cards_freed(move[0])
            cards3 = self.cards_freed(move[1])
            
            index1 = self.card_index_map[move[0]]
            index2 = self.card_index_map[move[1]]
            
            if index1[0] == index2[0]:
                if index1[1] > index2[1] and index1[1] - index2[1] == 1:
                    cards4 = [self.pyramid[index1[0] + 1][index2[1]]]
                    self.freed_cards_map[move] = cards2 + cards3 + cards4
                elif index1[1] < index2[1] and index2[1] - index1[1] == 1:
                    cards4 = [self.pyramid[index1[0] + 1][index1[1]]]
                    self.freed_cards_map[move] = cards2 + cards3 + cards4
                else:
                    self.freed_cards_map[move] = cards2 + cards3
            else:
                self.freed_cards_map[move] = cards2 + cards3
    
    # Gets the cards that can be freed by making a move
    def cards_freed(self, card):
        freed_cards = []
        index = self.card_index_map[card]
        
        if index[0] == 6 and index[1] == 0:
            return freed_cards
        
        if index[0] >= 0 and index[0] <= 5 and index[1] == 0:
            if self.pyramid[index[0]][index[1] + 1].playable == 0:
                freed_cards.append(self.pyramid[index[0] + 1][index[1]])
                return freed_cards
            else:
                return freed_cards
            
        if (index[0] == 0 and index[1] == 6)  or (index[0] == 1 and index[1] == 5) or (index[0] == 2 and index[1] == 4) or (index[0] == 3 and index[1] == 3) or (index[0] == 4 and index[1] == 2) or (index[0] == 5 and index[1] == 1):
            if self.pyramid[index[0]][index[1] - 1].playable == 0:
                freed_cards.append(self.pyramid[index[0] + 1][index[1] - 1])
                return freed_cards
            else:
                return freed_cards
        
        if self.pyramid[index[0]][index[1] - 1].playable == 0:
            freed_cards.append(self.pyramid[index[0] + 1][index[1] - 1])
            
        if self.pyramid[index[0]][index[1] + 1].playable == 0:
            freed_cards.append(self.pyramid[index[0] + 1][index[1]])
            
        return freed_cards
    
    # Clears the cards freed map
    def clear_cards_freed_map(self):
        self.freed_cards_map = {}

    # Sets the unique ID of the game state
    def update_state_id(self, id):
        self.id = id
    
    # Gets the string representation of the moves made in the game
    def get_moves_string(self, moves):
        moves_string = []
        
        for move in moves:
            if len(move) == 1:
                moves_string.append((move[0].card,))
            else:
                moves_string.append((move[0].card, move[1].card))
                
        return moves_string
    
    # Prints the current state of the game
    def print_game_state(self):
        print("\nPyramid:")
        for i, row in enumerate(reversed(self.pyramid)):
            leading_spaces = "   " * (7 - i)
            row_cards = []
            for j, card in enumerate(row):
                if card:
                    card_info = f"{card.card_num}{card.card_suit} ({card.playable})"
                    row_cards.append(card_info)
                else:
                    row_cards.append("       ") 

            print(f"{leading_spaces} {' '.join(row_cards)}")

        print("\nDeck:")
        deck_cards = []
        i = 0
        for card in self.deck:
            if card == self.current_deck_card: 
                card_info = f"[{card.card_num}{card.card_suit} ({card.playable})]"
                deck_cards.append(card_info)
            else:
                card_info = f"{card.card_num}{card.card_suit} ({card.playable})"
                deck_cards.append(card_info)
                
            if i == len(self.deck) / 2:
                deck_cards.append("   ")
        print(" ".join(deck_cards))
        
        print(f"\nCards in Pyramid: {self.cards_in_pyramid}")
        print(f"Cards in deck: {self.current_deck_pos + 1}")
        print(f"Current card in deck pile: {self.deck[self.current_deck_pos].card}")
        
        if self.current_waste_pos != -1:
            print(f"Cards in waste pile: {self.current_waste_pos + 1}")
            print(f"Current card in waste pile: {self.deck[self.current_waste_pos].card}")
        else:
            print(f"Cards in waste pile: {0}")
            print(f"Current card in waste pile: {0}")
            
        print(f"Deck round(s): {self.deck_rounds}")
        print("Is game over? ", self.is_game_over())
        print("Are there any moves left? ", self.has_moves())
        
        print("\nAvailable moves:")
        moves_list = self.get_moves_string(self.king_moves) + self.get_moves_string(self.valid_moves_in_pyramid) + self.get_moves_string(self.valid_moves_between) + self.get_moves_string(self.valid_moves_in_deck)
        print(moves_list)
        
        print("\nMoves made:")
        moves_made_list = self.get_moves_string(self.moves_made)
        print(moves_made_list)
    
    # Hashes the state id
    def __hash__(self):
        return hash(self.id)
    
    # Compares the state id with another state id
    def __eq__(self, other):
        if not isinstance(other, GameState):
            return False
        return self.id == other.id