class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.
    """

    def getAction(self, gameState):
        """
        getAction chooses among the best options according to the evaluation function.
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        A good evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        currentScore = float(successorGameState.getScore())
        x, y = newPos
        dx, dy = Actions.directionToVector(action)
        px, py = int(x + dx), int(y + dy)
        tx, ty = -1, -1
        for food in newFood.asList():
            fx, fy = food
            if fx == px and fy == py:
                currentScore += 10
                if newFood.count() == 1:
                    currentScore += 500
            if tx == -1 and ty == -1:
                tx, ty = fx, fy
            elif fx < tx:
                tx, ty = fx, fy
            elif fx == tx:
                if fy < ty:
                    tx, ty = fx, fy
        if abs(px - tx) + abs(py - ty) < abs(x - tx) + abs(y - ty):
            currentScore += 10.0 / float(abs(x - tx) + abs(y - ty))
        for ghostState in newGhostStates:
            a, b = ghostState.getPosition()
            hx, hy = Actions.directionToVector(ghostState.getDirection())
            gx, gy = int(a + hx), int(b + hy)
            if newScaredTimes[newGhostStates.index(ghostState)] > 0:
                    currentScore += 200.0 / (float(abs(px - gx)) + 1.0)
            else:
                if abs(px - gx) + abs(py - gy) < 5:
                    currentScore -= 500.0 / (float(abs(px - gx) + abs(py - gy)) + 1.0)   
        return int(currentScore)

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to multi-agent searchers.  
    Any methods defined here will be available to the MinimaxPacmanAgent, 
    AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method that will be used.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """

        return getUtility(gameState, 0, self.depth, self.evaluationFunction, self.index, gameState.getNumAgents())[1]
    
"""
helper method
"""
def getUtility(gameState, depth, maxDepth, evaluation, index, agentNum):
    if gameState.isWin() or gameState.isLose() or depth >= maxDepth * agentNum:
        return (evaluation(gameState), 0)
    else:
        nextAction = 0
        if index == 0:
            utility = -float('inf')
        else:
            utility = float('inf')
        for action in gameState.getLegalActions(index):
            if index == 0:
                currentAction = gameState.generateSuccessor(index, action)
                nextIndex = (index + 1) % agentNum
                currentUtility = getUtility(currentAction, depth + 1, maxDepth, evaluation, nextIndex, agentNum)[0]
                if currentUtility > utility:
                    nextAction = action
                    utility = currentUtility
            else:
                currentAction = gameState.generateSuccessor(index, action)
                nextIndex = (index + 1) % agentNum
                currentUtility = getUtility(currentAction, depth + 1, maxDepth, evaluation, nextIndex, agentNum)[0]
                if currentUtility < utility:
                    nextAction = action
                    utility = currentUtility
        return (utility, nextAction)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    A minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        if self.index == 0:
            return maxs(gameState, 0, self.depth, self.evaluationFunction, self.index, gameState.getNumAgents(), float('inf'), -float('inf'))[1]
        else:
            return mini(gameState, 0, self.depth, self.evaluationFunction, self.index, gameState.getNumAgents(), float('inf'), -float('inf'))[1]



def maxs(gameState, depth, maxDepth, evaluation, index, agentNum, maxPrune, minPrune):
    if gameState.isWin() or gameState.isLose() or depth >= maxDepth * agentNum:
        return (evaluation(gameState), 0)
    nextAction = 0
    maxUtility = -float('inf')
    for action in gameState.getLegalActions(index):
        nextIndex = (index + 1) % agentNum
        if nextIndex == 0:
            utility = maxs(gameState.generateSuccessor(index, action), depth + 1, maxDepth, evaluation, nextIndex, agentNum, maxPrune, max(maxUtility, minPrune))[0] 
        else:
            utility = mini(gameState.generateSuccessor(index, action), depth + 1, maxDepth, evaluation, nextIndex, agentNum, maxPrune, max(maxUtility, minPrune))[0]
        if utility > maxPrune:
            maxUtility = utility
            nextAction = action
            break
        elif utility > maxUtility:
            maxUtility = utility
            nextAction = action
    return (maxUtility, nextAction)


def mini(gameState, depth, maxDepth, evaluation, index, agentNum, maxPrune, minPrune):
    if gameState.isWin() or gameState.isLose() or depth >= maxDepth * agentNum:
        return (evaluation(gameState), 0)
    nextAction = 0
    minUtility = float('inf')
    for action in gameState.getLegalActions(index):
        nextIndex = (index + 1) % agentNum
        if nextIndex == 0:
            utility = maxs(gameState.generateSuccessor(index, action), depth + 1, maxDepth, evaluation, nextIndex, agentNum, min(minUtility, maxPrune), minPrune)[0] 
        else:
            utility = mini(gameState.generateSuccessor(index, action), depth + 1, maxDepth, evaluation, nextIndex, agentNum, min(minUtility, maxPrune), minPrune)[0]
        if utility < minPrune:
            minUtility = utility
            nextAction = action
            break
        elif utility < minUtility:
            minUtility = utility
            nextAction = action
    return (minUtility, nextAction)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Expectimax agent
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        return getExpectedScore(gameState, 0, self.depth, self.evaluationFunction, self.index, gameState.getNumAgents())[1]
        

def getExpectedScore(gameState, depth, maxDepth, evaluation, index, agentNum):
    if gameState.isWin() or gameState.isLose() or depth >= maxDepth * agentNum:
        return (evaluation(gameState), 0)
    if index == 0:
        nextAction = 0
        maxUtility = -float('inf')
        nextIndex = (index + 1) % agentNum
        for action in gameState.getLegalActions(index):
            utility = getExpectedScore(gameState.generateSuccessor(index, action), depth + 1, maxDepth, evaluation, nextIndex, agentNum)[0]
            if utility > maxUtility:
                maxUtility = utility
                nextAction = action
        return (maxUtility, nextAction)
    else:
        sumUtility = 0
        nextIndex = (index + 1) % agentNum
        actionNum = len(gameState.getLegalActions(index))
        for action in gameState.getLegalActions(index):
            sumUtility += getExpectedScore(gameState.generateSuccessor(index, action), depth + 1, maxDepth, evaluation, nextIndex, agentNum)[0]
        return (sumUtility / actionNum, 0)

def betterEvaluationFunction(currentGameState):
    """
    An extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function.
    """
    if currentGameState.isWin() or currentGameState.isLose():
        return currentGameState.getScore()
    else:
        currentScore = currentGameState.getScore()
        foodNum = currentGameState.getNumFood()
        px, py = currentGameState.getPacmanPosition()
        distance = float('inf')
        for ghostState in currentGameState.getGhostStates():
            gx, gy = ghostState.getPosition()
            distance = min(distance, abs(gx - px) + abs(gy - py))
        distanceScore = 0
        if distance < 5:
            distanceScore = 500 - distance * 100
        return currentScore + foodNum * 5 - distanceScore


