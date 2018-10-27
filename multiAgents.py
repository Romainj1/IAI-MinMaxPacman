# @Author: Romain Jacquier
# @Date:   2018-10-23T14:15:03+02:00
# @Email:  romain.jacquier@insa-rouen.fr
# @Last modified by:   Romain Jacquier
# @Last modified time: 2018-10-27T18:23:27+02:00



# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util
from time import *
from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        # sleep(1)
        # print legalMoves[chosenIndex]
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)


        scoreCalculated = 0
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        # print successorGameState.getNumFood()
        width = int( successorGameState.data.layout.width-1)
        height = int(successorGameState.data.layout.height-1)

        # find closest food It wait_for_keys
        closestFood = [0,0,1000]
        for i in range(1, width):
            for j in range(1, height):
                if newFood[i][j]:
                    distManhattan = manhattanDistance(newPos, (i,j))
                    if distManhattan < closestFood[2]:
                        closestFood = [i, j, distManhattan]

        # Calculate Score infunction of distManhattan (closestFood[2])
        if successorGameState.getNumFood()<currentGameState.getNumFood():
            scoreCalculated + 50
        else :
            scoreCalculated += 10 - closestFood[2]
        # scoreCalculated -= manhattanDistance(newPos, )

        closestGhostdistance = 1000
        for ghost in newGhostStates:
            if manhattanDistance(newPos, ghost.getPosition()) < closestGhostdistance:
                closestGhostdistance = manhattanDistance(newPos, ghost.getPosition())

        if closestGhostdistance == 0:
            scoreCalculated -= 30
        else:
            if closestGhostdistance < 5:
                scoreCalculated -= (1/closestGhostdistance)*20

        # Update score with scorechanging from game.
        scoreCalculated += successorGameState.data.scoreChange

        # If WIN :
        if (successorGameState.isWin()):
            return 6000
        return scoreCalculated

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
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

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

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """

        # Variables
        self.index = 0



        # Launch recursive MinMax
        scores = []
        for action in gameState.getLegalActions(self.index):
            scores.append(self.recursiveGetScore(gameState.generateSuccessor(self.index, action), self.index, self.depth))

        # Max highest layer.
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        # chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        chosenIndex = bestIndices[0] # Pick randomly among the best

        return gameState.getLegalActions(0)[chosenIndex]

    def recursiveGetScore(self, gameState, index, depthcount):

        # increase depth each time all agents are used.
        index += 1
        if index == gameState.getNumAgents():
            index = 0
            depthcount -= 1

        if depthcount <= 0:
            return self.evaluationFunction(gameState)

        scores = []
        for action in gameState.getLegalActions(index):
            scores.append(self.recursiveGetScore(gameState.generateSuccessor(index, action), index, depthcount))

        if index == 0:
            scores.append(-10000)
            return max(scores)
        else:
            scores.append(+10000)
            return min(scores)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
