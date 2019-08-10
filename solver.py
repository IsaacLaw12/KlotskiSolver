import numpy as np
from queue import Queue
from gameboard import GameBoard

class Solver:
    def __init__(self, game_board):
        self.game_board = game_board
        self.visited_states = []
        self.solve()

    def solve(self):
        explore_queue = Queue()
        base_state = self.game_board.get_state()
        explore_queue.put(base_state)
        explored_states = 0
        while explore_queue:
            explored_states += 1
            next_state = explore_queue.get()
            if self.solved(next_state):
                break
            self.extract_potential_moves(next_state, explore_queue)

    def extract_potential_moves(self, state, queue):
        possible_moves = self.game_board.set_state(state).available_moves()
        for state in possible_moves:
            hash_state = self.game_board.hash_state(state)
            if hash_state not in self.visited_states:
                self.visited_states.append(hash_state)
                queue.put(state)

    def solved(self, state):
        self.game_board.set_state(state)
        return self.game_board.solved()

if __name__ == "__main__":
    gb = GameBoard('./puzzles/only_18_steps.txt')
    gb.print_board()
