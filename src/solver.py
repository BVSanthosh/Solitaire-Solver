#Uses a search algorithm and a heuristic to calculate the best move to make

class Solver:
    def __init__(self, game_state):
        self.current_state = game_state
        
    def make_best_move(self):