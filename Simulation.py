import random
import math
from numpy import False_ #both are for rolling a die
import xlsxwriter as xw #write the statistic in a xlsx file

colors = (0, 1, 2, 3) #represents for players

'''
roll a die
return a random number from 1, 2, 3, 4, 5, 6
'''
def rolling():
    return math.floor(6 * random.random() + 1)

'''
try to start a plane
if succeed, return true, if not, return false
'''
def tryStart(planes, color, roll):
    if type(roll) != int:
        raise TypeError("roll should be an integer")
    elif roll > 6 or roll < 1:
        raise ValueError("roll should be from 1 to 6")
    elif color not in colors:
        raise ValueError("invalid color code")
    elif roll >= 5: 
        for i in range(4):
            if color * 10 + i in planes.keys():
                if planes[color * 10 + i] == -2:
                    planes[color * 10 + i] == -1
                    return True
    return False

'''
move a plane in specific roll
'''
def move(planes, plane, roll):
    if type(roll) != int:
        raise TypeError("roll should be an integer")
    elif roll > 6 or roll < 1:
        raise ValueError("roll should be from 1 to 6")
    elif plane not in planes:
        raise ValueError("invalid color code")
    planes[plane] += roll
    color = plane // 10
    if planes[plane] <= 50:
        for i in planes.keys():
            currentColor = i // 10
            if (planes[plane] - color * 13) % 52 == (planes[i] - currentColor * 13) % 52:
                planes[i] == -2 
        if planes[plane] == 18:
            planes[plane] = 30
            counterColor = (color + 2) % 4
            for i in range(4):
                if counterColor * 10 + i in planes.keys():
                    if planes[counterColor * 10 + i] == 53:
                        planes[counterColor * 10 + i] = -2
            for i in planes.keys():
                currentColor = i // 10
                if (planes[plane] - color * 13) % 52 == (planes[i] - currentColor * 13) % 52:
                    planes[i] == -2 
    else:
        if planes[plane] > 56:
            planes[plane] = 56 * 2 - planes[plane]
        if planes[plane] == 56:
            del planes[plane]

'''
get the sequence of the move to judge that which move should be applied first
'''
def getMoveSeq(planes, plane, roll):
    if type(roll) != int:
        raise TypeError("roll should be an integer")
    elif roll > 6 or roll < 1:
        raise ValueError("roll should be from 1 to 6")
    elif plane not in planes:
        raise ValueError("invalid color code")
    seq = 0
    intention = planes[plane] + roll
    color = plane // 10
    if intention <= 50:
        for i in planes.keys():
            currentColor = i // 10
            if (intention - color * 13) % 52 == (planes[i] - currentColor * 13) % 52:
                if currentColor == color:
                    seq -= 2
                else:
                    seq += 2
        if intention == 18:
            intention = 30
            seq += 1
            counterColor = (color + 2) % 4
            for i in range(4):
                if counterColor * 10 + i in planes.keys():
                    if planes[counterColor * 10 + i] == 53:
                        seq += 2
            for i in planes.keys():
                currentColor = i // 10
                if (intention - color * 13) % 52 == (planes[i] - currentColor * 13) % 52:
                    if currentColor == color:
                        seq -= 2
                    else:
                        seq += 2
    else:
        if planes[plane] > 56:
            seq -= 1
        if planes[plane] == 56:
            seq += 10
    return seq        
    
'''
check whether the game has ended
'''
def end(planes):
    winner = 0
    for i in range(4):
        winner = 1
        for j in range(4):
            if i * 10 + j in planes.keys():
                winner = 0
        if winner == 1:
            return True
    return False

'''
return the winner
'''
def winner(planes):
    if not end(planes):
        raise Exception("not end")
    else:
        winner = 0
        for i in range(4):
            winner = 1
            for j in range(4):
                if i * 10 + j in planes.keys():
                    winner = 0
            if winner == 1:
                return i
    raise Exception("no winner")

'''
move with strategy A
'''
def A(planes, color, roll):
    if type(roll) != int:
        raise TypeError("roll should be an integer")
    elif roll > 6 or roll < 1:
        raise ValueError("roll should be from 1 to 6")
    elif color not in colors:
        raise ValueError("invalid color code")
    max = -1
    for i in range(4):
        if color * 10 + i in planes.keys():
            if max == -1:
                max = i
            elif planes[color * 10 + i] > planes[color * 10 + max]:
                max = i
    move(planes, color * 10 + max, roll)

'''
move with strategy B
'''
def B(planes, color, roll):
    if type(roll) != int:
        raise TypeError("roll should be an integer")
    elif roll > 6 or roll < 1:
        raise ValueError("roll should be from 1 to 6")
    elif color not in colors:
        raise ValueError("invalid color code")
    max = -1
    for i in range(4):
        if color * 10 + i in planes.keys() and getMoveSeq(planes, color * 10 + i, roll) >= -1:
            if max == -1:
                max = i
            elif planes[color * 10 + i] > planes[color * 10 + max]:
                max = i
    if max == -1:
        A(planes, color, roll)
    else:
        move(planes, color * 10 + max, roll)

