SHAPES = {
    "I": [[1, 1, 1, 1]],

    "O": [[1, 1],
          [1, 1]],

    "T": [[1, 1, 1],
          [0, 1, 0]],

    "L": [[1, 1, 1],
          [1, 0, 0]],

    "J": [[1, 1, 1],
          [0, 0, 1]],

    "S": [[0, 1, 1],
          [1, 1, 0]],

    "Z": [[1, 1, 0],
          [0, 1, 1]]
}

COLOURS = {
    "I": (0, 255, 255),
    "O": (255, 255, 0),
    "T": (128, 0, 128),
    "L": (255, 165, 0),
    "J": (0, 0, 255),
    "S": (0, 255, 0),
    "Z": (255, 0, 0)
}

class Piece:
    def __init__(self, type, col, row, orientation=0):
        self.type = type # type is the block shape, represented by a letter
        self.shape = SHAPES[self.type] # automatically set the shape matrix based on given type
        self.colour = COLOURS[self.type] # automatically set the colour based on given type
        self.col = col # the column placement of the piece (top left corner of the piece)
        self.row = row # the row placement of the piece (top left corner of the piece)
        self.orientation = orientation

        # if an orientation (rotation) is given, rotate to it
        for i in range(orientation):
            self.rotate()

    # rotates a piece by manipulating the matrix
    # each part of the 1 liner explained below
    def rotate(self):
        # self.shape[::-1] -> flips rows
        # zip(*matrix) -> transposes the matrix (unpacks and zips rows)
        # results in the piece (represented as a matrix) rotated 90 degrees clockwise
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
        self.orientation = (self.orientation + 1) % 4 # update orientation (always 0-3)

    # rotate the piece until it matches the specified new orientation
    def set_orientation(self, new_orientation):
        if new_orientation < 0 or new_orientation > 3:
            return

        while self.orientation != new_orientation:
            self.rotate()