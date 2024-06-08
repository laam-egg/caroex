from .random import get_move as random_get_move
from .mcts import get_move as mcts_get_move
from .minimax_enhanced import get_move_enhanced as minimax_enhanced_get_move
from .minimax_ab import get_move_minimax as minimax_ab_get_move

def getAlgorithms():
    return {
        "random": random_get_move,
        "mcts": mcts_get_move,
        "minimax_enhanced": minimax_enhanced_get_move,
        "minimax_ab": minimax_ab_get_move
    }
