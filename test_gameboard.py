import unittest
import numpy as np
from gameboard import GameBoard
from block import Block

class test_board(unittest.TestCase):
    def test_file_loading(self):
        board = GameBoard('./puzzles/only_18_steps.txt')

        self.assertEqual(board.shape, tuple([8, 6]))
        self.assertEqual(tuple(board.board.min_corner), (0,0))
        self.assertEqual(tuple(board.board.max_corner), (8,6))
        block_names = ['A', '*', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
        for bn in block_names:
            self.assertTrue(bn in board.blocks)

    def test_hashing(self):
        board = GameBoard('./puzzles/only_18_steps.txt')
        board2 = GameBoard('./puzzles/only_18_steps.txt')
        self.assertEqual(board.hash_state(), board2.hash_state())

        board.blocks['A'].move_block(np.array([1,0]))
        board.blocks['D'].move_block(np.array([-1,0]))
        self.assertEqual(board.hash_state(), board2.hash_state())

        board.blocks['z'] = Block((1,1), (5,5))
        board2.blocks['z'] = Block((1,1), (5,5))
        self.assertEqual(board.hash_state(), board2.hash_state())

        board.blocks['z'].move_block(np.array([1,1]))
        self.assertNotEqual(board.hash_state(), board2.hash_state())

        board.blocks['z'].move_block(np.array([-1, -1]))
        self.assertEqual(board.hash_state(), board2.hash_state())



if __name__ == '__main__':
    unittest.main()
