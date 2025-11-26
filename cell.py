import pygame

class Cell:
    def __init__(self, value, row, col, size):
        self.value = value
        self.sketched_value = 0
        self.original_value = value
        self.row = row
        self.col = col
        self.size = size
        self.selected = False
        self.cell_size = 60

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self, surface):
        x = self.col * self.size
        y = self.row * self.size
        font = pygame.font.Font(None, 40)

        if self.value != 0:
            text = font.render(str(self.value), True, (0, 0, 0))
            surface.blit(text, (x + self.size // 3, y + self.size // 4))
        elif self.sketched_value != 0:
            small_font = pygame.font.Font(None, 20)
            text= small_font.render(str(self.sketched_value), True, (150, 150, 150))
            surface.blit(text, (x + 5 , y + 5))

        if self.selected:
            pygame.draw.rect(surface, (255, 0, 0), (x, y, self.size, self.size), 3)



