#Internal representation of the game state

from card_state import CardState

class GameState:
    def __init__(self, pyramid, deck):
        self.pyramid = [[None for _ in range(7 - row)] for row in range(7)]
        self.deck = [None for _ in range(25)]
        
        for row in range(7):
            for col in range(7 - row):
                self.pyramid[row][col] = CardState(pyramid[row][col])
                if row == 0:
                    self.pyramid[row][col].set_playable(True)
            
        for index in range(24):
            self.deck[index] = CardState(deck[index])
            self.deck[index].set_playable(True)
            
        self.cards_in_deck = self.count_cards_in_deck()
        self.cards_in_pyramid = self.count_cards_in_deck()
        self.valid_moves_in_pyramid = self.get_valid_moves_in_pyramid() 
        self.valid_moves_in_deck = self.get_valid_moves_in_deck()
        self.valid_moves_between = self.get_valid_moves_between
    
    def is_game_over(self):
        if not self.cards_in_pyramid == 0:
            return True
        else:
            return False 
    
    def has_moves(self):
        if not self.valid_moves_in_pyramid() or not self.valid_moves_in_deck() or not self.valid_moves_between() :
            return False
        else:
            return True
        
    def count_cards_in_pyramid(self):
        pyramid_count = 0
        for row in range(7):
            for col in range(7 - row):
                if self.pyramid[row][col].get_playable == True:
                    pyramid_count +=1
    
        return pyramid_count
    
    def count_cards_in_deck(self):
        deck_count = 0
        for cards in self.deck:
            if cards.get_playable == True:
                deck_count +=1
                
        return deck_count
    
    def get_valid_moves_in_pyramid(self):
        
        return self.valid_moves_in_pyramid

    def get_valid_moves_in_deck(self):
        
        return self.valid_moves_in_deck
    
    def get_valid_moves_between(self):
        
        return self.valid_moves_between
    
    def make_move(self):
        