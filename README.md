# Tic-Tac-Toe
A desktop Tic-Tac-Toe game written in Python using Tkinter for the GUI and SQLite for user/login and leaderboard storage. Supports 3 game modes: Player vs Player, Player vs Simple AI, and Player vs Hard AI. Includes login/registration, player statistics (wins/losses), and a leaderboard. Player scores are updated only in Player vs Player mode
🎮 Tic-Tac-Toe Game with AI and Multiplayer Modes
A feature-rich Tic-Tac-Toe game built in Python with a GUI using Tkinter. Supports multiplayer mode, AI opponents of varying difficulties, player statistics, and a leaderboard system powered by SQLite.

✨ Features
🔀 Three Game Modes:

Player vs Player (PvP) – Two users take turns and their stats are saved.
Player vs AI (Medium) – Random-move AI for casual players.
Player vs AI (Hard) – Strategic AI using classic game logic.
🔐 User Registration and Login System

📊 Player Statistics (wins, losses, total games)

🏆 Leaderboard with sorting/filtering

🖥️ Graphical User Interface (GUI) using Tkinter

💾 Persistent Data with SQLite Database

🛠 Technologies Used
Python 3
Tkinter (for GUI)
SQLite (for data storage)
NumPy (for game logic and AI)
Pandas (optional for data handling)
🚀 Installation & Setup
1. Clone the Repository
git clone https://github.com/yourusername/tic-tac-toe.git
cd tic-tac-toe
2. Install Dependencies
pip install numpy
pip install pandas
✅ Note: SQLite is built-in with Python, so no need to install separately.

3. Run the Game
python Main.py
🎮 Game Modes Explained
👫 Player vs Player (PvP)
Requires two users to log in.
Takes alternate turns on the board.
Tracks stats for both players.
🤖 Player vs AI (Medium)
Computer opponent plays randomly.
Good for practice or beginners.
🧠 Player vs AI (Hard)
AI follows a strategy:
Wins if possible
Blocks opponent's win
Takes center if free
Prefers corners
Takes any available space
🗄️ Database Schema
The game uses SQLite to store user data:

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    total_games INTEGER DEFAULT 0,
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0
);
🧭 Project Structure
tic-tac-toe/
├── Main.py                   # Entry point and game mode selector
├── database.py               # Handles database and user auth
├── details.py                # Statistics and leaderboard
├── fullautomatictictactoy.py # Hard AI logic
├── semiautomatictictactoy.py # Medium AI logic
├── tictactyo.py              # PvP game logic
└── README.md                 # This file
📸 Screenshots (To Add)
✅ Main Menu
✅ Login Screen
✅ PvP Gameplay
✅ AI Gameplay
✅ Statistics View
✅ Leaderboard
Screenshots can help users understand the app better. Add image links or markdown image embeds here.

🌱 Future Enhancements
Add difficulty levels between Medium and Hard
Implement Tournament Mode
Add Sound Effects and Animations
Build a Web-Based Version using Django + React
🧑‍💻 Contributing
Contributions, issues, and feature requests are welcome!
Feel free to fork the project and submit a pull request.

📜 License
This project is licensed under the MIT License – free to use and modify.

📬 Contact
Created by Om Dhamal
If you liked this project, give it a ⭐ on GitHub!
