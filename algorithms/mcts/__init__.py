import ctypes
import platform
from itertools import chain

import pathlib
DLL_PATH = pathlib.Path(__file__).parent.resolve() / "libmnks.so"

def get_move(board, size, team_role, line_length_to_win):
    if platform.system() == "Linux":
        libmnk = ctypes.CDLL(DLL_PATH)
        libmnk.getMove.restype = ctypes.c_int

        # Flatten the board
        ArrayOfSizeNxN = ctypes.c_char * (size * size)
        flattenedBoard = ArrayOfSizeNxN(*(ord(x) for x in chain.from_iterable(board)))

        # Board size
        N = ctypes.c_int(size)

        # Team role
        teamRole = ctypes.c_char(ord(team_role))

        # Line length to win
        lineLengthToWin = ctypes.c_int(line_length_to_win)

        # Whether this player is allowed to move first
        moveFirst = ctypes.c_bool(True) # always True, because the function is called only when it's this player's turn!

        # Analyze time per move, in seconds.
        # We currently set this according to board size.
        analyzeTime = ctypes.c_float(
             1.0 if size <=  5 else
             2.0 if size <=  7 else
             5.0 if size <= 10 else
            10.0 if size <= 15 else
            20.0 if size <= 17 else
            25.0 if size <= 19 else
            30.0
        )

        # out - Number of simulations performed
        out_numSimulations = ctypes.c_int(0)

        # out - The resultant move's row
        out_row = ctypes.c_int(0)

        # out - The resultant move's column
        out_col = ctypes.c_int(0)

        # out - The error message, if any
        out_error = ctypes.create_string_buffer(256)

        # FINALLY, call the C function !!!
        exitCode = libmnk.getMove(
            flattenedBoard,
            N,
            teamRole,
            lineLengthToWin,
            moveFirst,
            analyzeTime,
            ctypes.byref(out_numSimulations),
            ctypes.byref(out_row),
            ctypes.byref(out_col),
            out_error
        )

        if exitCode != 0:
            raise Exception(f"MCTS Error: {out_error.value.decode('utf-8')}")
        
        # print(f"MCTS: Number of simulations performed in {analyzeTime.value} seconds: {out_numSimulations.value}")
        
        return out_row.value, out_col.value
    else:
        raise Exception("MCTS is only supported on Linux at the moment; anyway, Windows will soon be.")
