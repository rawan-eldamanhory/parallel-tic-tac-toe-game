# Parallel Tic-Tac-Toe Game (Python)

This project implements a **Tic-Tac-Toe game with an AI opponent** using the **Minimax algorithm** and **parallel computation** to evaluate the best moves.

The AI evaluates all possible game states and always plays optimally.

---

## ✨ Features
- Minimax algorithm
- Parallel move evaluation using multiprocessing
- Human vs Computer gameplay
- Unbeatable AI
- Educational implementation of game theory

---

## 🧠 How the AI Works
1. Generates all possible legal moves.
2. Evaluates each move using Minimax.
3. Uses **parallel processing** to speed up evaluation.
4. Selects the optimal move.

---

## ▶️ Example Gameplay

Enter row (0, 1, or 2): 1

Enter column (0, 1, or 2): 1

Computer is thinking...

---

## 🚀 How to Run
```bash
python Parallel-Tic-Tac-Toe.py
```

## ⚠️ Performance Notes

Parallelism is mainly for educational purposes.

Due to the small board size (3×3), multiprocessing overhead outweighs speed benefits.

This design demonstrates how AI search problems scale.

## 📚 Concepts Covered

Game Theory

Minimax Algorithm

Parallel Computing

Decision Trees

Artificial Intelligence Basics
