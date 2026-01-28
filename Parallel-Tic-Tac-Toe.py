import multiprocessing
import random

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_winner(board, player):
    # Check rows, columns, and diagonals
    for i in range(3):
        if all(cell == player for cell in board[i]) or all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def evaluate_move(board, move, player):
    new_board = [row.copy() for row in board]
    new_board[move[0]][move[1]] = player
    return new_board

def minimax(board, depth, maximizing_player):
    if check_winner(board, "O"):
        return -1
    elif check_winner(board, "X"):
        return 1
    elif all(all(cell != " " for cell in row) for row in board):
        return 0

    if maximizing_player:
        max_eval = float("-inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    new_board = evaluate_move(board, (i, j), "X")
                    eval = minimax(new_board, depth + 1, False)
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    new_board = evaluate_move(board, (i, j), "O")
                    eval = minimax(new_board, depth + 1, True)
                    min_eval = min(min_eval, eval)
        return min_eval

def evaluate_move_parallel(args):
    board, move = args
    new_board = evaluate_move(board, move, "X")
    return minimax(new_board, 0, False)

def find_best_move(board):
    moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    
    if not moves:
        return None

    pool = multiprocessing.Pool()
    results = pool.map(evaluate_move_parallel, [(board, move) for move in moves])
    pool.close()
    pool.join()

    best_move = moves[results.index(max(results))]
    return best_move

def play_game():
    board = [[" " for _ in range(3)] for _ in range(3)]
    print_board(board)

    while True:
        # Player move
        row = int(input("Enter row (0, 1, or 2): "))
        col = int(input("Enter column (0, 1, or 2): "))
        if board[row][col] == " ":
            board[row][col] = "O"
        else:
            print("Cell already occupied. Try again.")
            continue

        print_board(board)

        if check_winner(board, "O"):
            print("You win!")
            break
        elif all(all(cell != " " for cell in row) for row in board):
            print("It's a tie!")
            break

        # Computer move
        print("Computer is thinking...")
        best_move = find_best_move(board)
        if best_move:
            board[best_move[0]][best_move[1]] = "X"

        print_board(board)

        if check_winner(board, "X"):
            print("Computer wins!")
            break
        elif all(all(cell != " " for cell in row) for row in board):
            print("It's a tie!")
            break

if __name__ == "__main__":
    play_game()



'''
#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
#include <omp.h>

void printBoard(const std::vector<std::vector<char>>& board) {
    for (const auto& row : board) {
        for (char cell : row) {
            std::cout << cell << " | ";
        }
        std::cout << "\n---------\n";
    }
}

bool checkWinner(const std::vector<std::vector<char>>& board, char player) {
    // Check rows, columns, and diagonals
    for (int i = 0; i < 3; ++i) {
        if (std::all_of(board[i].begin(), board[i].end(), [player](char cell) { return cell == player; }) ||
            std::all_of(board.begin(), board.end(), [i, player](const std::vector<char>& row) { return row[i] == player; }))
            return true;
    }

    return (board[0][0] == player && board[1][1] == player && board[2][2] == player) ||
           (board[0][2] == player && board[1][1] == player && board[2][0] == player);
}

std::vector<std::vector<char>> evaluateMove(const std::vector<std::vector<char>>& board, std::pair<int, int> move, char player) {
    auto newBoard = board;
    newBoard[move.first][move.second] = player;
    return newBoard;
}

int minimax(const std::vector<std::vector<char>>& board, int depth, bool maximizingPlayer) {
    char player = maximizingPlayer ? 'X' : 'O';

    if (checkWinner(board, 'O'))
        return -1;
    else if (checkWinner(board, 'X'))
        return 1;
    else if (std::all_of(board.begin(), board.end(), [](const std::vector<char>& row) {
        return std::all_of(row.begin(), row.end(), [](char cell) { return cell != ' '; });
    }))
        return 0;

    int bestVal = maximizingPlayer ? INT_MIN : INT_MAX;

    #pragma omp parallel for collapse(2) shared(board, maximizingPlayer) reduction(max:bestVal)
    for (int i = 0; i < 3; ++i) {
        for (int j = 0; j < 3; ++j) {
            if (board[i][j] == ' ') {
                auto newBoard = evaluateMove(board, {i, j}, player);
                int val = minimax(newBoard, depth + 1, !maximizingPlayer);

                if (maximizingPlayer)
                    bestVal = std::max(bestVal, val);
                else
                    bestVal = std::min(bestVal, val);
            }
        }
    }

    return bestVal;
}

std::pair<int, int> findBestMove(const std::vector<std::vector<char>>& board) {
    char player = 'X';
    int bestVal = INT_MIN;
    std::pair<int, int> bestMove;

    std::vector<std::pair<int, int>> moves;

    for (int i = 0; i < 3; ++i)
        for (int j = 0; j < 3; ++j)
            if (board[i][j] == ' ')
                moves.emplace_back(i, j);

    std::random_shuffle(moves.begin(), moves.end());

    #pragma omp parallel for shared(board, player, bestVal) schedule(static) collapse(2)
    for (size_t k = 0; k < moves.size(); ++k) {
        int i = moves[k].first;
        int j = moves[k].second;

        auto newBoard = evaluateMove(board, {i, j}, player);
        int moveVal = minimax(newBoard, 0, false);

        #pragma omp critical
        {
            if (moveVal > bestVal) {
                bestMove = {i, j};
                bestVal = moveVal;
            }
        }
    }

    return bestMove;
}

bool isBoardFull(const std::vector<std::vector<char>>& board) {
    return std::all_of(board.begin(), board.end(), [](const std::vector<char>& row) {
        return std::all_of(row.begin(), row.end(), [](char cell) { return cell != ' '; });
    });
}

void playGame() {
    std::vector<std::vector<char>> board(3, std::vector<char>(3, ' '));
    printBoard(board);

    while (true) {
        // Player move
        int row, col;
        std::cout << "Enter row (0, 1, or 2): ";
        std::cin >> row;
        std::cout << "Enter column (0, 1, or 2): ";
        std::cin >> col;

        if (row >= 0 && row < 3 && col >= 0 && col < 3 && board[row][col] == ' ') {
            board[row][col] = 'O';
        } else {
            std::cout << "Invalid move. Try again.\n";
            continue;
        }

        printBoard(board);

        if (checkWinner(board, 'O')) {
            std::cout << "You win!\n";
            break;
        } else if (isBoardFull(board)) {
            std::cout << "It's a tie!\n";
            break;
        }

        // Computer move
        std::cout << "Computer is thinking...\n";
        auto bestMove = findBestMove(board);
        board[bestMove.first][bestMove.second] = 'X';

        printBoard(board);

        if (checkWinner(board, 'X')) {
            std::cout << "Computer wins!\n";
            break;
        } else if (isBoardFull(board)) {
            std::cout << "It's a tie!\n";
            break;
        }
    }
}

int main() {
    playGame();
    return 0;
}

'''