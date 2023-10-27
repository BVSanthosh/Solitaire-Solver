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
        self.valid_moves_between = []
        self.valid_moves_in_deck = []
        
        self.initialise_pyramid(pyramid)
        self.initialise_deck(deck)
        self.count_cards_in_pyramid()
        self.get_valid_moves_in_pyramid()
        self.get_valid_moves_between()
        self.get_valid_moves_in_deck()
    
    def initialise_pyramid(self, pyramid):
        for i in range(MAX_ROWS):
            for j in range(MAX_ROWS - row):
                self.pyramid[i][j] = CardState(pyramid[i][j])
                if row == 0:
                    self.pyramid[i][j].set_playable(1)
    
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
        self.valid_moves_in_pyramid = []
        playable_cards = self.get_playable_cards()

        for i in range(len(playable_cards)):
            for j in range(i+1, len(playable_cards)):
                index1 = playable_cards[i]
                index2 = playable_cards[j]
                
                card1 = self.pyramid[index1[0]][index1[1]]  
                card2 = self.pyramid[index2[0]][index2[1]]
                
                if card1.card_num + card2.card_num == 13:
                    self.valid_moves_in_pyramid.append([index1, index2])
                    
    def get_valid_moves_between(self):
        self.valid_moves_between = []
        playable_cards = self.get_playable_cards()
        
        for i in range(len(self.deck)):
            for j in range(len(playable_cards)):
                index = playable_cards[j]
                
                card1 = self.pyramid[index[0]][index[1]] 
                card2 = self.deck[i]
                
                if card1.card_num + card2.card_num == 13:
                    self.valid_moves_between.append([(-1, i), index])

    def get_valid_moves_in_deck(self):
        self.valid_moves_in_deck = []
        
        for i in range(len(self.deck)):
            for j in range(i+1, len(self.deck)):
                card1 = self.deck[i]
                card2 = self.deck[j]
                
                if card1.card_num + card2.card_num == 13:
                    self.valid_moves_in_deck.append([(-1, i), (-1, j)])
                
    def get_playable_cards(self):
        playable_cards = []
        
        for row in range(MAX_ROWS):
            for col in range(MAX_ROWS - row):
                if self.pyramid[row][col].playable == 1:
                    playable_cards.append((row, col))
                    
        return playable_cards
        
    def make_move(self, move):
        card1_index1, card1_index2 = move[0]
        card2_index1, card2_index2 = move[1]
        
        if card1_index1 == -1 and card2_index1 == -1:
            self.deck[card1_index2].set_playable(0)
            self.deck[card2_index2].set_playable(0)
        elif card1_index1 == -1:
            self.deck[card1_index2].set_playable(0)
            self.pyramid[card2_index1][card2_index2].set_playable(0)
        else:
            self.pyramid[card1_index1][card1_index2].set_playable(0)
            self.pyramid[card2_index1][card2_index2].set_playable(0)