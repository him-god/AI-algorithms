import xlsxwriter as xw
import random


def gamePredictionFunction(levelA, levelB):
    return levelA / (levelA + levelB)


class Queue:
    "A container with a first-in-first-out (FIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Enqueue the 'item' into the queue"
        self.list.insert(0,item)

    def pop(self):
        """
          Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue.
        """
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the queue is empty"
        return len(self.list) == 0

    def asList(self):
        "Returns the queue as a list"
        return self.list
        

    def length(self):
        "Returns the length of the quque"
        return len(self.list)


    def count(self, item):
        "Returns the times the given item appears in the queue"
        return self.list.count(item)


class individual:
    
    def __init__(self, level, id):
        self.id = id
        self.level = level
        self.rank = 3
        self.recent = Queue()
        self.checkRankNum = {-18: 10, -17: 10, -16: 10, -15: 12, -14: 12, -13: 12, -12: 14, -11: 14, -10: 14, 
                             -9: 16, -8: 16, -7: 16, -6: 16, -5: 18, -4: 18, -3: 18, -2: 19, -1: 19, 1: 19, 
                             2: 19, 3: 20, 4: 20, 5: 20, 6: 20, 7: 20, 8: 20, 9: 20}
        self.rankWinRule = {-18: 6, -17: 6, -16: 6, -15: 7, -14: 7, -13: 7, -12: 8, -11: 8, -10: 8, -9: 10, 
                            -8: 10, -7: 10, -6: 10, -5: 11, -4: 11, -3: 11, -2: 12, -1: 12, 1: 12, 2: 12, 
                            3: 14, 4: 14, 5: 15, 6: 15, 7: 15, 8: 15, 9: 999}
        self.rankDoubleWinRule = {-18: 8, -17: 8, -16: 8, -15: 10, -14: 10, -13: 10, -12: 12, -11: 12, -10: 12, -9: 14, 
                                  -8: 14, -7: 14, -6: 14, -5: 15, -4: 15, -3: 15, -2: 16, -1: 16, 1: 16, 2: 16, 
                                  3: 18, 4: 18, 5: 20, 6: 20, 7: 20, 8: 999, 9: 999}
        self.rankLoseRule = {-18: 999, -17: 7, -16: 7, -15: 8, -14: 8, -13: 8, -12: 10, -11: 10, -10: 10, -9: 11, 
                             -8: 11, -7: 11, -6: 11, -5: 12, -4: 12, -3: 12, -2: 13, -1: 13, 1: 13, 2: 13, 
                             3: 13, 4: 13, 5: 13, 6: 13, 7: 13, 8: 13, 9: 13}
        self.rankDoubleLoseRule = {-18: 999, -17: 999, -16: 9, -15: 10, -14: 10, -13: 10, -12: 12, -11: 12, -10: 12, -9: 14, 
                                   -8: 14, -7: 14, -6: 14, -5: 16, -4: 16, -3: 16, -2: 17, -1: 17, 1: 17, 2: 17, 
                                   3: 17, 4: 17, 5: 17, 6: 17, 7: 17, 8: 17, 9: 17}


    def game(self, result):
        "Add a game for this user"
        self.recent.push(result)
        if self.recent.length() > self.checkRankNum[self.rank]:
            self.recent.pop()
        self.checkRank()


    def checkRank(self):
        "Check the change of the rank"
        if self.recent.count(True) >= self.rankDoubleWinRule[self.rank]:
            self.rank += 2
            if self.rank == 0 or self.rank == 1:
                self.rank += 1
        if self.recent.count(False) >= self.rankDoubleLoseRule[self.rank]:
            self.rank -= 2
            if self.rank == 0 or self.rank == -1:
                self.rank -= 1
        if self.recent.count(True) >= self.rankWinRule[self.rank]:
            if self.recent.count(False) > 20 - self.rankDoubleWinRule[self.rank]:
                self.rank += 1
                if self.rank == 0:
                    self.rank += 1
        if self.recent.count(False) >= self.rankLoseRule[self.rank]:
            if self.recent.count(True) > 20 - self.rankDoubleWinRule[self.rank]:
                self.rank -= 1
                if self.rank == 0:
                    self.rank -= 1
    
    def getLevel(self):
        return self.level

    def getRank(self):
        return self.rank

    def getGameData(self):
        return self.recent

    def playGame(self, opponent):
        "Play a game"
        game = random.random() 
        if game <= gamePredictionFunction(self.level, opponent.getLevel()):
            self.game(True)
            opponent.game(False)
        else:
            self.game(False)
            opponent.game(True)

    def getid(self):
        return self.id

'''
Create 10000 users with random level
'''
people = []
for i in range(10000):
    people.append(individual(random.uniform(0.0, 100.0), i))
print("ok")


'''
Play totally 5000000 games
'''
for i in range(5000000):
    randomA = random.choice(people)
    randomB = None
    for j in range(1000):
        current = random.choice(people)
        if randomA.getid() == current.getid():
            continue
        elif current.getRank() != randomA.getRank():
            continue
        else:
            randomB = current
            break
    if randomB != None:
        randomA.playGame(randomB)
    if i % 1000 == 0:
        print(i)
    

'''
Put the result to a xlsx file
'''
fileName = "game simulation.xlsx"
workbook = xw.Workbook(fileName) #create a xlsx file
worksheet1 = workbook.add_worksheet("sheet1") #add a worksheet in the file
worksheet1.activate() #activate the worksheet
title = ["id", "level", "rank", "recentGame"]
for i in people:
    id = i.getid()
    rank = i.getRank()
    if rank > 0:
        rankLevel = str(rank) + "D"
    else:
        rankLevel = str(-1 * rank) + "K"
    recentGame = i.getGameData()
    recentLevel = str(recentGame.count(True)) + "W" + str(recentGame.count(False)) + "L"
    insertData = [id, i.getLevel(), rankLevel, recentLevel]
    worksheet1.write_row('A' + (str)(id + 2), insertData) #put the data into the file
workbook.close()