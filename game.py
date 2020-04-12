import random
class Board:
    def __init__(self, myMarbles=None, opMarbles=None, myScore=None, opScore=None, myTurn=True):
        if not myMarbles:
            self.myMarbles = [4,4,4,4,4,4]
        else:
            self.myMarbles = myMarbles
        if not opMarbles:
            self.opMarbles = [4,4,4,4,4,4]
        else:
            self.opMarbles = opMarbles
        if not myScore:
            self.myScore = 0
        else:
            self.myScore = myScore
        if not opScore:
            self.opScore = 0
        else:
            self.opScore = opScore
        self.myTurn = myTurn
        print(self.__str__())

    def __str__(self):
        boardRep = "-- "
        for i in self.opMarbles:
            boardRep += str(i) + ' '
        boardRep += "--\n"
        boardRep += str(self.opScore) + "|            |" + str(self.myScore)
        if self.myTurn:
            boardRep += '  My turn '
        else:
            boardRep += '  Your turn '

        boardRep += '\n'
        boardRep += "-- "
        for i in self.myMarbles:
            boardRep += str(i) + ' '
        boardRep += "--"
            
        return boardRep

    def getMyMarbles(self):
        return self.myMarbles
    
    def getOpMarbles(self):
        return self.opMarbles

    def getMyScore(self):
        return self.myScore
    
    def getOpScore(self):
        return self.opScore

    def makeMove(self, pile):
        # Move is my move
        reward = 0
        try:        
            if (int(pile)>6) or (int(pile)<1):
                print('Choose a valid pile')
                return
        except:
            print('Choose a valid pile')
            return
        if self.myTurn:
            startIndex = 6-int(pile)
            numMarbles = self.myMarbles[startIndex]
            if numMarbles == 0:
                print('Choose a pile with marbles in it\n')
                return
            self.myMarbles[startIndex] = 0
            currentIndex = startIndex+1
            addToMine = True
            addToScore=False
            while numMarbles>0:
                if currentIndex == 6:
                    addToScore = True
                if addToScore:
                    self.myScore+=1
                    reward += 1
                    numMarbles -= 1
                    addToScore=False
                    currentIndex=5
                    addToMine=False
                else:
                    if addToMine:
                        self.myMarbles[currentIndex] += 1
                        numMarbles -= 1
                        currentIndex += 1
                    else:
                        self.opMarbles[currentIndex] += 1
                        numMarbles -= 1
                        currentIndex -= 1
                        if currentIndex == -1:
                            addToMine = True
                            currentIndex = 0
                            addToScore = False
            if (currentIndex == 5) and  (not addToMine) and (not addToScore):
                reward += 1
                self.myTurn = True
            else:
                self.myTurn = False

            if (addToMine) and (not addToScore) and (self.myMarbles[currentIndex-1] == 1) and (self.opMarbles[currentIndex-1]>0):
                self.myScore += 1
                self.myMarbles[currentIndex-1] = 0
                reward += self.opMarbles[currentIndex-1] + 1
                self.myScore += self.opMarbles[currentIndex-1]
                self.opMarbles[currentIndex-1] = 0
            if self.myScore>=25:
                reward += 25
        else:
            startIndex = int(pile)-1
            numMarbles = self.opMarbles[startIndex]
            if numMarbles == 0:
                print('Choose a pile with marbles in it\n')
                return
            self.opMarbles[startIndex] = 0
            currentIndex = startIndex-1
            addToTheirs = True
            addToTheirScore=False
            while numMarbles>0:
                if currentIndex == -1:
                    addToTheirScore = True
                # trial
                else:
                    addToTheirScore = False
                if addToTheirScore:
                    reward += 1
                    self.opScore+=1
                    numMarbles -= 1
                    addToTheirScore=False
                    currentIndex=0
                    addToTheirs=False
                else:
                    if addToTheirs:
                        self.opMarbles[currentIndex] += 1
                        numMarbles -= 1
                        currentIndex -= 1
                    else:
                        self.myMarbles[currentIndex] += 1
                        numMarbles -= 1
                        currentIndex += 1
                        if currentIndex == 6:
                            addToTheirs = True
                            currentIndex = 5
                            addToTheirScore = True
            if (currentIndex == 0) and  (not addToTheirs) and (not addToTheirScore):
                reward += 1
                self.myTurn = False
            else:
                self.myTurn = True


            # print(currentIndex)
            if (addToTheirs) and (not addToTheirScore) and (self.opMarbles[currentIndex+1] == 1) and (self.myMarbles[currentIndex+1]>0):
                self.opScore += 1
                self.opMarbles[currentIndex+1] = 0
                reward += self.myMarbles[currentIndex+1] + 1
                self.opScore += self.myMarbles[currentIndex+1]
                self.myMarbles[currentIndex+1] = 0
            if self.opScore>=25:
                reward += 20
        print(self.__str__())
        return reward
    def endGame(self):
        self.myScore += sum(self.myMarbles)
        self.opScore += sum(self.opMarbles)
        for i in range(len(self.myMarbles)):
            self.myMarbles[i] = 0
            self.opMarbles[i] = 0
        print(self.__str__())
        if self.myScore>self.opScore:
            who = "Brad"
        elif self.opScore>self.myScore:
            who = "Other player"
        else:
            who = 'both players, well fought'
        print('Congrats to ' + who)
    def isOver(self):
        if (sum(self.myMarbles) == 0) or (sum(self.opMarbles) == 0):
            self.endGame()
            return True
        else:
            return False
def playGame():
    board = Board()
    while not board.isOver():
        if board.myTurn:
            who = 'Brad: '
        else:
            who = "Other Player: "
        move = input(who + 'input which pile you would like to move: \n')
        print(board.makeMove(move))

# playGame()
