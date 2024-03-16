import copy
import time

class DFS:
    game_state_id = 0
    
    def __init__(self, state):
        self.current_path = [state]
        self.visited_states = set()
        self.solved_state = False
        self.solution = []
        self.nodes_visited = 0
        self.total_nodes = 1
        self.max_depth = 0
        self.backtracks = 0
        self.time_taken = 0
        self.start_time = time.time()

    def search_move(self):
        popped_item = self.current_path.pop() 
        popped_item.update_valid_moves()
        popped_item.update_cards_freed_map()
        popped_item.print_game_state()  
        
        self.nodes_visited += 1
        self.max_depth += 1
    
        if popped_item.is_game_over():
            end_time = time.time()
            self.time_taken = end_time - self.start_time
            
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
                self.time_taken = end_time - self.start_time
                
                moves_made = popped_item.get_moves_made()
                self.solution = popped_item.get_moves_string(moves_made) 
            else:
                self.backtracks += 1
                self.max_depth -= 1
    
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

    def implement_heuristic(self, state):
        reordered_pyramid_moves = self.reorder_moves(state.valid_moves_in_pyramid, state.freed_cards_map)
        reordered_between_moves = self.reorder_moves(state.valid_moves_between, state.freed_cards_map)
        moves_list = state.valid_moves_in_deck + reordered_between_moves + reordered_pyramid_moves + state.king_moves
        
        return moves_list
    
    def reorder_moves(self, moves_list, freed_cards_map):
        moves_list.sort(key=lambda move: len(freed_cards_map[move]))
        
        return moves_list
    
    def print_statistics(self):
        time_taken_str = "{:.5f}".format(self.time_taken)
        
        statistics = "\nStatistics:\n"
        statistics += f"Total nodes generated: {self.total_nodes}\n"
        statistics += f"Number of nodes visited: {self.nodes_visited}\n"
        statistics += f"Maximum depth reached: {self.max_depth}\n"
        statistics += f"Number of backtracks: {self.backtracks}\n"
        statistics += f"Time taken to solve: {time_taken_str} seconds"

        return statistics