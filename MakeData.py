import PerfectPlayer as PP

class MakeData:
	#This method just makes the list of states accessible from the start-state, and then runs the writeToFile method.
	def setup(self, startBoard):
		sum = startBoard[0]+1
		board = startBoard
		for i in range(1, len(board)):
			sum *= board[i]+1
		self.listOfStates = [0] * sum
		self.listOfStates[0] = board[:]
		for i in range(sum):
			for x in range(len(self.listOfStates[i])):
				for y in range(1, self.listOfStates[i][x] + 1):
					tmpValue = self.newIndex(x, y, board)
					if(self.listOfStates[i+tmpValue] == 0):
						tmpList = self.listOfStates[i][:]
						tmpList[x] -= y
						self.listOfStates[i+tmpValue] = tmpList[:]
		self.writeToFile(self.listOfStates)
			
	# This method exists for finding, given a move, how far down the list of states the new state is.
	def newIndex(self, heapIndex, amount, board):
		newMove = 1
		for i in range(len(board)-1, heapIndex, -1):
			newMove *= board[i]+1
		newMove *= amount
		return newMove

	#This file writes each state in the list to the file, and a correct move to make when in that state.
	def writeToFile(self, states):
		player = PP.PerfectPlayer()
		f = open("CorrectMoves.txt", "w")
		for i in range(len(states)):
			if (player.findNimSum(states[i]) != 0):
				tmp = [0]*len(states[0])
				result = player.makeMove(states[i])
				tmp[result[1]] = result[0]
				for j in range(len(states[i])):
					f.write(str(states[i][j]) + " ")
				f.write("\n")
				for j in range(len(states[i])):
					f.write(str(tmp[j]) + " ")
				f.write("\n")
	
	#This method returns the list of states, which is used to test programs, by having them play from many different states.
	def getStates(self):
		return self.listOfStates