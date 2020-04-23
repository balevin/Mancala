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
        self.state = self.myMarbles+self.opMarbles
        #print(self.__str__())

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

    def makeMove(self, pile, show=False):
        reward = 0
        #try:        
            #if (int(pile)>5) or (int(pile)<0):
                # print('Choose a valid pile')
        #        return
        #except:
            # print('Choose a valid pile')
        #        return
        if self.myTurn:
            startIndex = int(pile)
            numMarbles = self.myMarbles[startIndex]
            if numMarbles == 0:
                # print('Choose a pile with marbles in it\n')
                print('wtf how did we do this')
                print(pile)
                print(self)
                input()
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
        else:
            #print('making move')
            startIndex = int(pile)
            numMarbles = self.opMarbles[startIndex]
            #if numMarbles == 0:
                # print('Choose a pile with marbles in it\n')
               #return
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
                #print('return')
            else:
                self.myTurn = True
                #print('switch')


            if (addToTheirs) and (not addToTheirScore) and (self.opMarbles[currentIndex+1] == 1) and (self.myMarbles[currentIndex+1]>0):
                self.opScore += 1
                self.opMarbles[currentIndex+1] = 0
                reward += self.myMarbles[currentIndex+1] + 1
                self.opScore += self.myMarbles[currentIndex+1]
                self.myMarbles[currentIndex+1] = 0
        if show:
            print(self.__str__())
        #print(self.__str__())
        return reward
    def endGame(self):
        self.myScore += sum(self.myMarbles)
        self.opScore += sum(self.opMarbles)
        for i in range(len(self.myMarbles)):
            self.myMarbles[i] = 0
            self.opMarbles[i] = 0
        # print(self.__str__())
        if self.myScore>self.opScore:
            who = "Brad"
        elif self.opScore>self.myScore:
            who = "Other player"
        else:
            who = 'both players, well fought'
        # print('Congrats to ' + who)
    def isOver(self):
        if (sum(self.myMarbles) == 0) or (sum(self.opMarbles) == 0):
            self.endGame()
            return True
        else:
            return False
    def getState(self):
        return [self.myMarbles, self.opMarbles]
    
    def is_valid(self, pile, me):
        # associated with it being passed in as index number (0,11)
        if me:
            if (int(pile)>-1) and (int(pile)<6):
                if self.myMarbles[int(pile)] > 0:
                    return True
            return False
        else:
            if (int(pile)>5) and (int(pile)<12):
                if self.opMarbles[int(pile)-6] > 0:
                    return True
            return False
    def getMyAvailable(self):
        available = list(range(6))
        if self.myTurn: 
            zeroes = [i for i in range(len(self.myMarbles)) if self.myMarbles[i]==0]
        else:
            zeroes = [i for i in range(len(self.opMarbles)) if self.opMarbles[i]==0]
        available = [x for x in available if x not in zeroes]
        return available
    
    def getOpAvailable(self):
        # inputToIndexMap = {}
        # for i in range(1,7):
            # inputToIndexMap[i] = self.opMarbles[i-1]
        available = list(range(6))
        zeroes = [k for k in self.opMarbles if k==0]
        # zeroes = [k for k,v in inputToIndexMap.items() if v==0]
        available = [x for x in available if x not in zeroes]
        return available
    def didIWin(self):
        if self.isOver() and self.myScore>=25:
            return True
        return False
    def randomPossibleMove(self):
        possible = []
        if self.myTurn:
            for index, val in enumerate(self.myMarbles):
                if val!=0:
                    possible.append(index)
        else:
            for index, val in enumerate(self.opMarbles):
                if val!=0:
                    possible.append(index+6)
        numPossible = len(possible)
        randInd = random.randint(0,numPossible-1)
        # print('possible: ', possible)
        # print('randInd', randInd)
        return possible[randInd]

    def makeBallsBack(self):
        if self.myTurn:
            available = self.getMyAvailable()
            for i in reversed(range(6)):
                if i in available:
                    if i+self.myMarbles[i] == 6:
                        return i
        else:
            available = self.getMyAvailable()
            for i in reversed(range(6)):
                if i in available:
                    if self.opMarbles[i]-i == 1:
                        return i 
        return None
    
    def findCapture(self):
        available = self.getMyAvailable()
        maxSixe = 0
        capture = None
        if self.myTurn:
            for i in range(6):
                if i in available:
                    landing = i+self.myMarbles[i]%12
                    if landing<6:
                        if self.myMarbles[landing]==0:
                            if self.opMarbles[landing]>maxSixe:
                                maxSixe = self.opMarbles[landing]
                                capture = i
        else:
            for i in range(6):
                if i in available:
                    landing = i+self.opMarbles[i]%12
                    if landing<6:
                        if self.opMarbles[landing]==0:
                            if self.myMarbles[landing]>maxSixe:
                                maxSixe = self.myMarbles[landing]
                                capture = i     
        return capture
    def scorePoints(self):
        if self.myTurn:
            for i in reversed(range(6)):
                if i+self.myMarbles[i]>=6:
                    return i
        else:
            for i in range(6):
                if self.opMarbles[i]-i>=1:
                    return i
        return None
    def makeSmartMove(self):
        ballsBack = self.makeBallsBack()
        capture = self.findCapture()
        if not ballsBack:
            if not capture:
                if not self.scorePoints():
                    return self.randomPossibleMove()
                else:
                    return self.scorePoints()
            else:
                return capture
        else:
            if not capture:
                return ballsBack
            else:
                if self.myTurn:
                    if ballsBack>capture:
                        return ballsBack
                    else:
                        return capture
                else:
                    if ballsBack<capture:
                        return ballsBack
                    return capture

def playGame():
    # board = Board([1,0,0,0,1,7], [0,0,0,2,0,0], 13,24, True)
    board = Board()
    while not board.isOver():
        if board.myTurn:
            who = 'Brad: '
        else:
            who = "Other Player: "
        move = input(who + 'input which pile you would like to move: \n')
        board.makeMove(move)

# playGame()
