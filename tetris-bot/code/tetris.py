import pygame
import random
from piece import Piece
from bot import TetrisBot

pygame.init()

# Global variables for game content dimensions etc.
WIDTH, HEIGHT = 1400, 950 # size of game window
CELL_SIZE = 40 # size of a single cell on the game board
COLS, ROWS = 10, 20 # size of game board in terms of number of cells
BOARD_W, BOARD_H = COLS * CELL_SIZE, ROWS * CELL_SIZE # overall gameboard size in pixels
BORDER_THICKNESS = 6 # pixels
X_OFFSET = WIDTH // 2 - BOARD_W // 2 # X coord for left side of the game board
Y_OFFSET = HEIGHT // 2 - BOARD_H // 2 # Y coord for top of the game board

score = 0 # variable to keep track of score
total_lines_cleared = 0 # variable to keep track of lines cleared

bot_mode = "-" # variable for displaying the bot mode

screen = pygame.display.set_mode((WIDTH, HEIGHT)) # create main game screen
pygame.display.set_caption("Tetris") # window title

# Colours - 3-tuples representing RGB value
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GREY = (30, 30, 30)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Text initializations
font_1 = pygame.font.Font(None, 72) # Box titles
font_2 = pygame.font.Font(None, 28) # Stats
font_3 = pygame.font.Font(None, 36) # Button text

# Text setup for "STATS" title
text_surface_stats = font_1.render("STATS", True, WHITE)
text_rect_stats = text_surface_stats.get_rect(center=(
    X_OFFSET + BOARD_W + BORDER_THICKNESS + CELL_SIZE + (CELL_SIZE * 5) // 2,
    120))

# Text setup for "NEXT" title
text_surface_next = font_1.render("NEXT", True, WHITE)
text_rect_next = text_surface_next.get_rect(center=(
    X_OFFSET + BOARD_W + BORDER_THICKNESS + CELL_SIZE + (CELL_SIZE * 5) // 2,
    320)) # unnecessarily complicated math to find center of the box

# Button setup for "NEXT MOVE"
button_rect = pygame.Rect(150, 150, 200, 50)  # (x, y, width, height)
button_colour = BLUE

# Text setup for "NEXT MOVE" button text
button_text = font_3.render("NEXT MOVE", True, WHITE)
text_rect_next_move = button_text.get_rect(center=button_rect.center)

# text setup quit control
text_surface_quit = font_2.render(f"Press Q to quit", True, WHITE)
text_rect_quit = text_surface_quit.get_rect(topleft=(150, 285))

# text setup restart control
text_surface_restart = font_2.render(f"Press R to reset", True, WHITE)
text_rect_restart = text_surface_restart.get_rect(topleft=(150, 315))

# draw all borders and text to the screen
# dynamic text created in this method, static text created above
def draw_borders():
    # game board box
    pygame.draw.rect(screen, WHITE, (
        X_OFFSET,
        Y_OFFSET,
        BOARD_W + BORDER_THICKNESS * 2,
        BOARD_H + BORDER_THICKNESS * 2
    ), BORDER_THICKNESS)

    # score box
    pygame.draw.rect(screen, WHITE, (
        X_OFFSET + 11 * CELL_SIZE,
        Y_OFFSET,
        CELL_SIZE * 5 + BORDER_THICKNESS *2,
        CELL_SIZE * 4 + BORDER_THICKNESS * 2
    ), BORDER_THICKNESS)

    # next piece box
    pygame.draw.rect(screen, WHITE, (
        X_OFFSET + 11 * CELL_SIZE,
        Y_OFFSET + 5 * CELL_SIZE,
        CELL_SIZE * 5 + BORDER_THICKNESS * 2,
        CELL_SIZE * 7 + BORDER_THICKNESS * 2
    ), BORDER_THICKNESS)

    # draw "STATS" text
    screen.blit(text_surface_stats, text_rect_stats)

    # text setup for current score
    text_surface_curr_score = font_2.render(f"Score: {score}", True, WHITE)
    text_rect_curr_score = text_surface_curr_score.get_rect(topleft=(960, 155))
    # draw current score text
    screen.blit(text_surface_curr_score, text_rect_curr_score)

    # text setup for total lines cleared
    text_surface_cleared_lines = font_2.render(f"Lines Cleared: {total_lines_cleared}", True, WHITE)
    text_rect_cleared_lines = text_surface_cleared_lines.get_rect(topleft=(960, 180))
    # draw current lines cleared text
    screen.blit(text_surface_cleared_lines, text_rect_cleared_lines)

    # text setup for average score per line
    text_surface_average = font_2.render(f"Average: {'-' if total_lines_cleared == 0 else score // total_lines_cleared}", True, WHITE)
    text_rect_average = text_surface_average.get_rect(topleft=(960, 205))
    # draw current average per line text
    screen.blit(text_surface_average, text_rect_average)

    # text setup for autoplay
    text_surface_autoplay = font_2.render(f"Autoplay (spacebar): {'ON' if autoplay else 'OFF'}", True, WHITE)
    text_rect_autoplay = text_surface_autoplay.get_rect(topleft=(150, 225))
    # draw current autoplay text
    screen.blit(text_surface_autoplay, text_rect_autoplay)

    # text setup for bot mode
    text_surface_bot_mode = font_2.render(f"Bot mode: {bot_mode}", True, WHITE)
    text_rect_bot_mode = text_surface_bot_mode.get_rect(topleft=(150, 255))
    # draw current mode text
    screen.blit(text_surface_bot_mode, text_rect_bot_mode)

    # draw quit text
    screen.blit(text_surface_quit, text_rect_quit)

    # draw restart text
    screen.blit(text_surface_restart, text_rect_restart)

    # draw "NEXT" text
    screen.blit(text_surface_next, text_rect_next)

    # draw "NEXT MOVE" button and text
    pygame.draw.rect(screen, button_colour, button_rect, border_radius=10)
    screen.blit(button_text, text_rect_next_move)


