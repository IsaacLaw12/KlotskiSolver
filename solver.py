import numpy as np
from queue import Queue

class Block:
    def __init__(self, starting_position, shape=(1,1)):
        self.min_corner = np.array(starting_position)
        self.max_corner = self.min_corner + shape

    def __repr__(self):
        return str(self.min_corner) + str(self.max_corner) + "\n"

    def hash_corners(self):
        return hash((self.min_corner, self.max_corner))

    def include_coordinates(self, position):
        # Expand the block to contain the coordinates specified by position
        compare = np.array([self.min_corner, position])
        self.min_corner = np.min(compare, axis=0)

        position = position + np.array([1,1])
        compare = np.array([self.max_corner, position])
        self.max_corner = np.max(compare, axis=0)

    def covered_indexes(self):
        indexes = []
        for x_offset in range(self.max_corner[0] - self.min_corner[0]):
            for y_offset in range(self.max_corner[1] - self.min_corner[1]):
                index = self.min_corner + [x_offset, y_offset]
                indexes.append(index)
        return indexes

class GameBoard:
    def __init__(self, filename):
        self.filename = filename
        self.shape = (5, 4)
        self.blocks = {}
        self.load_game()

    def hash_board_state(self):
        # Create a hash of the current state.  Blocks of the same shape have the same
        # hash value
        block_hashes = []
        for key in self.blocks:
            block_hashes.append(hash(self.blocks[key]))
        block_hashes.sort()
        return hash(tuple(block_hashes))

    def load_game(self):
        lines = self.read_file()
        self.load_file(lines)

    def read_file(self):
        lines = []
        with open(self.filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    lines.append(line)
        return lines

    def load_file(self, lines):
        try:
            self.shape = [int(x) for x in lines[0].split()]
            for row in range(1, self.shape[0]+1):
                for col in range(self.shape[1]):
                    current = lines[row][col]
                    position = [row-1, col]
                    if current in self.blocks:
                        self.blocks[current].include_coordinates(position)
                    else:
                        self.blocks[current] = Block(position)
        except IndexError:
            print("Invalid game format")

    def get_state(self):
        return self.blocks

    def set_state(self, blocks):
        self.blocks = blocks

    def available_moves(self):
        # Find empty blocks
        # Iterate through blocks, find if they are adjacent to empty blocks
        # Check whether the move can be made without collisons

    def print_board(self):
        board = np.chararray(self.shape)
        for letter in self.blocks:
            for index in self.blocks[letter].covered_indexes():
                board[tuple(index)] = letter
        print(board)

class Solver:
    def __init__(self, game_board):
        self.game_board = game_board
        self.visited_states = []
        self.solve()

    def solve(self):
        explore_queue = Queue()



if __name__ == "__main__":
    gb = GameBoard('./puzzles/only_18_steps.txt')
    gb.print_board()
