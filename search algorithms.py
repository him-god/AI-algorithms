import util  #util is a package that includes several data structure.

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Return a list of actions that reaches the goal by dfs algorithm.

    Stack is a data structure using the linked list algorithm. User can delete 
    and add node at the end of the stack.
    """

    start = problem.getStartState()
    path = util.Stack()
    choices = []
    visited = []
    visited.append(start)
    current = start
    while not problem.isGoalState(current):
        next = None
        currentChoice = ()
        for choice in choices:
            if choice[0] == current:
                currentChoice = choice[1]
                break
        if len(currentChoice) == 0:
            currentChoice = problem.getSuccessors(current)
            choices.append((current, currentChoice))
        for node in currentChoice:
            if node[0] not in visited:
                path.push((current, node[1])) #push(self, item) add item to the stack
                next = node[0]
                current = next
                visited.append(current)
                break
        if next == None:
            if path.isEmpty():
                return
            else:
                current = path.pop()[0]
    result = []
    while not path.isEmpty():
        result.append(path.pop()[1]) #pop(self) return and delete the last item of the stack
    result.reverse()
    return result      

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    start = problem.getStartState()
    layer = []
    visited = []
    layer.append((start, []))
    visited.append(start)
    while True:
        newLayer = []
        for node in layer:
            if problem.isGoalState(node[0]):
                return node[1]
            for next in problem.getSuccessors(node[0]):
                if next[0] not in visited:
                    newPath = []
                    for i in node[1]:
                        newPath.append(i)
                    newPath.append(next[1])
                    newLayer.append((next[0], newPath))
                    visited.append(next[0])
        if len(newLayer) == 0:
            return
        else:
            layer = newLayer

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    
    Priority Queue is a data structure that sort the elements from its priority
    and allow users to delete the first element of the queue.
    """
    start = problem.getStartState()
    choices = util.PriorityQueue()
    visited = []
    current = start
    visited.append(start)
    currentEnergy = 0
    currentPath = []
    while not problem.isGoalState(current):
        for node in problem.getSuccessors(current):
            if node[0] not in visited:
                path = []
                for i in currentPath:
                    path.append(i)
                path.append(node[1])
                choices.update((node[0], path, currentEnergy + node[2]), currentEnergy + node[2]) 
                #update(self, item, priority)
                # If item already in priority queue with higher priority, update its priority and rebuild the heap.
                # If item already in priority queue with equal or lower priority, do nothing.
                # If item not in priority queue, add item to the priority queue
        if choices.isEmpty():
            return
        currentNode = choices.pop()  #pop(self) delete the first element in the priority queue
        while currentNode[0] in visited:
            currentNode = choices.pop()
        current = currentNode[0]
        currentPath = currentNode[1]
        currentEnergy = currentNode[2]
        visited.append(current)
    return currentPath
        
    

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    start = problem.getStartState()
    choices = util.PriorityQueue()
    visited = []
    current = start
    visited.append(start)
    currentEnergy = 0
    currentPath = []
    while not problem.isGoalState(current):
        for node in problem.getSuccessors(current):
            if node[0] not in visited:
                path = []
                for i in currentPath:
                    path.append(i)
                path.append(node[1])
                choices.update((node[0], path, currentEnergy + node[2]), currentEnergy + node[2] + heuristic(node[0], problem))
        if choices.isEmpty():
            return
        currentNode = choices.pop()
        while currentNode[0] in visited:
            currentNode = choices.pop()
        current = currentNode[0]
        currentPath = currentNode[1]
        currentEnergy = currentNode[2]
        visited.append(current)
    return currentPath


class CornersProblem(search.SearchProblem):
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function
    """

    def __init__(self, startingGameState):
        """
        Stores the walls, pacman's starting position and corners.
        """
        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top, right = self.walls.height-2, self.walls.width-2
        self.corners = ((1,1), (1,top), (right, 1), (right, top))
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                print('Warning: no food in corner ' + str(corner))
        self._expanded = 0 # Number of search nodes expanded



    def getStartState(self):
        """
        Returns the start state (in your state space, not the full Pacman state
        space)
        """
        return (self.startingPosition, self.corners)

    def isGoalState(self, state):
        """
        Returns whether this search state is a goal state of the problem.
        """
        return len(state[1]) == 0

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state[0]
            dx, dy = Actions.directionToVector(action) #transfer a direction to a vector
            nextx, nexty = int(x + dx), int(y + dy)
            hitsWall = self.walls[nextx][nexty]
            if not hitsWall:
                position = (nextx, nexty)
                food = []
                for i in state[1]:
                    if position != i:
                        food.append(i)                    
                food = tuple(food)                
                successors.append(((position, food), action, 1))

        self._expanded += 1
        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999.
        """
        if actions == None: return 999999
        x,y= self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
        return len(actions)


def cornersHeuristic(state, problem):
    """
    A heuristic for the CornersProblem that you defined.

      state:   The current search state
               (a data structure you chose in your search problem)

      problem: The CornersProblem instance for this layout.
    """
    
    corners = problem.corners # These are the corner coordinates
    walls = problem.walls # These are the walls of the maze, as a Grid (game.py)

    x, y = state[0]
    food = state[1]
    if len(food) == 0:
        return 0
    value = 0
    maxValue = 0
    for posi in food:
        a, b = posi
        maxValue = max(maxValue, (abs(x - a) + abs(y - b)))
        value += (abs(x - a) + abs(y - b)) * 2
    return int(value - maxValue)