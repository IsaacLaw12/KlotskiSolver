import numpy as np

class Block:
    def __init__(self, starting_position, shape=(1,1)):
        self.min_corner = np.array(starting_position)
        self.max_corner = self.min_corner + shape

    def __repr__(self):
        return str(self.min_corner) + str(self.max_corner) + "\n"

    def include_coordinates(self, position):
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

    def print_board(self):
        board = np.chararray(self.shape)
        for letter in self.blocks:
            for index in self.blocks[letter].covered_indexes():
                board[tuple(index)] = letter
        print(board)

if __name__ == "__main__":
    gb = GameBoard('./puzzles/only_18_steps.txt')
    gb.print_board()
