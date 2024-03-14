#Internal representation of the game state

from card_state import CardState

MAX_ROWS = 7
DECK_SIZE = 24

class GameState:
    def __init__(self, pyramid, deck):
        self.id = 0
        self.pyramid = [[None for _ in range(MAX_ROWS - row)] for row in range(MAX_ROWS)]
        self.deck = [None] * DECK_SIZE
        self.valid_moves_in_pyramid = []
        self.valid_moves_between = []
        self.valid_moves_in_deck = []
        self.king_moves = []
        self.moves_made = []
        self.card_index_map = {}
        self.card_moves_map = {}
        self.freed_cards_map = {}
        self.current_deck_card = None
        self.current_waste_card = None
        self.current_deck_pos = 0
        self.current_waste_pos = -1
        self.deck_rounds = 0
        self.cards_in_pyramid = 0
        self.count = 0
        
        self.initialise_pyramid(pyramid)
        self.initialise_deck(deck)
        self.initialise_card_pos_map()
        self.initialise_card_moves_map()
        self.count_cards_in_pyramid()
    
    def initialise_pyramid(self, pyramid):
        for i in range(MAX_ROWS):
            for j in range(MAX_ROWS - i):
                self.pyramid[i][j] = CardState(pyramid[i][j])
                if i == 0:
                    self.pyramid[i][j].set_playable(1)
    
    def initialise_deck(self, deck):
        for index in range(DECK_SIZE):
            self.deck[index] = CardState(deck[index])
            self.deck[index].set_playable(1)
            
        self.current_deck_card = self.deck[0]
            
    def initialise_card_pos_map(self):
        for i in range(MAX_ROWS):
            for j in range(MAX_ROWS - i):
                self.card_index_map[self.pyramid[i][j]] = (i, j)
                
        for index in range(DECK_SIZE):
            self.card_index_map[self.deck[index]] = (-1, index)
    
    def is_game_over(self):
        return self.cards_in_pyramid == 0 
    
    def has_moves(self):
        return bool(self.valid_moves_in_pyramid) or bool(self.valid_moves_between) or bool(self.valid_moves_in_deck) or bool(self.king_moves)
        
    def count_cards_in_pyramid(self):
        self.cards_in_pyramid = sum(card.playable != 0 for row in self.pyramid for card in row)
    
    def next_card_in_deck(self):
        self.search_playable_deck()
        self.search_playable_waste()
            
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
            
    def get_playable_cards(self):
        playable_cards = []
        
        for row in range(MAX_ROWS):
            for col in range(MAX_ROWS - row):
                if self.pyramid[row][col].playable == 1:
                    playable_cards.append(self.pyramid[row][col])
                    
        return playable_cards
        
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
        
    def update_moves_made(self, move):
        self.moves_made.append(move)
        
    def get_moves_made(self):
        return self.moves_made
        
    def update_pyramid(self):
        for row in range(MAX_ROWS - 1):
            for col in range(MAX_ROWS - row - 1):
                if self.pyramid[row][col].playable == 0 and self.pyramid[row][col+1].playable == 0 and self.pyramid[row + 1][col].playable == 2:
                    self.pyramid[row + 1][col].playable = 1
              
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
                    
    def get_card_obj(self, card):
        for row in range(MAX_ROWS):
            for col in range(MAX_ROWS - row):
                if self.pyramid[row][col].card == card:
                    return self.pyramid[row][col]
                    
        for index in range(DECK_SIZE):
            if self.deck[index].card == card:
                return self.deck[index]
            
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
                    
    def update_card_moves_map(self, card):
        if card in self.card_moves_map:
            del self.card_moves_map[card]
        
        for key, values in self.card_moves_map.items():
            if card in values:
                values.remove(card)
                
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
    
    def undo_deletion(self, key_list, card):
        for key in key_list:
            self.card_moves_map[key].append(card)
   
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
    
    def clear_cards_freed_map(self):
        self.freed_cards_map = {}

    def update_state_id(self, id):
        self.id = id
        
    def get_moves_string(self, moves):
        moves_string = []
        
        for move in moves:
            if len(move) == 1:
                moves_string.append((move[0].card,))
            else:
                moves_string.append((move[0].card, move[1].card))
                
        return moves_string
    
    def print_game_state(self):
        print("\nPyramid:")
        for row in reversed(self.pyramid):
            row_cards = []
            for card in row:
                if card: 
                    card_info = f"{card.card_num}{card.card_suit} ({card.playable})"
                    row_cards.append(card_info)
            print(" ".join(row_cards))

        print("\nDeck:")
        deck_cards = []
        for card in self.deck:
            if card: 
                card_info = f"{card.card_num}{card.card_suit} ({card.playable})"
                deck_cards.append(card_info)
        print(" ".join(deck_cards))
        
        print(f"\nCards in Pyramid: {self.cards_in_pyramid}")
        print(f"Current card in deck pile: {self.current_deck_pos}")
        print(f"Current card in waste pile: {self.current_waste_pos}")
        print(f"Deck round(s): {self.deck_rounds}")
        print("Is game over? ", self.is_game_over())
        print("Are there any moves left? ", self.has_moves())
        
        print("\nValid moves:")
        moves_list = self.get_moves_string(self.king_moves) + self.get_moves_string(self.valid_moves_in_pyramid) + self.get_moves_string(self.valid_moves_between) + self.get_moves_string(self.valid_moves_in_deck)
        print(moves_list)
        
        print("\nMoves made:")
        moves_made_list = self.get_moves_string(self.moves_made)
        print(moves_made_list)
        
    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if not isinstance(other, GameState):
            return False
        
        return self.id == other.id