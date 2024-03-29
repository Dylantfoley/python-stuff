"""This program is not fully correct. I need some help
getting the correct boolean expression for the 2 incorrect
variables"""

correct = [[".",".",".",".","4",".","9",".","."],
 [".",".","2","1",".",".","3",".","."],
 [".",".",".",".",".",".",".",".","."],
 [".",".",".",".",".",".",".",".","3"],
 [".",".",".","2",".",".",".",".","."],
 [".",".",".",".",".","7",".",".","."],
 [".",".",".","6","1",".",".",".","."],
 [".",".","9",".",".",".",".",".","."],
 [".",".",".",".",".",".",".","9","."]]

incorrect = [[".",".",".",".",".",".","5",".","."],
 [".",".",".",".",".",".",".",".","."],
 [".",".",".",".",".",".",".",".","."],
 ["9","3",".",".","2",".","4",".","."],
 [".",".","7",".",".",".","3",".","."],
 [".",".",".",".",".",".",".",".","."],
 [".",".",".","3","4",".",".",".","."],
 [".",".",".",".",".","3",".",".","."],
 [".",".",".",".",".","5","2",".","."]]
incorrect2 = [[".","4",".",".",".",".",".",".","."],
 [".",".","4",".",".",".",".",".","."],
 [".",".",".","1",".",".","7",".","."],
 [".",".",".",".",".",".",".",".","."],
 [".",".",".","3",".",".",".","6","."],
 [".",".",".",".",".","6",".","9","."],
 [".",".",".",".","1",".",".",".","."],
 [".",".",".",".",".",".","2",".","."],
 [".",".",".","8",".",".",".",".","."]]


def sudoku2(grid):
    n = len(grid)
    if n < 1:
        return False
    else:
        for i in range(0, n):
            horizontal = []
            vertical = []
            subgrid = []
            for k in range(0, n):
                # vertical check
                if grid[k][i] in vertical:
                    return False
                vertical.append(grid[k][i])
                vertical = [x for x in vertical if x != '.']
                if grid[i][k] in horizontal:
                    return False
                horizontal.append(grid[i][k])
                horizontal = [x for x in horizontal if x != '.']
        for x in (0, 3, 6):
            for y in (0, 3, 6):
                subgrid = grid[y][x:x + 3] + grid[y + 1][x:x + 3] + grid[y + 2][x:x + 3]
                subgrid = [x for x in subgrid if x != '.']
                if sorted(subgrid) != len(subgrid):
                    continue
                else:
                    return False
    return True
print(sudoku2(correct))
print(sudoku2(incorrect))
print(sudoku2(incorrect2))