'''
move with strategy C
'''
def C(planes, color, roll):
    if type(roll) != int:
        raise TypeError("roll should be an integer")
    elif roll > 6 or roll < 1:
        raise ValueError("roll should be from 1 to 6")
    elif color not in colors:
        raise ValueError("invalid color code")
    max = -1
    for i in range(4):
        if color * 10 + i in planes.keys() and getMoveSeq(planes, color * 10 + i, roll) >= 3:
            if max == -1:
                max = i
            elif planes[color * 10 + i] > planes[color * 10 + max]:
                max = i
    if max == -1:
        for i in range(4):
            if color * 10 + i in planes.keys() and getMoveSeq(planes, color * 10 + i, roll) >= 2:
                if max == -1:
                    max = i
                elif planes[color * 10 + i] > planes[color * 10 + max]:
                    max = i
    if max == -1:
        B(planes, color, roll)
    else:
        move(planes, color * 10 + max, roll)

'''
move with strategy D
'''
def D(planes, color, roll):
    if type(roll) != int:
        raise TypeError("roll should be an integer")
    elif roll > 6 or roll < 1:
        raise ValueError("roll should be from 1 to 6")
    elif color not in colors:
        raise ValueError("invalid color code")
    max = -1
    for i in range(4):
        if color * 10 + i in planes.keys() and getMoveSeq(planes, color * 10 + i, roll) >= 3:
            if max == -1:
                max = i
            elif planes[color * 10 + i] > planes[color * 10 + max]:
                max = i
    if max == -1:
        for i in range(4):
            if color * 10 + i in planes.keys() and getMoveSeq(planes, color * 10 + i, roll) >= 2:
                if max == -1:
                    max = i
                elif planes[color * 10 + i] > planes[color * 10 + max]:
                    max = i
    if max == -1:
        for i in range(4):
            if color * 10 + i in planes.keys() and getMoveSeq(planes, color * 10 + i, roll) >= 0:
                if max == -1:
                    max = i
                elif planes[color * 10 + i] > planes[color * 10 + max]:
                    max = i
    if max == -1:
        B(planes, color, roll)
    else:
        move(planes, color * 10 + max, roll)

'''
move with strategy E
'''
def E(planes, color, roll):
    if type(roll) != int:
        raise TypeError("roll should be an integer")
    elif roll > 6 or roll < 1:
        raise ValueError("roll should be from 1 to 6")
    elif color not in colors:
        raise ValueError("invalid color code")
    max = -1
    for i in range(4):
        if color * 10 + i in planes.keys() and getMoveSeq(planes, color * 10 + i, roll) >= 3:
            if max == -1:
                max = i
            elif planes[color * 10 + i] > planes[color * 10 + max]:
                max = i
    if max == -1:
        for i in range(4):
            if color * 10 + i in planes.keys() and getMoveSeq(planes, color * 10 + i, roll) >= 2:
                if max == -1:
                    max = i
                elif planes[color * 10 + i] > planes[color * 10 + max]:
                    max = i
    if max == -1:
        for i in range(4):
            if color * 10 + i in planes.keys() and getMoveSeq(planes, color * 10 + i, roll) >= 1:
                if max == -1:
                    max = i
                elif planes[color * 10 + i] > planes[color * 10 + max]:
                    max = i
    if max == -1:
        for i in range(4):
            if color * 10 + i in planes.keys() and getMoveSeq(planes, color * 10 + i, roll) >= 0:
                if max == -1:
                    max = i
                elif planes[color * 10 + i] > planes[color * 10 + max]:
                    max = i
    if max == -1:
        B(planes, color, roll)
    else:
        move(planes, color * 10 + max, roll)

'''
play a game and return the winner
'''
def newGame(strategy, bot):
    planes = {}
    for i in range(16):
        planes[(i // 4) * 10 + i % 4] = -2
    moveColor = 0
    while not end(planes):
        roll = rolling()
        if not tryStart(planes, moveColor, roll):
            if moveColor == 0:
                if strategy == 'A':
                    A(planes, moveColor, roll)
                elif strategy == 'B':
                    B(planes, moveColor, roll)
                elif strategy == 'C':
                    C(planes, moveColor, roll)
                elif strategy == 'D':
                    D(planes, moveColor, roll)
                elif strategy == 'E':
                    E(planes, moveColor, roll)
            else:
                if bot == 'A':
                    A(planes, moveColor, roll)
                elif bot == 'B':
                    B(planes, moveColor, roll)
                elif bot == 'C':
                    C(planes, moveColor, roll)
                elif bot == 'D':
                    D(planes, moveColor, roll)
                elif bot == 'E':
                    E(planes, moveColor, roll)
            moveColor += 1
            if moveColor >= 4:
                moveColor = 0
    return winner(planes)


fileName = "Simulation Result3.xlsx" #the name of the xlsx file
workbook = xw.Workbook(fileName) #create a xlsx file
worksheet1 = workbook.add_worksheet("sheet1") #add a worksheet in the file
worksheet1.activate() #activate the worksheet
title = ["my", "bot", "win rate"]
worksheet1.write_row("A1", title) #put the titles in the first row
simulationNum = 1000 #the number of the simulated games
winNum = 0 #the number of the game I win
for i in range(1):
    winNum = 0
    for num in range(simulationNum):
        red = [-1, -1, -1, -1]
        yellow = [-1, -1, -1, -1]
        blue = [-1, -1, -1, -1]
        green = [-1, -1, -1, -1]
        board = []
        for m in range(52):
            board.append(0)
            win = newGame('A', 'A')
        if win == 3:
            winNum += 1
        print(num + i * 1000)
    insertData = ['A', 'A', winNum / simulationNum]
    worksheet1.write_row('A' + (str)(i + 2), insertData) #put the data into the file
workbook.close()
            


            
        


