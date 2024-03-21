import json
import os
import threading
import queue
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from game_state import GameState
from tree_traversal import DFS
from screen_interaction import scan_window, read_cards, execute_moves

"""
This module contains the SolverWindow class, which is used to create the GUI for the Pyramid Solitaire solver.

This file isn't intended to be part of the final submission but can still be run to test the GUI. Instructions on how to run the GUI are provided in the README.md file.

The code for the GUI has been written with the help of ChatGPT.
"""

class SolverWindow:
    initial_state = None
        
    def __init__(self, root):
        self.root = root
        root.title("Pyramid Solver")
        root.geometry("1000x1000")
        root.resizable(True, True)
        root.attributes("-topmost", True)
        root.iconbitmap("resources/icon/icon.ico")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.customFont = tkFont.Font(family="Helvetica", size=12)
        self.customFontBold = tkFont.Font(family="Helvetica", size=12, weight="bold")
    
        style = ttk.Style()
        style.configure("TButton", font=self.customFont, padding=6, relief="flat", background="#ccc")
        style.map("TButton", background=[('active', '#eee')])
        
        self.pyramid_cards = {}
        self.update_queue = queue.Queue()
        
        self.check_queue()
        self.setup_empty_game()
        
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(side=tk.BOTTOM, pady=10)

        self.scan_button = ttk.Button(self.button_frame, text="Scan Window", command=self.scan, style='TButton')
        self.scan_button.pack(side=tk.LEFT, padx=5)

        self.solve_button = ttk.Button(self.button_frame, text="Solve Game", command=self.solve, style='TButton', state='disabled')
        self.solve_button.pack(side=tk.LEFT, padx=5)
        
        self.status_text = tk.Text(self.root, height=10, width=50, state='disabled', wrap='word', font=self.customFont)
        self.scrollbar = tk.Scrollbar(self.root, command=self.status_text.yview)
        self.status_text['yscrollcommand'] = self.scrollbar.set
        
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady= 10, padx=(100, 100))
        
        self.update_status("Click 'Scan Window' to begin")
        
        self.button_frame.pack(side=tk.BOTTOM, pady=10) 
        
    # Sets up the empty game display
    def setup_empty_game(self):
        key_int = 0
        tk.Frame(self.root, height=40).pack()
        
        self.pyramid_frame = tk.Frame(self.root)
        self.pyramid_frame.pack(expand=True)

        for row in range(1, 8):
            row_frame = tk.Frame(self.pyramid_frame)
            row_frame.pack()
            for _ in range(row):  
                card_label = tk.Label(row_frame, text="", borderwidth=2, relief="groove", width=3, height=2, font=self.customFontBold)
                card_label.pack(side=tk.LEFT, padx=10, pady=2)
                self.hover_effect(card_label, on_enter_color="lightblue", on_leave_color="SystemButtonFace")
                self.pyramid_cards[key_int] = card_label
                key_int += 1
                
        tk.Frame(self.root, height=20).pack()
        
        self.deck_frame = tk.Frame(self.root)
        self.deck_frame.pack(expand=True)

        for _ in range(2): 
            row_frame = tk.Frame(self.deck_frame)
            row_frame.pack()
            for _ in range(12): 
                card_label = tk.Label(row_frame, text="", borderwidth=2, relief="groove", width=3, height=2, font=self.customFontBold)
                card_label.pack(side=tk.LEFT, padx=3, pady=2)
                self.hover_effect(card_label, on_enter_color="lightblue", on_leave_color="SystemButtonFace")
                self.pyramid_cards[key_int] = card_label
                key_int += 1
                
        tk.Frame(self.root, height=30).pack()
    
    # Resets the game display
    def reset_display(self):
        for label in self.pyramid_cards.values():
            label.config(text="")
    
    # Updates the game display with the card text
    def update_game_display(self, card_id, card_text):
        card_label = self.pyramid_cards[card_id]
        card_label.config(text=card_text)
        self.root.update_idletasks()
        
    # Updates the textbox status message
    def update_status(self, message):
        self.status_text.config(state='normal')
        self.status_text.delete(1.0, tk.END)
        self.status_text.tag_configure('center', justify='center')
        self.status_text.insert(tk.END, message)
        self.status_text.tag_add('center', 1.0, "end")
        self.status_text.config(state='disabled')
    
    # Adds a hover effect to the label widget
    def hover_effect(self, label_widget, on_enter_color, on_leave_color):
        def on_enter(event):
            label_widget.config(background=on_enter_color)

        def on_leave(event):
            label_widget.config(background=on_leave_color)

        label_widget.bind("<Enter>", on_enter)
        label_widget.bind("<Leave>", on_leave)
    
    # Highlights the card labels
    def highlight_cards(self, card):
        card_label = self.find_label(card)
        
        if card_label:
            highlight_color = "silver"
            card_label.config(background=highlight_color)
            self.root.update_idletasks()
    
    # Finds the label widget with the card text
    def find_label(self, card_text):
        for key, label in self.pyramid_cards.items():
            if label["text"] == card_text:
                return label
        return None
    
    # Checks the update queue for new commands
    def check_queue(self):
        try:
            while True:
                update_command = self.update_queue.get_nowait()
                update_command()
        except queue.Empty:
            pass
        self.root.after(100, self.check_queue)
    
    # Function to scan the game window and loads the initial game state when "Scan Window" button is clicked
    def scan(self):
        def scan_card_callback(card_id, card_text):
            self.update_queue.put(lambda: self.update_game_display(card_id, card_text))
            
        def on_scan_complete():
            global initial_state
            initial_state = self.load_initial_state("game_state/initial_state.json")
            
            if not initial_state:
                print("\nScan was unsuccessfully. Please try again.") 
                self.update_status("Scan unsuccessful. Please try again.")
                self.scan_button['state'] = 'normal'
            else:
                card_int = 0
                
                print("\nScan was successfully. Initial game state obtained.") 
                
                pyramid_cards = initial_state["pyramid"]
                deck_cards = initial_state["deck"]
                
                combined_rows = []
                for row in range(6, -1, -1):
                    combined_rows += pyramid_cards[row]
                
                for card in combined_rows:
                    self.pyramid_cards[card_int].config(text=card)
                    card_int += 1
                    
                for card in deck_cards:
                    self.pyramid_cards[card_int].config(text=card)
                    card_int += 1
                
                self.solve_button['state'] = 'normal'
                self.update_status("Scanned initial game state. Ready to solve.")
                
        def scan_and_load():
            if scan_window():
                read_cards(scan_card_callback)
            
            self.update_queue.put(on_scan_complete)
            
        self.scan_button['state'] = 'disabled'
        self.reset_display()
            
        with open("game_state/initial_state.json", "w") as file:
            json.dump({}, file)
        
        print("\nScanning game window...")
        self.update_status("Scanning game window...")
        
        scanning_thread = threading.Thread(target=scan_and_load)
        scanning_thread.start()
    
    # Function to solve the game when "Solve Game" button is clicked
    def solve(self): 
        global initial_state
        result_text = ""
        
        def highlight_cards_callback(card):
            self.update_queue.put(lambda: self.highlight_cards(card))
            
        def output_stats():
            print("\nGame solved successfully!")
            solution_message = "Game solved successfully!\n" + solver_instance.print_statistics()
            self.update_status(solution_message)
            self.scan_button['state'] = 'normal'
            
        def solve_and_output_result():
            execute_moves(solution_moves, highlight_cards_callback)
            self.update_queue.put(output_stats)
        
        self.solve_button['state'] = 'disabled'
            
        game_instance = GameState(initial_state["pyramid"], initial_state["deck"])
        solver_instance = DFS(game_instance)
        
        print("\nSearching for solution...") 
        self.update_status("Searching for solution...")
        
        while True:
            solver_instance.search_move()
        
            if solver_instance.solved_state:
                result_text += "\nSolution found!\n"
                result_text += solver_instance.print_statistics() + "\n"
                result_text += "\nExecuting moves..."
                self.update_status("Solution found! \nExeceuting moves...")
                break
            elif len(solver_instance.current_path) == 0:
                result_text += "\nSolution not found!"
                result_text += solver_instance.print_statistics()
                result_text += "\nExecuting moves..."
                self.update_status("Solution not found. \nExecuting moves.")
                break
        
        print(result_text)
        solution_moves = solver_instance.solution
            
        solving_thread = threading.Thread(target=solve_and_output_result)
        solving_thread.start()
    
    # Loads the initial game state from the JSON file
    def load_initial_state(self, initial_state_file):
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
    
    # Termminates the program when the solver window is closed
    def on_close(self):
            self.root.destroy() 
            os._exit(0)
        
def main():
    root = tk.Tk()   # Creates the main window
    app = SolverWindow(root)   # Creates the SolverWindow instance
    root.mainloop()   # Runs the main event loop
    
if __name__ == "__main__":
    main()