import unittest
import numpy as np
from queue import Queue
from gameboard import GameBoard
from block import Block
from solver import Solver

class test_solver(unittest.TestCase):
    def test_completion(self):
        board = GameBoard('./puzzles/only_18_steps.txt')
        board_solver = Solver(board)
        # Arrange board so that player only needs to move down 2 blocks to win

        for block in ['G', 'H', 'K', 'L']:
            board_solver.game_board.blocks[block].move_block((-2, 0))
        board_solver.game_board.blocks[GameBoard.PLAYER_CHAR].move_block((3, 0))
        self.assertTrue(board_solver.game_board.current_state_valid())
        # Add the previous state to visited states so that the player can not move backwards
        board_solver.mark_state_visited()
        board_solver.game_board.blocks[GameBoard.PLAYER_CHAR].move_block((1, 0))
        self.assertTrue(board_solver.game_board.player_escaped())

        for _ in range(2):
            correct_move_states = self.simulated_move_states(board_solver, GameBoard.PLAYER_CHAR, [(1, 0)])
            self._test_available_moves(board_solver, correct_move_states)
            board_solver.mark_state_visited()
            board_solver.game_board.blocks[GameBoard.PLAYER_CHAR].move_block((1,0))
        self.assertTrue(board_solver.game_board.solved())

    def simulated_move_states(self, solver, block_key, move_list):
        result_states = []
        for move in move_list:
            move = np.array(move)
            solver.game_board.blocks[block_key].move_block(move)
            result_states.append(solver.game_board.get_state())
            solver.game_board.blocks[block_key].move_block(move *-1)
        return result_states

    def _test_available_moves(self, solver, expected_available_states):
        state_queue = Queue()
        current_state = solver.game_board.get_state()
        solver.extract_potential_moves(current_state, state_queue)
        state_list = [solver.game_board.hash_state(x) for x in list(state_queue.queue)]
        expected_available_states = [solver.game_board.hash_state(x) for x in expected_available_states]
        self.assertEqual(len(state_list), len(expected_available_states))
        for state in expected_available_states:
            self.assertTrue(state in state_list)


    def _test_queue(self, queue, contents, length, erase=False):
        self.assertEqual(queue.qsize(), length)
        new_queue = Queue()
        try:
            for i in range(length):
                current_test = contents[i]
                current_object = queue.get()
                if not erase:
                    new_queue.put(current_object)
                self.assertEqual(current_test, current_object)
        except IndexError:
            print("Queue fails comparison")
        queue = new_queue




if __name__ == '__main__':
    unittest.main()
