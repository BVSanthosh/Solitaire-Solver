# Automated Solver for Pyramid Solitaire

## Description

This project is a Python application that implements a solver for pyramid that solves the game automatically by interacting with the Windows Solitiare application. The key features of this project include:

## How to run the solver

To run the solver for Pyramid Solitaire, follow these steps:

- Card recognition to obtain the initial state of the game from the game window
- Depth-First Search for finding the winning sequence of moves
- Heuristics to guide the search
- Automated execution of moves in the game window
- A GUI for the solver

## Directory Structure

The directory structure of the project is as follows:

Solitaire-Solver:
│
├───report/
│   │   Playing Pyramid Solitaire Automatically.pdf : The report for the project
│   │
│   ├───figures/ : Contains all the figures included in the report
│   └───test_results/ : Contains all the recorded results from the
|                       performance testing  
│
└───src/
    │   card_state.py : Implements the CardState class 
    │   game_state.py : Implements the GameState class
    │   pyramid_solver.py : The starting point of the solver
    │   screen_interaction.py : Handles the interaction with the game window,
    |                           including card recognition and automated 
    |                           execution of moves.
    │   solver_window.py : Provides a GUI for the solver.
    │   tree_traversal.py: Implements the tree traversal algorithm and heuristics
    │
    ├───game_state
    │       initial_state.json : Stores the initial state of the game
    │
    └───resources
        │   image_to_card.json : Stores the mapping from card screenshots to
        |                        the string representation of the cards       
        │   regions.json : Stores the region data for the cards and buttons
        │
        ├───button/ : Contains screenshots for all the relevant buttons
        ├───cards/ : Contains screenshots for each card's suit and rank
        └───icon/ : Contains an image for the applicaation's icon

## Dependencies

This project requires the following dependencies:

- pygetwindow (0.0.9)
- pyautogui (0.9.54)

You can install these dependencies by running the following command:
pip install -r requirements.txt

## How to run the solver 

1. Make sure you have Python installed on your system. You can download Python from the official website: [python.org](https://www.python.org/downloads/).

2. Clone or download the Solitaire-Solver project from the GitHub repository: [github.com/BVSanthosh/Solitaire-Solver](https://github.com/BVSanthosh/Solitaire-Solver).

3. Open a terminal or command prompt and navigate to the project directory.

4. Install the required dependencies by running: pip install -r requirements.txt.

5. Start the solver by running: python pyramid_solver.py

6. This solver only works on the Windows Solitire applicataion so make sure that the game window is open and isn't minimise before running the solver. 

## Using the GUI

Alternatively, the solver can be started with a GUI by running: python solver_window.py. In screen_interaction.py, the commented-out lines of code need to be uncommented before running the program. These have been labelled. 