#Main loop of the game

from game_state import GameState
from solver import Solver

def main():
    game_instance = GameState([
    ["11H", "4H", "9H", "11C", "7D", "9D", "13D"],
    ["5H", "13C", "3C", "10S", "13H", "7S"],
    ["1S", "8H", "12D", "8C", "13H"],
    ["1H", "7H", "8S", "10H"],
    ["1C", "9C", "5S"],
    ["6D", "10D"],
    ["3D"]
    ], ["9S", "6C", "3S", "4S", "11S", "4C", "5D", "1H",
    "2H", "11D", "6H", "12C", "7C", "12S", "2D", "5C",
    "6S", "4D", "3H", "2C", "10C", "8D", "13S", "2S"])
    
    solver_instance = Solver(game_instance, [])
    
    while  True:
        solver_instance.search_move()
    
        if solver_instance.solved_state:
            print("Game won!")
            break
        elif len(solver_instance.current_path) == 0:
            print("Game cannot be won")
            break
    
if __name__ == "__main__":
    main()