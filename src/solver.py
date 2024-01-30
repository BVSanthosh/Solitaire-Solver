#Uses a search algorithm and a heuristic to calculate the best move to make

import copy
import time

class Solver:
    def __init__(self, state, moves_made):
        self.current_path = [(state, moves_made)]
        self.visited_states = set()
        self.solved_state = False

    def search_move(self):
        popped_item = self.current_path.pop() 
        popped_item[0].update_valid_moves()
        
        popped_item[0].print_game_state()  
        popped_item[0].print_game_info() 
        print("\n Moves made:" + str(popped_item[1]))
        
        if popped_item[0].is_game_over():
            self.solved_state = True
        elif popped_item[0].has_moves() and popped_item[0] not in self.visited_states:
            self.visited_states.add(popped_item[0])
            self.current_path.extend(self.get_child_states(popped_item))
            print("\nEntering node:" + str(popped_item[0]) + "\n")
        else:
            print("Backtracking from node: " + str(popped_item[0]) )
        
        #time.sleep(2)
    
    def get_child_states(self, state):
        reversed_pyramid_moves = list(reversed(state[0].valid_moves_in_pyramid))
        reversed_between_moves = list(reversed(state[0].valid_moves_between))
        reversed_deck_moves = list(reversed(state[0].valid_moves_in_deck))
        
        moves_list = reversed_deck_moves + reversed_between_moves + reversed_pyramid_moves
        next_states = []
        
        for move in moves_list:
            next_state = copy.deepcopy(state[0])
            next_state.make_move(move)
            next_states.append((next_state, state[1] + [move]))
            
        return next_states