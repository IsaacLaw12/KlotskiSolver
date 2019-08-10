import numpy as np
from block import Block

class GameBoard:
    self.PLAYER_CHAR = "*"
    self.GOAL_CHAR = "_"
    def __init__(self, filename):
        self.filename = filename
        self.shape = (5, 4)
        self.blocks = {}
        self.goal_block = None
        self.load_game()

    def hash_blocks(self, blocks=None):
        # Create a hash of the current state.  Blocks of the same shape have the same
        # hash value
        if blocks is None:
            blocks = self.blocks
        block_hashes = []
        for key in blocks:
            block_hashes.append(blocks[key].hash_corners())
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
                pass

    def is_valid_move(self, block_key, move):
        pass

    def solved(self):
        return False


    def print_board(self):
        board = np.chararray(self.shape)
        for letter in self.blocks:
            for index in self.blocks[letter].covered_indexes():
                board[tuple(index)] = letter
        print(board)
