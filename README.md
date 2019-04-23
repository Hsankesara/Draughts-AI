# Draughts-AI

## Introduction

The game of checkers is considered a complicated game with <img src="/tex/dbab8293b66086459d4464168538e091.svg?invert_in_darkmode&sanitize=true" align=middle width=29.54351234999999pt height=26.76175259999998pt/> possible legal positions in the English draughts version ( <img src="/tex/5786a8e466b20e868a9d801cbb6c4521.svg?invert_in_darkmode&sanitize=true" align=middle width=36.52961069999999pt height=21.18721440000001pt/> board) alone (much more on higher dimensions). In this attempt to create a game agent, a tree traversal approach has been used. This approach is not only fast but also efficient given that good heuristics are used. The agent has been created which is capable of playing the game of draughts or checkers with a remarkable win rate against average players. Draughts is a 1vs1 zero-sum game. Minimax or Minimax algorithm is best suited for such types of games. Following is the development procedure practised during the development of the project.

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

<img src="/tex/bf0a32a5f35b6300f9b8952604ae4499.svg?invert_in_darkmode&sanitize=true" align=middle width=273.21628949999996pt height=22.465723500000017pt/>

Where <img src="/tex/ef0de0b48cb187b636ae34b0aea8c1db.svg?invert_in_darkmode&sanitize=true" align=middle width=15.20454704999999pt height=22.465723500000017pt/> and <img src="/tex/9bb870c8b2e1c548bbfae64f1f287b01.svg?invert_in_darkmode&sanitize=true" align=middle width=28.199971799999986pt height=22.465723500000017pt/> are the player’s and opponent’s pawns and <img src="/tex/655ca15e2b101fb431577b12d4442580.svg?invert_in_darkmode&sanitize=true" align=middle width=18.61211054999999pt height=22.465723500000017pt/> and <img src="/tex/0bbd4f73c8c87e1bf32d188183e057ec.svg?invert_in_darkmode&sanitize=true" align=middle width=31.607535299999988pt height=22.465723500000017pt/> are the player’s and Opponent’s Kings respectively.

#### Piece and Board part to value

<img src="/tex/35f6dbbfe732e7296273ed13dd89bc75.svg?invert_in_darkmode&sanitize=true" align=middle width=613.57211025pt height=24.65753399999998pt/>

Where <img src="/tex/1506c48c2e589e3eb1276d619c08abc6.svg?invert_in_darkmode&sanitize=true" align=middle width=43.04128784999999pt height=22.465723500000017pt/> and <img src="/tex/0fca7f06c4e7b48a1626a0222076e53c.svg?invert_in_darkmode&sanitize=true" align=middle width=56.03671259999999pt height=22.465723500000017pt/> are the player’s and Opponent’s Pawns in their own respective halves and <img src="/tex/799e49842e138209ff82830d45ab7d28.svg?invert_in_darkmode&sanitize=true" align=middle width=43.28669234999999pt height=22.465723500000017pt/> and <img src="/tex/e06f07044ecba1e22f83d6b32b22410b.svg?invert_in_darkmode&sanitize=true" align=middle width=56.28211709999999pt height=22.465723500000017pt/> are their Pawns in their respective enemies halves.
<img src="/tex/655ca15e2b101fb431577b12d4442580.svg?invert_in_darkmode&sanitize=true" align=middle width=18.61211054999999pt height=22.465723500000017pt/> and <img src="/tex/0bbd4f73c8c87e1bf32d188183e057ec.svg?invert_in_darkmode&sanitize=true" align=middle width=31.607535299999988pt height=22.465723500000017pt/> are the player’s and Opponent’s Kings respectively.

#### Piece and Row to value

<img src="/tex/f2e6ee47dada6de07618ebd5e8e7dc06.svg?invert_in_darkmode&sanitize=true" align=middle width=535.8073182pt height=24.65753399999998pt/>

Where <img src="/tex/ef0de0b48cb187b636ae34b0aea8c1db.svg?invert_in_darkmode&sanitize=true" align=middle width=15.20454704999999pt height=22.465723500000017pt/> and <img src="/tex/9bb870c8b2e1c548bbfae64f1f287b01.svg?invert_in_darkmode&sanitize=true" align=middle width=28.199971799999986pt height=22.465723500000017pt/> is the player’s and Opponent’s Pawns and <img src="/tex/655ca15e2b101fb431577b12d4442580.svg?invert_in_darkmode&sanitize=true" align=middle width=18.61211054999999pt height=22.465723500000017pt/> and <img src="/tex/0bbd4f73c8c87e1bf32d188183e057ec.svg?invert_in_darkmode&sanitize=true" align=middle width=31.607535299999988pt height=22.465723500000017pt/> are the player’s and Opponent’s Kings respectively. <img src="/tex/212f899c5235a861a1f6146dc8d1582f.svg?invert_in_darkmode&sanitize=true" align=middle width=13.520829299999992pt height=14.15524440000002pt/>, <img src="/tex/3cf87ea38a615ed99e0232f8ed9431fe.svg?invert_in_darkmode&sanitize=true" align=middle width=12.067218899999991pt height=14.15524440000002pt/> are the row number of the respective piece.

