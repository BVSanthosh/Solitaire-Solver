#Internal representation of the game state

from card_state import CardState

MAX_ROWS = 7
DECK_SIZE = 24

class GameState:
    def __init__(self, pyramid, deck):
        self.pyramid = [[None for _ in range(MAX_ROWS - row)] for row in range(MAX_ROWS)]
        self.deck = [None] * DECK_SIZE
        self.valid_moves_in_pyramid = []
        self.valid_moves_between = []
        self.valid_moves_in_deck = []
        self.current_card_in_deck = 0
        self.cards_in_pyramid = 0
        
        self.initialise_pyramid(pyramid)
        self.initialise_deck(deck)
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
    
    def is_game_over(self):
        return self.cards_in_pyramid == 0 
    
    def has_moves(self):
        return bool(self.valid_moves_in_pyramid) or bool(self.valid_moves_between)
        
    def count_cards_in_pyramid(self):
        self.cards_in_pyramid = sum(card.playable != 0 for row in self.pyramid for card in row)
    
    def next_card_in_deck(self):
        self.current_card_in_deck += 1
        
        if self.current_card_in_deck == DECK_SIZE:
            self.current_card_in_deck = 0
    
    def get_valid_moves_in_pyramid(self):
        self.valid_moves_in_pyramid = []
        playable_cards = self.get_playable_cards()

        for i in range(len(playable_cards)):
            index1 = playable_cards[i]
            card1 = self.pyramid[index1[0]][index1[1]]  
            
            if card1.card_num == 13:
                self.valid_moves_in_pyramid.append([index1])
                continue
                
            for j in range(i+1, len(playable_cards)):
                index2 = playable_cards[j]
                card2 = self.pyramid[index2[0]][index2[1]]
                
                if card1.card_num + card2.card_num == 13:
                    self.valid_moves_in_pyramid.append([index1, index2])
                    
    def get_valid_moves_between(self):
        self.valid_moves_between = []
        playable_cards = self.get_playable_cards()
        
        for i in range(len(self.deck)):
            card1 = self.deck[i]
            
            if card1.playable == 0:
                continue
            
            if card1.card_num == 13:
                self.valid_moves_between.append([(-1, i)])
                continue
            
            for j in range(len(playable_cards)):
                index = playable_cards[j]
                card2 = self.pyramid[index[0]][index[1]] 
                
                if card2.card_num + card1.card_num == 13:
                    self.valid_moves_between.append([(-1, i), index])

    def get_valid_moves_in_deck(self):
        playable_cards = []
        self.valid_moves_in_deck = []
        
        for index in range(DECK_SIZE):
            if self.deck[index].playable == 1:
                playable_cards.append((index))
                    
        for i in range(len(playable_cards) - 1):
            card1_index = playable_cards[i]
            card2_index = playable_cards[i + 1]
            
            card1 = self.deck[card1_index]
            card2 = self.deck[card2_index]
            if card1.card_num + card2.card_num == 13:
                self.valid_moves_in_deck.append([(-1, card1_index), (-1, card2_index)])
            else:
                continue
                
    def get_playable_cards(self):
        playable_cards = []
        
        for row in range(MAX_ROWS):
            for col in range(MAX_ROWS - row):
                if self.pyramid[row][col].playable == 1:
                    playable_cards.append((row, col))
                    
        return playable_cards
    
    def update_valid_moves(self):
        self.get_valid_moves_in_pyramid()
        self.get_valid_moves_between()
        self.get_valid_moves_in_deck()
        
    def make_move(self, move):
        if len(move) == 1:
            card1_index1, card1_index2 = move[0]
            
            if card1_index1 == -1:
                self.deck[card1_index2].set_playable(0)
                self.count_cards_in_pyramid()
            else:
                self.pyramid[card1_index1][card1_index2].set_playable(0)
                self.count_cards_in_pyramid()
        else:
            card1_index1, card1_index2 = move[0]
            card2_index1, card2_index2 = move[1]
            
            if card1_index1 == -1 and card2_index1 == -1:
                self.deck[card1_index2].set_playable(0)
                self.deck[card2_index2].set_playable(0)
                self.count_cards_in_pyramid()
            elif card1_index1 == -1:
                self.deck[card1_index2].set_playable(0)
                self.pyramid[card2_index1][card2_index2].set_playable(0)
                self.count_cards_in_pyramid()
            else:
                self.pyramid[card1_index1][card1_index2].set_playable(0)
                self.pyramid[card2_index1][card2_index2].set_playable(0)
                self.count_cards_in_pyramid()
                
        self.update_pyramid()
        
    def update_pyramid(self):
        for row in range(MAX_ROWS - 1):
            for col in range(MAX_ROWS - row - 1):
                if self.pyramid[row][col].playable == 0 and self.pyramid[row][col+1].playable == 0 and self.pyramid[row + 1][col].playable == 2:
                    self.pyramid[row + 1][col].playable = 1
    
    def print_game_state(self):
        print("\nPyramid State:")
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
        
    def print_game_info(self):
        print("\nValid moves in Pyramid:")
        for move in self.valid_moves_in_pyramid:
            print(move)

        print("\nValid moves between Pyramid and Deck:")
        for move in self.valid_moves_between:
            print(move)

        print("\nValid moves in Deck:")
        for move in self.valid_moves_in_deck:
            print(move)
        
        print(f"\nCards in Pyramid: {self.cards_in_pyramid}")
        print(f"\nCurrent card in deck index: {self.current_card_in_deck}")
        print("\nIs game over? ", self.is_game_over())
        print("Are there any moves left? ", self.has_moves())
    
    def __eq__(self, other):
        if not isinstance(other, GameState):
            return False
        
        for row_self, row_other in zip(self.pyramid, other.pyramid):
            for card_self, card_other in zip(row_self, row_other):
                if card_self != card_other:
                    return False
            
        for card_self, card_other in zip(self.deck, other.deck):
            if card_self != card_other:
                return False
            
        if self.valid_moves_in_pyramid != other.valid_moves_in_pyramid:
            return False

        if self.valid_moves_between != other.valid_moves_between:
            return False

        if self.valid_moves_in_deck != other.valid_moves_in_deck:
            return False
            
        return True
    
    def __hash__(self):
        pyramid_hash = hash(tuple(tuple(row) for row in self.pyramid))
        deck_hash = hash(tuple(self.deck))
        moves_in_pyramid_hash = hash(tuple(tuple(move) for move in self.valid_moves_in_pyramid))
        moves_in_deck_hash = hash(tuple(tuple(move) for move in self.valid_moves_in_deck))
        moves_between_hash = hash(tuple(tuple(move) for move in self.valid_moves_between))

        return hash((pyramid_hash, deck_hash, moves_in_pyramid_hash, moves_in_deck_hash, moves_between_hash))