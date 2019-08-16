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
        solutions = 0
        while not explore_queue.empty():
            #print(explore_queue.qsize())
            #print(len(self.visited_states))
            explored_states += 1
            current_state = explore_queue.get()
            if self.game_board.solved(current_state):
                solutions += 1
            else:
                self.extract_potential_moves(current_state, explore_queue)
        print("Finished solving. %d solutions found and %d states explored " % (solutions, explored_states))

    def extract_potential_moves(self, state, queue):
        self.game_board.set_state(state)
        # Try to move the player first, otherwise move all the other blocks
        possible_moves = self.unique_player_moves()
        if not possible_moves:
            possible_moves = self.game_board.available_moves()

        for state in possible_moves:
            hash_state = self.game_board.hash_state(state)
            if hash_state not in self.visited_states:
                self.visited_states.append(hash_state)
                queue.put(state)

    def unique_player_moves(self):
        possible_player_moves = self.game_board.valid_moves(GameBoard.PLAYER_CHAR)
        possible_moves = []
        if possible_player_moves:
            for move in possible_player_moves:
                if self.game_board.hash_state(move) not in self.visited_states:
                    possible_moves.append(move)
        return possible_moves

if __name__ == "__main__":
    gb = GameBoard('./puzzles/only_18_steps.txt')
    solve = Solver(gb)
    # gb.print_board()
