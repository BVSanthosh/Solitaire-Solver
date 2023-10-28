#Main loop of the game

from game_state import GameState
from solver import Solver

def main():
    print("Pyramid Solver starting...")
    
    game_instance = GameState([
    ["9S", "10H", "11C", "12D", "13C", "1H", "2S"],
    ["3D", "4S", "5H", "6D", "7C", "8D"],
    ["11D", "12S", "13H", "1C", "2H"],
    ["7S", "8H", "9D", "10C"],
    ["4H", "5D", "6C"],
    ["2D", "3S"],
    ["1S"]
    ], [
    "3H", "4D", "5S", "6H", "7D", "8S", "9H", "10D",
    "11S", "12H", "13D", "1D", "2C", "3C", "4C", "5C",
    "6S", "7H", "8C", "9C", "10S", "11H", "12S", "13S"
    ])
    
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