# m,n,k-game experiment conductor (caroex)

A tool to evaluate the correctness and
effectiveness of algorithms solving
[m,n,k-games](https://en.wikipedia.org/wiki/M,n,k-game).
Currently, only the case `m = n` is
supported.

This project is inspired by [this one](https://github.com/nnphuc/UET_AICaroGame).

## Setup

```sh
git clone https://github.com/laam-egg/caroex.git
cd caroex
virtualenv venv -p $(which python3.12)
source ./venv/bin/activate
pip install -r requirements.txt
```

## Run the Experiment Conductor

```sh
cd caroex
python app.py
```

You will be prompted for experiment parameters
like this:

```plain
Select an algorithm for team 1:
1. random
2. mcts
Enter the number of the algorithm you want to use: 1
## TEAM 1 USES: random
Select an algorithm for team 2:
1. random
2. mcts
Enter the number of the algorithm you want to use: 2
## TEAM 2 USES: mcts
Enter size: 15
Enter line length to win: 5
Enter time limit (real number, in seconds): 100
Enter number of matches: 30
```

After the conductor finishes, results are dumped
into the `./results/matchlog` directory. You
can open the `index.html` file in there directly
to view the statistics as well as how the games
were actually played.

## Add your own Algorithm

Go to the `algorithms` folder to add
your own algorithm.

There are some predefined algorithms
serving as examples for you.

Basically, you need to expose a Python
function defined as follows:

```py
def get_move(board, size, team_role, line_length_to_win):
    ...
```

where:

- `size` is the size (N) of the board,

- `board` is a two-dimensional array of size
    NxN, whose each element is a string `"x"`,
    `"o"`, or `" "` (one space).

- The `team_role` parameter is your team role
    in the game, which can be either `"x"` or
    `"o"`.

- The `line_length_to_win` parameter is the
    number of horizontally, vertically, or
    diagonally consecutive marks must be
    made by a player in order to win.

Then, you need to *register* your algorithm
in the file `./algorithms/__init__.py`.

Re-run the experiment conductor, and you will
see your algorithm listed as an option for
each team.

If your algorithm is selected, your function
will automatically be called when it's your
turn.

## License

[The Unlicense](./LICENSE.txt).
