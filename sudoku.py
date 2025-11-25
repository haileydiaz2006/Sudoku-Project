import pygame, sys
from board import Board
from sudoku_generator import generate_Sudoku

# 1. Initialize Pygame
pygame.init()

# 2. Constants and Screen Setup
WIDTH = 600
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)

# Fonts
title_font = pygame.font.Font(None, 60)
button_font = pygame.font.Font(None, 40)
text_font = pygame.font.Font(None, 30)

# 3. Global Variables
game_state = "start"  # options: "start", "play", "win", "lose"
board = None  # Will act as the Board object
difficulty = 0  # 30, 40, or 50


# --- Helper Function to Draw Text ---
def draw_text(surface, text, font, color, center_x, center_y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(center_x, center_y))
    surface.blit(text_surface, text_rect)


# 4. Main Game Loop
while True:

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # Handle Mouse Clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if game_state == "start":
                # Check Easy Button (x=50, y=400, w=150, h=60)
                if 50 <= x <= 200 and 400 <= y <= 460:
                    difficulty = 30
                    game_state = "play"
                # Check Medium Button (x=225, y=400)
                elif 225 <= x <= 375 and 400 <= y <= 460:
                    difficulty = 40
                    game_state = "play"
                # Check Hard Button (x=400, y=400)
                elif 400 <= x <= 550 and 400 <= y <= 460:
                    difficulty = 50
                    game_state = "play"

                # If a button was clicked, Generate the Board
                if game_state == "play":
                    # generate_Sudoku returns (board_data, solution)
                    # We only need the board_data for the Board class
                    board_data, solution = generate_Sudoku(9, difficulty)

                    # Create the Board object (540x540 pixels to fit nicely)
                    board = Board(540, 540, screen, difficulty, board_data)

            elif game_state == "play":
                # Check Reset Button (Bottom Left)
                if 50 <= x <= 200 and 600 <= y <= 650:
                    board.reset_to_original()

                # Check Restart Button (Bottom Middle)
                elif 225 <= x <= 375 and 600 <= y <= 650:
                    game_state = "start"

                # Check Exit Button (Bottom Right)
                elif 400 <= x <= 550 and 600 <= y <= 650:
                    sys.exit()

                # Check Board Click (if y is within the board area)
                elif y < 540:
                    clicked_pos = board.click(x, y)
                    if clicked_pos:
                        board.select(clicked_pos[0], clicked_pos[1])

            elif game_state == "win" or game_state == "lose":
                # Restart Button logic for end screens
                if 225 <= x <= 375 and 400 <= y <= 460:
                    game_state = "start"

        # Handle Keyboard Input (Only when playing)
        if event.type == pygame.KEYDOWN and game_state == "play":
            if board.selected:
                row, col = board.selected

                # Number keys 1-9 to sketch
                if event.key == pygame.K_1: board.sketch(1)
                if event.key == pygame.K_2: board.sketch(2)
                if event.key == pygame.K_3: board.sketch(3)
                if event.key == pygame.K_4: board.sketch(4)
                if event.key == pygame.K_5: board.sketch(5)
                if event.key == pygame.K_6: board.sketch(6)
                if event.key == pygame.K_7: board.sketch(7)
                if event.key == pygame.K_8: board.sketch(8)
                if event.key == pygame.K_9: board.sketch(9)

                # Arrow keys to move selection
                if event.key == pygame.K_LEFT and col > 0:
                    board.select(row, col - 1)
                if event.key == pygame.K_RIGHT and col < 8:
                    board.select(row, col + 1)
                if event.key == pygame.K_UP and row > 0:
                    board.select(row - 1, col)
                if event.key == pygame.K_DOWN and row < 8:
                    board.select(row + 1, col)

                # Delete/Backspace to clear
                if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    board.clear()

                # Enter key to submit the sketch
                if event.key == pygame.K_RETURN:
                    # We need to get the sketched value from the specific cell
                    cell = board.cells[row][col]
                    if cell.sketched_value != 0:
                        board.place_number(cell.sketched_value)

                        # After placing, check if game is over
                        if board.is_full():
                            if board.check_board():
                                game_state = "win"
                            else:
                                game_state = "lose"

    # --- Drawing Logic ---
    screen.fill(WHITE)  # Always clear screen first

    if game_state == "start":
        # Draw Title
        draw_text(screen, "Welcome to Sudoku", title_font, BLACK, WIDTH // 2, 200)

        # Draw Buttons
        pygame.draw.rect(screen, ORANGE, (50, 400, 150, 60))  # Easy
        draw_text(screen, "Easy", button_font, BLACK, 125, 430)

        pygame.draw.rect(screen, ORANGE, (225, 400, 150, 60))  # Medium
        draw_text(screen, "Medium", button_font, BLACK, 300, 430)

        pygame.draw.rect(screen, ORANGE, (400, 400, 150, 60))  # Hard
        draw_text(screen, "Hard", button_font, BLACK, 475, 430)

    elif game_state == "play":
        # Draw the Board
        board.draw()

        # Draw Buttons below the board
        pygame.draw.rect(screen, ORANGE, (50, 600, 150, 50))  # Reset
        draw_text(screen, "Reset", button_font, BLACK, 125, 625)

        pygame.draw.rect(screen, ORANGE, (225, 600, 150, 50))  # Restart
        draw_text(screen, "Restart", button_font, BLACK, 300, 625)

        pygame.draw.rect(screen, ORANGE, (400, 600, 150, 50))  # Exit
        draw_text(screen, "Exit", button_font, BLACK, 475, 625)

    elif game_state == "win":
        draw_text(screen, "Game Won!", title_font, BLACK, WIDTH // 2, 200)

        # Draw Restart Button
        pygame.draw.rect(screen, ORANGE, (225, 400, 150, 60))
        draw_text(screen, "Restart", button_font, BLACK, 300, 430)

    elif game_state == "lose":
        draw_text(screen, "Game Over :(", title_font, BLACK, WIDTH // 2, 200)

        # Draw Restart Button
        pygame.draw.rect(screen, ORANGE, (225, 400, 150, 60))
        draw_text(screen, "Restart", button_font, BLACK, 300, 430)

    # 5. Update Display
    pygame.display.update()