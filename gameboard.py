import numpy as np
from copy import deepcopy
from block import Block

class GameBoard:
    PLAYER_CHAR = "*"
    GOAL_CHAR = "="
    EMPTY_CHAR = "_"
    OBSTACLE_CHAR = "#"
    PASSABLE_OBSTACLE_CHAR = "/"

    def __init__(self, filename):
        self.filename = filename
        self.shape = (5, 4)
        self.blocks = {}
        self.obstacles = []
        self.passable_obstacles = []
        self.goal_block = None
        self.load_game()

    def hash_state(self, blocks=None):
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
                if line:
                    lines.append(line)
        return lines

    def load_file(self, lines):
        try:
            self.set_shape([int(x) for x in lines[0].split()])
            lines.pop(0)
            for row in range(self.shape[0]):
                for col in range(self.shape[1]):
                    current = lines[row][col]
                    position = [row, col]
                    self.process_char(current, position)
        except IndexError:
            print("Invalid game format")

    def process_char(self, character, position):
        if character == GameBoard.EMPTY_CHAR:
            return
        elif character == GameBoard.GOAL_CHAR:
            self.set_goal(position)
        elif character == GameBoard.OBSTACLE_CHAR:
            self.obstacles.append(position)
        elif character == GameBoard.PASSABLE_OBSTACLE_CHAR:
            self.passable_obstacles.append(position)
        elif character in self.blocks:
            self.blocks[character].append_coordinate(position)
        else:
            self.blocks[character] = Block(position)

    def set_shape(self, shape):
        self.shape = tuple(shape)

    def set_goal(self, position):
        if self.goal_block is None:
            self.goal_block = Block(position)
        else:
            self.goal_block.append_coordinate(position)

    def get_state(self):
        return deepcopy(self.blocks)

    def set_state(self, blocks):
        self.blocks = deepcopy(blocks)

    def available_moves(self):
        empty_blocks = self.empty_blocks()
        # Iterate through blocks, find if they are adjacent to empty blocks
        possible_obstacles = []
        for key in self.blocks:
            obstacle = self.blocks[key]
            for empty_block in empty_blocks:
                if obstacle.is_adjacent(empty_block):
                    possible_obstacles.append(key)
        return self.valid_moves(possible_obstacles)

    def empty_blocks(self):
        # Returns a list of the 1x1 blocks that are empty
        board, _ = self.board_coverage()
        empty_blocks = []
        for row in range(board.shape[0]):
            for col in range(board.shape[1]):
                position = tuple([row, col])
                if not board[position]:
                    empty_blocks.append(Block(position))
        return empty_blocks

    def board_coverage(self):
        # Returns an array in the shape of board, each index contains a count of
        # blocks containing it
        board = self.board_with_obstacles()
        blocks_out_of_bounds = False
        for letter in self.blocks:
            for index in self.blocks[letter].covered_indexes():
                if not self.index_in_bounds(index):
                    blocks_out_of_bounds = True
                else:
                    board[tuple(index)] += 1
        return board, blocks_out_of_bounds

    def board_with_obstacles(self):
        # Adds obstacles to board
        board = np.zeros(self.shape)
        for position in self.obstacles:
            board[tuple(position)] += 1
        player_indexes = self.blocks[GameBoard.PLAYER_CHAR].covered_indexes()
        for index in self.passable_obstacles:
            # The player block is the only one allowed to overlap with the passable_obstacles
            # Otherwise it blocks competition
            if index not in player_indexes:
                board[tuple(index)] += 1
        return board

    def index_in_bounds(self, index):
        in_bounds = False
        if index[0] >=0 and index[0] < self.shape[0]:
            if index[1] >=0 and index[1] < self.shape[1]:
                in_bounds = True
        return in_bounds

    def valid_moves(self, obstacle_keys):
        # Attempt to move each passed obstacle in all four directions
        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        valid_states = []
        for move in moves:
            for obstacle_k in obstacle_keys:
                is_valid, move_state = self.is_valid_state(obstacle_k, np.array(move))
                if is_valid:
                    valid_states.append(move_state)
        return valid_states

    def is_valid_state(self, block_key, move):
        self.blocks[block_key].move_block(move)
        move_state = self.get_state()
        board_coverage, blocks_out_of_bounds = self.board_coverage()
        self.blocks[block_key].move_block(move*-1)
        is_valid = (board_coverage <= 1).all() and not blocks_out_of_bounds
        return is_valid, move_state

    def intersects_passable_obstacle(self, obstacle_key):
        indexes = self.blocks[obstacle_key].covered_indexes()
        result = False
        for obstacle_index in self.passable_obstacles:
            if obstacle_index in indexes:
                result = True
                break
        return result

    def solved(self, test_blocks=None):
        if test_blocks is None:
            test_blocks = self.blocks
        else:
            self.set_state(test_blocks)
        player_block = self.blocks[GameBoard.PLAYER_CHAR]
        return self.goal_block.contains(player_block)

    def print_board(self):
        board = np.chararray(self.shape, unicode=True)
        eb = self.empty_blocks()
        for block in eb:
            for position in block.covered_indexes():
                board[tuple(position)] = "_"
        for position in self.obstacles:
            board[tuple(position)] = '#'
        for position in self.goal_block.covered_indexes():
            board[tuple(position)] = '='
        for letter in self.blocks:
            for index in self.blocks[letter].covered_indexes():
                board[tuple(index)] = letter
        for row in range(self.shape[0]):
            for col in range(self.shape[1]):
                print(board[tuple([row, col])], end="")
            print()
