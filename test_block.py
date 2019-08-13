import unittest
import numpy as np
from block import Block

class test_block(unittest.TestCase):
    def test_adjacent(self):
        orig = Block((0,0), (3,3))
        down = Block((3,0), (1,1))
        right = Block((0,3), (1,1))
        inside = Block((0,0), (1,1))
        not_adj = Block((5,5), (1,1))
        self.assertTrue(orig.is_adjacent(down))
        self.assertTrue(orig.is_adjacent(right))
        self.assertTrue(down.is_adjacent(orig))
        self.assertTrue(right.is_adjacent(orig))

        self.assertTrue(not orig.is_adjacent(inside))
        self.assertTrue(not orig.is_adjacent(not_adj))
        self.assertTrue(not inside.is_adjacent(orig))
        self.assertTrue(not not_adj.is_adjacent(orig))

    def test_contains(self):
        orig = Block((0,0), (3,3))
        inside = Block((0,0), (1,1))
        partially_inside = Block((2,2), (2,2))
        outside = Block((5,5), (1,1))
        self.assertTrue(orig.contains(inside))
        self.assertTrue(not orig.contains(partially_inside))
        self.assertTrue(not orig.contains(outside))

    def test_intersection(self):
        first = Block((2,2),(4,4))
        second = Block((1,1),(2,2))
        self.assertEqual(first.intersection(second), {(2,2)})

    def test_append_coordinates(self):
        block = Block((0,0))
        self.assertEqual(tuple(block.min_corner), (0,0))
        self.assertEqual(tuple(block.max_corner), (1,1))

        block.append_coordinate([6,6])
        self.assertEqual(tuple(block.min_corner), (0,0))
        self.assertEqual(tuple(block.max_corner), (7,7))

if __name__ == '__main__':
    unittest.main()
