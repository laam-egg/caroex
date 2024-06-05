import jinja2
from os import makedirs
from shutil import copytree, rmtree
import multiprocessing
from copy import deepcopy
import json
import webbrowser

from algorithms import getAlgorithms

LINE_LENGTH_TO_WIN = 5

import time
if time.get_clock_info('perf_counter').monotonic:
    _realtime_func = time.perf_counter
else:
    _realtime_func = time.monotonic # less precise than time.perf_counter

def realtime() -> float:
    return _realtime_func()

class ResultExporter:
    def __init__(self) -> None:
        pass

    def export(self, matches, stats, experimentSetName: str):
        while True:
            try:
                makedirs("results/matchlog", exist_ok=False)
            except FileExistsError:
                print("ERROR: The results directory already exists.")
                print("Press ENTER to remove it, or Ctrl-C to cancel the whole operation.")
                input()
                rmtree("results")
                print("Removed the results directory.")
            else:
                break

        copytree("./templates/public", "./results/matchlog", dirs_exist_ok=True)

        allMatches = []
        for i, match in enumerate(matches):
            self._exportOneMatch(match, f"match-{i+1}.html")
            allMatches.extend(match)
        
        self._exportOneMatch(allMatches, "all-matches.html")

        self._exportIndex(experimentSetName, len(matches), stats, "index.html")

    def _exportOneMatch(self, gameInfoList, fileName):
        templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "match.jinja"
        template = templateEnv.get_template(TEMPLATE_FILE)
        templateVars = {
            "gameInfoListJSON": json.dumps(gameInfoList),
        }
        outputText = template.render(templateVars)

        with open(f"results/matchlog/{fileName}", "w") as f:
            f.write(outputText)
    
    def _exportIndex(self, experimentSetName: str, numMatches, stats, fileName):
        templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "index.jinja"
        template = templateEnv.get_template(TEMPLATE_FILE)
        templateVars = {
            "experimentSetName": experimentSetName,
            "numMatches": numMatches,
            "players": stats,
        }
        print(f"Num matches here: {numMatches}")
        outputText = template.render(templateVars)

        with open(f"results/matchlog/{fileName}", "w") as f:
            f.write(outputText)

def select_agent(teamNumber: int):
    print(f"Select an algorithm for team {teamNumber}:")
    algorithms = getAlgorithms()
    algorithmKeys = list(algorithms.keys())

    while True:
        for i, algorithmName in enumerate(algorithmKeys):
            print(f"{i + 1}. {algorithmName}")
        selection = int(input("Enter the number of the algorithm you want to use: "))
        if selection < 1 or selection > len(algorithmKeys):
            print("Invalid selection, try again.")
            continue
        break

    print(f"## TEAM {teamNumber} USES: {algorithmKeys[selection - 1]}")

    return {
        "name": algorithmKeys[selection - 1],
        "func": algorithms[algorithmKeys[selection - 1]]
    }

def move_callback(q: multiprocessing.Queue, agent, board, size, teamRole, lineLengthToWin):
    q.get()
    try:
        move = agent(board, size, teamRole, lineLengthToWin)
    except Exception as e:
        print("Error in move_callback:", e)
        q.put({ "move": None, "error": e })
        print("q.put done")
    else:
        q.put({ "move": move })

