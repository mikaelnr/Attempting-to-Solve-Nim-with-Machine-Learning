import numpy as np
import random
import time

class ReinforcementSarsa:
	
	#The initialization takes the starting board, and finds the amount of states in its untrimmed game-tree, which is called self.sum. It also initializes T and Q.
	def __init__(self, startBoard):
		self.sum = startBoard[0]+1
		self.board = startBoard
		for i in range(1, len(self.board)):
			self.sum *= self.board[i]+1
		self.listOfStates = [0] * self.sum
		self.listOfStates[0] = self.board[:]
		self.T = []
		self.Q = []

	"""This method is for setting up the matrices T and Q, as well as creating the list of states. For each state it makes all possible moves it can,
	and for each of those, it adds them to their spot in listOfStates, if the state wasnt already there, using the method newIndex to find the states' index.
	All those moves are also added to T, which searchingis the main purpose. Then Q is made, by setting all positions in T with 1, to have small random values in Q.
	The other positions in Q gets the value of negative infinity, -np.inf, so that they are always smaller than the expected reward of a move.
	Lastly the method sets up the inputs for the training, and runs it as well. Lastly the method takes the time used both by the setup and the training."""
	def setup(self, type):
		timeStart = time.time()
		for i in range(self.sum):
			self.T.append([0] * self.sum)
			for x in range(len(self.listOfStates[i])):
				for y in range(1, self.listOfStates[i][x] + 1):
					tmpValue = self.newIndex(x, y)
					self.T[i][i+tmpValue] = 1
					if(self.listOfStates[i+tmpValue] == 0):
						tmpList = self.listOfStates[i][:]
						tmpList[x] -= y
						self.listOfStates[i+tmpValue] = tmpList[:]
			
			self.Q.append([])
			for j in range(self.sum-1):
				if(self.T[i][j] == 1):
					self.Q[i].append(random.random())
				else:
					self.Q[i].append(-np.inf)
			if (self.T[i][self.sum-1] == 1):
				self.Q[i].append(100.0)
			else:
				self.Q[i].append(-np.inf)
		timeEnd = time.time()
		setupTime = timeEnd-timeStart
		if(type == 0):
			epsilon = 0
			mu = 0.5
			gamma = 0.5
			amountEpisodes = 1000
			timeStart = time.time()
			self.train(amountEpisodes, epsilon, mu, gamma)
			timeEnd = time.time()
			trainTime = timeEnd-timeStart
		
			times = []
			times.append(setupTime)
			times.append(trainTime)
		
			return times
		return -1
	
	# This method exists for finding, given a move, how far down the list of states the new state is.
	def newIndex(self, heapIndex, amount):
		newMove = 1
		for i in range(len(self.board)-1, heapIndex, -1):
			newMove *= self.board[i]+1
		newMove *= amount
		return newMove
	
	"""This is the method that finds the best state to make a move to, from the input state. It does this by searching through list to find the current state,
	and then using np.argmax to find the following state with the highest expected reward. Then it finds the heap where the move was made,
	to find exactly what to return, that is the amount of counters removed and the index of the heap removed from."""
	def makeMove(self, state):
		curState = state[:]
		nextState = []
		move = []
		if (len(state)<len(self.listOfStates[0])):
			dif = len(self.listOfStates[0])-len(state)
			for i in range(dif):
				curState.append(0)
		for i in range(len(self.listOfStates)):
			if (curState == self.listOfStates[i]):
				nextState = self.listOfStates[np.argmax(self.Q[i])]
		for i in range(len(curState)):
			if (curState[i] != nextState[i]):
				move.append(curState[i] - nextState[i])
				move.append(i)
				return move

	"""This method is for training the matrix Q, by using the Sarsa algorithm. The main difference is that it removes the calculated reward, instead of adding it.
	It trains by playing against itself, until it wins, and then starts again. each game is an episode."""
	def train(self, amountEpisodes, epsilon, mu, gamma):
		for neverUsed in range(amountEpisodes):
			curState = 0
			curAction = self.epsilonGreedyChoice(curState, epsilon)
			playing = 1
			while(playing):
				curReward = self.Q[curState][curAction]
				nextState = curAction
				nextAction = self.epsilonGreedyChoice(nextState, epsilon)
				self.Q[curState][curAction] -= mu * (curReward + gamma*self.Q[nextState][nextAction] - self.Q[curState][curAction])
				curState = nextState
				curAction = nextAction
				if (curAction == self.sum-1):
					playing = 0
	
	#This is an implementation of the epsilon greedy policy, by the use of numpy.argmax when finding the best move, or just random choice of the possible moves otherwise.
	def epsilonGreedyChoice(self, state, epsilon):
		if(random.random()<epsilon):
			tmpList = []
			for i in range(state, self.sum):
				if(self.T[state][i] == 1):
					tmpList.append(i)
			return tmpList[random.randrange(0, len(tmpList))]
		else:
			return np.argmax(self.Q[state])

	#This method returns the list of states, which is used to test the program, by having it play from many different states.
	def getListOfStates(self):
		return self.listOfStates