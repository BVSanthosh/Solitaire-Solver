#Internal representation of the state of each card

class CardState:
    def __init__(self, card):
        self.card = card
        self.card_num = int(self.card[:-1])
        self.card_suit = self.card[-1]
        self.playable = 2
    
    def set_playable(self, flag):
        self.playable = flag
    
    def __hash__(self):
        return hash(self.card)

    def __eq__(self, other):
        if not isinstance(other, CardState):
            return NotImplemented
        return self.card == other.card