import os

import chess
import math
import random
import time
import pickle

SEARCH_TIME = 5
C = math.sqrt(2)

new_board = chess.Board()

class Node:

    def __init__(self, board_epd, player, parent):
        self.wins = 0
        self.sims = 0
        self.player = player
        self.boardstate = board_epd
        self.children = {}
        self.parent = parent
        self.legal_moves_remaining = list(chess.Board(board_epd).legal_moves)
        self.total_legal_moves = len(self.legal_moves_remaining)

    # Selection

    def find_best_child_explore(self):
        max_score = 0
        best = None
        for child in self.children.values():
            child_score = child.wins / child.sims + C * math.sqrt(math.log(self.sims)/child.sims)
            if child_score > max_score:
                max_score = child_score
                best = child
        return best

    def find_bottom_node(self):
        best = self.find_best_child_explore()
        while best and best.children:
            best = best.find_best_child_explore()
        if best:
            return best
        return self

    # Expansion

    def expand_tree(self):
        new_leaf = random.random() < len(self.legal_moves_remaining) / self.total_legal_moves if self.total_legal_moves else False
        bottom = self if new_leaf else self.find_bottom_node()
        board = chess.Board(bottom.boardstate)
        move = random.choice(list(bottom.legal_moves_remaining)) if bottom.legal_moves_remaining else None
        if move:
            bottom.legal_moves_remaining.pop(bottom.legal_moves_remaining.index(move))
            board.push(move)
            new_node = Node(board.epd(), 'W' if bottom.player == 'B' else 'B', bottom)
            bottom.children[move] = new_node
            return new_node
        return bottom

    # Simulation
    def simulate_game(self):
        board = chess.Board(self.boardstate)
        while not board.is_game_over():
            board.push(random.choice(list(board.legal_moves)))
        wins = 0
        if board.result == '1-0' and self.player == 'W' or board.result == '0-1' and self.player == 'B':
            wins = 2
        elif board.result == '1/2-1/2':
            wins = 1
        self.wins += wins
        self.sims += 2

        return wins

    def back_propagate(self, wins):
        node = self
        while node.parent:
            wins = 2 - wins
            node.parent.wins += wins
            node.parent.sims += 2
            node = node.parent
        return None

    # all together now
    def run_simulator(self):
        now = time.time()
        while time.time() - SEARCH_TIME < now:
            new_node = self.expand_tree()
            wins = new_node.simulate_game()
            new_node.back_propagate(wins)

    def pick_move(self):
        max_score = 0
        best = None
        for child in self.children.values():
            child_score = child.wins / child.sims
            if child_score > max_score:
                max_score = child_score
                best = child
        return best

class GameRunner:

    memory = 'pickled_tree.P'

    def __init__(self):
        # self.player = 'W'
        self.root = Node(new_board.epd(), 'W', None)
        self.node_pointer = self.root

    def run(self):
        self.node_pointer = self.root
        os.system('clear')
        print("Welcome to Monte Carlo!")
        print("You'll be playing white")
        board = chess.Board(self.node_pointer.boardstate)
        while not board.is_game_over():
            os.system('clear')
            print(board)
            move = chess.Move.from_uci(input("Make a move "))
            board.push(move)
            if move in self.node_pointer.children.keys():
                self.node_pointer = self.node_pointer.children.get(move)
            else:
                # self.player = 'B'
                new_node = Node(board.epd(), 'B', self.node_pointer)
                self.node_pointer.children[move] = new_node
                self.node_pointer = new_node
            self.node_pointer.run_simulator()
            self.node_pointer = self.node_pointer.find_best_child_explore()
            if self.node_pointer:
                board = chess.Board(self.node_pointer.boardstate)
            else:
                break
        print(board.result())

    def save(self):
        with open(self.memory, 'wb') as file:
            pickle.dump(self.root, file)

    def load(self):
        with open(self.memory, 'rb') as file:
            self.root = pickle.load(file)

g = GameRunner()



