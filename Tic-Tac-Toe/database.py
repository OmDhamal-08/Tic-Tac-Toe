import hashlib
import hmac
import os
import sqlite3
import tkinter as tk
from tkinter import messagebox

from db_utils import connect_db, ensure_users_table

MODE_PVP = "Player vs Player"
MODE_AI_MEDIUM = "Player vs AI (Medium)"
MODE_AI_HARD = "Player vs AI (Hard)"
VALID_MODES = {MODE_PVP, MODE_AI_MEDIUM, MODE_AI_HARD}


def hash_password(password, iterations=150_000):
    salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return f"pbkdf2_sha256${iterations}${salt.hex()}${hashed.hex()}"


def verify_password(password, stored_value):
    if stored_value.startswith("pbkdf2_sha256$"):
        _, iter_str, salt_hex, hash_hex = stored_value.split("$")
        iterations = int(iter_str)
        salt = bytes.fromhex(salt_hex)
        stored_hash = bytes.fromhex(hash_hex)
        computed = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
        return hmac.compare_digest(stored_hash, computed)
    return hmac.compare_digest(password, stored_value)


class LoginRegisterGUI:
    def __init__(self, master, mode):
        self.master = master
        self.master.title("Login / Registration")
        self.master.geometry("300x300")
        self.db = Data_store_class()

        if mode not in VALID_MODES:
            raise ValueError(f"Unsupported mode: {mode}")
        self.mode = mode

        # GUI widgets...
        self.title_label = tk.Label(master, text="Welcome to Tic-Tac-Toe", font=("Arial", 14, "bold"))
        self.title_label.pack(pady=10)

        self.username_label = tk.Label(master, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(master)
        self.username_entry.pack()

        self.password_label = tk.Label(master, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(master, text="Login & Continue", command=self.login_user)
        self.login_button.pack(pady=5)

        self.register_button = tk.Button(master, text="Register", command=self.register_user)
        self.register_button.pack(pady=5)

        self.logged_in_users = []

    def login_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        result = self.db.login_individual(username, password)
        if result:
            self.logged_in_users.append(username)

            if self.mode == MODE_PVP:
                if len(self.logged_in_users) == 1:
                    messagebox.showinfo("Login Success", f"Player 1: {username} logged in.\nNow, login Player 2.")
                    self.username_entry.delete(0, tk.END)
                    self.password_entry.delete(0, tk.END)
                    self.title_label.config(text="Login Player 2")
                elif len(self.logged_in_users) == 2:
                    self.master.destroy()
                    self.launch_game(self.logged_in_users[0], self.logged_in_users[1])
            else:
                self.master.destroy()
                self.launch_game(username, "AI")
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")


    def register_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        success = self.db.new_registration(username, password)
        if success:
            messagebox.showinfo("Registration Successful", "Account created successfully!")
        else:
            messagebox.showerror("Registration Failed", "Username already exists or error occurred.")

    def launch_game(self, player1, player2):
        if self.mode == MODE_PVP:
            from tictactyo import GameGUI

            game_window = tk.Tk()
            GameGUI(game_window, player1, player2)
            game_window.mainloop()
        elif self.mode == MODE_AI_MEDIUM:
            from semiautomatictictactoy import start_game

            start_game(player1)
        elif self.mode == MODE_AI_HARD:
            from fullautomatictictactoy import start_game

            start_game(player1)
        else:
            messagebox.showerror("Error", "Invalid game mode selected.")


class Data_store_class():
  def __init__(self):
      ensure_users_table()

  def new_registration(self,username,password):
      try:
        hashed = hash_password(password)
        conn=connect_db()
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        return True

      except sqlite3.IntegrityError:
         print("Username already exists")
         return False

      except Exception as E:
         print(f"Exception {E} is occurs at registration")
         return False

      finally:
         conn.close()

  def login_individual(self,username,password):
     try:
        conn=connect_db()
        c = conn.cursor()
        c.execute("SELECT id, username, password, total_games, wins, losses FROM users WHERE username = ?", (username,))
        result = c.fetchone()
        if not result:
            return None

        stored_password = result[2]
        if verify_password(password, stored_password):
            if not stored_password.startswith("pbkdf2_sha256$"):
                new_hash = hash_password(password)
                self.update_password(username, new_hash)
            return result
        return None
     except Exception as E:
        print(f"Exception {E} is occurs at login")
        return False
     finally:
        conn.close()

  def update_password(self, username, new_password_hash):
      with connect_db() as conn:
          conn.execute("UPDATE users SET password = ? WHERE username = ?", (new_password_hash, username))
          

def main(mode=MODE_PVP):
    root = tk.Tk()
    login_app = LoginRegisterGUI(root,mode)
    root.mainloop()

if __name__ == "__main__":
    main()

