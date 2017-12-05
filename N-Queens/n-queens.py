import random
import numpy as np

n = 8
moves = 0

def createBoard(): # Creates the board using random
    board = []
    for x in range(n):
        board.append(random.randint(0, n-1))
    return board
     
def countThreats(board): # Heuristic function
    threats = 0
    for i in range(n): # For loop starting after the current column i
        for j in range(i+1, n):
            offset = j-i  # Used to check diagonal threats
            # Check all threats
            if board[i]==board[j]-offset or board[i]==board[j]+offset or board[i]==board[j]:
                threats += 1
    return threats
    
def finalBoard(board): #Checks Neighbours to find the best neighbour
    bestThreat, tempThreat = (countThreats(board),)*2
    bestNeighbour, tempNeighbour = (list(board),)*2
    global moves
    moves = 0
    better = True
    while better: # Loops while there is better neighbours
        better = False
        for x in range(n):
            board = list(bestNeighbour) # Used to reset board so only one piece moves
            for y in range(-1, 3, 3): # For loop - back one forward two. As to check both vertical movements
                board[x]+=y
                if board[x]>=0 and board[x]<n: # Checks that numbers are on the board
                    threats = countThreats(board)
                    if threats<tempThreat: # Used so you can check all neighbours without updating
                        tempThreat = threats
                        tempNeighbour = list(board)
        if tempThreat<bestThreat: # Updates best baord after all neighbours are checked
            bestThreat = tempThreat
            bestNeighbour = list(tempNeighbour)
            better = True
            moves += 1
    return bestNeighbour

def randomRestart(board):
    bestBoard, tempBoard, firstBoard = (list(board),)*3
    bestThreats = countThreats(bestBoard)
    # Either loops works. For loop stops even without the best. While keeps going til it finds an answer
    for x in range (500):
    #while bestThreats>0:
        startBoard = createBoard()
        tempBoard = finalBoard(startBoard)
        threats = countThreats(tempBoard)
        if threats<bestThreats:
            bestThreats = threats
            bestBoard = list(tempBoard)
            firstBoard = list(startBoard)
            movements = moves
    print("\nRandom Restart Start Board")
    printBoard(firstBoard)
    print("Threats:", countThreats(firstBoard))
    print("\nRandom Restart Best Board")
    printBoard(bestBoard)
    print("Threats:", countThreats(bestBoard))
    print("Moves:", movements)
    
def annealing():
    board = createBoard()
    bestThreat, tempThreat = (countThreats(board),)*2
    bestNeighbour, tempNeighbour = (list(board),)*2
    temp = 8000
    moves = 0
    print("\nAnnealing Start Board")
    printBoard(board)
    print("Threats:", countThreats(board))
    while temp>0:
        change = False
        for x in range(n):
            board = list(bestNeighbour)
            for y in range(-1, 3, 3):
                board[x]+=y
                if board[x]>=0 and board[x]<n: # Checks that numbers are on the board
                    threats = countThreats(board)
                    if threats<tempThreat: # Used so you can check all neighbours without updating
                        tempThreat = threats
                        tempNeighbour = list(board)
                        change = True
                    elif temp>0: # If temp is greater than 0 it checks neighbour with annealing.
                        prob = np.exp(-threats-bestThreat/temp)
                        randomNo = random.uniform(0,1)
                        #print(-threats-bestThreat," | ", prob, "|", randomNo)
                        if randomNo < prob:
                            tempThreat = threats
                            tempNeighbour = list(board)
                            change=True
        if change==True:
            bestThreat = tempThreat
            bestNeighbour = list(tempNeighbour)
            moves+=1
        temp-=1
    print("\nAnnealing Start Board")
    printBoard(bestNeighbour)
    print("Threats:", countThreats(bestNeighbour))
    print("Moves:", moves)
                    
        

def printBoard(board): # Prints the board in an easy to read way
    print(board)
    for x in range(n-1):
        for y in range(n):
            print("|", end="")
            if x==board[y]:
                print("Q", end="")
            else:
                print("-", end="")
        print("|")

board = createBoard()
print("Hill Climbing Start Board")
printBoard(board)
print("Threats:", countThreats(board))
best = finalBoard(board)
print("\nHill Climbing Best Board")
printBoard(best)
print("Threats:", countThreats(best))
print("Moves:", moves)
randomRestart(board)
annealing()