#Main loop of the game

from game_state import GameState
from solver import Solver

def main():
    game_instance = GameState([
    ["3D", "5S", "8C", "3C", "5H", "2H", "13S"],
    ["6D", "2D", "12H", "2C", "10D", "10S"],
    ["3S", "9C", "12S", "4C", "10C"],
    ["12D", "13S", "5C", "13H"],
    ["2S", "1C", "1D"],
    ["13D", "4D"],
    ["5H"]
    ], ["6H", "10H", "4S", "9H", "11S", "9D", "7H", "12C",
    "11H", "3H", "7C", "7D", "7S", "4H", "3D", "6S",
    "9S", "11C", "1H", "6C", "1S", "8S", "5D", "11D"])
    '''
    moves_made = [[(0, 1), (0, 2)], [(0, 6)], [(-1, 1), (0, 0)], [(-1, 1), (0, 3)], [(-1, 4), (0, 5)], [(-1, 4), (1, 1)], [(-1, 6), (1, 0)], [(1, 5), (2, 0)], [(-1, 18), (1, 2)], [(-1, 2), (2, 1)], [(-1, 18), (3, 0)], [(-1, 21), (0, 4)], [(-1, 4), (1, 3)], [(-1, 9), (1, 4)], [(-1, 3), (2, 3)], [(-1, 9), (2, 4)], [(3, 3)], [(-1, 18), (2, 2)], [(3, 1)], [(-1, 4), (4, 0)], [(-1, 21), (3, 2)], [(-1, 7), (4, 1)], [(5, 0)], [(-1, 7), (4, 2)], [(-1, 11), (-1, 19)], [(-1, 12), (-1, 15)], [(-1, 5), (-1, 13)], [(-1, 0), (-1, 10)], [(-1, 5), (5, 1)]]
    
    for move in moves_made:
        print("\nMove made: " + str(move))
        game_instance.make_move(move)
        game_instance.update_valid_moves()
        game_instance.print_game_state()
        game_instance.print_game_info()
    '''
    solver_instance = Solver(game_instance, [])
    
    while  True:
        solver_instance.search_move()
        
        if len(solver_instance.current_path) == 0:
            print("Game cannot be won")
            break
        elif solver_instance.solved_state:
            print("Game won!")
            break
    
if __name__ == "__main__":
    main()