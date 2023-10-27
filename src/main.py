#Main loop of the game

from game_state import GameState
from solver import Solver
import screen_capture

def main():
    print("Pyramid Solver starting...")
    
    game_instance = GameState([], [])
    
    while True:
        if game_instance.is_game_over():
            print("Game Won")
            break
        elif not(game_instance.has_moves()):
            print("Out of moves")
            break
        
        solver_instance = Solver(game_instance)
        best_move = solver_instance.make_best_move()
        move_made = game_instance.make_move(best_move) 
        
        if not(move_made):
            print("Failed to execute the move")

if __name__ == "__main__":
    main()