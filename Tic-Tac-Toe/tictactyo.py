import tkinter as tk
from tkinter import messagebox

from details import update_match_result
from game_logic import (
    check_winner,
    format_board,
    new_board,
    place_symbol,
)
class Game:
    def __init__(self):
        self.obj_array = new_board()
        self.separator = "-" * 20

    def instructons(self):
        try:
            print("\t", self.separator)
            print("\tWelcome to Tic Tac Toe Game")
            print("\t", self.separator)
            print("\nPlayer 1 is 'X' and Player 2 is 'Y'\n")
            print("  1 | 2 | 3 ")
            print(" ---+---+---")
            print("  4 | 5 | 6 ")
            print(" ---+---+---")
            print("  7 | 8 | 9 ")
            print(self.separator)
            for i in range(9):
                if i % 2 == 0:
                    print("player 1 (having character'X') turn")
                    valid = False
                    while not valid:
                        given = int(input("Kindly Enter the position on which you need to add your symbol:"))
                        valid = self.add_symbol(given, "X")
                else:
                    print("player 2 (having character'Y') turn")
                    valid=False
                    while not valid:
                        given=int(input("Kindly Enter the position on which you need to add you symbol:"))
                        valid=self.add_symbol(given, "Y")
                win=self.winner()
                if win in {"X","Y"}:
                    print(f"{self.separator}Winner is{self.separator}")
                    print(f"{self.separator}Player {win} {self.separator}")
                    return
            print(f"{self.separator}It's a tie{self.separator}")
            print(f"{self.separator}Thanks for playing the game{self.separator}")

        except Exception as  E:
             print(f"An error occurred: {E}")

    def printing_array(self):
        print(f"{self.separator}Current state of the game{self.separator}")
        print(format_board(self.obj_array))
        print(self.separator)

    def add_symbol(self, given, symbol):
        try:
            place_symbol(self.obj_array, given, symbol)
            self.printing_array()
            return True
        except ValueError as exc:
            print(f"{self.separator}{exc}{self.separator}")
            return False

    def adder1(self,given):
        return self.add_symbol(given, "X")

    def adder2(self,given):
        return self.add_symbol(given, "Y")

    def winner(self):
        return check_winner(self.obj_array)


class GameGUI:
    def __init__(self, master, username1, username2):
        self.master = master
        self.master.title("Tic Tac Toe - GUI Version")
        self.game = Game()
        self.turn = 0
        self.username1 = username1
        self.username2 = username2
        self.status_var = tk.StringVar(value="")

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_widgets()
        self._update_status()

    def ask_replay(self):
        response = messagebox.askyesno("Play Again?", "Do you want to play again with the same players?")
        if response:
            self.reset_game()
        else:
            self.master.destroy()
            import Main  # ✅ Import main launcher here
            root = tk.Tk()
            Main.GameModeLauncher(root)
            root.mainloop()


    def create_widgets(self):
        for i in range(3):
            for j in range(3):
                b = tk.Button(self.master, text="", font=("Arial", 24), width=5, height=2,
                              command=lambda row=i, col=j: self.handle_click(row, col))
                b.grid(row=i, column=j)
                self.buttons[i][j] = b

        self.reset_button = tk.Button(self.master, text="Restart", font=("Arial", 14),
                                      command=self.reset_game)
        self.reset_button.grid(row=3, column=0, columnspan=3, sticky="nsew")

        status = tk.Label(self.master, textvariable=self.status_var, font=("Arial", 12))
        status.grid(row=4, column=0, columnspan=3, pady=10)

    def handle_click(self, row, col):
        pos = 3 * row + col + 1

        if self.game.obj_array[row][col] != 0:
            messagebox.showwarning("Invalid Move", "Position already occupied.")
            return

        if self.turn % 2 == 0:
            self.game.adder1(pos)
            self.buttons[row][col]["text"] = "X"
        else:
            self.game.adder2(pos)
            self.buttons[row][col]["text"] = "Y"

        winner = self.game.winner()
        if winner:
            messagebox.showinfo("Game Over", f"Player {winner} wins!")
            self.update_scores(winner)  
            self.disable_all_buttons()
            self.ask_replay() 
        elif self.turn == 8:
            messagebox.showinfo("Game Over", "It's a tie!")
            self.update_scores(None) 
            self.disable_all_buttons()
            self.ask_replay() 

        self.turn += 1
        self._update_status()


    def update_scores(self, winner):
        opponent = None if self.username2 == "AI" else self.username2
        update_match_result(self.username1, opponent, winner)

    def _update_status(self):
        current_player = self.username1 if self.turn % 2 == 0 else self.username2
        symbol = "X" if self.turn % 2 == 0 else "Y"
        self.status_var.set(f"{current_player} ({symbol}) to move")


    def disable_all_buttons(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")

    def reset_game(self):
        self.turn = 0
        self.game = Game()  # Reset original logic
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["text"] = ""
                self.buttons[i][j]["state"] = "normal"
        self._update_status()

# def main():
#     # g=Game()
#     # g.instructons()
#     root =tk.Tk()
#     app = GameGUI(root)
#     root.mainloop()
# if __name__ == "__main__":
#     main()
