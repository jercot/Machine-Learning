import random
import numpy as np
import timeit

start = timeit.default_timer()
n = 8
moves = 0
temp = 1000
stsa, sahc, sthc, rrhc, stsa, rrsa, = ([],)*6

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
            if board[i]==board[j]-offset or board[i]==board[j]+offset or board[i]==board[j]: # Check all threats
                threats += 1
    return threats

def bestNeighbour(input): # Checks Neighbours to find the best neighbour
    tempNeighbour, rBoard = (list(input),)*2
    tempThreats = countThreats(tempNeighbour)
    for x in range(n):
        board = list(rBoard) # Used to reset board so only one piece moves
        for y in range(0, n-1): # For loop - back one forward two. As to check both vertical movements
            board[x]=y
            if board[x]>=0 and board[x]<n: # Checks that numbers are on the board
                threats = countThreats(board)
                if threats<tempThreats: # Used so you can check all neighbours without updating
                    tempNeighbour = list(board)
                    tempThreats = countThreats(tempNeighbour)
    return tempNeighbour

def hillClimb(input): # Climnbs hill for best answer. Has both annealing and steepest hill
    global moves, temp
    bestBoard, board = (list(input),)*2
    bestThreats = countThreats(bestBoard)
    best = False
    while not best: # Stops when no better neighbour
        board = bestNeighbour(board)
        threats = countThreats(board)
        if bestThreats>threats: # Checks for any better board
            bestBoard = list(board)
            bestThreats = threats
            moves += 1
        else:
            best = True
    return bestBoard
            
def randomRestart(): # Restarts 500 times to find the best board | I count the total moves in all genereated boards
    start, bestBoard = (createBoard(),)*2
    bestThreats = countThreats(bestBoard)
    for x in range(500):
        startBoard = createBoard()
        board = hillClimb(startBoard)
        threats = countThreats(board)
        if threats<bestThreats:
            bestBoard= list(board)
            start = list(startBoard)
            bestThreats = threats
            if bestThreats==0:
                break # Exit loop if optimal solution is found.
    return start, bestBoard

def annealHillClimb(input): # Same as above hillclimb but includes annealing
    global moves, temp
    bestBoard, board = (list(input),)*2
    bestThreats = countThreats(bestBoard)
    change = False
    board = bestNeighbour(board)
    threats = countThreats(board)
    if bestThreats>threats: # Checks for any better board
        bestBoard = list(board)
        bestThreats = threats
        moves += 1
        change = True
    elif not change and temp>0: # Calculates annealing probability
        prob = np.exp(-threats-bestThreats/temp)
        randomNo = random.uniform(0,1)
        if randomNo<prob:
            bestBoard = list(board)
            bestThreats = threats
            moves += 1
    return bestBoard

def annealing(): # Runs random restart annealing with temp of 4000
    start, bestBoard = (createBoard(),)*2
    bestThreats = countThreats(bestBoard)
    global temp
    for x in range(10): # Change this to one to remove the restart of Annealing
        temp = 100
        while temp>0 and bestThreats>0:
            startBoard = createBoard()
            board = annealHillClimb(startBoard)
            threats = countThreats(board)
            if threats<bestThreats:
                bestBoard= list(board)  
                bestThreats = threats
                start = list(startBoard)
                if bestThreats==0: # Exits inner loop at optimal
                    break
            temp -= 1
        if bestThreats==0: # Exits outter loop at optimal
            break
    return start, bestBoard

stsa = createBoard()
printBoard("Steepest Ascent Start Board", stsa)
sahc = hillClimb(stsa)
printBoard("\nSteepest Ascent Best Board", sahc)
moves = 0
sthc, rrhc = randomRestart()
printBoard("\nRandom Restart Start Board", sthc)
printBoard("\nRandom Restart Best Board", rrhc)
moves = 0
stsa, rrsa = annealing()
printBoard("\nAnnealed Start Baord", stsa)
printBoard("\nAnnealed Best Board", rrsa)

time_taken = timeit.default_timer() - start
unit = "Seconds"
if time_taken > 60:
    time_taken = time_taken / 60
    unit = "Minutes"
print("Time taken:", round(time_taken, 2), unit)