"""
This module contains the CardState class, which is used to represent the state of each card in the game.
"""

class CardState:
    def __init__(self, card):
        self.card = card  # Stores the card value
        self.card_num = int(self.card[:-1])  # Extracts the numerical value of the card
        self.card_suit = self.card[-1]  # Extracts the suit of the card
        self.playable = 2  # Sets the default playable status to 2
        
    # Updates the playable status of the card
    def set_playable(self, flag):
        self.playable = flag
        
    # Hashes the card value
    def __hash__(self):
        return hash(self.card)  
    
    # Compares the card value with another card
    def __eq__(self, other):
        if not isinstance(other, CardState):
            return NotImplemented
        return self.card == other.card
