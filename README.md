# Machine Learning Snake Game
Snake game for Python that uses different algorithms and machine learning models
to acheive the best score possible


## Getting Started

There are two different ways to run it, with a GUI or through terminal

To run the GUI version with pygame, use:
```
python snake_gui.py
```

To run the terminal version, use:
```
python snake_console.py
```

## Algorithms

### Greedy
The game uses a greedy algorithm based of the Euclidean distance if all else fails
or if the other algorithms fail

### KNN
The game will use its previous data based of saved game data and the current gameboard
to figure out which move it will make.

It will rank each move based of the scores each move got on previous games

It chooses the best move with the highest average score for that move


## Authors

* **Tyler Lyczak**

## Future Updates

* **Neural Network to decide on movement**