class MatchDriver:
    def __init__(self, roomId, matchId, team1Id, team2Id, team1Agent, team2Agent, size, timeLimit, initialScore1, initialScore2) -> None:
        self.roomId = str(roomId)
        self.matchId = str(matchId)
        self.team1Id = str(team1Id) + "+x"
        self.team2Id = str(team2Id) + "+o"
        self.agent1 = team1Agent
        self.agent2 = team2Agent
        self.size = size
        self.timeLimit = timeLimit
        self.board = self.generate_empty_board(self.size)
        self.turn = 1
        self.gameInfoHistory = []
        self.time1 = 0.0
        self.time2 = 0.0
        self.score1 = initialScore1
        self.score2 = initialScore2
        self.numMoves1 = 0
        self.numMoves2 = 0
    
    @staticmethod
    def generate_empty_board(size):
        return [[' ' for _ in range(size)] for _ in range(size)]
    
    def accept_move(self, move):
        if self.board[move[0]][move[1]] != ' ':
            return False
        self.board[move[0]][move[1]] = 'x' if self.turn == 1 else 'o'
        return True
    
    def check_endgame(self):
        # Check rows
        for i in range(self.size):
            for j in range(self.size - LINE_LENGTH_TO_WIN + 1):
                if all(self.board[i][j + k] == 'x' for k in range(LINE_LENGTH_TO_WIN)):
                    return 1
                if all(self.board[i][j + k] == 'o' for k in range(LINE_LENGTH_TO_WIN)):
                    return 2
        
        # Check columns
        for i in range(self.size):
            for j in range(self.size - LINE_LENGTH_TO_WIN + 1):
                if all(self.board[j + k][i] == 'x' for k in range(LINE_LENGTH_TO_WIN)):
                    return 1
                if all(self.board[j + k][i] == 'o' for k in range(LINE_LENGTH_TO_WIN)):
                    return 2
        
        # Check diagonals
        for i in range(self.size - LINE_LENGTH_TO_WIN + 1):
            for j in range(self.size - LINE_LENGTH_TO_WIN + 1):
                if all(self.board[i + k][j + k] == 'x' for k in range(LINE_LENGTH_TO_WIN)):
                    return 1
                if all(self.board[i + k][j + k] == 'o' for k in range(LINE_LENGTH_TO_WIN)):
                    return 2
                if all(self.board[i + k][j + LINE_LENGTH_TO_WIN - k - 1] == 'x' for k in range(LINE_LENGTH_TO_WIN)):
                    return 1
                if all(self.board[i + k][j + LINE_LENGTH_TO_WIN - k - 1] == 'o' for k in range(LINE_LENGTH_TO_WIN)):
                    return 2
        
        # Check for a draw
        if all(self.board[i][j] != ' ' for i in range(self.size) for j in range(self.size)):
            return 0
        
        return -1
    
    def play(self):
        q = multiprocessing.Queue()
        
        while True:
            q.put({ "move": None })
            if self.turn == 1:
                proc = multiprocessing.Process(target=move_callback, args=(q, self.agent1, self.board, self.size, 'x', LINE_LENGTH_TO_WIN))
            else:
                proc = multiprocessing.Process(target=move_callback, args=(q, self.agent2, self.board, self.size, 'o', LINE_LENGTH_TO_WIN))
            
            start = realtime()
            proc.start()
            timeout = self.timeLimit - (self.time1 if self.turn == 1 else self.time2)

            proc.join(timeout)
            if proc.is_alive():
                proc.kill()
                move = None
            else:
                entry = q.get()
                error = entry.get("error", None)
                if error is not None:
                    raise error
                move = entry["move"]
                if self.turn == 1:
                    self.numMoves1 += 1
                else:
                    self.numMoves2 += 1

            # move_callback(q, self.agent1, self.board, self.size, 'x', LINE_LENGTH_TO_WIN)
            # entry = q.get()
            # error = entry.get("error", None)
            # if error is not None:
            #     raise error
            # move = entry["move"]
            # if self.turn == 1:
            #     self.numMoves1 += 1
            # else:
            #     self.numMoves2 += 1
            end = realtime()

            if self.turn == 1:
                self.time1 += end - start
                if self.time1 >= self.timeLimit:
                    self.score2 += 1
                    self.gameInfoHistory.append({
                        "room_id": self.roomId,
                        "match_id": self.matchId,
                        "team1_id": self.team1Id,
                        "team2_id": self.team2Id,
                        "size": self.size,
                        "status": f"Team {self.team1Id} out of time, so team {self.team2Id} won",

                        "board": deepcopy(self.board),
                        "time1": self.time1,
                        "time2": self.time2,
                        "turn": self.turn,
                        "score1": self.score1,
                        "score2": self.score2,
                    })
                    return
            else:
                self.time2 += end - start
                if self.time2 >= self.timeLimit:
                    self.score1 += 1
                    self.gameInfoHistory.append({
                        "room_id": self.roomId,
                        "match_id": self.matchId,
                        "team1_id": self.team1Id,
                        "team2_id": self.team2Id,
                        "size": self.size,
                        "status": f"Team {self.team2Id} out of time, so team {self.team1Id} won",

                        "board": deepcopy(self.board),
                        "time1": self.time1,
                        "time2": self.time2,
                        "turn": self.turn,
                        "score1": self.score1,
                        "score2": self.score2,
                    })
                    return

            if move is None or not self.accept_move(move):
                if self.turn == 1:
                    self.score2 += 1
                    self.gameInfoHistory.append({
                        "room_id": self.roomId,
                        "match_id": self.matchId,
                        "team1_id": self.team1Id,
                        "team2_id": self.team2Id,
                        "size": self.size,
                        "status": f"Team ${self.team1Id} plays invalid move, so team {self.team2Id} won",

                        "board": deepcopy(self.board),
                        "time1": self.time1,
                        "time2": self.time2,
                        "turn": self.turn,
                        "score1": self.score1,
                        "score2": self.score2,
                    })
                    return
                else:
                    self.score1 += 1
                    self.gameInfoHistory.append({
                        "room_id": self.roomId,
                        "match_id": self.matchId,
                        "team1_id": self.team1Id,
                        "team2_id": self.team2Id,
                        "size": self.size,
                        "status": f"Team ${self.team2Id} plays invalid move, so team {self.team1Id} won",

                        "board": deepcopy(self.board),
                        "time1": self.time1,
                        "time2": self.time2,
                        "turn": self.turn,
                        "score1": self.score1,
                        "score2": self.score2,
                    })
                    return
            
            endgame = self.check_endgame()
            if endgame != -1:
                self.score1 += (1 if endgame == 1 else 0)
                self.score2 += (1 if endgame == 2 else 0)
                self.gameInfoHistory.append({
                    "room_id": self.roomId,
                    "match_id": self.matchId,
                    "team1_id": self.team1Id,
                    "team2_id": self.team2Id,
                    "size": self.size,
                    "status": f"Team {self.team1Id} wins" if endgame == 1 else f"Team {self.team2Id} wins" if endgame == 2 else "Draw",

                    "board": deepcopy(self.board),
                    "time1": self.time1,
                    "time2": self.time2,
                    "turn": self.turn,
                    "score1": self.score1,
                    "score2": self.score2,
                })
                return
            else:
                self.gameInfoHistory.append({
                    "room_id": self.roomId,
                    "match_id": self.matchId,
                    "team1_id": self.team1Id,
                    "team2_id": self.team2Id,
                    "size": self.size,
                    "status": None,

                    "board": deepcopy(self.board),
                    "time1": self.time1,
                    "time2": self.time2,
                    "turn": self.turn,
                    "score1": self.score1,
                    "score2": self.score2,
                })
            
            self.turn = 3 - self.turn

