# in this we just 
import tkinter as tk
from tkinter import messagebox

from details import update_match_result
from game_logic import (
    board_full,
    check_winner,
    format_board,
    new_board,
    place_symbol,
    random_move,
    set_symbol,
)
class Game:
    def __init__(self):
        self.obj_array = new_board()
        self.seperator = "-" * 20

    def instruction(self):
        try:
            print("\t",self.seperator)
            print("\tWelcome to Tic Tac Toe Game")
            print("\t",self.seperator)
            print("\nPlayer 1 is 'X' and Player 2 is 'Y'\n")
            print("  1 | 2 | 3 ")
            print(" ---+---+---")
            print("  4 | 5 | 6 ")
            print(" ---+---+---")
            print("  7 | 8 | 9 ")
            print(self.seperator)
            for i in range(9):
                if(i%2==0):
                    valid=False
                    while not valid:
                        given=int(input("Player 1 it is your just enter the position"))
                        valid=self.player1(given)
                else:
                    print("Pc turn")
                    self.player2()

                win=self.winner()
                if win=='X':
                    print(f"{self.seperator}Winner is{self.seperator}")
                    print(f"{self.seperator}Player X {self.seperator}")
                    return
                elif win=='Y':
                    print(f"{self.seperator}Winner is{self.seperator}")
                    print(f"{self.seperator}Player Y {self.seperator}")
                    return
                if i==8 and win is None:
                    print(f"{self.seperator}It's a tie{self.seperator}")
                    print(f"{self.seperator}Thanks for playing the game{self.seperator}")
        except Exception as E:
            print(f"{self.seperator}An error occurred{self.seperator}")
            print(E)

    def player1(self,given):
        try:
            place_symbol(self.obj_array, given, 'X')
            self.printing_array()
            return True
        except ValueError as exc:
            print(f"{self.seperator}{exc}{self.seperator}")
            return False
    
    def player2(self):
        move = random_move(self.obj_array)
        if move:
            row, col = move
            set_symbol(self.obj_array, row, col, 'Y')
            self.printing_array()


    def printing_array(self):
        print(f"{self.seperator}Current state of the game{self.seperator}")
        print(format_board(self.obj_array))
        print(self.seperator)
        
    
    def winner(self):
        return check_winner(self.obj_array)
class GameGUI:
    def __init__(self, master, username):
        self.master = master
        self.master.title("Tic Tac Toe - Medium AI")
        self.game = Game()
        self.turn = 0  # Even = Player 1 (X), Odd = Player 2 (Y)
        self.username = username
        self.status_var = tk.StringVar(value="")

        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.create_widgets()
        self._update_status()

    def create_widgets(self):
        for i in range(3):
            for j in range(3):
                b = tk.Button(self.master, text="", font=("Arial", 24), width=5, height=2,
                              command=lambda row=i, col=j: self.handle_click(row, col))
                b.grid(row=i, column=j)
                self.buttons[i][j] = b

        status = tk.Label(self.master, textvariable=self.status_var, font=("Arial", 12))
        status.grid(row=3, column=0, columnspan=3, pady=10)

    def handle_click(self, row, col):
        if self.game.obj_array[row][col] != 0:
            messagebox.showwarning("Invalid Move", "Position already occupied.")
            return

        pos = 3 * row + col + 1
        self.game.player1(pos)
        self.buttons[row][col]["text"] = "X"
        self.buttons[row][col]["state"] = "disabled"
        self.turn += 1

        winner = self.game.winner()
        if winner:
            self.end_game(winner)
            return
        elif board_full(self.game.obj_array):
            self.end_game(None)
            return

        self.master.after(500, self.computer_turn)


    def computer_turn(self):
        prev_state = [row.copy() for row in self.game.obj_array]
        self.game.player2()

        for i in range(3):
            for j in range(3):
                if prev_state[i][j] != self.game.obj_array[i][j]:
                    self.buttons[i][j]["text"] = "Y"
                    self.buttons[i][j]["state"] = "disabled"
                    self.turn += 1
                    break

        winner = self.game.winner()
        if winner:
            self.end_game(winner)
            return
        elif board_full(self.game.obj_array):
            self.end_game(None)
            return
        self._update_status()



    def disable_all_buttons(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")

    def reset_game(self):
        self.turn = 0
        self.game = Game()
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["text"] = ""
                self.buttons[i][j]["state"] = "normal"
        self._update_status()

    def end_game(self, winner):
        if winner:
            messagebox.showinfo("Game Over", f"{'You' if winner == 'X' else 'Computer'} wins!")
        else:
            messagebox.showinfo("Game Over", "It's a tie!")
        self.disable_all_buttons()
        update_match_result(self.username, None, winner)
        self.ask_play_again()

    def ask_play_again(self):
        play_again = messagebox.askyesno("Play Again", "Do you want to play again?")
        if play_again:
            self.reset_game()
        else:
            self.master.destroy()
            from Main import main
            main()

    def _update_status(self):
        symbol = "X" if self.turn % 2 == 0 else "Y"
        player = self.username if symbol == "X" else "Computer"
        self.status_var.set(f"{player} ({symbol}) to move")

def start_game(username):
    root = tk.Tk()
    GameGUI(root, username)
    root.mainloop()


def main():
    root=tk.Tk()
    app=GameGUI(root, "Guest")
    root.mainloop()


if __name__ == "__main__":
    main()