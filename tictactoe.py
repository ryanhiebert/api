"""
A basic Tic Tac Toe game.

The board is intended to be used as an immutable structure,
and its methods return new instances of a Tic Tac Toe board.
"""


class TicTacToe(tuple):
    """
    A basic Tic Tac Toe game board.

    The players are represented by 'x' and 'o'.
    None is used as a sentinel for an empty space.
    """

    def __str__(self):
        """Convert to a string, using '-' for an empty space."""
        indexes = ((r,c) for c in range(3) for r in range(3))
        reprs = ['-' if self[r][c] is None else self[r][c] for r,c in indexes]
        return ''.join(reprs)

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, repr(str(self)))

    def __new__(cls, board=None):
        if board is None:
            board = [[None] * 3] * 3

        if isinstance(board, str):
            board = (board[:3], board[3:6], board[6:])

        board = (tuple(None if s == '-' else s for s in row) for row in board)

        return tuple.__new__(cls, board)

    def move(self, player, space):
        """
        Player is one of 'x' or 'y'.

        Space is a tuple representing the row and column space to occupy,
        using 0-based integer indexes.
        """
        if player not in 'xy':
            raise ValueError('not a valid player: {}'.format(repr(player)))

        if space[0] not in list(range(3)) or space[1] not in list(range(3)):
            raise ValueError('not a valid space: {}'.format(repr(space)))

        board = [list(row) for row in self]
        row, col = space
        board[row][col] = player
        return TicTacToe(board)

    def empty(self):
        """Returns the row, column index of empty spaces"""
        indexes = [(r,c) for c in range(3) for r in range(3)]
        return [(r,c) for r,c in indexes if self[r][c] is None]

    def full(self):
        indexes = [(r,c) for c in range(3) for r in range(3)]
        return all(self[r][c] is not None for r,c in indexes)

    def turn(self):
        flat = [self[r][c] for c in range(3) for r in range(3)]
        return 'o' if flat.count('o') < flat.count('x') else 'x'

    def winner(self):
        row_vectors = [[(r,c) for c in range(3)] for r in range(3)]
        col_vectors = [[(r,c) for r in range(3)] for c in range(3)]
        diagonals = [((0,0), (1,1), (2,2)), ((0,2), (1,1), (2,0))]
        win_vectors = row_vectors + col_vectors + diagonals

        for vector in win_vectors:
            if not all(self[r][c] is not None for r,c in vector):
                continue
            fill = [self[r][c] for r,c in vector]
            if fill[0] == fill[1] == fill[2]:
                return fill[0]

        return None

    def completed(self):
        return self.full() or bool(self.winner())
