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
