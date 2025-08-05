import random
import copy
from piece import Piece

class TetrisBot:
    def __init__(self):
        self.score = 0
        self.marked = [[0 for _ in range(10)] for _ in range(20)] # used for recursive pathing function to mark already checked paths
        self.valid_moves = [] # valid moves for current piece
        self.valid_next_moves = [] # valid moves for next piece (reset for each current piece valid move)
        self.mode = "Scoring" # bot play style mode

        # Weights - defaulted for Scoring mode
        self.weight_holes = 50
        self.weight_evenness = 1
        self.weight_board_fill = 1
        self.weight_lines_cleared_1 = -100
        self.weight_lines_cleared_2 = -80
        self.weight_lines_cleared_3 = -50
        self.weight_lines_cleared_4 = 10000
        self.weight_last_col = 1000 # scoring mode

    # main function to facilitate choosing a move
    def move(self, grid, piece, next_piece):
        piece_copy = copy.deepcopy(piece) # make copy to alter
        next_copy = copy.deepcopy(next_piece)

        # need to change next_copy position so it's at top of the board instead of in the NEXT box
        match next_copy.type:
            case "I":
                next_copy.col = 3
                next_copy.row = 0
            case "O":
                next_copy.col = 4
                next_copy.row = 0
            case _:
                next_copy.col = 4
                next_copy.row = 0

        ### SET WEIGHTS BASED ON MODE
        # if any column is higher than 12 blocks, switch to recovery mode; adjust weights accordingly
        evenness, heights = self.check_board_evenness(grid)
        for height in heights:
            if height > 12:
                self.weight_last_col = 0
                self.weight_lines_cleared_1 = 100
                self.weight_lines_cleared_2 = 400
                self.weight_lines_cleared_3 = 900
                self.mode = "Recovery"

        ### FIND ALL VALID MOVES AND STORE THEM ###
        self.find_valid_moves_setup(grid, piece_copy, False)
        self.marked = [[0 for _ in range(10)] for _ in range(20)] # reset marked matrix

        ### CALCULATE MOVE ###
        best_move = None # variable to store best move so far
        best_score = -100000000 # starting with a very low number (essentially negative infinity)

        # for each valid move (current piece)
        for move in self.valid_moves:
            # lock move in grid copy
            grid_copy = copy.deepcopy(grid)
            self.lock_piece(grid_copy, move)

            # find valid moves for next_piece
            self.find_valid_moves_setup(grid_copy, next_copy, True)
            self.marked = [[0 for _ in range(10)] for _ in range(20)] # reset marked again

            # for next_move in valid_next_moves
            # evaluate the board with both pieces placed
            for next_move in self.valid_next_moves:
                score = self.evaluate_board(grid_copy, next_move)
                if score > best_score:
                    best_score = score
                    best_move = copy.deepcopy(move)

            self.valid_next_moves.clear()

        # RANDOM MOVE -
        # random_move = random.choice(self.valid_moves)
        # piece_copy.row = random_move[0]
        # piece_copy.col = random_move[1]
        # piece_copy.set_orientation(random_move[2])
        # self.evaluate_board(grid, None)

        # return final choice (or the original piece if there wasn't any valid moves)
        # also returning mode used for displaying purposes
        return (best_move or piece), self.mode

    # check for collision
    def is_collision(self, row, col, grid, piece):
        # ensure the current row and col is within bounds (top left corner of piece 'box')
        if not (0 <= row <= 19 and 0 <= col <= 9):
            return True

        # ensure the rest of the piece is within bounds
        if row + len(piece.shape) > 20 or col + len(piece.shape[0]) > 10:
            return True

        # if a block of the piece and the grid (in that position) both have a value -> collision
        for i in range(len(piece.shape)):
            for j in range(len(piece.shape[i])):
                if piece.shape[i][j] == 1:
                    if grid[row + i][col + j] != 0:
                        return True
        return False

    # initial setup for facilitating finding all valid moves
    # handles all rotations efficiently (some pieces need 0 or 1 rotations only)
    def find_valid_moves_setup(self, grid, piece, next):
        match piece.type:
            case "I": # "I" piece only needs to rotate once
                self.find_valid_moves(piece.row, piece.col, grid, piece, next)
                self.marked = [[0 for _ in range(10)] for _ in range(20)]
                piece.rotate()
                self.find_valid_moves(piece.row, piece.col, grid, piece, next)
            case "O": # "O" piece doesn't need to rotate
                self.find_valid_moves(piece.row, piece.col, grid, piece, next)
            case _: # All other pieces have 4 rotations
                self.find_valid_moves(piece.row, piece.col, grid, piece, next)
                self.marked = [[0 for _ in range(10)] for _ in range(20)]
                for i in range(3):
                    piece.rotate()
                    self.find_valid_moves(piece.row, piece.col, grid, piece, next)
                    self.marked = [[0 for _ in range(10)] for _ in range(20)]

    # recursive function to find all valid moves
    # moves the piece recursively in 3 directions (down, right, left)
    # bounds checking and repetitive work checking to be efficient
    def find_valid_moves(self, row, col, grid, piece, next):
        if not (0 <= row <= 19 and 0 <= col <= 9):
            return

        if self.marked[row][col]: # if this location on the board already checked, return
            return

        self.marked[row][col] = 1 # mark this location as checked

        # check if we can move down, if not, then we've gone down as far as we can -> valid move
        # if yes, move down
        if self.is_collision(row + 1, col, grid, piece):
            if next:
                self.valid_next_moves.append(Piece(piece.type, col, row, piece.orientation))
            else:
                self.valid_moves.append(Piece(piece.type, col, row, piece.orientation))
        else:
            self.find_valid_moves(row + 1, col, grid, piece, next)

        # check if we can move right, if not, end this branch
        # if yes, move right
        if self.is_collision(row, col + 1, grid, piece):
            return
        else:
            self.find_valid_moves(row, col + 1, grid, piece, next)

        # check if we can move left, if not, end this branch
        # if yes, move left
        if self.is_collision(row, col - 1, grid, piece):
            return
        else:
            self.find_valid_moves(row, col - 1, grid, piece, next)

    # main function to facilitate calculating a score for the piece placements
    def evaluate_board(self, grid, move):
        # place move (make new temporary board)
        grid_copy = copy.deepcopy(grid)
        self.lock_piece(grid_copy, move)

        # check lines cleared and update the grid with the removed lines
        lines_cleared, grid_copy = self.check_lines_cleared(grid_copy)

        # check number of holes
        holes = self.check_num_holes(grid_copy)

        # check board evenness (and get array of heights to use below)
        evenness, heights = self.check_board_evenness(grid_copy)

        # check board fill
        board_fill = sum(heights)

        # check danger zone
        danger = False
        for i in [3, 4, 5, 6]:
            if heights[i] >= 16:
                danger = True

        # check if blocks in last column
        last_col_block_count = self.check_last_col(grid_copy)

        # return score
        score = self.calculate_score(holes, evenness, board_fill, danger, lines_cleared, last_col_block_count)

        return score

    def check_num_holes(self, grid):
        # boolean array to keep track if we've seen a block yet for each column
        # any 0 in the grid under a block is considered a hole
        block_seen = [False] * 10
        hole_count = 0 # lower is better

        for row in grid:
            for j, col in enumerate(row):
                if block_seen[j]:
                    if row[j] == 0:
                        hole_count += 1
                else:
                    if row[j] != 0:
                        block_seen[j] = True

        return hole_count

    # Function to check how bumpy the board is
    # Returns additional useful information that is calculated here anyway
    def check_board_evenness(self, grid):
        heights = [0] * 10
        evenness_score = 0 # lower is better

        # calculate height of each column
        for j in range(len(grid[0])):
            for i in range(len(grid)):
                if grid[i][j] != 0:
                    heights[j] = 20 - i
                    break

        # calculate evenness score
        for i in range(len(heights) - 1):
            evenness_score += abs(heights[i] - heights[i + 1])

        return evenness_score, heights

    # check if and how many lines can be cleared, and clear them from the grid
    def check_lines_cleared(self, grid):
        # copy rows that aren't full to new grid
        new_grid = [row for row in grid if any(cell == 0 for cell in row)]
        # 20 minus size of new grid is how many rows were cleared
        cleared = 20 - len(new_grid)
        # add empty rows to the top to keep it 20 rows
        updated_grid = [[0] * 10 for _ in range(cleared)] + new_grid

        return cleared, updated_grid

    # for scoring mode, check how many blocks in last column (which we want to keep empty until a Tetris)
    def check_last_col(self, grid):
        count = 0
        for row in grid:
            if row[9] != 0:
                count += 1

        return count

    # permanently add a piece to the game grid
    def lock_piece(self, grid, piece):
        for row in range(len(piece.shape)):
            for col in range(len(piece.shape[row])):
                if piece.shape[row][col] == 1:
                    grid[piece.row + row][piece.col + col] = piece.colour

    # calculate the final score for the move
    def calculate_score(self, holes, evenness, board_fill, danger, lines_cleared, last_col_count):
        score = 0

        score -= (self.weight_holes * holes)
        score -= (self.weight_evenness * evenness)
        score -= (self.weight_board_fill * board_fill)
        score -= (danger * 1000)
        score -= (self.weight_last_col * last_col_count)
        match lines_cleared: # different scores depending on how many lines cleared
            case 1:
                score += self.weight_lines_cleared_1
            case 2:
                score += self.weight_lines_cleared_2
            case 3:
                score += self.weight_lines_cleared_3
            case 4:
                score += self.weight_lines_cleared_4

        return score
