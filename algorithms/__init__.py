from .random import get_move as random_get_move
from .mcts import get_move as mcts_get_move

def getAlgorithms():
    return {
        "random": random_get_move,
        "mcts": mcts_get_move
    }
