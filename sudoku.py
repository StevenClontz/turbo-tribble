import random
import time
from constraint import *
import svgwrite

# check if problem has 0, 1, or (>=)2 solutions
def count_solutions_to(problem):
    solution_iter = problem.getSolutionIter()
    try:
        next(solution_iter)
    except:
        return 0
    try:
        next(solution_iter)
    except:
        return 1
    return 2

def latin_square():
    base = [
        '957613284',
        '483257196',
        '612849537',
        '178364952',
        '524971368',
        '369528741',
        '845792613',
        '291436875',
        '736185429',
    ]
    base = [[int(s) for s in row] for row in base]
    first = []
    for n in range(3):
        rows = base[3*n:3*n+3]
        random.shuffle(rows)
        first = first+rows
    transpose = list(map(list, zip(*first)))
    square = []
    for n in range(3):
        rows = transpose[3*n:3*n+3]
        random.shuffle(rows)
        square = square+rows
    return  {(x,y):square[x][y] for x in range(9) for y in range(9)}

def new_sudoku(square,givens):
    problem = Problem()
    for x in range(9):
        for y in range(9):
            if (x,y) in givens:
                problem.addVariables([(x,y)],[square[(x,y)]])
            else:
                problem.addVariables([(x,y)],range(1,10))
    for x in range(9):
        problem.addConstraint(AllDifferentConstraint(),[(x,y) for y in range(9)])
        problem.addConstraint(AllDifferentConstraint(),[(y,x) for y in range(9)])
    for x in range(3):
        for y in range(3):
            problem.addConstraint(AllDifferentConstraint(),[(3*x+m,3*y+n) for m in range(3) for n in range(3)])
    return problem

def print_sudoku(square,givens=None):
    for x in range(9):
        for y in range(9):
            if not(givens) or (x,y) in givens:
                print(square[(x,y)],end="")
            else:
                print(" ",end="")
        print()

# Set seed
random.seed(20240810)

# Set SVG size
CM = 35

times = []
for puz_num in range(99):
    start = time.time()
    try:
        with open(f"sudoku{puz_num:02}.txt") as f:
            lines = [line.rstrip() for line in f.readlines()]
            givens = [(x,y) for x in range(9) for y in range(9) if len(lines[x])>y and lines[x][y]!=' ']
    except:
        break
    square = latin_square()
    for _ in range(10000):
        sudoku = new_sudoku(square,givens)
        if count_solutions_to(sudoku) == 1:
            break
        else:
            square = latin_square()
    if count_solutions_to(sudoku) > 1:
        print('TOO MANY SOLUTIONS')
        break

    print(f"Puzzle {puz_num}")
    print_sudoku(square,givens)
    print()
    print("Solutions")
    for solution in sudoku.getSolutions():
        for x in range(9):
            for y in range(9):
                print(solution[(x,y)],end="")
            print()
        print()
    times.append(time.time()-start)

    # build SVG to save to file
    dwg = svgwrite.Drawing(f'sudoku{puz_num:02}.svg', size=(2*9*CM,2*9*CM), profile='tiny')
    for x in range(9-1):
        n = 2*(x+1)*CM
        dwg.add(dwg.line((0,n),(2*9*CM,n),stroke='gray'))
        dwg.add(dwg.line((n,0),(n,2*9*CM),stroke='gray'))
    for x in range(3):
        m = 2*3*x
        for y in range(3):
            n = 2*3*y
            dwg.add(dwg.rect((m*CM,n*CM),((m+6)*CM,(n+6)*CM),stroke='black',fill='none',stroke_width="3"))
    for x in range(9):
        for y in range(9):
            if (x,y) in givens:
                dwg.add(dwg.text(solution[(x,y)],y=[(2*x+1)*CM],x=[(2*y+1)*CM],color='gray',text_anchor="middle"))
    dwg.save()
    for x in range(9):
        for y in range(9):
            if (x,y) not in givens:
                dwg.add(dwg.text(solution[(x,y)],y=[(2*x+1)*CM],x=[(2*y+1)*CM],fill="red",text_anchor="middle"))
    dwg.saveas(f'sudoku{puz_num:02}_solution.svg')

print(times)