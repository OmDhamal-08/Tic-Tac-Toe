import tkinter as tk

import database as dt
import details as dtt
from database import MODE_AI_HARD, MODE_AI_MEDIUM, MODE_PVP

class GameModeLauncher:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic-Tac-Toe Game Mode Launcher")
        self.master.geometry("350x400")
        self.master.resizable(False, False)

        tk.Label(master, text="Welcome to Tic-Tac-Toe", font=("Arial", 16, "bold")).pack(pady=15)
        tk.Label(master, text="Choose a Game Mode:", font=("Arial", 12)).pack(pady=10)

        tk.Button(master, text="Player vs Player", width=25, command=self.start_pvp).pack(pady=5)
        tk.Button(master, text="Player vs AI (Medium)", width=25, command=self.start_ai_medium).pack(pady=5)
        tk.Button(master, text="Player vs AI (Hard)", width=25, command=self.start_ai_hard).pack(pady=5)
        tk.Button(master, text="My Stats", width=25, command=lambda: dtt.prompt_and_show_player_stats(master)).pack(pady=5)
        tk.Button(master, text="Leaderboard", width=25, command=lambda: dtt.show_leaderboard_gui(master)).pack(pady=5)


    def start_pvp(self):
        self.master.destroy()
        dt.main(MODE_PVP)  

    def start_ai_medium(self):
        self.master.destroy()
        dt.main(MODE_AI_MEDIUM) 

    def start_ai_hard(self):
        self.master.destroy()
        dt.main(MODE_AI_HARD) 

def main():
    root = tk.Tk()
    app = GameModeLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main()
