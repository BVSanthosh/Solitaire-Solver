#Uses a search algorithm and a heuristic to calculate the best move to make

import copy

class Solver:
    def __init__(self, state, moves_made):
        self.current_path = [(state, moves_made)]
        self.visited_states = set()

    def search_move(self):
        popped_item = self.current_path.pop() 
        
        if popped_item[0].is_game_over():
            print("Game won!")
        elif popped_item[0].has_moves() and popped_item[0] not in self.visited_states:
            self.visited_states.add(popped_item[0])
            self.current_path.extend(self.get_child_states(popped_item))
            print("Entering node:" + str(popped_item[0]))
        else:
            print("Backtracking from node: " + str(popped_item[0]) )
        
    def get_child_states(self, state):
        next_states = []
        moves_list = state[0].get_valid_moves_in_deck() + state[0].get_valid_moves_between() + state[0].get_valid_moves_in_pyramid()
        
        for move in moves_list:
            next_state = copy.deepcopy(state[0])
            next_state.make_move(move)
            next_states.append((next_state, state[1] + [move]))
            
        return next_states