import numpy as np
import random

class Board:

    def __init__(self):
        self.state = np.zeros((3,3))
        self.turn = 'x'
        self.moves = 0


    def reset(self):
        self.state = np.zeros((3,3))
        self.turn = 'x'
        self.moves = 0


    def addToken(self, one:int, two:int):

        try:
            if self.state[one,two] == 0:

                if self.turn == 'x':
                    self.state[one,two] += 1

                elif self.turn == 'o':
                    self.state[one,two] += 2

            else:
                return "bad"

        except ValueError:
            raise "invalid input"

    def niceBoard(self):

        board = [[],[],[]]
        state = self.state.tolist()

        for i in range(len(state)):
            line = state[i]

            for j in range(len(line)):

                if line[j] == 0:
                    board[i].append(' - ')

                elif line[j] == 1:
                    board[i].append('x')

                elif line[j] == 2:
                    board[i].append('o')

        return board


    def winCheck(self):

        self.outcome = 'win'
        # check horizontal
        for i in self.state:
            uniques = np.unique(i)

            if len(uniques) == 1 and uniques[0] != 0:
                return True

        # check vertical
        for i in range(len(self.state)):
            uniques = np.unique(self.state[:,i])

            if len(uniques) == 1 and uniques[0] != 0:
                return True

        # check diagonal
        uniqueL = np.unique(self.state.diagonal())
        uniqueR = np.unique(np.fliplr(self.state).diagonal())

        if (len(uniqueL) == 1 and uniqueL[0] != 0) or (len(uniqueR) == 1 and uniqueR[0] != 0):
            return True

        if 0 in self.state:
            return False

        self.outcome = 'draw'
        return True # it's tied


    def showBoard(self):

        for i in self.state:
            print(i)


    def next(self):

        if self.turn == 'x':
            self.turn = 'o'

        else:
            self.turn = 'x'


    def getMoves(self):

        self.moves = np.where(self.state == 0)
        moves = []

        for i in range(len(self.moves[0])):
            moves.append((self.moves[0][i],self.moves[1][i]))

        return moves


    def move(self,one,two):

        if self.turn == 'x':
            place = (one,two)
            return place

        else:
            moves = self.getMoves()
            move = moves[random.randint(0,len(moves)-1)]
            return move


    def randoMove(self):
        moves = self.getMoves()
        move = moves[random.randint(0,len(moves)-1)]
        self.addToken(move[0],move[1])


    def getMessage(self):

        if self.winCheck() == True:

            if self.outcome == 'win':
                message = f"{self.turn} has won"

            else:
                message = "drawed"

            return True, message

        else:
            message = 'cont'
            return False, message


class Train(Board):

    def __init__(self):
        Board.__init__(self)
        self.stable = []
        self.qtable = np.zeros((10000,9))
        self.alpha = 0.1
        self.discount = 0.9
        self.epsilon = 1
        self.max_epsilon = 1
        self.min_epsilon = 0.01
        self.epsilon_decay = -0.0005
        self.episodes = 50000


    def randomMove(self):

        moves = self.getMoves()
        move = moves[random.randint(0,len(moves)-1)]
        return move


    def getMove(self):

        if self.state.tolist() in self.stable:
            i = self.stable.index(self.state.tolist())

            if np.amax(self.qtable[i]) == 0:
                move = self.randomMove()

            else:
                move = np.unravel_index(np.argmax(self.qtable[i]),(3,3))

            return self.state.tolist(), move

        else:
            self.stable.append(self.state.tolist())
            move = self.randomMove()
            return self.state.tolist(), move


    def getReward(self):

        if self.outcome == 'draw':
            self.draws += 1
            return 0.5

        elif self.turn == 'x':
            self.wins += 1
            return 1

        else:
            self.losses += 1
            return -1


    def agentMove(self):

        if self.state.tolist() in self.stable:
            i = self.stable.index(self.state.tolist())
            move = np.unravel_index(np.argmax(self.qtable[i]),(3,3))

            if np.amax(self.qtable[i]) == 0:
                move = self.randoMove()

            else:
                self.addToken(move[0], move[1])

        else:
            move = self.randoMove()


    def start(self):

        self.stable = []
        self.qtable = np.zeros((10000,9))
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.total = 0
        session = 1000

        for episode in range(self.episodes):

            self.reset()
            done = False

            while done == False:

                # agent starts first (turn = 1)
                ethreshold = random.uniform(0, 1)
                # choose which moves to take
                if ethreshold > self.epsilon:
                    state, move = self.getMove()

                else:
                    move = self.randomMove()
                    state = self.state.tolist()
                    if state not in self.stable:
                        self.stable.append(state)

                self.addToken(move[0], move[1])

                # get reward
                if self.winCheck() == True:
                    reward = self.getReward()
                    self.total += reward
                    done = True

                else:
                    reward = 0
                    # random opponent's turn
                    self.next()
                    self.randoMove()

                    if self.winCheck() == True:
                        reward = self.getReward()
                        self.total += reward
                        done = True

                    else:
                        self.next()

                # prepare to update q-table
                if self.state.tolist() not in self.stable:
                    self.stable.append(self.state.tolist())

                index = self.stable.index(state)
                new_index = self.stable.index(self.state.tolist())
                # convert move tuple into single index
                move = np.ravel_multi_index(move,(3,3))
                # update q-table
                self.qtable[index][move] = self.qtable[index][move] + self.alpha * (reward + self.discount * np.max(self.qtable[new_index]) - self.qtable[index][move])

            self.epsilon = self.min_epsilon + (self.max_epsilon - self.min_epsilon) * np.exp(self.epsilon_decay * episode)
"""
            if episode % session == 0 and episode != 0:

                print(f"wins: {self.wins} losses: {self.losses} draws: {self.draws} in {session} games - lose %: {(self.losses/session)*100}")
                self.wins = 0
                self.losses = 0
                self.draws = 0

        print(f"wins: {self.wins} losses: {self.losses} draws: {self.draws} in {session} games - lose %: {(self.losses/session)*100}")
"""

def main():

    t = Train()
    t.start()



if __name__ == "__main__":
    main()
