# Draughts-AI

## Introduction

The game of checkers is considered a complicated game with 10^20 possible legal positions in the English draughts version (8\*8 board) alone (much more on higher dimensions). In this attempt to create a game agent, a tree traversal approach has been used. This approach is not only fast but also efficient given that good heuristics are used. The agent has been created which is capable of playing the game of draughts or checkers with a remarkable win rate against average players. Draughts is a 1vs1 zero-sum game. Minimax or Minimax algorithm is best suited for such types of games. Following is the development procedure practised during the development of the project.

1. Implemented a basic Minimax Agent with limited depth.
2. Applied ⍺-β pruning.
3. Improved the evaluation functions.

<table>
    <tr>
        <td><img src="imgs/checker_gif_1.gif" alt="AI vs Player I"></td>
        <td><img src="imgs/checker_gif_4.gif" alt="AI vs Player II"></td>
    </tr>
    <tr>
        <td><img src="imgs/checker_gif_7.gif" alt="AI vs Player I"></td>
        <td><img src="imgs/checker_gif_8.gif" alt="AI vs AI II"></td>
    </tr>
</table>

## Evaluation Functions

Two types of evaluation functions have been used depending upon the state of the game. These are mid evaluation and end game evaluation function. Following is the report for the same.
List all the evaluation functions:

### Mid Evaluation

#### Piece to Value

> score = ∑Pi + 2 × ∑Ki - ∑OPi - 2 × ∑OKi

Where Pi and OPi are the player’s and Opponent’s Pawns and Ki and OKi are the player’s and Opponent’s Kings respectively.

#### Piece and Board part to value

> score = (5 × ∑PHPi + 7 × ∑EHPi + 10 × ∑Ki) - (5 × ∑PHOPi + 7 × ∑EHOPi + 10 × ∑OKi)

Where PHPi and PHOPi are the player’s and Opponent’s Pawns in their own respective halves and EHPi and EHOPi are their Pawns in their respective enemies’ halves.
Ki and OKi are the player’s and Opponent’s Kings respectively.

#### Piece and Row to value

> score = (∑[5 × (Pi) +ri ] + ∑[7 × (Ki) + ri ]) - ((∑[5(OPi) + rj] + ∑[7(OKi) + rj]))

Where Pi and OPi is the player’s and Opponent’s Pawns and Ki and OKi are the player’s and Opponent’s Kings respectively. rj, ri are the row number of the respective piece.

#### Piece and Board part to value (modified)

> score = (5 × ∑PHPi + 7 × ∑EHPi + 10 × ∑Ki) - (5 × ∑PHOPi + 7 × ∑EHOPi + 10 × ∑OKi) / n

Where PHPi and PHOPi is the player’s and Opponent’s Pawns in their own respective halves and EHPi and EHOPi are their Pawns in their respective enemies’ halves. Ki and OKi are the player’s and Opponent’s Kings respectively.
n is the number of pieces on the board.

### End Evaluation

#### Sum of Distances

Dij = Distance of ith King of player from jth King of the enemy.

> score = ∑∑Dij

where i belongs to all the player's pieces and j belongs to all the opponent's pieces

Minimise S if more number of pieces than opponent else maximise .

#### Farthest Piece

Dij = Distance of ith King of player from jth King of the enemy.

> score = max(∑Dij)

where i belongs to all the player's pieces and j belongs to all the opponent's pieces

Minimise Dmax if more number of pieces than opponent else maximise.

## How to run the code

First install Requirements

```
pip3 install -r requirements.txt
```

### Run the Game

```bash
python3 main.py
```

**You can tweak the parameters of the game bot from [main](main.py) file**

## Conclusion

1. Heuristics can be drastically improved by adding specific features.
2. The depth of the game tree has a significant influence on the quality of the computer player.
3. There's a tradeoff between calculation time and quality of the game.
4. It is not efficient to use Minimax without optimizations while with them it can be a good solution.
5. Alpha-Beta pruning is exponentially improving in comparison to Minimax as the depth grows.
6. Certain heuristics are clearly better than others but some of the “bad” ones still work well in some cases.

## References

1. Two player draughts game template has been taken from [Pygame-Checkers](https://github.com/everestwitman/Pygame-Checkers/)

## Contributing

Found a bug? Create an **[issue](https://github.com/Hsankesara/Draughts-AI/issues/new)**.

```

```
