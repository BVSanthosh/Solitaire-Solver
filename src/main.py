import sys
import json
import os
import sys

from game_state import GameState
from solver import Solver
from screen_interaction import scan_window, execute_moves

def main():
    initial_state = None
    initial_state_file = "game_state/initial_state.json"

    print("Scanning game window...")
    scan_window()
    
    initial_state = load_initial_state(initial_state_file)
    
    if not initial_state:
        print("Error: Initial game state not found. Please try again.")
        sys.exit(1)
        
    print("\nInitial game state obtained. Searching for solution...")  
    game_instance = GameState(initial_state["pyramid"], initial_state["deck"])
    solver_instance = Solver(game_instance)
     
    while  True:
        solver_instance.search_move()
    
        if solver_instance.solved_state:
            print("\nSolution found!")
            break
        elif len(solver_instance.current_path) == 0:
            print("\nSolution not found.")
            break
    
    solution_moves = solver_instance.solution

    print("\nExecuting moves...")
    execute_moves(solution_moves)
    
def load_initial_state(initial_state_file):
    if os.path.exists(initial_state_file) and os.path.getsize(initial_state_file) > 0:
        try:
            with open(initial_state_file, 'r') as file:
                initial_state = json.load(file) 
                
            if not initial_state:  
                print("Error: The JSON file is empty.")
                return None
            
            return initial_state
        except json.JSONDecodeError:
            print("Error decoding JSON file. Please check the file format.")
            return None
    else:
        return None
    
if __name__ == "__main__":
    main()