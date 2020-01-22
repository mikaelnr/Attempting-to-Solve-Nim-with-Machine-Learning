class PerfectPlayer:
	#This method applies the deterministic algorithm for making perfect moves in Nim, and returns the index of the move and the amoiunt of counters removed.
	def makeMove(self, state):
		nimSum = self.findNimSum(state)
		for i in range(len(state)):
			remove = nimSum^state[i]
			if(remove < state[i]):
				result = [state[i] - remove, i]
				return result
		for i in range(len(state)):
			if(state[i] != 0):
				result = [1, i]
				return result
		return -1
	
	#Since finding nimsums is relevant in the program Run.py this program finds the nimsum of the input state.
	def findNimSum(self, state):
		nimSum = 0
		for i in range(len(state)):
			nimSum = nimSum^state[i]
		return nimSum