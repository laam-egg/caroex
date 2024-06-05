# MCTS Algorithm

I wrote this algorithm in C++
([source code here](https://github.com/laam-egg/mnk)),
compiled the shared library `libmnks.so`
and put it straight to version control
of this project just for convenience.

The Python code then invokes
the exposed C function via the
foreign function interface `ctypes`.

Currently this `libmnks.so` is compiled
from [commit 6cd4b2f](https://github.com/laam-egg/mnk/commit/6cd4b2f86089dd6b25002284887f4c518a7a50e4).
