import numpy as np
import random
from scipy.special import expit

class mlp:
	def __init__(self, nhidden, stateLen):
		self.beta = 1
		self.eta = 0.1
		self.momentum = 0.0
		self.matrix1 = []
		self.matrix2 = []
		self.inputAmount = stateLen
		self.outputAmount = stateLen
		self.hiddenAmount = nhidden
		self.outputA = [0.0] * (self.outputAmount)
		self.outputList = [0.0] * (self.outputAmount)
		self.hiddenU = [0.0] * (nhidden)
		self.hiddenList = [0.0] * (nhidden)
		for i in range(self.inputAmount + 1):
			self.matrix1.append([])
			for j in range(nhidden):
				self.matrix1[i].append(random.random())
		for i in range(nhidden + 1):
			self.matrix2.append([])
			for j in range(self.outputAmount):
				self.matrix2[i].append(random.random())
		
	def sigmoidDerived(self, x):
		return expit(x)*(1-expit(x))
	
	def identityFunction(self, x):
		return x
	
	def identityDerived(self, x):
		return 1
	
	#this function calculates the sum of squares error of all the valid inputs and targets, and sums them, and returns that for the earlystopping to use for figuring out when to stop.
	def totalError(self, inputs, targets):
		accumError = 0.0
		for i in range(len(inputs)):
			accum = 0.0
			self.forward(inputs[i])
			for j in range(self.outputAmount):
				accum += (targets[i][j] - self.outputList[j])**2
			accumError += accum/2
		return accumError

	#earlystopping, stops when error increases, or decreases too slowly
	def earlystopping(self, inputs, targets, valid, validtargets):
		stopTraining = 0
		lowestError = self.totalError(valid, validtargets)
		while not stopTraining:
			self.train(inputs, targets, 10)
			newError = self.totalError(valid, validtargets)
			if newError > lowestError or lowestError-newError < 0.5:
				stopTraining = 1
			else:
				lowestError = newError

	#train trains the neural net for the inputted amount of iterations. One pass through the dataset is an iteration.
	def train(self, inputs, targets, iterations=100):
		for notUsed in range(iterations):
			for ite in range(len(inputs)):
				self.forward(inputs[ite])
				outDelta = []
				for i in range(self.outputAmount):
					outDelta.append((self.outputList[i] - targets[ite][i]) * self.identityDerived(self.outputA[i]))
				hiddenDelta = []
				for i in range(self.hiddenAmount):
					accumulator = 0.0
					for j in range(self.outputAmount):
						accumulator += outDelta[j] * self.matrix2[i+1][j]
					hiddenDelta.append(self.sigmoidDerived(self.hiddenU[i]) * accumulator)
				for j in range(self.outputAmount):
					self.matrix2[0][j] -= self.eta * outDelta[j] * 1
					for i in range(self.hiddenAmount):
						self.matrix2[i+1][j] -= self.eta * outDelta[j] * self.hiddenList[i]
				for j in range(self.hiddenAmount):
					self.matrix1[0][j] -= self.eta * hiddenDelta[j] * 1
					for i in range(self.inputAmount):
						self.matrix1[i+1][j] -= self.eta * hiddenDelta[j] * inputs[ite][i]

	#forward passes the inputs through the neural net to get the outputs.
	def forward(self, inputs):
		for i in range(len(self.hiddenList)):
			self.hiddenU[i]	= 1*self.matrix1[0][i]
			for j in range(self.inputAmount):
				self.hiddenU[i] += inputs[j] * self.matrix1[j+1][i]
			self.hiddenList[i] = expit(self.hiddenU[i])
		for i in range(len(self.outputList)):
			self.outputA[i]	= 1*self.matrix2[0][i]
			for j in range(len(self.hiddenList)):
				self.outputA[i] += self.hiddenList[j]*self.matrix2[j+1][i]
			self.outputList[i] = self.identityFunction(self.outputA[i])
	
	"""To find the best move, the input is run forward through the neural net. The highest output is considered the chosen move.
	If the chosen output is illegal it is trimmed, to make it legal, either making it bigger or smaller. if the index is of a hap of 0,
	a removal of 1 in some non-empty heap is chosen."""
	def makeMove(self, state):
		self.forward(state)
		if(state[0] < -1):
			1/0
		move = [0,0]
		move[1] = np.argmax(self.outputList)
		move[0] = int(self.outputList[move[1]])
		if(move[0] < 1):
			move[0] = 1
		elif(move[0] > state[move[1]]):
			move[0] = state[move[1]]
		if(state[move[1]] == 0):
			for i in range(len(state)):
				if(state[i] > 0):
					move[0] = 1
					move[1] = i
		return move