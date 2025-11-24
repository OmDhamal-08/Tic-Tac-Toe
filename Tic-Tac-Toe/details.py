import tkinter as tk
from tkinter import Toplevel, Label, ttk, simpledialog

from db_utils import connect_db, db_cursor

def get_player_stats(username):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username, total_games, wins, losses FROM users WHERE username = ?", (username,))
        return cursor.fetchone()

def get_all_stats():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT username, total_games, wins, losses, 
                   CASE WHEN total_games > 0 THEN ROUND(CAST(wins AS FLOAT) / total_games, 2) ELSE 0 END AS win_rate
            FROM users ORDER BY win_rate DESC, wins DESC LIMIT 10
        """)
        return cursor.fetchall()

def show_player_stats_gui(root, username):
    data = get_player_stats(username)
    win = Toplevel(root)
    win.title("Player Stats")
    if data:
        Label(win, text=f"Username    : {data[0]}").pack()
        Label(win, text=f"Total Games : {data[1]}").pack()
        Label(win, text=f"Wins        : {data[2]}").pack()
        Label(win, text=f"Losses      : {data[3]}").pack()
    else:
        Label(win, text="No data found for this user.").pack()

def show_leaderboard_gui(root):
    from tkinter import ttk

    def load_leaderboard(sort_by):
        for row in tree.get_children():
            tree.delete(row)

        with connect_db() as conn:
            cursor = conn.cursor()
            if sort_by == "Most Wins":
                cursor.execute("""
                    SELECT username, total_games, wins, losses,
                        CASE WHEN total_games > 0 THEN ROUND(CAST(wins AS FLOAT) / total_games, 2) ELSE 0 END AS win_rate
                    FROM users
                    ORDER BY wins DESC, win_rate DESC
                    LIMIT 10
                """)
            elif sort_by == "Most Games Played":
                cursor.execute("""
                    SELECT username, total_games, wins, losses,
                        CASE WHEN total_games > 0 THEN ROUND(CAST(wins AS FLOAT) / total_games, 2) ELSE 0 END AS win_rate
                    FROM users
                    ORDER BY total_games DESC
                    LIMIT 10
                """)
            elif sort_by == "Highest Win Rate":
                cursor.execute("""
                    SELECT username, total_games, wins, losses,
                        CASE WHEN total_games > 0 THEN ROUND(CAST(wins AS FLOAT) / total_games, 2) ELSE 0 END AS win_rate
                    FROM users
                    WHERE total_games >= 5
                    ORDER BY win_rate DESC
                    LIMIT 10
                """)
            data = cursor.fetchall()

        for row in data:
            tree.insert("", "end", values=row)

    win = tk.Toplevel(root)
    win.title("Leaderboard")

    # Dropdown to select sorting criteria
    tk.Label(win, text="Sort By:", font=("Arial", 12)).pack(pady=5)
    sort_var = tk.StringVar()
    sort_box = ttk.Combobox(win, textvariable=sort_var, values=["Most Wins", "Most Games Played", "Highest Win Rate"], state="readonly")
    sort_box.pack()
    sort_box.current(0)  # Default selected

    # Table setup
    tree = ttk.Treeview(win, columns=("Username", "Games", "Wins", "Losses", "Win Rate"), show='headings')
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    tree.pack(expand=True, fill="both", pady=10)

    # Load data when a sort option is selected
    sort_box.bind("<<ComboboxSelected>>", lambda e: load_leaderboard(sort_var.get()))

    # Load default leaderboard
    load_leaderboard("Most Wins")


def prompt_and_show_player_stats(root):
    username = simpledialog.askstring("My Stats", "Enter your username:")
    if username:
        show_player_stats_gui(root, username)


def _record_outcome(cursor, username, outcome):
    if not username:
        return

    cursor.execute("UPDATE users SET total_games = total_games + 1 WHERE username = ?", (username,))
    if outcome == "win":
        cursor.execute("UPDATE users SET wins = wins + 1 WHERE username = ?", (username,))
    elif outcome == "loss":
        cursor.execute("UPDATE users SET losses = losses + 1 WHERE username = ?", (username,))


def update_match_result(player_x, player_o, winner):
    """
    Persist the outcome of a completed match.

    player_x always represents the user controlling 'X'. player_o may be None for AI modes.
    winner can be 'X', 'Y', or None for a draw.
    """
    with db_cursor() as cursor:
        if winner == "X":
            _record_outcome(cursor, player_x, "win")
            _record_outcome(cursor, player_o, "loss")
        elif winner == "Y":
            _record_outcome(cursor, player_x, "loss")
            _record_outcome(cursor, player_o, "win")
        else:
            _record_outcome(cursor, player_x, None)
            _record_outcome(cursor, player_o, None)
