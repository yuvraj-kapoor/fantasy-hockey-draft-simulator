# 🏒 Fantasy Hockey Draft Simulator

A **Python-based fantasy hockey draft simulator** that allows users to build teams under budget and roster constraints while calculating fantasy performance scores. The project simulates a real fantasy draft environment with player statistics, drafting logic, and team management mechanics.

---

## 🚀 Overview

This project models a fantasy hockey drafting system where users select players while managing:
- salary budget
- positional requirements
- fantasy point optimization

The simulator supports both:
- multiplayer drafting
- drafting against a computer opponent

The project demonstrates practical applications of:
- algorithmic decision-making
- modular programming
- data parsing
- game simulation logic

---

## ✨ Features

- Draft players under a fixed salary cap
- Support for:
  - forwards
  - defencemen
  - goalies
- Multiplayer and computer drafting modes
- Fantasy score calculations based on player stats
- Dynamic budget management
- Roster validation system
- Player availability tracking
- Interactive command-line gameplay

---

## 🧠 Key Concepts

- Modular programming
- Functions and abstraction
- File I/O
- Lists and dictionaries
- Game simulation logic
- Constraint validation
- Fantasy point algorithms

---

## 📊 Fantasy Scoring System

Player fantasy scores are calculated using:
- goals
- assists
- defensive contributions
- hits
- goalie statistics

Example scoring categories include:

- Goal points
- Assist points
- Defensive contribution points
- Hit points
- Save percentage value
- Goals against average penalties

---

## ⚙️ Game Mechanics

### 💰 Budget Management
Each general manager must draft a complete roster while staying under a salary cap.

### 🏒 Position Constraints
Teams must contain the required number of:
- forwards
- defencemen
- goalies

### 🤖 Computer Drafting
The simulator supports drafting against an automated opponent.

### 📈 Team Scoring
At the end of the draft, total fantasy scores are calculated to determine the winner.

---

## ▶️ How to Run

1. Clone the repository:

```bash
git clone https://github.com/yourusername/fantasy-hockey-draft-simulator.git
```

2. Navigate into the project directory:

```bash
cd fantasy-hockey-draft-simulator
```

3. Run the program:

```bash
python fantasy_draft.py
```

---

## 🧪 Sample Gameplay

```text
==================================================
Welcome to the UTSC Fantasy Hockey Draft!
==================================================

Please select a mode:
0 : Computer
1 : Multiplayer

Mode: 0

GM 1, it is your turn.
You have 0 fantasy points and $100 remaining.
```

---

## 📂 Project Structure

```text
├── fantasy_draft.py              # Main game loop
├── fantasy_draft_functions.py    # Fantasy scoring and helper functions
├── players.txt                   # Player dataset
├── constants.py                  # Game constants
├── README.md
```

---

## ⏱ Time Complexity

| Operation | Complexity |
|---|---|
| Player Search | O(n) |
| Draft Validation | O(n) |
| Fantasy Score Calculation | O(1) |
| Team Score Calculation | O(n) |

---

## 📌 Notes

- Built as part of a computer science programming assignment.
- Focused on algorithmic thinking and simulation design.
- Emphasizes clean modular code organization.

---

## 🔮 Future Improvements

- Smarter AI drafting strategies
- GUI implementation
- Real NHL API integration
- Online multiplayer support
- Statistical draft analysis
- Team optimization algorithms

---

## 👨‍💻 Author

**Yuvraj Kapoor**  
Computer Science Student
