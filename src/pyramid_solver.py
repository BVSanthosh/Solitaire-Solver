import sys
import json
import os
import sys
from game_state import GameState
from tree_traversal import DFS
from screen_interaction import scan_window, read_cards, execute_moves

"""
This module contains the main function for the Pyramid Solitaire solver.
"""

# Main function for the Pyramid Solitaire solver
def pyramid_solver():
    initial_state = None   # Stores the initial game state
    initial_state_file = "game_state/initial_state.json"   # Stores the file path for the initial game state

    print("Scanning game window...")
    if scan_window():   # Checks if the game window is found
        read_cards()   # Reads the cards from the game window and stores them in the initial game state file
    else:
        print("Error: Game window not found. Please try again.")
        sys.exit(1)

    initial_state = load_initial_state(initial_state_file)   # Loads the initial game state from the JSON file
    
    if not initial_state:   # Checks if the initial game state is found
        print("Error: Initial game state not found. Please try again.")
        sys.exit(1)
        
    print("\nInitial game state obtained. Searching for solution...")  
    game_instance = GameState(initial_state["pyramid"], initial_state["deck"])   # Creates a game state instance
    solver_instance = DFS(game_instance)   # Creates a depth-first search instance
     
    while True:   # Loops until a solution is found or the search is exhausted
        solver_instance.search_move()   # Searches for the next move
    
        if solver_instance.solved_state:   # Checks if a solution is found
            print("\nSolution found!")
            break
        elif len(solver_instance.current_path) == 0:   # Checks if the search is exhausted
            print("\nSolution not found.")
            break

    print(solver_instance.print_statistics())   # Prints the search statistics
    solution_moves = solver_instance.solution   # Gets the solution moves

    print("Executing moves...")
    execute_moves(solution_moves)   # Executes the solution moves

# Loads the initial game state from the JSON file
def load_initial_state(initial_state_file):
    if os.path.exists(initial_state_file) and os.path.getsize(initial_state_file) > 0:  # Checks if the JSON file exists and is not empty
        try:
            with open(initial_state_file, 'r') as file:   # Opens the JSON file
                initial_state = json.load(file) 
                
            if not initial_state:  # Checks if the JSON file is empty
                print("Error: The JSON file is empty.")
                return None
            
            return initial_state   # Returns the initial game state
        except json.JSONDecodeError:
            print("Error decoding JSON file. Please check the file format.")
            return None
    else:
        return None
    
if __name__ == "__main__":
    pyramid_solver()