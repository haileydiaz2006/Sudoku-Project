
from cell import Cell
import pygame

class Board:
    def __init__(self, width, height, screen, difficulty, board_data):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.board_data = board_data
        self.rows = 9
        self.cols = 9
        self.cell_size = width // 9
        self.selected = None
        self.model = None
        self.cells = self.cells = [[Cell(board_data[r][c], r, c, self.cell_size)
                       for c in range(self.cols)] for r in range(self.rows)]
        self.update_board()

    def draw(self):
        self.screen.fill((255, 255, 255))
        for i in range(self.rows+1):
            if i % 3 == 0:
                thickness = 4
            else:
                thickness = 1
            pygame.draw.line(self.screen, (0,0,0), (0, i * self.cell_size),(self.width, i * self.cell_size), thickness)
            pygame.draw.line(self.screen, (0, 0, 0), ( i * self.cell_size, 0), (i * self.cell_size, self.height), thickness)

            for row in self.cells:
                for cell in row:
                    cell.draw(self.screen)

    def select(self, row, col):
        for r in range(self.rows):
            for c in range(self.cols):
                self.cells[r][c].selected = False

        self.cells[row][col].selected = True
        self.selected = (row, col)

    def click(self, x, y):
        if x < 0 or x > self.width or y < 0 or y > self.height:
            return None
        row = y // self.cell_size
        col = x // self.cell_size
        return (int(row), int(col))

    def clear(self):
        if self.selected:
            r, c = self.selected
            cell = self.cells[r][c]

            if cell.original_value == 0:
                cell.value = 0
                cell.sketched_value = 0
                self.update_board()

    def sketch(self, value):
        if self.selected:
            r, c = self.selected
            cell = self.cells[r][c]

            if cell.original_value ==0:
                cell.sketched_value = value

    def place_number(self, value):
        if self.selected:
            r, c = self.selected
            cell = self.cells[r][c]

            if cell.original_value ==0:
                cell.value = value
                cell.sketched_value = 0
                self.update_board()

    def reset_to_original(self):
        for row in self.cells:
            for cell in row:
                cell.value = cell.original_value
                cell.sketched_value = 0
        self.update_board()

    def is_full(self):
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def update_board(self):
        self.model = [[self.cells[r][c].value for c in range(9)] for r in range(9)]

    def find_empty(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.cells[r][c].value == 0:
                    return(r, c)
        return None

    def check_board(self):
        self.update_board()

        for row in self.model:
            if sorted(row) != list(range(1, 10)):
                return False

        for c in range(9):
            col = [self.model[r][c]for r in range(9)]
            if sorted(col) != list(range(1, 10)):
                return False

        for box_row in range(3):
            for box_col in range(3):
                block = []
                for r in range(box_row * 3, box_row * 3 + 3):
                    for c in range(box_col * 3, box_col * 3 + 3):
                        block.append(self.model[r][c])
                if sorted(block) != list(range(1, 10)):
                    return False
        return True
