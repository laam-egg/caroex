RING = 1
SIZE = 6
WIN_VALUE = 1000000000

class Evaluation:
    def __init__(self):
        self.winValue = WIN_VALUE
        win = [
            [1, 1, 1, 1, 1]
        ]
        unCovered4 = [
            [0, 1, 1, 1, 1, 0],
        ]
        unCovered3 = [
            [0, 1, 1, 1, 0, 0],
            [0, 0, 1, 1, 1, 0],
            [0, 1, 0, 1, 1, 0],
            [0, 1, 1, 0, 1, 0],
            [1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1],
            [1, 1, 1, 0, 1],
            [1, 1, 0, 1, 1],
            [1, 0, 1, 1, 1],
            # [1, 1, 0, 1, 1, 1],
            # [1, 0, 1, 1, 1, 1],
            # [1, 1, 1, 0, 1, 1],
            # [1, 1, 1, 1, 0, 1],
            # [1, 0, 1, 1, 1, 1, 1], 
            # [1, 1, 0, 1, 1, 1, 1],
            # [1, 1, 1, 0, 1, 1, 1],
            # [1, 1, 1, 1, 0, 1, 1],
            # [1, 1, 1, 1, 1, 0, 1],
        ]
        unCovered2 = [
            [0, 0, 1, 1, 0, 0],
            [0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 0],
            [0, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0],
            [0, 1, 0, 0, 1, 0]
        ]
        covered4 = [
            [-1, 1, 0, 1, 1, 1],
            [-1, 1, 1, 0, 1, 1],
            [-1, 1, 1, 1, 0, 1],
            [-1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, -1],
            [1, 0, 1, 1, 1, -1],
            [1, 1, 0, 1, 1, -1],
            [1, 1, 1, 0, 1, -1]
        ]
        covered3 = [
            [-1, 1, 1, 1, 0, 0],
            [-1, 1, 1, 0, 1, 0],
            [-1, 1, 0, 1, 1, 0],
            [0, 0, 1, 1, 1, -1],
            [0, 1, 0, 1, 1, -1],
            [0, 1, 1, 0, 1, -1],
            [-1, 1, 0, 1, 0, 1, -1],
            [-1, 0, 1, 1, 1, 0, -1],
            [-1, 1, 1, 0, 0, 1, -1],
            [-1, 1, 0, 0, 1, 1, -1]
        ]
        allCombos = [win, unCovered4, unCovered3, unCovered2, covered4, covered3]
        for k in range(len(allCombos)):
            temp = []
            for j in range(len(allCombos[k])):
                tmp = []
                for i in range(len(allCombos[k][j])):
                    tmp.append(-allCombos[k][j][i])
                temp.append(tmp)
            for m in range(len(temp)):
                allCombos[k].append(temp[m])
        self.win, self.unCovered4, self.unCovered3, self.unCovered2, self.covered4, self.covered3 = allCombos
        # print(self.win, self.unCovered4, self.unCovered3, self.unCovered2, self.covered4, self.covered3)
                

    def value_combo(self, w, u2, u3, u4, c3, c4):
        if w > 0:
            return 1000000000
        if u4 > 0:
            return 100000000
        if c4 > 1:
            return 10000000
        if u3 > 0 and c4 > 0:
            return 1000000
        if u3 > 1:
            return 100000

        if u3 == 1:
            if u2 == 3:
                return 40000
            if u2 == 2:
                return 38000
            if u2 == 1:
                return 35000
            return 3450

        if c4 == 1:
            if u2 == 3:
                return 4500
            if u2 == 2:
                return 4200
            if u2 == 1:
                return 4100
            return 4050

        if c3 == 1:
            if u2 == 3:
                return 3400
            if u2 == 2:
                return 3300
            if u2 == 1:
                return 3100

        if c3 == 2:
            if u2 == 2:
                return 3000
            if u2 == 1:
                return 2900

        if c3 == 3:
            if u2 == 1:
                return 2800

        if u2 == 4:
            return 2700
        if u2 == 3:
            return 2500
        if u2 == 2:
            return 2000
        if u2 == 1:
            return 1000
        return 0

    def value_position(self, arr1, arr2, arr3, arr4):
        w = 0
        u2 = 0
        u3 = 0
        u4 = 0
        c3 = 0
        c4 = 0
        allArr = [arr1, arr2, arr3, arr4]
        for i in range(len(allArr)):
            if self.is_any_in_arrays(self.win, allArr[i]):
                w += 1
                continue
            if self.is_any_in_arrays(self.covered4, allArr[i]):
                c4 += 1
                continue
            if self.is_any_in_arrays(self.covered3, allArr[i]):
                c3 += 1
                continue
            if self.is_any_in_arrays(self.unCovered4, allArr[i]):
                u4 += 1
                continue
            if self.is_any_in_arrays(self.unCovered3, allArr[i]):
                u3 += 1
                continue
            if self.is_any_in_arrays(self.unCovered2, allArr[i]):
                u2 += 1
        return self.value_combo(w, u2, u3, u4, c3, c4)
        
    def is_any_in_arrays(self, combos, arr):
        for i in range(len(combos)):
            if self.find_arr(arr, combos[i]):
                return True
        return False
    
    def find_arr(self, arr1, arr2):
        fCount = len(arr1)
        sCount = len(arr2)
        for i in range(fCount - sCount + 1):
            if arr1[i:i + sCount] == arr2:
                return True
        return False
    
    def get_combo(self, board, size, x, y, dx, dy):
        player = board[x][y]
        combo = [player]
        for i in range(1, 5):
            u = x + i * dx
            v = y + i * dy
            if u < 0 or u >= size or v < 0 or v >= size:
                break
            combo.append(board[u][v])
            if board[u][v] == -player:
                break
            
        for i in range(1, 5):
            u = x - i * dx
            v = y - i * dy
            if u < 0 or u >= size or v < 0 or v >= size:
                break
            combo = [board[u][v]] + combo
            if board[u][v] == -player:
                break
        return combo
    
    def evaluate(self, board, size, lastMove):
        i, j = lastMove
        player = board[i][j]
        # print(board)
        # print(player)
        # print(lastMove)
        playerVal = self.value_position(self.get_combo(board, size, i, j, 1, 0),
                                        self.get_combo(board, size, i, j, 0, 1),
                                        self.get_combo(board, size, i, j, 1, 1),
                                        self.get_combo(board, size, i, j, 1, -1))
        board[i][j] = -player
        opponentVal = self.value_position(self.get_combo(board, size, i, j, 1, 0),    
                                        self.get_combo(board, size, i, j, 0, 1),
                                        self.get_combo(board, size, i, j, 1, 1),
                                        self.get_combo(board, size, i, j, 1, -1))
        return 2 * playerVal + opponentVal
        
