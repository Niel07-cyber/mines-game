import tkinter as tk
from tkinter import messagebox, simpledialog
import random


class MinesGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Mines Game")

        # Screen dimensions
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        # Game Variables
        self.grid_size = 4  # 4x4 grid
        self.difficulty = 3  # Default number of mines
        self.money = 0
        self.mines = set()
        self.safe_boxes = 16
        self.buttons = []
        self.user_name = ""
        self.scores = {}

        # Create UI
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        self.title_label = tk.Label(
            self.root, text="Welcome to Mines Game", font=("Arial", 18, "bold")
        )
        self.title_label.pack(pady=10)

        # Username Input
        self.user_name = simpledialog.askstring(
            "User Name", "Enter your name to start:"
        )
        if not self.user_name:
            self.user_name = "Guest"

        # Difficulty Level Buttons
        difficulty_frame = tk.Frame(self.root)
        difficulty_frame.pack()

        tk.Label(difficulty_frame, text="Select Difficulty:").pack(side=tk.LEFT)
        for level in [3, 5, 8, 10]:
            tk.Button(
                difficulty_frame,
                text=f"{level} Mines",
                command=lambda lvl=level: self.start_game(lvl),
            ).pack(side=tk.LEFT, padx=5)

        # Game Grid Frame
        self.grid_frame = tk.Frame(self.root, bg="white", width=400, height=400)
        self.grid_frame.pack_propagate(False)
        self.grid_frame.pack(pady=20)

        # Score and Reset Frame
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack()

        self.money_label = tk.Label(
            bottom_frame, text="Earnings: $0", font=("Arial", 14)
        )
        self.money_label.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(
            bottom_frame, text="Reset Game", command=self.reset_game, state="disabled"
        )
        self.reset_button.pack(side=tk.LEFT, padx=10)

    def start_game(self, difficulty):
        # Reset game state
        self.difficulty = difficulty
        self.money = 0
        self.mines = set()
        self.safe_boxes = 16 - difficulty
        self.buttons = []

        # Update money label
        self.money_label.config(text="Earnings: $0")
        self.reset_button.config(state="disabled")

        # Clear grid frame
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        # Generate Mines
        self.mines = set(random.sample(range(16), difficulty))

        # Create Grid Buttons
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                button = tk.Button(
                    self.grid_frame,
                    text="",
                    width=5,
                    height=2,
                    bg="#f0f0f0",
                    command=lambda r=row, c=col: self.on_box_click(r, c),
                )
                button.grid(row=row, column=col, padx=5, pady=5)
                self.buttons.append(button)

    def on_box_click(self, row, col):
        box_id = row * self.grid_size + col

        if box_id in self.mines:
            self.buttons[box_id].config(text="X", bg="red", state="disabled")
            self.game_over(False)
        else:
            self.money += 5  # Earn $5 for each correct box
            self.safe_boxes -= 1
            self.buttons[box_id].config(text="✓", bg="green", state="disabled")
            self.money_label.config(text=f"Earnings: ${self.money}")

            if self.safe_boxes == 0:
                self.game_over(True)

    def game_over(self, won):
        # Disable all buttons
        for i, button in enumerate(self.buttons):
            button.config(state="disabled")
            if i in self.mines:
                button.config(text="X", bg="red")

        if won:
            messagebox.showinfo(
                "Game Over",
                f"Congratulations {self.user_name}! You won ${self.money}!",
            )
            self.scores[self.user_name] = self.money
        else:
            messagebox.showerror(
                "Game Over",
                f"Sorry {self.user_name}, you hit a mine! Your total earnings are ${self.money}.",
            )

        self.reset_button.config(state="normal")

    def reset_game(self):
        self.start_game(self.difficulty)


# Run the Game
if __name__ == "__main__":
    root = tk.Tk()
    game = MinesGame(root)
    root.mainloop()
 