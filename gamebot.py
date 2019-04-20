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
    def __init__(self, game, color, method='random', mid_eval=None, end_eval=None, depth=1):
        self.method = method
        if mid_eval == 'piece2val':
            self._mid_eval = self._piece2val
        elif mid_eval == 'piece_and_board':
            self._mid_eval = self._piece_and_board2val
        elif mid_eval == 'piece_and_row':
            self._mid_eval = self._piece_and_row2val
        elif mid_eval == 'piece_and_board_pov':
            self._mid_eval = self._piece_and_board_pov2val
        if end_eval == 'sum_of_dist':
            self._end_eval = self._sum_of_dist
        elif end_eval == 'farthest_piece':
            self._end_eval = self._farthest_piece
        else:
            self._end_eval = None
        self.depth = depth
        self.game = game
        self.color = color
        if self.color == BLUE:
            self.adversary_color = RED
        else:
            self.adversary_color = BLUE
        self._current_eval = self._mid_eval
        self._end_eval_time = False

    def step(self, board):
        if(self._end_eval is not None and self._end_eval_time == False):
            if self._all_kings(board):
                print('END EVAL is on')
                self._end_eval_time  = True
                self._current_eval = self._end_eval
        if self.method == 'random':
            self._random_step(board)
        elif self.method == 'minmax':
            self._minmax_step(board)
        elif self.method == 'alpha_beta':
            self._alpha_beta_step(board)

    def _action(self, selected_piece, mouse_pos, board):
        if selected_piece is None:
            print('NONE')
            return
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

    def _random_step(self, board):
        possible_moves = self._generate_all_possible_moves(board)
        if possible_moves == []:
            self.game.end_turn()
            self.game.turn = BLUE
            return
        random_move = random.choice(possible_moves)
        rand_choice = random.choice(random_move[2])
        self._action(random_move, rand_choice, board)
        return

    def _generate_all_possible_moves(self, board):
        possible_moves = []
        for i in range(8):
            for j in range(8):
                if(board.legal_moves(i, j, self.game.hop) != [] and board.location(i, j).occupant != None and board.location(i, j).occupant.color == self.game.turn):
                    possible_moves.append(
                        (i, j, board.legal_moves(i, j, self.game.hop)))
        return possible_moves

    def _generate_move(self, board):
        for i in range(8):
            for j in range(8):
                if(board.legal_moves(i, j, self.game.hop) != [] and board.location(i, j).occupant != None and board.location(i, j).occupant.color == self.game.turn):
                    yield (i, j, board.legal_moves(i, j, self.game.hop))

    def _piece2val(self, board):
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

    def _piece_and_row2val(self, board):
        score = 0
        if(self.color == RED):
            for i in range(8):
                for j in range(8):
                    occupant = board.location(i, j).occupant
                    if(occupant is not None):
                        if occupant.color == self.color:
                            score += 5 + j + 2 * (occupant.king)
                        else:
                            score -= 5 + (8 - j) + 2 * (occupant.king)
        else:
            for i in range(8):
                for j in range(8):
                    occupant = board.location(i, j).occupant
                    if(occupant is not None):
                        if occupant.color == self.color:
                            score += 5 + (8 - j) + 2 * (occupant.king)
                        else:
                            score -= 5 + j + 2 * (occupant.king)
        return score

    def _piece_and_board2val(self, board):
        score = 0
        if(self.color == RED):
            for i in range(8):
                for j in range(8):
                    occupant = board.location(i, j).occupant
                    if(occupant is not None):
                        if occupant.color == self.color and occupant.king:
                            score += 10
                        elif occupant.color != self.color and occupant.king:
                            score -= 10
                        elif occupant.color == self.color and j < 4:
                            score += 5
                        elif occupant.color != self.color and j < 4:
                            score -= 7
                        elif occupant.color == self.color and j > 4:
                            score += 7
                        elif occupant.color != self.color and j > 4:
                            score -= 5
        else:
            for i in range(8):
                for j in range(8):
                    occupant = board.location(i, j).occupant
                    if(occupant is not None):
                        if occupant.color == self.color and occupant.king:
                            score += 10
                        elif occupant.color != self.color and occupant.king:
                            score -= 10
                        elif occupant.color == self.color and j < 4:
                            score += 7
                        elif occupant.color != self.color and j < 4:
                            score -= 5
                        elif occupant.color == self.color and j > 4:
                            score += 7
                        elif occupant.color != self.color and j > 4:
                            score -= 5
        return score

    def _piece_and_board_pov2val(self, board):
        score = 0
        num_pieces = 0
        if(self.color == RED):
            for i in range(8):
                for j in range(8):
                    occupant = board.location(i, j).occupant
                    if(occupant is not None):
                        num_pieces += 1
                        if occupant.color == self.color and occupant.king:
                            score += 10
                        elif occupant.color != self.color and occupant.king:
                            score -= 10
                        elif occupant.color == self.color and j < 4:
                            score += 5
                        elif occupant.color != self.color and j < 4:
                            score -= 7
                        elif occupant.color == self.color and j > 4:
                            score += 7
                        elif occupant.color != self.color and j > 4:
                            score -= 5
        else:
            for i in range(8):
                for j in range(8):
                    occupant = board.location(i, j).occupant
                    if(occupant is not None):
                        num_pieces += 1
                        if occupant.color == self.color and occupant.king:
                            score += 10
                        elif occupant.color != self.color and occupant.king:
                            score -= 10
                        elif occupant.color == self.color and j < 4:
                            score += 7
                        elif occupant.color != self.color and j < 4:
                            score -= 5
                        elif occupant.color == self.color and j > 4:
                            score += 7
                        elif occupant.color != self.color and j > 4:
                            score -= 5
        return score / num_pieces

    def _minmax_step(self, board):
        random_move, random_choice, _ = self._minmax(
            self.depth - 1, board, 'max')
        self._action(random_move, random_choice, board)
        return

    def _alpha_beta_step(self, board):
        random_move, random_choice, _ = self._alpha_beta(
            self.depth - 1, board, 'max', alpha=-float('inf'), beta=float('inf'))
        #print(self.color, self.game.turn, self.game.hop)
        self._action(random_move, random_choice, board)
        #print(self.color, self.game.turn, self.game.hop)
        return

    def _minmax(self, depth, board, fn):
        if depth == 0:
            if fn == 'max':
                max_value = -float("inf")
                best_pos = None
                best_action = None
                for pos in self._generate_move(board):
                    for action in pos[2]:
                        board_clone = deepcopy(board)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        self._action_on_board(board_clone, pos, action)
                        step_value = self._current_eval(board_clone)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        #print('max->', depth, step_value, (pos[0], pos[1]), action, self.color)
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
                for pos in self._generate_move(board):
                    for action in pos[2]:
                        board_clone = deepcopy(board)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        self._action_on_board(board_clone, pos, action)
                        step_value = self._current_eval(board_clone)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        #print('min->', depth, step_value, (pos[0], pos[1]), action, self.color)
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
                for pos in self._generate_move(board):
                    for action in pos[2]:
                        #print('POS', (pos[0], pos[1]), 'ACK', action)
                        board_clone = deepcopy(board)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        self._action_on_board(board_clone, pos, action)
                        _, _, step_value = self._minmax(
                            depth - 1, board_clone, 'min')
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        #print('max->', depth, step_value, (pos[0], pos[1]), action, self.color)
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
                for pos in self._generate_move(board):
                    for action in pos[2]:
                        board_clone = deepcopy(board)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        self._action_on_board(board_clone, pos, action)
                        _, _, step_value = self._minmax(
                            depth - 1, board_clone, 'max')
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        if step_value < min_value:
                            min_value = step_value
                            best_pos = (pos[0], pos[1])
                            best_action = (action[0], action[1])
                        elif step_value == min_value and random.random() <= 0.5:
                            min_value = step_value
                            best_pos = pos
                            best_action = action
                return best_pos, best_action, min_value

    def _alpha_beta(self, depth, board, fn, alpha, beta):
        if depth == 0:
            if fn == 'max':
                max_value = -float("inf")
                best_pos = None
                best_action = None
                for pos in self._generate_move(board):
                    for action in pos[2]:
                        board_clone = deepcopy(board)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        self._action_on_board(board_clone, pos, action)
                        step_value = self._current_eval(board_clone)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        #print('max->', depth, step_value, (pos[0], pos[1]), action, self.color)
                        if step_value > max_value:
                            max_value = step_value
                            best_pos = pos
                            best_action = (action[0], action[1])
                        elif step_value == max_value and random.random() <= 0.5:
                            max_value = step_value
                            best_pos = (pos[0], pos[1])
                            best_action = (action[0], action[1])
                        alpha = max(alpha, max_value)
                        if beta <= alpha:
                            ##print('beta cutoff')
                            break
                    if beta <= alpha:
                        ##print('beta cutoff')
                        break
                return best_pos, best_action, max_value
            else:
                min_value = float("inf")
                best_pos = None
                best_action = None
                for pos in self._generate_move(board):
                    for action in pos[2]:
                        board_clone = deepcopy(board)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        self._action_on_board(board_clone, pos, action)
                        step_value = self._current_eval(board_clone)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        #print('min->', depth, step_value, (pos[0], pos[1]), action, self.color)
                        if step_value < min_value:
                            min_value = step_value
                            best_pos = pos
                            best_action = action
                        elif step_value == min_value and random.random() <= 0.5:
                            min_value = step_value
                            best_pos = pos
                            best_action = action
                        beta = min(beta, min_value)
                        if beta <= alpha:
                            ##print('alpha cutoff')
                            break
                    if beta <= alpha:
                        ##print('alpha cutoff')
                        break
                return best_pos, best_action, min_value
        else:
            if fn == 'max':
                max_value = -float("inf")
                best_pos = None
                best_action = None
                for pos in self._generate_move(board):
                    for action in pos[2]:
                        board_clone = deepcopy(board)
                        #print('POS', (pos[0], pos[1]), 'ACK', action)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        self._action_on_board(board_clone, pos, action)
                        _, _, step_value = self._alpha_beta(depth - 1, board_clone, 'min', alpha, beta)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        #print('max->', depth, step_value, (pos[0], pos[1]), action, self.color)
                        if step_value > max_value:
                            max_value = step_value
                            best_pos = pos
                            best_action = action
                        elif step_value == max_value and random.random() <= 0.5:
                            max_value = step_value
                            best_pos = pos
                            best_action = action
                        alpha = max(alpha, max_value)
                        if beta <= alpha:
                            ##print('beta cutoff')
                            break
                    if beta <= alpha:
                        ##print('alpha cutoff')
                        break
                return best_pos, best_action, max_value
            else:
                min_value = float("inf")
                best_pos = None
                best_action = None
                for pos in self._generate_move(board):
                    for action in pos[2]:
                        board_clone = deepcopy(board)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        self._action_on_board(board_clone, pos, action)
                        _, _, step_value = self._alpha_beta( depth - 1, board_clone, 'max', alpha, beta)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        #print('min->', depth, step_value, (pos[0], pos[1]), action, self.color)
                        if step_value < min_value:
                            min_value = step_value
                            best_pos = (pos[0], pos[1])
                            best_action = (action[0], action[1])
                        elif step_value == min_value and random.random() <= 0.5:
                            min_value = step_value
                            best_pos = pos
                            best_action = action
                        beta = min(beta, min_value)
                        if beta <= alpha:
                            ##print('alpha cutoff')
                            break
                    if beta <= alpha:
                        ##print('alpha cutoff')
                        break
                return best_pos, best_action, min_value

    def _action_on_board(self, board, selected_piece, mouse_pos, hop=False):
        if hop == False:
            if board.location(mouse_pos[0], mouse_pos[1]).occupant != None and board.location(mouse_pos[0], mouse_pos[1]).occupant.color == self.game.turn:
                selected_piece = mouse_pos

            elif selected_piece != None and mouse_pos in board.legal_moves(selected_piece[0], selected_piece[1]):

                board.move_piece(
                    selected_piece[0], selected_piece[1], mouse_pos[0], mouse_pos[1])

                if mouse_pos not in board.adjacent(selected_piece[0], selected_piece[1]):
                    ##print("REMOVE", selected_piece, mouse_pos)
                    board.remove_piece(selected_piece[0] + (mouse_pos[0] - selected_piece[0]) //
                                       2, selected_piece[1] + (mouse_pos[1] - selected_piece[1]) // 2)
            return

    def _all_kings(self, board):
        for i in range(8):
            for j in range(8):
                occupant = board.location(i, j).occupant
                if(occupant is not None and occupant.king == False):
                    return False
        return True

    def _dist(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def _pieces_loc(self, board):
        player_pieces = []
        adversary_pieces = []
        for i in range(8):
            for j in range(8):
                occupant = board.location(i, j).occupant
                if(occupant is not None):
                    if(occupant.color == self.color):
                        player_pieces.append((i, j))
                    else:
                        adversary_pieces.append((i, j))
        return player_pieces, adversary_pieces

    def _sum_of_dist(self, board):
        player_pieces, adversary_pieces = self._pieces_loc(board)
        sum_of_dist = 0
        for pos in player_pieces:
            for adv in adversary_pieces:
                sum_of_dist += self._dist(pos[0], pos[1], adv[0], adv[1])
        if(len(player_pieces) >= len(adversary_pieces)):
            sum_of_dist *= -1
        return sum_of_dist

    def _farthest_piece(self, board):
        player_pieces, adversary_pieces = self._pieces_loc(board)
        farthest_dist = 0
        for pos in player_pieces:
            for adv in adversary_pieces:
                farthest_dist += max(farthest_dist, self._dist(pos[0], pos[1], adv[0], adv[1]))
        if(len(player_pieces) >= len(adversary_pieces)):
            farthest_dist *= -1
        return farthest_dist