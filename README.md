### This project is used to make decisions of playing gobang with no forbidden hand mode.
\
### Goals
#### Use Minmax algorithm
#### Use Alpha-beta pruning
#### Use iterative deepening
#### Use Zobrist optimization
\
#### Test answer:
1.[x,y] \
2.[0, 4] \
3.[1, 4], [1, 0] \
4.[1, 3] \
5.[0, 8], [1, 8], [4, 8], [5, 8], [1, 5], [1, 9], [1, 10] \

#### model1.py: basic code, can't pass base test
#### model2.py: add evaluation fucntion, can pass base test
#### model3.py: add branches judgment for evaluated points
#### model4.py: advanced branches judgment
#### model5.py(not finished): give up evaluation_points, add evaluation_board and alpha-beta pruning
#### model6.py(behave worse than model4): modify model4, add more branches judgment and complete 2 layers searching
\
Model4.py is best now.
\
In model1.py I only use evaluate function to find 1 step next and choose max value. In model2.py I want to write Minmax algorithm to search further. First I test how long the Minmax algorithm needs to find scores of the whole chessboard without speeding up. After test, the increasing speed of time depends on the number of branches of each node(1 max layer:about 0.005s, 1 max layer + 1 min layer:about 0.5s, 2 max layers + 1 min layer:about 110s). \
bug fixed:model2.py alive FOUR is not detectived. Modify the evaluation function and counting score function to fix this bug. \
