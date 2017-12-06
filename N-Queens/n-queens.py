import random
import numpy as np

n = 25
moves = 0
threat = 0
temp = 4000
stsh, shhc, sthc, rrhc, stsa, rrsa, bestNeighbour = ([],)*7

def createBoard(): # Creates the board using random
    board = []
    for x in range(n):
        board.append(random.randint(0, n-1))
    return board

def printBoard(title, board): # Prints the board in an easy to read way
    print(title)
    print(board)
    for x in range(n):
        for y in range(n):
            print("|", end="")
            if x==board[y]:
                print("Q", end="")
            else:
                print("-", end="")
        print("|")
    print("Threats:", countThreats(board))
    if "Start" not in title:
        print("Moves:", moves)

def countThreats(board): # Heuristic function
    threats = 0
    for i in range(n): # For loop starting after the current column i
        for j in range(i+1, n):
            offset = j-i  # Used to check diagonal threats
            # Check all threats
            if board[i]==board[j]-offset or board[i]==board[j]+offset or board[i]==board[j]:
                threats += 1
    return threats

def bestNeighbour(input): # Checks Neighbours to find the best neighbour
    tempNeighbour = list(input)
    for x in range(n):
        board = list(tempNeighbour) # Used to reset board so only one piece moves
        for y in range(-1, 3, 3): # For loop - back one forward two. As to check both vertical movements
            board[x]+=y
            if board[x]>=0 and board[x]<n: # Checks that numbers are on the board
                threats = countThreats(board)
                if threats<countThreats(tempNeighbour): # Used so you can check all neighbours without updating
                    tempNeighbour = list(board)
    return tempNeighbour

def hillClimb(input): # Climnbs hill for best answer. Has both annealing and steepest hill
    global moves, temp
    bestBoard, board = (list(input),)*2
    best = False
    while not best: # Stops when no better neighbour
        board = bestNeighbour(board)
        if countThreats(bestBoard) > countThreats(board): # Checks for any better board
            bestBoard = list(board)
            moves += 1
        else:
            best = True
    return bestBoard
            
def randomRestart(): # Restarts 500 times to find the best board
    start, bestBoard = (createBoard(),)*2
    for x in range(500):
        startBoard = createBoard()
        board = hillClimb(startBoard)
        if countThreats(board) < countThreats(bestBoard):
            bestBoard= list(board)
            start = list(startBoard)
            if countThreats(bestBoard)==0:
                break # Exit loop if optimal solution is found.
    return start, bestBoard

def annealHillClimb(input):
    global moves, temp
    bestBoard, board = (list(input),)*2
    change = False
    board = bestNeighbour(board)
    if countThreats(bestBoard) > countThreats(board): # Checks for any better board
        bestBoard = list(board)
        moves += 1
        change = True
    elif not change and temp>0: # Calculates annealing probability
        prob = np.exp(-countThreats(board)-countThreats(bestBoard)/temp)
        randomNo = random.uniform(0,1)
        if randomNo<prob:
            bestBoard = list(board)
            moves += 1
    return bestBoard

def annealing(): # Runs random restart annealing with temp of 4000
    start, bestBoard = (createBoard(),)*2
    global temp
    for x in range(10):
        temp = 4000
        while temp>0 and countThreats(bestBoard)>0:
            startBoard = createBoard()
            board = annealHillClimb(startBoard)
            if countThreats(board) < countThreats(bestBoard):
                bestBoard= list(board)
                start = list(startBoard)
                if countThreats(bestBoard)==0:
                    break
            temp -= 100
    return start, bestBoard

stsh = createBoard()
printBoard("Hill Climbing Start Board", stsh)
shhc = hillClimb(stsh)
printBoard("\nHill Climbing Best Board", shhc)
moves = 0
sthc, rrhc = randomRestart()
printBoard("\nRandom Restart Start Board", sthc)
printBoard("\nRandom Restart Best Board", rrhc)
moves = 0
stsa, rrsa = annealing()
printBoard("\nAnnealed Start Baord", stsa)
printBoard("\nAnnealed Best Board", rrsa)