#### Piece and Board part to value (modified)

<img src="/tex/06566d53dff3c19f365551bb5ba11162.svg?invert_in_darkmode&sanitize=true" align=middle width=442.48182660000003pt height=33.20539859999999pt/>

Where <img src="/tex/1506c48c2e589e3eb1276d619c08abc6.svg?invert_in_darkmode&sanitize=true" align=middle width=43.04128784999999pt height=22.465723500000017pt/> and <img src="/tex/0fca7f06c4e7b48a1626a0222076e53c.svg?invert_in_darkmode&sanitize=true" align=middle width=56.03671259999999pt height=22.465723500000017pt/> is the player’s and Opponent’s Pawns in their own respective halves and <img src="/tex/799e49842e138209ff82830d45ab7d28.svg?invert_in_darkmode&sanitize=true" align=middle width=43.28669234999999pt height=22.465723500000017pt/> and <img src="/tex/e06f07044ecba1e22f83d6b32b22410b.svg?invert_in_darkmode&sanitize=true" align=middle width=56.28211709999999pt height=22.465723500000017pt/> are their Pawns in their respective enemies’ halves. <img src="/tex/655ca15e2b101fb431577b12d4442580.svg?invert_in_darkmode&sanitize=true" align=middle width=18.61211054999999pt height=22.465723500000017pt/> and <img src="/tex/0bbd4f73c8c87e1bf32d188183e057ec.svg?invert_in_darkmode&sanitize=true" align=middle width=31.607535299999988pt height=22.465723500000017pt/> are the player’s and Opponent’s Kings respectively. <img src="/tex/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode&sanitize=true" align=middle width=9.86687624999999pt height=14.15524440000002pt/> is the number of pieces on the board.

### End Evaluation

#### Sum of Distances

<img src="/tex/68929b64645e6d7f6c50194224fea764.svg?invert_in_darkmode&sanitize=true" align=middle width=24.365003849999987pt height=22.465723500000017pt/> = Distance of ith king of the player from jth King of the adversary.

<img src="/tex/2dcc18a587457bfd193aaddbc8fdde0f.svg?invert_in_darkmode&sanitize=true" align=middle width=184.99128284999998pt height=31.75825949999999pt/>

where <img src="/tex/3c7e3568fa1625fede3ff436bfec732d.svg?invert_in_darkmode&sanitize=true" align=middle width=16.41942389999999pt height=14.15524440000002pt/> is total number of kings of the player in the board and <img src="/tex/3ff44da77b122337fa0f84a268ccf932.svg?invert_in_darkmode&sanitize=true" align=middle width=16.41942389999999pt height=14.15524440000002pt/> is total number of kings of the adversary in the board.

Minimise <img src="/tex/6c315990d0571215c3ee124e84a53921.svg?invert_in_darkmode&sanitize=true" align=middle width=38.31442724999999pt height=14.15524440000002pt/> if player has more number of pieces than adversary else maximise.

#### Farthest Piece

<img src="/tex/68929b64645e6d7f6c50194224fea764.svg?invert_in_darkmode&sanitize=true" align=middle width=24.365003849999987pt height=22.465723500000017pt/> = Distance of ith King of player from jth King of the enemy.

<img src="/tex/a0264dd532c39c450135dbf9adcaf5e5.svg?invert_in_darkmode&sanitize=true" align=middle width=286.8996504pt height=26.438629799999987pt/>

where <img src="/tex/3c7e3568fa1625fede3ff436bfec732d.svg?invert_in_darkmode&sanitize=true" align=middle width=16.41942389999999pt height=14.15524440000002pt/> is total number of kings of the player in the board and <img src="/tex/3ff44da77b122337fa0f84a268ccf932.svg?invert_in_darkmode&sanitize=true" align=middle width=16.41942389999999pt height=14.15524440000002pt/> is total number of kings of the adversary in the board.

Minimise <img src="/tex/6c315990d0571215c3ee124e84a53921.svg?invert_in_darkmode&sanitize=true" align=middle width=38.31442724999999pt height=14.15524440000002pt/> if player has more number of pieces than adversary else maximise.

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