evaluation = Evaluation()        


def get_childs(board, size):
    candidates = []
    for i in range(size):
        for j in range(size):
            if board[i][j] != 0:
                for k in range(i - RING, i + RING + 1):
                    for l in range(j - RING, j + RING + 1):
                        if k >= 0 and l >= 0 and k < size and l < size:
                            if board[k][l] == 0:
                                curPoint = [k, l]
                                if curPoint not in candidates:
                                    candidates.append(curPoint)
    
    return candidates

def minimax_ab_enhanced(board, size, depth, isMaximizing, alpha, beta, lastMove, player):
    value = evaluation.evaluate(board, size, lastMove)
    if isMaximizing:    
        value = -value
    if depth == 0 or abs(value) >= WIN_VALUE:
        return value
    child = get_childs(board, size)
    
    if len(child) == 0:
        return 0
    
    bestValue = -WIN_VALUE if isMaximizing else WIN_VALUE
    for u, v in child:
        newBoard = [row[:] for row in board]
        newBoard[u][v] = player
        value = minimax_ab_enhanced(newBoard, size, depth - 1, not isMaximizing, alpha, beta, [u, v], -player)
        if isMaximizing:
            alpha = max(alpha, value)
            bestValue = max(bestValue, value)
        else:
            beta = min(beta, value)
            bestValue = min(bestValue, value)   
        if alpha >= beta:
            break
        
    return bestValue

def convert_board(board, size):
    cnt_move = 0
    newBoard = [[0] * size for _ in range(size)]    
    for i in range(size):
        for j in range(size):
            if board[i][j] == ' ':
                continue
            newBoard[i][j] = 1 if board[i][j] == 'x' else -1
            cnt_move += 1
    
    return newBoard, cnt_move

def get_move_enhanced(board, size, player, winLength):
    board, cnt_move = convert_board(board, size)
    # print(board)
    # exit(0)
    childs = get_childs(board, size)
    player = 1 if player == 'x' else -1
    
    if len(childs) == 0 or (cnt_move == 1 and board[size // 2][size // 2] == 0):
        return (size // 2, size // 2)
    bestMove = None
    bestValue = -WIN_VALUE
    
    for u, v in childs:
        newBoard = [row[:] for row in board]
        newBoard[u][v] = player
        value = minimax_ab_enhanced(newBoard, size, 0, False, 5* -WIN_VALUE, 5* WIN_VALUE, [u, v], -player)
        if value > bestValue:
            bestValue = value
            bestMove = (u, v)
            
    return bestMove
# evaluation = Evaluation()
# board = [['x', 'x', 'x', ' ', ' ', ' '], 
#          ['o', 'o', ' ', 'o', 'o', ' '], 
#          [' ', ' ', 'x', 'x', ' ', ' '], 
#          ['x', 'x', ' ', 'o', ' ', 'x'], 
#          ['x', 'x', 'o', 'x', ' ', 'x'], 
#          ['o', ' ', ' ', ' ', ' ', 'x']]

# board = [[1, 1, 1, 1, 1, 0], 
#          [-1, -1, 1, -1, 0, 0], 
#          [0, 0, 1, 1, 0, 0], 
#          [1, 1, 0, -1, 0, 1], 
#          [1, 1, -1, 1, 0, 1], 
#          [-1, 0, 0, 0, 1, 1]]
# preboard = [[1, 1, 1, 1, 0, 0], 
#          [-1, -1, -1, -1, 0, 0], 
#          [0, 0, 1, 1, 0, 0], 
#          [1, 1, 0, -1, 0, 1], 
#          [1, 1, -1, 1, 0, 1], 
#          [-1, 0, 0, 0, 1, 1]]
# print(evaluation.get_combo(board, 6, 1, 0, 1, 1, 1))
# evaluation.evaluate(preboard, board, 6)
# print(evaluation.is_any_in_arrays(evaluation.win, [0, 0, -1, -1, -1, -1, -1, 0]))
# print(get_childs(board, 6, 1)[0])
# board = [[' '] * SIZE for _ in range(SIZE)]
# u, v = get_move_enhanced(board, SIZE, -1)
# print(u, v)