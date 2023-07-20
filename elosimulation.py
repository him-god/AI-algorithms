'''
estimate rank for elo:
18k: (-∞, -2920)  avg: -3000
17k: [-2920, -2680)  avg: -2760
16k: [-2680, -2440)  avg: -2520
15k: [-2440, -2260)   avg: -2320
14k: [-2260, -2080)  avg: -2140
13k: [-2080, -1900)  avg: -1960
12k: [-1900, -1690)  avg: -1740
11k: [-1690, -1480)  avg: -1530
10k: [-1480, -1270)  avg: -1320
9k: [-1270, -1050)  avg: -1130
8k: [-1050, -830)  avg: -910
7k: [-830, -610)  avg: -690
6k: [-610, -390)  avg: -470
5k: [-390, -190)  avg: -270
4k: [-190, 10)  avg: -70
3k: [10, 210)  avg: 130
2k: [210, 450)  avg: 350
1k: [450, 690)  avg: 590
1d: [690, 930)  avg: 830
2d: [930, 1170)  avg: 1070
3d: [1170, 1430)  avg: 1280
4d: [1430, 1690)  avg: 1540
5d: [1690, 2000)  avg: 1800
6d: [2000, 2310)  avg: 2110
7d: [2310, 2620)  avg: 2420
8d: [2620, 2930)  avg: 2730
9d: [2930, +∞)  avg: 3040
'''

import random
import sys
import xlwt as xw


CHANGE_RULE = {
        -17: (10, (6, 8), (999, 999)), 
        -16: (10, (6, 8), (7, 999)), 
        -15: (10, (6, 8), (7, 9)), 
        -14: (12, (7, 10), (8, 10)), 
        -13: (12, (7, 10), (8, 10)), 
        -12: (12, (7, 10), (8, 10)), 
        -11: (14, (8, 12), (10, 12)),
        -10: (14, (8, 12), (10, 12)),
        -9: (14, (8, 12), (10, 12)), 
        -8: (16, (10, 14), (11, 14)), 
        -7: (16, (10, 14), (11, 14)),
        -6: (16, (10, 14), (11, 14)), 
        -5: (16, (10, 14), (11, 14)), 
        -4: (18, (11, 15), (12, 16)), 
        -3: (18, (11, 15), (12, 16)),
        -2: (18, (11, 15), (12, 16)), 
        -1: (19, (12, 16), (13, 17)), 
        0: (19, (12, 16), (13, 17)), 
        1: (19, (12, 16), (13, 17)),
        2: (19, (12, 16), (13, 17)), 
        3: (20, (14, 18), (13, 17)), 
        4: (20, (14, 18), (13, 17)), 
        5: (20, (15, 20), (13, 17)),
        6: (20, (15, 20), (13, 17)), 
        7: (20, (15, 20), (13, 17)), 
        8: (20, (15, 999), (13, 17)), 
        9: (20, (999, 999), (13, 17))
        }

class Player:
    def __init__(self, id: int, elo: float) -> None:
        self.id = id
        self.rank = 0
        self.elo = elo
        self.__game_history = []
        
    
    def __rank_change(self):
        if self.__game_history.count(1) >= CHANGE_RULE[self.rank][1][1]:
            self.rank += 2
            self.__game_history.clear()
        elif self.__game_history.count(0) >= CHANGE_RULE[self.rank][2][1]:
            self.rank -= 2
            self.__game_history.clear()
        elif self.__game_history.count(1) >= CHANGE_RULE[self.rank][1][0] and \
             self.__game_history.count(0) > CHANGE_RULE[self.rank][0] - CHANGE_RULE[self.rank][1][1]:
            self.rank += 1
            self.__game_history.clear()
        elif self.__game_history.count(0) >= CHANGE_RULE[self.rank][2][0] and \
             self.__game_history.count(1) > CHANGE_RULE[self.rank][0] - CHANGE_RULE[self.rank][2][1]:
            self.rank -= 1
            self.__game_history.clear()

    def update_history(self, result: int):
        #result = 1: win; result = 0: lose
        self.__game_history.append(result)
        if len(self.__game_history) > CHANGE_RULE[self.rank][0]:
            self.__game_history.pop(0)
        self.__rank_change()

    def get_history(self):
        return self.__game_history.count(1), self.__game_history.count(0)

    def __repr__(self):
        return str(self.id) + ": (rank: " + str(self.rank) + ", elo: " + str(self.elo) \
            + ", history" + str(self.__game_history) + ")"


class Server():

    def __init__(self, players: list[Player]) -> None:
        self.playerList = {}
        for rank in range(-17, 10):
            self.playerList[rank] = []
        for player in players:
            self.playerList[player.rank].append(player)
        for rank in range(-17, 10):
            random.shuffle(self.playerList[rank])

        
    def match(self):
        for rank in range(-17, 10):
            players = self.playerList[rank]
            if len(players) % 2 == 1 and rank != 9:
                self.playerList[rank + 1].append(players.pop())
                self.playerList[rank + 1].reverse()
            for index in range(len(players) // 2):
                self.play(players[2 * index], players[2 * index + 1])

    def play(self, player1: Player, player2: Player):
        player1_winrate = 1 / (pow(10, -(player1.elo - player2.elo)) + 1)
        result = random.random()
        if result < player1_winrate:
            player1.update_history(1)
            player2.update_history(0)
        elif result > player1_winrate:
            player1.update_history(0)
            player2.update_history(1)

    def __del__(self):
        pass
        

def main():
    players = []
    for id in range(1, 100001):
        elo = random.choice(range(-3500, 3501))
        player = Player(id, elo)
        players.append(player)
    all_player = tuple(players)
    for times in range(10000):
        players = list(all_player)
        random.shuffle(players)
        online_player = players[0: 30001]
        server = Server(online_player)
        server.match()

    wb = xw.Workbook()
    ws1 = wb.add_sheet('Data1')
    ws2 = wb.add_sheet('Data2')
    ws1.write(0, 0, "id")
    ws1.write(0, 1, "elo")
    ws1.write(0, 2, "rank")
    ws1.write(0, 3, "recent win num")
    ws1.write(0, 4, "recent lose num")
    ws2.write(0, 0, "id")
    ws2.write(0, 1, "elo")
    ws2.write(0, 2, "rank")
    ws2.write(0, 3, "recent win num")
    ws2.write(0, 4, "recent lose num")
    for player in all_player[0:50000]:
        ws1.write(player.id, 0, player.id)
        ws1.write(player.id, 1, player.elo)
        ws1.write(player.id, 2, player.rank)
        ws1.write(player.id, 3, player.get_history()[0])
        ws1.write(player.id, 4, player.get_history()[1])
    for player in all_player[50000:]:
        ws2.write(player.id - 50000, 0, player.id)
        ws2.write(player.id - 50000, 1, player.elo)
        ws2.write(player.id - 50000, 2, player.rank)
        ws2.write(player.id - 50000, 3, player.get_history()[0])
        ws2.write(player.id - 50000, 4, player.get_history()[1])
    
    wb.save("elo data 10000 games.xls")

main()