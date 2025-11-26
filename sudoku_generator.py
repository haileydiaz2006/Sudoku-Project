import random
from copy import deepcopy
#https://github.com/haileydiaz2006/Sudoku-Project

class SudokuGenerator:
    def __init__(self, row_length = 9, removed_cells= 40):
        assert row_length == 9
        self.N = row_length
        self.SRN = 3
        self.removed_cells = removed_cells
        self.board = [[0 for _ in range(self.N)] for _ in range(self.N)]
        self.Solution = None

        self.fill_values()
        self.Solution = deepcopy(self.board)
        self.remove_cells()
        self.initial_board = deepcopy(self.board)

    def get_board(self):
        return deepcopy(self.board)

    def print_board(self, board = None):
        if board is None:
            board = self.board
        for r in range(self.N):
            if r % self.SRN == 0 and r!= 0:
                print("-" * (self.N * 2 + self.SRN -1))
            row_str = ""
            for c in range(self.N):
                if c % self.SRN == 0 and c != 0:
                    row_str += "| "
                val = board[r][c]
                row_str += (str(val) if val != 0 else ".") + " "
            print(row_str.rstrip())
        print()

    def valid_in_row(self, row, num):
        return num not in self.board[row]

    def valid_in_col(self, col, num):
        for r in range(self.N):
            if self.board[r][col] == num:
                return False
        return True

    def valid_in_box(self, row_start, col_start, num):
        for r in range(row_start, row_start + self.SRN):
            for c in range(col_start, col_start + self.SRN):
                if self.board[r][c] == num:
                    return False
        return True

    def is_valid(self, row, col, num):
        return (self.valid_in_row(row, num) and self.valid_in_col(col, num) and self.valid_in_box(row - row % self.SRN, col - col % self.SRN, num))


    def fill_box(self, row_start, col_start):
        nums = list(range(1, self.N + 1))
        random.shuffle(nums)
        idx = 0
        for i in range(row_start, row_start + self.SRN):
            for j in range(col_start, col_start + self.SRN):
                self.board[i][j] = nums[idx]
                idx += 1

    def fill_diagonal(self):
        for i in range(0, self.N, self.SRN):
            self.fill_box(i, i)

    def find_empty_location(self):
        for i in range(self.N):
            for j in range(self.N):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def fill_remaining(self):
        empty = self.find_empty_location()
        if not empty:
            return True
        row, col = empty

        nums = list(range(1, self.N + 1))
        random.shuffle(nums)
        for num in nums:
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining():
                    return True
                self.board[row][col] = 0
        return False

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining()

    def remove_cells(self):
        removed = 0
        N = self.N
        removed_positions = set()
        attempts = 0

        while removed < self.removed_cells and attempts < self.removed_cells * 10:
            attempts += 1
            i = random.randrange(0, N)
            j = random.randrange(0, N)
            if (i , j)  in removed_positions:
                continue
            removed_positions.add((i,j))
            self.board[i][j] = 0
            removed += 1
        if removed < self.removed_cells:
            for i in range(N):
                for j in range(N):
                    if removed >= self.removed_cells:
                        break
                    if (i, j) not in removed_positions:
                        self.board[i][j] = 0
                        removed += 1
                if removed >= self.removed_cells:
                    break

    def reset_to_original(self):
        self.board = deepcopy(self.initial_board)

    def get_solution(self):
        return deepcopy(self.Solution)

def generate_Sudoku(size = 9, removed = 40):
    gen = SudokuGenerator(row_length = size, removed_cells = removed)
    return gen.get_board(), gen.get_solution()