# draw a single cell of a piece at the specified column and row
# the extra 20 if centered shifts the block a half a cell if it needs to be centered this way
def draw_block(col, row, colour, centered=False):
    x = X_OFFSET + col * CELL_SIZE + BORDER_THICKNESS + (20 if centered else 0 ) # Convert column to x position
    y = Y_OFFSET + row * CELL_SIZE + BORDER_THICKNESS  # Convert row to y position

    pygame.draw.rect(screen, colour, (x + 1, y + 1, 38, 38))  # Draw block (28x28)

# draw an entire piece to the screen
# does not add the piece to the actual game grid matrix
# used for new piece drawn at top of board, or piece in 'next' box
# calls helper function draw_block() to draw the piece one cell at a time
# centered argument helps with centering some pieces in the 'next' box
def draw_piece(piece, centered=False):
    for row in range(len(piece.shape)):
        for col in range(len(piece.shape[row])):
            if piece.shape[row][col] == 1:
                draw_block(piece.col + col, piece.row + row, piece.colour, centered)

# draws all pieces that are saved in the game grid matrix
def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            if game_grid[row][col] != 0:
                draw_block(col, row, game_grid[row][col])

# permanently adds a piece to the game grid matrix
def lock_piece(piece):
    for row in range(len(piece.shape)):
        for col in range(len(piece.shape[row])):
            if piece.shape[row][col] == 1:
                game_grid[piece.row + row][piece.col + col] = piece.colour

# detects if there has been a collision, returns True if so, otherwise False
def is_collision(piece):
    for row in range(len(piece.shape)):
        for col in range(len(piece.shape[row])):
            if piece.shape[row][col] == 1:
                if game_grid[piece.row + row][piece.col + col] != 0:
                    return True
    return False

# checks for full rows and clears them
def clear_rows():
    global game_grid
    global score
    global total_lines_cleared

    new_grid = [row for row in game_grid if any(cell == 0 for cell in row)]  # keep non-full rows
    cleared = ROWS - len(new_grid)  # number of cleared rows
    game_grid = [[0] * COLS for _ in range(cleared)] + new_grid  # add empty rows at the top to maintain 20x10

    total_lines_cleared += cleared # track total lines cleared

    # add score based on number of lines cleared
    match cleared:
        case 1: score += 40
        case 2: score += 100
        case 3: score += 300
        case 4: score += 1200

    if cleared > 0:
        return True
    return False

# checks if a newly added piece to the top of the board causes a collision, if so game over
def check_game_over():
    for row in range(len(current_piece.shape)):
        for col in range(len(current_piece.shape[row])):
            if current_piece.shape[row][col] and game_grid[current_piece.row + row][current_piece.col + col] != 0:
                return True
    return False

# display game over screen, wait for keyboard input 'R' to restart
def show_game_over():
    font = pygame.font.Font(None, 50)
    text = font.render("GAME OVER", True, RED)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # if window is closed
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r: # if user presses 'R'
                reset_game()
                waiting = False

