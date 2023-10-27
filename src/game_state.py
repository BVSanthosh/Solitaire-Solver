#Internal representation of the game state

from card_state import CardState

MAX_ROWS = 7
DECK_SIZE = 24

class GameState:
    def __init__(self, pyramid, deck):
        self.pyramid = [[None for _ in range(MAX_ROWS - row)] for row in range(MAX_ROWS)]
        self.deck = [None] * DECK_SIZE
        self.current_card_in_deck = 0
        self.cards_in_pyramid = 0
        self.valid_moves_in_pyramid = []
        self.valid_moves_in_deck = []
        self.valid_moves_between = []
        
        self.initialise_pyramid(pyramid)
        self.initialise_deck(deck)
        self.count_cards_in_pyramid()
        self.get_valid_moves_in_pyramid()
        self.get_valid_moves_in_deck()
        self.get_valid_moves_between()
    
    def initialise_pyramid(self, pyramid):
        for row in range(MAX_ROWS):
            for col in range(MAX_ROWS - row):
                self.pyramid[row][col] = CardState(pyramid[row][col])
                if row == 0:
                    self.pyramid[row][col].set_playable(1)
    
    def initialise_deck(self, deck):
        for index in range(DECK_SIZE):
            self.deck[index] = CardState(deck[index])
            self.deck[index].set_playable(1)
    
    def is_game_over(self):
        return self.cards_in_pyramid == 0 
    
    def has_moves(self):
        return self.valid_moves_in_pyramid() and self.valid_moves_in_deck() and self.valid_moves_between()
        
    def count_cards_in_pyramid(self):
        self.pyramid_count = sum(1 for row in self.pyramid for card in row if card.playable > 0)
    
    def next_card_in_deck(self):
        self.current_card_in_deck = (self.current_card_in_deck + 1) % 24
    
    def get_valid_moves_in_pyramid(self):
        

    def get_valid_moves_in_deck(self):
        
    
    def get_valid_moves_between(self):
        
    
    def make_move(self):
        