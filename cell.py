import pygame

class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.sketched_value = 0
        self.row = row
        self.col = col
        self.screen = screen
        self.selected = False
        self.cell_size = 60

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        x = self.col * self.cell_size
        y = self.row * self.cell_size
        if self.selected:
            outline_color = (255, 0, 0)
            outline_width = 3
        else:
            outline_color = (0, 0, 0)
            outline_width = 1

        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, self.cell_size, self.cell_size))
        pygame.draw.rect(self.screen, outline_color, (x, y, self.cell_size, self.cell_size), outline_width)

        value_font = pygame.font.SysFont("arial", 36)
        value_font = pygame.font.SysFont("arial", 20)

        if self.value != 0:
            text = value_font.render(str(self.value), True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
            self.screen.blit(text, text_rect)

        elif self.sketched_value != 0:
            sketch = sketch_font.render(str(self.sketched_value), True, (128, 128, 128))
            self.screen.blit(sketch, (x + 5, y + 5))



