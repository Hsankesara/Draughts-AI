import checkers
import gamebot
from time import sleep
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


def main():
    for _ in range(10):
        game = checkers.Game(loop_mode=True)
        game.setup()
        bot = gamebot.Bot(game, RED, mid_eval='piece2val',
                          end_eval='sum_of_dist', method='minmax', depth=3)
        random_bot_blue = gamebot.Bot(
            game, BLUE, mid_eval='piece_and_board_pov', method='alpha_beta', depth=3, end_eval='sum_of_dist')
        while True:  # main game loop
            if game.turn == BLUE:
                # print('BLUE')
                game.player_turn()
                # random_bot_blue.step(game.board)
                game.update()
            else:
                # print('RED')
                bot.step(game.board)
                game.update()
                # print('####################')
            if game.endit:
                break
        print('****************')


if __name__ == "__main__":
    main()
    pass
