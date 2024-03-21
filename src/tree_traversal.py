import copy
import time

"""
This module contains the DFS class, which is used to perform depth-first search.
"""

class DFS:
    game_state_id = 0   # Stores a counter for the game state id
    
    def __init__(self, state):
        self.current_path = [state]   # Stores the current path of the search
        self.visited_states = set()   # Stores the visited states
        self.solved_state = False   # Stores whether the current state is the winning state
        self.solution = []   # Stores the final solution moves
        self.nodes_visited = 0   # Stores the number of nodes visited
        self.total_nodes = 1   # Stores the total number of nodes generated
        self.depth_level = 0   # Stores the depth level of the winning state
        self.backtracks = 0   # Stores the number of backtracks
        self.time_taken = 0   # Stores the time taken to solve
        self.start_time = time.time()   # Stores the start time of the search
        
    # Gets the next node in the search space
    def search_move(self):
        popped_item = self.current_path.pop() 
        popped_item.update_valid_moves()
        popped_item.update_cards_freed_map()
        popped_item.print_game_state()  
        
        self.nodes_visited += 1
        self.depth_level += 1
    
        if popped_item.is_game_over():
            end_time = time.time()
            self.time_taken = (end_time - self.start_time) * 1000
            
            moves_made = popped_item.get_moves_made()
            self.solution = popped_item.get_moves_string(moves_made)
            self.solved_state = True
        elif popped_item.has_moves() and popped_item not in self.visited_states:
            print(f"\n=> Entering node: {popped_item.id}")
            
            self.visited_states.add(popped_item)
            self.current_path.extend(self.get_child_states(popped_item))
        else:
            print(f"\n<= Backtracking from node: {popped_item.id}")
            
            if len(self.current_path) == 0:
                end_time = time.time()
                self.time_taken = (end_time - self.start_time) * 1000
                
                moves_made = popped_item.get_moves_made()
                self.solution = popped_item.get_moves_string(moves_made) 
            else:
                self.backtracks += 1
                self.depth_level -= 1
    
    # Gets the child nodes of the current node
    def get_child_states(self, state):
        moves_list = self.implement_heuristic(state)
        next_states = []
        
        self.total_nodes += len(moves_list)
        
        for move in moves_list:
            next_state = copy.deepcopy(state)
            DFS.game_state_id += 1
            next_state.update_state_id(DFS.game_state_id)
            next_state.make_move(move)
            next_state.update_moves_made(move)
            next_state.clear_cards_freed_map()
            next_states.append(next_state)
            
        return next_states
    
    # Implements the heuristic for the search
    def implement_heuristic(self, state):
        reordered_pyramid_moves = self.reorder_moves(state.valid_moves_in_pyramid, state.freed_cards_map)
        reordered_between_moves = self.reorder_moves(state.valid_moves_between, state.freed_cards_map)
        moves_list = state.valid_moves_in_deck + reordered_between_moves + reordered_pyramid_moves + state.king_moves
        
        return moves_list
    
    # Reorders the moves based on the number of freed cards
    def reorder_moves(self, moves_list, freed_cards_map):
        moves_list.sort(key=lambda move: len(freed_cards_map[move]))
        
        return moves_list
    
    # Prints the search statistics
    def print_statistics(self):
        time_taken_str = "{:.5f}".format(self.time_taken)
        
        statistics = "\nStatistics:\n"
        statistics += f"Total nodes generated: {self.total_nodes}\n"
        statistics += f"Number of nodes visited: {self.nodes_visited}\n"
        statistics += f"Depth-level reached: {self.depth_level}\n"
        statistics += f"Number of backtracks: {self.backtracks}\n"
        statistics += f"Time taken to solve: {time_taken_str} ms\n"

        return statistics