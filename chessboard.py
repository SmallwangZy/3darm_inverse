import tkinter as tk
from tkinter import messagebox
import keyboard

# 初始化游戏板
board = [[' ' for _ in range(3)] for _ in range(3)]

# 定义玩家和电脑的棋子
player_piece = 'X'
computer_piece = 'O'

# 定义方向键对应的移动
directions = {
    'up': (-1, 0),
    'down': (1, 0),
    'left': (0, -1),
    'right': (0, 1)
}

# 电脑随机选择一个空位置下棋
def computer_move(board):
    empty_positions = np.argwhere(board == 0)
    if len(empty_positions) > 0:
        return empty_positions[np.random.choice(len(empty_positions))]
    return None

# 检查是否有玩家或电脑获胜
def check_winner(board, piece):
    # 检查行
    for row in board:
        if all(x == piece for x in row):
            return True
    # 检查列
    for col in range(3):
        if all(board[row][col] == piece for row in range(3)):
            return True
    # 检查对角线
    if all(board[i][i] == piece for i in range(3)) or all(board[i][2-i] == piece for i in range(3)):
        return True
    return False

# 游戏主循环
def game_loop():
    current_player = player_piece
    while True:
        print_board()
        if current_player == player_piece:
            # 玩家移动
            move = keyboard.read_key()
            if move in directions:
                row, col = np.argwhere(board == current_player)[0]
                row += directions[move][0]
                col += directions[move][1]
                if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == ' ':
                    board[row][col] = current_player
                    if check_winner(board, current_player):
                        messagebox.showinfo("游戏结束", "玩家获胜！")
                        break
                    current_player = computer_piece
                else:
                    print("无效移动，请重新输入。")
            else:
                print("无效输入，请输入上/下/左/右。")
        else:
            # 电脑移动
            row, col = computer_move(board)
            if row is not None:
                board[row][col] = computer_piece
                if check_winner(board, computer_piece):
                    messagebox.showinfo("游戏结束", "电脑获胜！")
                    break
                current_player = player_piece
            else:
                print("电脑无法移动，游戏结束。")
                break

# 打印游戏板
def print_board():
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

# 开始游戏
game_loop()
