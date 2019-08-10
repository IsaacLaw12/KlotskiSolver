import numpy as np
from queue import Queue

class Block:
    def __init__(self, starting_position, shape=(1,1)):
        self.min_corner = np.array(starting_position)
        self.max_corner = self.min_corner + shape

    def __repr__(self):
        return str(self.min_corner) + str(self.max_corner) + "\n"

    def dimensions(self):
        self.max_corner - self.min_corner

    def hash_corners(self):
        return hash((self.min_corner, self.max_corner))

    def append_coordinate(self, position):
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

    def is_adjacent(self, block):
        # Blocks share sides, but do not overlap
        x_overlap, y_overlap = self.xy_overlaps(block)
        shared_edge = 0 in [x_overlap, y_overlap] and x_overlap + y_overlap > 0
        return shared_edge

    def does_intersect(self, block):
        # Blocks share some area
        x_overlap, y_overlap = self.xy_overlaps(block)
        x_overlap = max(x_overlap, 0)
        y_overlap = max(y_overlap, 0)
        return x_overlap * y_overlap > 0

    def contains(self, block):
        x_overlap, y_overlap = self.xy_overlaps(block)
        return block.dimensions() == np.array([x_overlap, y_overlap])

    def xy_overlaps(self, block):
        # Calculates the amount the blocks overlap in the x and y directions
        # Negative values represent distance between blocks
        x_overlap = self.block_overlap(block, axis=0)
        y_overlap = self.block_overlap(block, axis=1)
        return x_overlap, y_overlap

    def block_overlap(self, block, axis):
        # Returns the overlap between the current block and block, along axis
        overlap = min(self.max_corner[axis], block.max_corner[axis]) - max(self.min_corner[axis], block.min_corner[axis])
        return overlap


class GameBoard:
    self.PLAYER_CHAR = "*"
    self.GOAL_CHAR = "_"
    def __init__(self, filename):
        self.filename = filename
        self.shape = (5, 4)
        self.blocks = {}
        self.goal_block = None
        self.load_game()

    def hash_board_state(self):
        # Create a hash of the current state.  Blocks of the same shape have the same
        # hash value
        block_hashes = []
        for key in self.blocks:
            block_hashes.append(self.blocks[key].hash_corners())
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
                    # Leave empty spots empty
                    if current == self.GOAL_CHAR:
                        continue
                    position = [row-1, col]
                    if current in self.blocks:
                        self.blocks[current].append_coordinate(position)
                    else:
                        self.blocks[current] = Block(position)
        except IndexError:
            print("Invalid game format")

    def get_state(self):
        return self.blocks

    def set_state(self, blocks):
        self.blocks = blocks

    def available_moves(self):
        empty_blocks = self.empty_blocks()
        # Iterate through blocks, find if they are adjacent to empty blocks
        adjacent_obstacles = []
        for key in self.blocks:
            obstacle = self.blocks(key)
            for empty_block in empty_blocks:
                if obstacle.is_adjacent(empty_block):
                    adjacent_obstacles.append(keys)
        # Check whether a move can be made without collisons
        return self.valid_moves(adjacent_obstacles)

    def empty_blocks(self):
        # Returns a list of the 1x1 blocks that are empty
        board = np.zeros(self.shape)
        for letter in self.blocks:
            for index in self.blocks[letter].covered_indexes():
                board[tuple(index)] = 1
        empty_blocks = []
        for row in range(board.shape[0]):
            for col in range(board.shape[1]):
                position = [row, col]
                if not board[position]:
                    empty_blocks.append(Block(position))
        return empty_blocks

    def valid_moves(self, obstacle_keys):
        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for move in moves:
            for obstacle_k in obstacle_keys:

    def is_valid_move(self, block_key, move):



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
