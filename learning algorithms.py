import random
import util

class MarkovDecisionProcess:
    """
    MDP algorithms
    """

    def getStates(self):
        """
        Return a list of all states in the MDP.
        Not generally possible for large MDPs.
        """
        abstract

    def getStartState(self):
        """
        Return the start state of the MDP.
        """
        abstract

    def getPossibleActions(self, state):
        """
        Return list of possible actions from 'state'.
        """
        abstract

    def getTransitionStatesAndProbs(self, state, action):
        """
        Returns list of (nextState, prob) pairs
        representing the states reachable
        from 'state' by taking 'action' along
        with their transition probabilities.
        """
        abstract

    def getReward(self, state, action, nextState):
        """
        Get the reward for the state, action, nextState transition.
        """
        abstract

    def isTerminal(self, state):
        """
        Returns true if the current state is a terminal state.  By convention,
        a terminal state has zero future rewards.  Sometimes the terminal state(s)
        may have no possible actions.  It is also common to think of the terminal
        state as having a self-loop action 'pass' with zero reward; the formulations
        are equivalent.
        """
        abstract


class ValueIterationAgent(ValueEstimationAgent):
    """
        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        nextUtility = {}
        for i in range(self.iterations):
            for state in self.mdp.getStates():
                if self.mdp.isTerminal(state):
                    nextUtility[state] = self.values[state]
                else:
                    maxValue = -float('inf')
                    for action in self.mdp.getPossibleActions(state):
                        sum = 0
                        for transition in self.mdp.getTransitionStatesAndProbs(state, action):
                            nextState, prob = transition
                            sum += prob * (self.mdp.getReward(state, action, nextState) + self.discount * self.values[nextState])
                        if sum > maxValue:
                            maxValue = sum
                    nextUtility[state] = maxValue
            self.values = nextUtility.copy()


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        qValue = 0    
        transitionList = self.mdp.getTransitionStatesAndProbs(state, action)
        for transition in transitionList:
            nextState, prob = transition
            reward = self.mdp.getReward(state, action, nextState)
            qValue += prob * (reward + self.discount * self.getValue(nextState))
        return qValue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          If there are no legal actions, which is the case at the
          terminal state, return None.
        """
        maxValue = -float('inf')
        bestAction = None
        for action in self.mdp.getPossibleActions(state):
            qValue = self.computeQValueFromValues(state, action)
            if  qValue > maxValue:
                bestAction = action
                maxValue = qValue
        return bestAction

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)


class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Instance variables:
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions:
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "initialize Q-values"
        ReinforcementAgent.__init__(self, **args)

        self.qValue = {}

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        if state not in self.qValue:
          return 0.0
        index = self.getLegalActions(state).index(action)
        return self.qValue[state][index]


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, return a value of 0.0.
        """
        legalActions = self.getLegalActions(state)
        if state not in self.qValue.keys():
          self.qValue[state] = []
          for i in range(len(legalActions)):
            self.qValue[state].append(0.0)
        if len(legalActions) == 0:
          return 0.0
        return max(self.qValue[state])

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          return None.
        """
        legalActions = self.getLegalActions(state)
        if state not in self.qValue.keys():
          self.qValue[state] = []
          for i in range(len(legalActions)):
            self.qValue[state].append(0.0)
        if len(legalActions) == 0:
          return None
        maxQValue = -float('inf')
        bestActionIndex = -1
        for index in range(len(legalActions)):
          if self.qValue[state][index] > maxQValue:
            maxQValue = self.qValue[state][index]
            bestActionIndex = index
        return legalActions[bestActionIndex]

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, choose None as the action.
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        if util.flipCoin(self.epsilon):
          action = random.choice(legalActions)
        else:
          action = self.computeActionFromQValues(state)
        return action

    def update(self, state, action, nextState, reward):
        """
         Update Q-value
        """
        legalActions = self.getLegalActions(state)
        nextStateLegalAction = self.getLegalActions(nextState)
        if state not in self.qValue.keys():
          self.qValue[state] = []
          for i in range(len(legalActions)):
            self.qValue[state].append(0.0)
        if nextState not in self.qValue.keys():
          self.qValue[nextState] = []
          if len(nextStateLegalAction) == 0:
            self.qValue[nextState].append(0)
          else:
            for i in range(len(nextStateLegalAction)):
              self.qValue[nextState].append(0.0)
        index = legalActions.index(action)
        oldQ = self.qValue[state][index]
        maxQNext = max(self.qValue[nextState])
        sample = reward + self.discount * maxQNext
        self.qValue[state][index] = (1 - self.alpha) * oldQ + self.alpha * sample


    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)
