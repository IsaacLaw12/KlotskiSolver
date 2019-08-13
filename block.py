import numpy as np

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

    def move_block(self, move):
        self.min_corner = self.min_corner + move
        self.max_corner = self.max_corner + move

    def covered_indexes(self):
        indexes = []
        for x_offset in range(self.max_corner[0] - self.min_corner[0]):
            for y_offset in range(self.max_corner[1] - self.min_corner[1]):
                index = self.min_corner + [x_offset, y_offset]
                indexes.append(index)
        return indexes

    def intersection(self, block):
        these_indexes = set(self.covered_indexes())
        other_indexes = set(block.covered_indexes())
        return these_indexes.intersection(other_indexes)

    def contains(self, block):
        intersect = self.intersection(block)
        return intersect == set(block.covered_indexes())

    def is_adjacent(self, block):
        # Blocks share sides, but do not overlap
        x_overlap = self.block_overlap(block, axis=0)
        y_overlap = self.block_overlap(block, axis=1)
        shares_edge = 0 in [x_overlap, y_overlap] and x_overlap + y_overlap > 0
        return shares_edge

    def block_overlap(self, block, axis):
        # Returns the overlap between the current block and block, along axis
        overlap = min(self.max_corner[axis], block.max_corner[axis]) - max(self.min_corner[axis], block.min_corner[axis])
        return overlap
