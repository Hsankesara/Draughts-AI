import pygame
import sys
from pygame.locals import *
import random
from copy import deepcopy
import math
pygame.font.init()

##COLORS##
#             R    G    B
WHITE = (255, 255, 255)
BLUE = (0,   0, 255)
RED = (255,   0,   0)
BLACK = (0,   0,   0)
GOLD = (255, 215,   0)
HIGH = (160, 190, 255)

##DIRECTIONS##
NORTHWEST = "northwest"
NORTHEAST = "northeast"
SOUTHWEST = "southwest"
SOUTHEAST = "southeast"


class Bot:
    def __init__(self, game, color, method='rational', heuristic=None, depth=1):
        self.method = method
        if heuristic == 'piece2val':
            self.heuristic = self.__piece2val
        self.depth = depth
        self.game = game
        self.color = color
        if self.color == BLUE:
            self.adversary_color = RED
        else:
            self.adversary_color = BLUE

    def step(self, board):
        if self.method == 'random':
            self.__random_step(board)
        elif self.method == 'rational':
            self.__rational_step(board)

    def __action(self, selected_piece, mouse_pos, board):
        if self.game.hop == False:
            if board.location(mouse_pos[0], mouse_pos[1]).occupant != None and board.location(mouse_pos[0], mouse_pos[1]).occupant.color == self.game.turn:
                selected_piece = mouse_pos

            elif selected_piece != None and mouse_pos in board.legal_moves(selected_piece[0], selected_piece[1]):

                board.move_piece(
                    selected_piece[0], selected_piece[1], mouse_pos[0], mouse_pos[1])

                if mouse_pos not in board.adjacent(selected_piece[0], selected_piece[1]):
                    board.remove_piece(selected_piece[0] + (mouse_pos[0] - selected_piece[0]) //
                                       2, selected_piece[1] + (mouse_pos[1] - selected_piece[1]) // 2)

                    self.game.hop = True
                    selected_piece = mouse_pos
                else:
                    self.game.end_turn()

        if self.game.hop == True:
            if selected_piece != None and mouse_pos in board.legal_moves(selected_piece[0], selected_piece[1], self.game.hop):
                board.move_piece(
                    selected_piece[0], selected_piece[1], mouse_pos[0], mouse_pos[1])
                board.remove_piece(selected_piece[0] + (mouse_pos[0] - selected_piece[0]) //
                                   2, selected_piece[1] + (mouse_pos[1] - selected_piece[1]) // 2)

            if board.legal_moves(mouse_pos[0], mouse_pos[1], self.game.hop) == []:
                self.game.end_turn()
            else:
                selected_piece = mouse_pos
        if self.game.hop != True:
            self.game.turn = self.adversary_color

    def __random_step(self, board):
        possible_moves = self.__generate_all_possible_moves(board)
        if possible_moves == []:
            self.game.end_turn()
            self.game.turn = BLUE
            return
        random_move = random.choice(possible_moves)
        rand_choice = random.choice(random_move[2])
        self.__action(random_move, rand_choice, board)
        return

    def __generate_all_possible_moves(self, board):
        possible_moves = []
        for i in range(8):
            for j in range(8):
                if(board.legal_moves(i, j, self.game.hop) != [] and board.location(i, j).occupant != None and board.location(i, j).occupant.color == self.game.turn):
                    possible_moves.append(
                        (i, j, board.legal_moves(i, j, self.game.hop)))
        return possible_moves

    def __generate_move(self, board):
        for i in range(8):
            for j in range(8):
                if(board.legal_moves(i, j, self.game.hop) != [] and board.location(i, j).occupant != None and board.location(i, j).occupant.color == self.game.turn):
                    yield (i, j, board.legal_moves(i, j, self.game.hop))

    def __piece2val(self, board):
        score = 0
        for i in range(8):
            for j in range(8):
                occupant = board.location(i, j).occupant
                if(occupant is not None):
                    if(occupant.color == self.color):
                        score += occupant.value
                    else:
                        score -= occupant.value
        return score

    def __rational_step(self, board):
        # possible_moves = self.__generate_all_possible_moves(board)
        # if possible_moves == []:
        #    self.game.end_turn()
        #    self.game.turn = BLUE
        #    return
        random_move, random_choice, _ = self.__alpha_beta_pruning(
            self.depth - 1, board, 'max')
        self.__action(random_move, random_choice, board)
        return

    def __alpha_beta_pruning(self, depth, board, fn):
        if depth == 0:
            if fn == 'max':
                max_value = -float("inf")
                best_pos = None
                best_action = None
                for pos in self.__generate_move(board):
                    for action in pos[2]:
                        board_clone = deepcopy(board)
                        self.__action_on_board(board_clone, pos, action)
                        step_value = self.heuristic(board_clone)
                        if step_value > max_value:
                            max_value = step_value
                            best_pos = (pos[0], pos[1])
                            best_action = (action[0], action[1])
                        elif step_value == max_value and random.random() <= 0.5:
                            max_value = step_value
                            best_pos = (pos[0], pos[1])
                            best_action = (action[0], action[1])
                return best_pos, best_action, max_value
            else:
                min_value = float("inf")
                best_pos = None
                best_action = None
                for pos in self.__generate_move(board):
                    for action in pos[2]:
                        board_clone = deepcopy(board)
                        self.__action_on_board(board_clone, pos, action)
                        step_value = self.heuristic(board_clone)
                        if step_value < min_value:
                            min_value = step_value
                            best_pos = pos
                            best_action = action
                        elif step_value == min_value and random.random() <= 0.5:
                            min_value = step_value
                            best_pos = pos
                            best_action = action
                return best_pos, best_action, min_value
        else:
            if fn == 'max':
                max_value = -float("inf")
                best_pos = None
                best_action = None
                for pos in self.__generate_move(board):
                    for action in pos[2]:
                        board_clone = deepcopy(board)
                        self.__action_on_board(board_clone, pos, action)
                        _, __, step_value = self.__alpha_beta_pruning(
                            depth - 1, board_clone, 'min')
                        if step_value > max_value:
                            max_value = step_value
                            best_pos = pos
                            best_action = action
                        elif step_value == max_value and random.random() <= 0.5:
                            max_value = step_value
                            best_pos = pos
                            best_action = action
                return best_pos, best_action, max_value
            else:
                min_value = float("inf")
                best_pos = None
                best_action = None
                for pos in self.__generate_move(board):
                    for action in pos[2]:
                        board_clone = deepcopy(board)
                        self.__action_on_board(board_clone, pos, action)
                        _, __, step_value = self.__alpha_beta_pruning(
                            depth - 1, board_clone, 'max')
                        if step_value < min_value:
                            min_value = step_value
                            best_pos = (pos[0], pos[1])
                            best_action = (action[0], action[1])
                        elif step_value == min_value and random.random() <= 0.5:
                            min_value = step_value
                            best_pos = pos
                            best_action = action
                return best_pos, best_action, min_value

    def __action_on_board(self, board, selected_piece, mouse_pos, hop=False):
        if hop == False:
            if board.location(mouse_pos[0], mouse_pos[1]).occupant != None and board.location(mouse_pos[0], mouse_pos[1]).occupant.color == game.turn:
                selected_piece = mouse_pos

            elif selected_piece != None and mouse_pos in board.legal_moves(selected_piece[0], selected_piece[1]):

                board.move_piece(
                    selected_piece[0], selected_piece[1], mouse_pos[0], mouse_pos[1])

                if mouse_pos not in board.adjacent(selected_piece[0], selected_piece[1]):
                    board.remove_piece(selected_piece[0] + (mouse_pos[0] - selected_piece[0]) //
                                       2, selected_piece[1] + (mouse_pos[1] - selected_piece[1]) // 2)
            return
