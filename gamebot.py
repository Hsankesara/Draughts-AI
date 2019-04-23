import pygame
import sys
from pygame.locals import *
import random
from copy import deepcopy
import math
from time import sleep
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
        self.eval_color = color
        if self.color == BLUE:
            self.adversary_color = RED
        else:
            self.adversary_color = BLUE
        self._current_eval = self._mid_eval
        self._end_eval_time = False
        self._count_nodes = 0

    def step(self, board, return_count_nodes=False):
        self._count_nodes = 0
        if(self._end_eval is not None and self._end_eval_time == False):
            if self._all_kings(board):
                print('END EVAL is on')
                self._end_eval_time = True
                self._current_eval = self._end_eval
        if self.method == 'random':
            self._random_step(board)
        elif self.method == 'minmax':
            self._minmax_step(board)
        elif self.method == 'alpha_beta':
            self._alpha_beta_step(board)
        if return_count_nodes:
            return self._count_nodes

    def _action(self, current_pos, final_pos, board):
        if current_pos is None:
            self.game.end_turn()
            # board.repr_matrix()
            # print(self._generate_all_possible_moves(board))
        # print(current_pos, final_pos, board.location(current_pos[0], current_pos[1]).occupant)
        if self.game.hop == False:
            if board.location(final_pos[0], final_pos[1]).occupant != None and board.location(final_pos[0], final_pos[1]).occupant.color == self.game.turn:
                current_pos = final_pos

            elif current_pos != None and final_pos in board.legal_moves(current_pos[0], current_pos[1]):

                board.move_piece(
                    current_pos[0], current_pos[1], final_pos[0], final_pos[1])

                if final_pos not in board.adjacent(current_pos[0], current_pos[1]):
                    board.remove_piece(current_pos[0] + (final_pos[0] - current_pos[0]) //
                                       2, current_pos[1] + (final_pos[1] - current_pos[1]) // 2)

                    self.game.hop = True
                    current_pos = final_pos
                    final_pos = board.legal_moves(
                        current_pos[0], current_pos[1], True)
                    if final_pos != []:
                        # print("HOP in Action", current_pos, final_pos)
                        self._action(current_pos, final_pos[0], board)
                    self.game.end_turn()

        if self.game.hop == True:
            if current_pos != None and final_pos in board.legal_moves(current_pos[0], current_pos[1], self.game.hop):
                board.move_piece(
                    current_pos[0], current_pos[1], final_pos[0], final_pos[1])
                board.remove_piece(current_pos[0] + (final_pos[0] - current_pos[0]) //
                                   2, current_pos[1] + (final_pos[1] - current_pos[1]) // 2)

            if board.legal_moves(final_pos[0], final_pos[1], self.game.hop) == []:
                self.game.end_turn()
            else:
                current_pos = final_pos
                final_pos = board.legal_moves(
                    current_pos[0], current_pos[1], True)
                if final_pos != []:
                    # print("HOP in Action", current_pos, final_pos)
                    self._action(current_pos, final_pos[0], board)
                self.game.end_turn()
        if self.game.hop != True:
            self.game.turn = self.adversary_color

    def _action_on_board(self, board, current_pos, final_pos, hop=False):
        if hop == False:
            if board.location(final_pos[0], final_pos[1]).occupant != None and board.location(final_pos[0], final_pos[1]).occupant.color == self.game.turn:
                current_pos = final_pos

            elif current_pos != None and final_pos in board.legal_moves(current_pos[0], current_pos[1]):

                board.move_piece(
                    current_pos[0], current_pos[1], final_pos[0], final_pos[1])

                if final_pos not in board.adjacent(current_pos[0], current_pos[1]):
                    # print("REMOVE", current_pos, final_pos)
                    board.remove_piece(current_pos[0] + (final_pos[0] - current_pos[0]) //
                                       2, current_pos[1] + (final_pos[1] - current_pos[1]) // 2)
                    hop = True
                    current_pos = final_pos
                    final_pos = board.legal_moves(current_pos[0], current_pos[1], True)
                    if final_pos != []:
                        # print("HOP in Action", current_pos, final_pos)
                        self._action_on_board(board, current_pos, final_pos[0],hop=True)
        else:
            # print(current_pos, final_pos)
            if current_pos != None and final_pos in board.legal_moves(current_pos[0], current_pos[1], hop):
                board.move_piece(current_pos[0], current_pos[1], final_pos[0], final_pos[1])
                board.remove_piece(current_pos[0] + (final_pos[0] - current_pos[0]) // 2, current_pos[1] + (final_pos[1] - current_pos[1]) // 2)

            if board.legal_moves(final_pos[0], final_pos[1], self.game.hop) == []:
                return
            else:
                current_pos = final_pos
                final_pos = board.legal_moves(current_pos[0], current_pos[1], True)
                if final_pos != []:
                    # print("HOP in Action", current_pos, final_pos)
                    self._action_on_board(board, current_pos, final_pos[0],hop=True)

    def _generate_move(self, board):
        for i in range(8):
            for j in range(8):
                if(board.legal_moves(i, j, self.game.hop) != [] and board.location(i, j).occupant != None and board.location(i, j).occupant.color == self.game.turn):
                    yield (i, j, board.legal_moves(i, j, self.game.hop))

    def _generate_all_possible_moves(self, board):
        possible_moves = []
        for i in range(8):
            for j in range(8):
                if(board.legal_moves(i, j, self.game.hop) != [] and board.location(i, j).occupant != None and board.location(i, j).occupant.color == self.game.turn):
                    possible_moves.append(
                        (i, j, board.legal_moves(i, j, self.game.hop)))
        return possible_moves

    def _random_step(self, board):
        possible_moves = self._generate_all_possible_moves(board)
        if possible_moves == []:
            self.game.end_turn()
            return
        random_move = random.choice(possible_moves)
        rand_choice = random.choice(random_move[2])
        self._action(random_move, rand_choice, board)
        return

    def _minmax_step(self, board):
        random_move, random_choice, _ = self._minmax(
            self.depth - 1, board, 'max')
        self._action(random_move, random_choice, board)
        return

    def _alpha_beta_step(self, board):
        random_move, random_choice, _ = self._alpha_beta(self.depth - 1, board, 'max', alpha=-float('inf'), beta=float('inf'))
        # print(self.eval_color, self.game.turn, self.game.hop)
        self._action(random_move, random_choice, board)
        # print(self.eval_color, self.game.turn, self.game.hop)
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
                        self._count_nodes += 1
                        step_value = self._current_eval(board_clone)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color

                        if step_value > max_value:
                            max_value = step_value
                            best_pos = pos
                            best_action = (action[0], action[1])
                        elif step_value == max_value and random.random() <= 0.5:
                            max_value = step_value
                            best_pos = (pos[0], pos[1])
                            best_action = (action[0], action[1])
                        if(step_value == -float("inf") and best_pos is  None):
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
                        self._count_nodes += 1
                        self._action_on_board(board_clone, pos, action)
                        step_value = self._current_eval(board_clone)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        if step_value < min_value:
                            min_value = step_value
                            best_pos = pos
                            best_action = action
                        elif step_value == min_value and random.random() <= 0.5:
                            min_value = step_value
                            best_pos = pos
                            best_action = action
                        if(step_value == float("inf") and best_pos is  None):
                            best_pos = (pos[0], pos[1])
                            best_action = (action[0], action[1])
                return best_pos, best_action, min_value
        else:
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
                        self._count_nodes += 1
                        if self._check_for_endgame(board_clone):
                            step_value = float("inf")
                        else:
                            _, _, step_value = self._minmax(depth - 1, board_clone, 'min')
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        # print('POS', (pos[0], pos[1]), 'ACK', action, 'MAX', depth, step_value)
                        if(step_value is None):
                            continue
                        # print('max->', depth, step_value, (pos[0], pos[1]), action, self.color)
                        if step_value > max_value:
                            max_value = step_value
                            best_pos = pos
                            best_action = action
                        elif step_value == max_value and random.random() <= 0.5:
                            max_value = step_value
                            best_pos = pos
                            best_action = action
                        if(step_value == -float("inf") and best_pos is  None):
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
                        # print('POS', (pos[0], pos[1]), 'ACK', action, 'MIN', depth)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        self._count_nodes += 1
                        self._action_on_board(board_clone, pos, action)
                        if self._check_for_endgame(board_clone):
                            step_value = -float("inf")
                        else:
                            _, _, step_value = self._minmax( depth - 1, board_clone, 'max')
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        if(step_value is None):
                            continue
                        if step_value < min_value:
                            min_value = step_value
                            best_pos = (pos[0], pos[1])
                            best_action = (action[0], action[1])
                        elif step_value == min_value and random.random() <= 0.5:
                            min_value = step_value
                            best_pos = pos
                            best_action = action
                        if(step_value == float("inf") and best_pos is  None):
                            best_pos = (pos[0], pos[1])
                            best_action = (action[0], action[1])
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
                        self._count_nodes += 1
                        self._action_on_board(board_clone, pos, action)
                        step_value = self._current_eval(board_clone)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        # print('max->', depth, step_value, (pos[0], pos[1]), action, self.color)
                        if step_value > max_value:
                            max_value = step_value
                            best_pos = pos
                            best_action = (action[0], action[1])
                        elif step_value == max_value and random.random() <= 0.5:
                            max_value = step_value
                            best_pos = (pos[0], pos[1])
                            best_action = (action[0], action[1])
                        if(step_value == -float("inf") and best_pos is  None):
                            best_pos = (pos[0], pos[1])
                            best_action = (action[0], action[1])
                        alpha = max(alpha, max_value)
                        if beta < alpha:
                            # print('beta cutoff')
                            break
                    if beta < alpha:
                        # print('beta cutoff')
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
                        self._count_nodes += 1
                        step_value = self._current_eval(board_clone)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        # print('min->', depth, step_value, (pos[0], pos[1]), action, self.color)
                        if step_value < min_value:
                            min_value = step_value
                            best_pos = pos
                            best_action = action
                        elif step_value == min_value and random.random() <= 0.5:
                            min_value = step_value
                            best_pos = pos
                            best_action = action
                        if(step_value == float("inf") and best_pos is  None):
                            best_pos = (pos[0], pos[1])
                            best_action = (action[0], action[1])
                        beta = min(beta, min_value)
                        if beta < alpha:
                            # print('alpha cutoff')
                            break
                    if beta < alpha:
                        # print('alpha cutoff')
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
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        self._action_on_board(board_clone, pos, action)
                        self._count_nodes += 1
                        if self._check_for_endgame(board_clone):
                            step_value = float("inf")
                        else:
                            _, _, step_value = self._alpha_beta(depth - 1, board_clone, 'min', alpha, beta)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        # print('POS', (pos[0], pos[1]), 'ACK', action, 'MAX', depth, step_value)
                        if(step_value is None):
                            continue
                        # print('max->', depth, step_value, (pos[0], pos[1]), action, self.color)
                        if step_value > max_value:
                            max_value = step_value
                            best_pos = pos
                            best_action = action
                        elif step_value == max_value and random.random() <= 0.5:
                            max_value = step_value
                            best_pos = pos
                            best_action = action
                        if(step_value == -float("inf") and best_pos is  None):
                            best_pos = (pos[0], pos[1])
                            best_action = (action[0], action[1])
                        alpha = max(alpha, max_value)
                        if beta <= alpha:
                            # print('beta cutoff')
                            break
                    if beta < alpha:
                        # print('alpha cu3toff')
                        break
                return best_pos, best_action, max_value
            else:
                min_value = float("inf")
                best_pos = None
                best_action = None
                for pos in self._generate_move(board):
                    for action in pos[2]:
                        board_clone = deepcopy(board)
                        # print('POS', (pos[0], pos[1]), 'ACK', action, 'MIN', depth)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        self._count_nodes += 1
                        self._action_on_board(board_clone, pos, action)
                        if self._check_for_endgame(board_clone):
                            step_value = -float("inf")
                        else:
                            _, _, step_value = self._alpha_beta( depth - 1, board_clone, 'max', alpha, beta)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        if(step_value is None):
                            continue
                        if step_value < min_value:
                            min_value = step_value
                            best_pos = (pos[0], pos[1])
                            best_action = (action[0], action[1])
                        elif step_value == min_value and random.random() <= 0.5:
                            min_value = step_value
                            best_pos = pos
                            best_action = action
                        # print('min->', depth, step_value, (pos[0], pos[1]), action, self.color)
                        if(step_value == float("inf") and best_pos is  None):
                            best_pos = (pos[0], pos[1])
                            best_action = (action[0], action[1])
                        beta = min(beta, min_value)
                        if beta < alpha:
                            # print('alpha cutoff')
                            break
                    if beta < alpha:
                        # print('alpha cutoff')
                        break
                return best_pos, best_action, min_value

    def _piece2val(self, board):
        score = 0
        for i in range(8):
            for j in range(8):
                occupant = board.location(i, j).occupant
                if(occupant is not None):
                    if(occupant.color == self.eval_color):
                        score += occupant.value
                    else:
                        score -= occupant.value
        return score

    def _piece_and_row2val(self, board):
        score = 0
        if(self.eval_color == RED):
            for i in range(8):
                for j in range(8):
                    occupant = board.location(i, j).occupant
                    if(occupant is not None):
                        if occupant.color == self.eval_color:
                            score += 5 + j + 2 * (occupant.king)
                        else:
                            score -= 5 + (8 - j) + 2 * (occupant.king)
        else:
            for i in range(8):
                for j in range(8):
                    occupant = board.location(i, j).occupant
                    if(occupant is not None):
                        if occupant.color == self.eval_color:
                            score += 5 + (8 - j) + 2 * (occupant.king)
                        else:
                            score -= 5 + j + 2 * (occupant.king)
        return score

    def _piece_and_board2val(self, board):
        score = 0
        if(self.eval_color == RED):
            for i in range(8):
                for j in range(8):
                    occupant = board.location(i, j).occupant
                    if(occupant is not None):
                        if occupant.color == self.eval_color and occupant.king:
                            score += 10
                        elif occupant.color != self.eval_color and occupant.king:
                            score -= 10
                        elif occupant.color == self.eval_color and j < 4:
                            score += 5
                        elif occupant.color != self.eval_color and j < 4:
                            score -= 7
                        elif occupant.color == self.eval_color and j >= 4:
                            score += 7
                        elif occupant.color != self.eval_color and j >= 4:
                            score -= 5
        else:
            for i in range(8):
                for j in range(8):
                    occupant = board.location(i, j).occupant
                    if(occupant is not None):
                        if occupant.color == self.eval_color and occupant.king:
                            score += 10
                        elif occupant.color != self.eval_color and occupant.king:
                            score -= 10
                        elif occupant.color == self.eval_color and j < 4:
                            score += 7
                        elif occupant.color != self.eval_color and j < 4:
                            score -= 5
                        elif occupant.color == self.eval_color and j >= 4:
                            score += 7
                        elif occupant.color != self.eval_color and j >= 4:
                            score -= 5
        return score

    def _piece_and_board_pov2val(self, board):
        score = 0
        num_pieces = 0
        if(self.eval_color == RED):
            for i in range(8):
                for j in range(8):
                    occupant = board.location(i, j).occupant
                    if(occupant is not None):
                        num_pieces += 1
                        if occupant.color == self.eval_color and occupant.king:
                            score += 10
                        elif occupant.color != self.eval_color and occupant.king:
                            score -= 10
                        elif occupant.color == self.eval_color and j < 4:
                            score += 5
                        elif occupant.color != self.eval_color and j < 4:
                            score -= 7
                        elif occupant.color == self.eval_color and j >= 4:
                            score += 7
                        elif occupant.color != self.eval_color and j >= 4:
                            score -= 5
        else:
            for i in range(8):
                for j in range(8):
                    occupant = board.location(i, j).occupant
                    if(occupant is not None):
                        num_pieces += 1
                        if occupant.color == self.eval_color and occupant.king:
                            score += 10
                        elif occupant.color != self.eval_color and occupant.king:
                            score -= 10
                        elif occupant.color == self.eval_color and j < 4:
                            score += 7
                        elif occupant.color != self.eval_color and j < 4:
                            score -= 5
                        elif occupant.color == self.eval_color and j >= 4:
                            score += 7
                        elif occupant.color != self.eval_color and j >= 4:
                            score -= 5
        return score / num_pieces

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
                    if(occupant.color == self.eval_color):
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

    def _check_for_endgame(self, board):
        for x in range(8):
            for y in range(8):
                if board.location(x, y).color == BLACK and board.location(x, y).occupant != None and board.location(x, y).occupant.color == self.game.turn:
                    if board.legal_moves(x, y) != []:
                        return False
        return True
