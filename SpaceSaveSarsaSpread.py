import numpy as np
import random
import math
import time

class SpaceSaveSarsaSpread:

	#The initialization takes the starting board, and finds the amount of states in its untrimmed game-tree, which is called self.sum. It also initializes T and Q.
	def __init__(self, startBoard):
		self.board = startBoard
		self.sum = self.getSum()
		self.board.sort(reverse = True)
		self.listOfStates = []
		self.listOfStates.append(self.board[:])
		self.T = []
		self.Q = []

	#This method is for finding the amount of states reachable from the start-state, for the trimmed game-tree.
	def getSum(self):
		return int(math.factorial(len(self.board)+ self.board[0])/(math.factorial(len(self.board))*math.factorial(self.board[0])))

	#This method is for taking a state and a move in the state, and returning the resulting state in the correct order.
	def newState(self, heapIndex, amount, state):
		curState = state[:]
		curAmount = amount
		for i in range(heapIndex, len(state)-1):
			dif = curState[i] - curState[i+1]
			if (dif >= curAmount):
				curState[i] -= curAmount
				curAmount = 0
				break
			else:
				curState[i] -= dif
				curAmount -= dif
		if (curAmount > 0):
			curState[len(curState)-1] -= curAmount
		return curState

	"""This method is for setting up the matrices T and Q, as well as creating the list of states. For each state it makes all possible moves it can,
	and for each of those, it adds them to their spot in listOfStates. The function newState is used to get the resulting state from a given move.
	the states are added at the end of the list of states in this case, unless they are already in the list.
	All those moves are also added to T, which is the main purpose. Then Q is made, by setting all positions in T with 1, to have small random values in Q.
	The other positions in Q gets the value of negative infinity, -np.inf, so that they are always smaller than the expected reward of a move.
	Lastly the method sets up the inputs for the training, and runs it as well. Lastly the method takes the time used both by the setup and the training."""	
	def setup(self, type = 0):
		timeStart = time.time()
		emptyBoard = [0] * len(self.listOfStates[0])
		for i in range(self.sum):
			self.T.append([0] * self.sum)
			for x in range(len(self.listOfStates[i])-1, -1, -1):
				atEnd = 0
				curIndex = i+1
				for y in range(1, self.listOfStates[i][x]+1):
					newState = self.newState(x, y, self.listOfStates[i])
					if(atEnd):
						self.T[i][curIndex] = 1
						self.listOfStates.append(newState)
						curIndex += 1
					else:
						atEnd = 1
						for j in range(curIndex, len(self.listOfStates)):
							if (newState == self.listOfStates[j]):
								self.T[i][j] = 1
								curIndex = j+1
								atEnd = 0
								break
						if (atEnd):
							self.T[i][len(self.listOfStates)] = 1
							self.listOfStates.append(newState)
							curIndex = len(self.listOfStates)
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

	""" This is the method for making a move, it finds the state(which is sorted first) in the list of states, by calculating its index. Then the best move is found by use
	of the function np.argmax. Lastly it identifies the index of the heap in which the move is made, and it finds a heap of the same size
	in the input state."""
	def makeMove(self, state):
		curState = state[:]
		curState.sort(reverse = True)
		nextState = []
		move = []
		if (len(state)<len(self.listOfStates[0])):
			dif = len(self.listOfStates[0])-len(state)
			for i in range(dif):
				curState.append(0)
		goal = 0
		progress = self.board[0]
		for i in range(len(self.board)):
			heaps = len(self.board)- (i+1)
			for j in range(progress, -1, -1):
				if(j == curState[i]):
					break
				else:
					if(heaps == 0):
						goal += j-curState[i]
						break
					result = 1
					for x in range(1, heaps + 1):
						result *= (j + x)
					goal += (result)//math.factorial(heaps)
					progress -= 1
		nextState = self.listOfStates[np.argmax(self.Q[goal])][:]
		numToDec = 0
		for i in range(len(curState)-1, -1, -1):
			if (curState[i] != nextState[i]):
				numToDec += curState[i]-nextState[i]
				newIndex = curState[i]
		move.append(numToDec)
		for i in range(len(state)):
			if(newIndex == state[i]):
				newIndex = i
				break
		move.append(newIndex)
		return move

	"""This method is for training the matrix Q, by using the Sarsa algorithm, as well as training not just from the start states, 
	but from all states(except the win-state)"""
	def train(self, amountEpisodes, epsilon, mu, gamma):
		curStartState = 0
		for neverUsed in range(amountEpisodes):
			curState = curStartState
			curAction = self.epsilonGreedyChoice(curState, epsilon)
			playing = 1
			while(playing):
				curReward = self.Q[curState][curAction]
				nextState = curAction
				if(nextState == len(self.listOfStates)-1):
					break
				nextAction = self.epsilonGreedyChoice(nextState, epsilon)
				self.Q[curState][curAction] -= mu * (curReward + gamma*self.Q[nextState][nextAction] - self.Q[curState][curAction])
				curState = nextState
				curAction = nextAction
				if (nextAction == self.sum-1):
					playing = 0
			curStartState += 1
			if(curStartState >= len(self.listOfStates)-2):
				curStartState = 0

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