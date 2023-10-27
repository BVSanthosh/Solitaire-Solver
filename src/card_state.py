#Internal representation of the state of each card

class CardState:
    def __init__(self, card):
        self.card = card
        self.card_num = self.get_card_num()
        self.card_suit = self.get_card_suit()
        self.playable = False
        
    def get_card_num(self):
        if len(self.card) == 2:
            return int(self.card[0])
        else:
            return int(self.card[0:2])
            
    def get_card_suit(self):
        return self.card[:0]
    
    def set_playale(self, playable):
        self.is_playale = playable
    
    def get_playale(self):
        return self.playable