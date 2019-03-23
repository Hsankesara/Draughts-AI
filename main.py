import checkers


def main():
    game = checkers.Game()
    game.setup()
    while True:  # main game loop
        game.player_turn()
        game.update()
        game.player_turn()
        game.update()


if __name__ == "__main__":
    main()
    pass
