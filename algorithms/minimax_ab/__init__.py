
def check_winner(board, size, num=5):
    for i in range(size):
        for j in range(size-num+1):
            if all(board[i][j+k] == 'x' for k in range(num)):
                return 'x'
            if all(board[j+k][i] == 'x' for k in range(num)):
                return 'x'
            if all(board[i][j+k] == 'o' for k in range(num)):
                return 'o'
            if all(board[j+k][i] == 'o' for k in range(num)):
                return 'o'

    for i in range(size-num+1):
        for j in range(size-num+1):
            if all(board[i+k][j+k] == 'x' for k in range(num)):
                return 'x'
            if all(board[i+k][j+k] == 'o' for k in range(num)):
                return 'o'

    for i in range(size):
        for j in range(size):
            if board[i][j] == ' ':
                return None
    return 'tie'


def minimax_ab(board, depth, alpha, beta, is_maximizing, size, team_roles):
    # Check if the game is over
    result = check_winner(board, size)

    if result is not None:
        if result == team_roles:
            return 10 + depth
        elif result == 'tie':
            return 0 + depth
        else:
            return -10 + depth

    # If the depth is 0, return 0
    if depth == 0:
        return 0 + depth

    if is_maximizing:
        max_eval = -float('inf')
        for i in range(size):
            for j in range(size):
                if board[i][j] == ' ':
                    board[i][j] = team_roles
                    eval = minimax_ab(board, depth - 1, alpha,
                                      beta, False, size, team_roles)
                    board[i][j] = ' '
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(size):
            for j in range(size):
                if board[i][j] == ' ':
                    board[i][j] = 'o' if team_roles == 'x' else 'x'
                    eval = minimax_ab(board, depth - 1, alpha,
                                      beta, True, size, team_roles)
                    board[i][j] = ' '
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval


def get_move_minimax(board, size, team_roles, win_length=5):
    best_eval = -float('inf')
    # best_move = get_move(board, size, is_minimax=True)
    if (board[size//2][size//2] == ' '):
        return (size//2, size//2)
    best_move = None

    if best_move:
        return best_move

    for i in range(size):
        for j in range(size):
            if board[i][j] == ' ':
                board[i][j] = team_roles
                eval = minimax_ab(board, 4, -float('inf'),
                                  float('inf'), False, size, team_roles)
                board[i][j] = ' '
                if eval > best_eval:
                    best_eval = eval
                    best_move = (i, j)
    return best_move
