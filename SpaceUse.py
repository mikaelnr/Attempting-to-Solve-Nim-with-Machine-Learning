import numpy as np
import random

a = [2, 1]
sum = a[0]+1
for i in range(1, len(a)):
	sum *= a[i]+1



def newIndex(heapIndex, amount):
	newMove = 1
	for i in range(len(a)-1, heapIndex, -1):
		newMove *= a[i]+1
	newMove *= amount
	return newMove

print(newIndex(0, 1))
		
print(sum)
listOfStates = [0] * sum
listOfStates[0] = a[:]
T = []
Q = []
newSum = 1

def makeMove(state):
	curState = state[:]
	nextState = []
	move = []
	if (len(state)<len(listOfStates[0])):
		dif = len(listOfStates[0])-len(state)
		for i in range(dif):
			curState.append(0)
	for i in range(len(listOfStates)):
		if (curState == listOfStates[i]):
			nextState = listOfStates[np.argmax(Q[i])]
	for i in range(len(curState)):
		if (curState[i] != nextState[i]):
			move.append(curState[i] - nextState[i])
			move.append(i)
			return move

for i in range(sum):
	T.append([0] * sum)
	for x in range(len(listOfStates[i])):
		for y in range(1, listOfStates[i][x] + 1):
			tmpValue = newIndex(x, y)
			T[i][i+tmpValue] = 1
			if(listOfStates[i+tmpValue] == 0):
				tmpList = listOfStates[i][:]
				tmpList[x] -= y
				listOfStates[i+tmpValue] = tmpList[:]
			
	Q.append([])
	for j in range(sum-1):
		if(T[i][j] == 1):
			Q[i].append(random.random())
		else:
			Q[i].append(-np.inf)
	if (T[i][sum-1] == 1):
		Q[i].append(100.0)
	else:
		Q[i].append(-np.inf)

epsilon = 0.2
mu = 0.1
gamma = 0.1
amountEpisodes = 200

def epsilonGreedyChoice(state):
	if(random.random()<epsilon):
		tmpList = []
		for i in range(state, sum):
			if(T[state][i] == 1):
				tmpList.append(i)
		return tmpList[random.randrange(0, len(tmpList))]
	else:
		return np.argmax(Q[state])
for neverUsed in range(amountEpisodes):
	curState = 0
	curAction = epsilonGreedyChoice(curState)
	playing = 1
	while(playing):
		curReward = Q[curState][curAction]
		nextState = curAction
		nextAction = epsilonGreedyChoice(nextState)
		Q[curState][curAction] += mu * (curReward - gamma*Q[nextState][nextAction] - Q[curState][curAction])
		curState = nextState
		curAction = nextAction
		if (curAction == sum-1):
			playing = 0

for i in range(sum):
	print(Q[i])
for i in range(sum):
	print(T[i])
print(listOfStates)
print(makeMove([0, 1]))
