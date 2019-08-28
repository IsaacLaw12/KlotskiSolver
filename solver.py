import numpy as np
from queue import Queue
from gameboard import GameBoard

class Solver:
    def __init__(self, game_board):
        self.game_board = game_board
        self.visited_states = set()

    def solve(self, break_at_first_solution=False):
        explore_queue = Queue()
        base_state = self.game_board.get_state()
        explore_queue.put(base_state)
        num_explored_states = 0
        solutions = 0
        while not explore_queue.empty():
            num_explored_states += 1
            current_state = explore_queue.get()
            if self.game_board.solved(current_state):
                solutions += 1
                if break_at_first_solution:
                    break
            else:
                self.extract_potential_moves(current_state, explore_queue)
        print("Finished solving. %d solutions found and %d states explored " % (solutions, num_explored_states))

    def extract_potential_moves(self, state, queue):
        self.game_board.set_state(state)
        adjacent_move_states = self.game_board.available_moves()
        # If the player block is now unimpeded don't bother moving other blocks
        if self.game_board.player_escaped():
            player_move_states = self.unique_player_moves()
            if player_move_states:
                adjacent_move_states = player_move_states

        for state in adjacent_move_states:
            hash_state = self.game_board.hash_state(state)
            if hash_state not in self.visited_states:
                self.visited_states.add(hash_state)
                queue.put(state)

    def unique_player_moves(self):
        adjacent_player_states = self.game_board.valid_moves(GameBoard.PLAYER_CHAR)
        possible_states = []
        if adjacent_player_states:
            for state in adjacent_player_states:
                if self.game_board.hash_state(state) not in self.visited_states:
                    possible_states.append(state)
        return possible_states

    def mark_state_visited(self, hashed_state=None):
        if hashed_state is None:
            hashed_state = self.game_board.hash_state()
        self.visited_states.add(hashed_state)

if __name__ == "__main__":
    gb = GameBoard('./puzzles/only_18_steps.txt')
    solver = Solver(gb)
    solver.solve(True)