class ExperimentDriver:
    def __init__(self, agentInfoList, size, lineLengthToWin, timeLimit, numMatches):
        self.agentInfoList = [dict(**a, score=0) for a in agentInfoList]
        self.numMatches = numMatches
        self.stats = {}
        self.size = size
        global LINE_LENGTH_TO_WIN
        LINE_LENGTH_TO_WIN = self.lineLengthToWin = lineLengthToWin
        self.timeLimit = timeLimit
    
    def run(self):
        self.stats.clear()
        for a in self.agentInfoList:
            self.stats[a["name"]] = {
                "total_wins": 0,
                "total_time": 0,
                "total_moves": 0,
                "total_wins_as_first_player": 0,
                "num_matches_as_first_player": 0,
            }
        matches = []
        roomId = " vs ".join([a["name"] for a in self.agentInfoList])
        for i in range(self.numMatches):
            matchId = f"{roomId} (match {i+1})"
            print("Running match", i + 1, "...", end=" ")
            team1Index = i % 2
            team2Index = 1 - team1Index
            team1Id = self.agentInfoList[team1Index]["name"]
            team2Id = self.agentInfoList[team2Index]["name"]

            matchDriver = MatchDriver(roomId=roomId, matchId=matchId, team1Id=team1Id, team2Id=team2Id,
                team1Agent=self.agentInfoList[team1Index]["func"],
                team2Agent=self.agentInfoList[team2Index]["func"],
                size=self.size, timeLimit=self.timeLimit,
                initialScore1=self.agentInfoList[team1Index]["score"],
                initialScore2=self.agentInfoList[team2Index]["score"]
            )

            matchDriver.play()

            delta1 = matchDriver.score1 - self.agentInfoList[team1Index]["score"]
            delta2 = matchDriver.score2 - self.agentInfoList[team2Index]["score"]

            team1_won = team2_won = False
            if delta1 == 1:
                team1_won = True
            elif delta2 == 1:
                team2_won = True
            
            assert not(team1_won is True and team2_won is True), "this case should never happen"

            matches.append(matchDriver.gameInfoHistory)
            self.agentInfoList[team1Index]["score"] = matchDriver.score1
            self.agentInfoList[team2Index]["score"] = matchDriver.score2

            self.stats[self.agentInfoList[team1Index]["name"]]["total_time"] += (
                0 if len(matchDriver.gameInfoHistory) == 0 else matchDriver.gameInfoHistory[-1]["time1"]
            )
            self.stats[self.agentInfoList[team2Index]["name"]]["total_time"] += (
                0 if len(matchDriver.gameInfoHistory) == 0 else matchDriver.gameInfoHistory[-1]["time2"]
            )

            self.stats[self.agentInfoList[team1Index]["name"]]["total_moves"] += matchDriver.numMoves1
            self.stats[self.agentInfoList[team2Index]["name"]]["total_moves"] += matchDriver.numMoves2

            if team1_won:
                self.stats[self.agentInfoList[team1Index]["name"]]["total_wins"] += 1
                self.stats[self.agentInfoList[team1Index]["name"]]["total_wins_as_first_player"] += 1
            elif team2_won:
                self.stats[self.agentInfoList[team2Index]["name"]]["total_wins"] += 1
            
            self.stats[self.agentInfoList[team1Index]["name"]]["num_matches_as_first_player"] += 1

            print("Done")
        
        self.export_results(matches=matches, experimentSetName=roomId)
        print("DONE. Experiments' results rendered in ./results folder.")
        print("Opening in browser for you...")
        webbrowser.open("./results/matchlog/index.html")
    
    def export_results(self, matches, experimentSetName):
        resultExporter = ResultExporter()
        resultExporter.export(matches, self.stats, experimentSetName)

if __name__ == '__main__':
    ExperimentDriver(
        agentInfoList=[
            select_agent(1),
            select_agent(2),
        ],
        size=abs(int(input("Enter size: "))),
        lineLengthToWin=abs(int(input("Enter line length to win: "))),
        timeLimit=abs(float(input("Enter time limit (real number, in seconds): "))),
        numMatches=abs(int(input("Enter number of matches: "))),
    ).run()