# reset all variables and clear the game grid, to restart the game
def reset_game():
    global game_grid, game_state, current_piece, next_piece, current_piece_letter, next_piece_letter
    global score, total_lines_cleared
    global autoplay

    game_grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    current_piece, next_piece, current_piece_letter, next_piece_letter = None, None, None, None
    score = 0
    total_lines_cleared = 0
    autoplay = False

    game_state = "generate piece"

game_grid = [[0 for _ in range(COLS)] for _ in range(ROWS)] # construct empty game grid (all 0's)
pieces = ["I", "O", "T", "L", "J", "S", "Z"] # array of piece types represented by corresponding letter

current_piece = None # the current piece the bot must move
next_piece = None # the next piece
current_piece_letter = None # letter representation of the current piece
next_piece_letter = None # letter representation of the next piece

autoplay = False
bot_delay = 500
clear_delay = 300

# initial game state, used to know which code to execute in the game loop, depending on current state
game_state = "generate piece"
running = True # variable for continually running the game loop

# function to generate the next piece
def generate_next_piece():
    global current_piece_letter, next_piece_letter, current_piece, next_piece, game_state

    # extra condition on this for start of game (no next piece yet), else the next piece becomes the current
    current_piece_letter = random.choice(pieces) if next_piece_letter is None else next_piece_letter
    next_piece_letter = random.choice(pieces)

    # use the letter to construct the piece placed at the top of the board
    match current_piece_letter:
        case "I":
            current_piece = Piece(current_piece_letter, 3, 0)
        case "O":
            current_piece = Piece(current_piece_letter, 4, 0)
        case _:
            current_piece = Piece(current_piece_letter, 4, 0)

    # use the randomly chosen letter to construct and place the next piece in the 'next' box
    match next_piece_letter:
        case "I":
            next_piece = Piece(next_piece_letter, 11, 8)
        case "O":
            next_piece = Piece(next_piece_letter, 12, 8)
        case _:
            next_piece = Piece(next_piece_letter, 12, 8)

    game_state = "new piece" # switch to next game state

# main game loop - this runs for every frame (which is why the game_state variable is needed
while running:
    screen.fill(DARK_GREY) # draw the main screen
    draw_borders() # draw all the borders and text

    # event loop (cycles through all detected events such as button clicks and keyboard presses)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # user closed the window
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN: # user pressed the mouse button
            # if button pressed over the 'next move' button, and autoplay is off, generate next piece
            # also checks state so other states aren't interrupted
            if not autoplay and button_rect.collidepoint(event.pos) and game_state == "generate piece":
                generate_next_piece()
        elif event.type == pygame.KEYDOWN: # keyboard key pressed
            if event.key == pygame.K_q: # if q is pressed, stop running - quit game
                running = False
            elif event.key == pygame.K_r: # if r is pressed, reset game
                reset_game()
            elif event.key == pygame.K_SPACE: # if spacebar is pressed, toggle autoplay
                autoplay = not autoplay

    # will continually generate new pieces if autoplay is on (after the cycle of states for a full move runs)
    if autoplay and game_state == "generate piece":
        generate_next_piece()

    # for some states, there isn't a next piece yet so the box needs to be empty
    if next_piece:
        draw_piece(next_piece, True if next_piece_letter in ["I", "O"] else False)

    # draws new piece at the top of the game board then advances the state
    if game_state == "new piece":
        draw_piece(current_piece)
        game_state = "check new piece collision"

    # checks for collision now that the new piece entered the board, if so calls game over,
    # else keep drawing the piece and advance the game state
    elif game_state == "check new piece collision":
        if is_collision(current_piece):
            show_game_over()
            continue
        draw_piece(current_piece)
        game_state = "place piece"

    # get the move and the mode used from the bot
    # lock the move to the board, displaying game over if collision
    # else set current_piece to None
    # add artificial delay
    # advance game state
    elif game_state == "place piece":
        bot = TetrisBot()
        chosen_move, mode = bot.move(game_grid, current_piece, next_piece)
        bot_mode = mode
        if lock_piece(chosen_move):
            show_game_over()
            continue
        current_piece = None
        pygame.time.delay(bot_delay)
        game_state = "clear rows"

    # check board with newly placed piece for rows cleared, and clear them
    # reset to initial state
    elif game_state == "clear rows":
        if clear_rows():
            pygame.time.delay(clear_delay)
        game_state = "generate piece"

    draw_grid() # always show the grid no matter which state
    pygame.display.flip() # draw the frame

pygame.quit()