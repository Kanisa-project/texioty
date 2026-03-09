import os
import sys
import random
import string

def place_word(board, word):
    orientation = random.randint(0, 3)
    placed = False
    while not placed:
        if orientation == 0:
            row = random.randint(0, len(board) - 1)
            col = random.randint(0, len(board) - len(word))
            reverse = random.choice([True, False])
            if reverse:
                word = word[::-1]
            space_available = all(board[row][c] == '-' or board[row][c] == word[i] for i, c in enumerate(range(col, col + len(word))))
            if space_available:
                for i, c in enumerate(range(col, col + len(word))):
                    board[row][c] = word[i]
                placed = True
        elif orientation == 1:
            row = random.randint(0, len(board) - len(word))
            col = random.randint(0, len(board) - 1)
            reverse = random.choice([True, False])
            if reverse:
                word = word[::-1]
            space_available = all(board[r][col] == '-' or board[r][col] == word[i] for i, r in enumerate(range(row, row + len(word))))
            if space_available:
                for i, r in enumerate(range(row, row + len(word))):
                    board[r][col] = word[i]
                placed = True
        elif orientation == 2:
            row = random.randint(0, len(board) - len(word))
            col = random.randint(0, len(board) - len(word))
            reverse = random.choice([True, False])
            if reverse:
                word = word[::-1]
            space_available = all(board[r][c] == '-' or board[r][c] == word[i] for i, (r, c) in enumerate(zip(range(row, row + len(word)), range(col, col + len(word)))))
            if space_available:
                for i, (r, c) in enumerate(zip(range(row, row + len(word)), range(col, col + len(word)))):
                    board[r][c] = word[i]
                placed = True
        elif orientation == 3:
            row = random.randint(len(word) - 1, len(board) - 1)
            col = random.randint(0, len(board) - len(word))
            reverse = random.choice([True, False])
            if reverse:
                word = word[::-1]
            space_available = all(board[r][c] == '-' or board[r][c] == word[i] for i, (r, c) in enumerate(zip(range(row, row - len(word), -1), range(col, col + len(word)))))
            if space_available:
                for i, (r, c) in enumerate(zip(range(row, row - len(word), -1), range(col, col + len(word)))):
                    board[r][c] = word[i]
                placed = True

def fill_empty_spaces(board):
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == '-':
                board[row][col] = random.choice(string.ascii_lowercase)

def create_wordsearch(wordset, size=10) -> list:
    board = [['-' for _ in range(size)] for _ in range(size)]
    for word in wordset:
        place_word(board, word)
    fill_empty_spaces(board)
    return board
