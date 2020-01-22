import time
import sys
import ReinforcementSarsa as RS
import ReinforcementQlearning as RQ
import PerfectPlayer as PP
import SpaceSaveSarsa as SS
import SpaceSaveQlearning as SQ
import OneDSarsa as ODS
import SpaceSaveSarsaSpread as SSSS

if(len(sys.argv) < 11):
	print("Error: too few arguments. Got " + str(len(sys.argv)-1) + ", Expected 10")
elif (len(sys.argv) > 11):
	print("Error: too many arguments. Got, " + str(len(sys.argv)-1) + ", Expected 10")
else:
	#Parsing the input.
	heapSizeLower = int(sys.argv[1])
	heapSizeUpper = int(sys.argv[2])
	heapAmountLower = int(sys.argv[3])
	heapAmountUpper = int(sys.argv[4])

	player = PP.PerfectPlayer()

	ssstatistics = open("ssstatistics.txt", "w")
	
	#writing the header of the statistics file, to show which numbers correspond to which program.
	header = ""
	if(int(sys.argv[5]) == 1):
		header += "\t\t\t\t\t\tRS\t"
	if(int(sys.argv[6]) == 1):
		header += "\t\t\t\t\t\tRQ\t"
	if(int(sys.argv[7]) == 1):
		header += "\t\t\t\t\t\tTS\t"
	if(int(sys.argv[8]) == 1):
		header += "\t\t\t\t\t\tTQ\t"
	if(int(sys.argv[9]) == 1):
		header += "\t\t\t\t\t\tODS\t"
	if(int(sys.argv[10]) == 1):
		header += "\t\t\t\t\t\tNew Program"
	header += "\n"
	ssstatistics.write(header)
	#The loop that defines the start-states from which the programs will be run.
	for heapSize in range(heapSizeLower, heapSizeUpper+1):
		for heapAmount in range(heapAmountLower, heapAmountUpper+1):
			state = [heapSize] * heapAmount
			print(state)
			line = ""
			"""This repeats for each program. For each start-state they are run 10 times, taking their time use, after which they are set to play against the perfect player
			for all starts it can play from, from which it can win when starting. That is, the states with a nim-sum != 0. The averages of the times and winrate is then
			written into the statistics file."""
			if(int(sys.argv[5]) == 1):
				timeAvg = 0
				percent = 0
				setupTime = 0
				trainTime = 0
				for i in range(10):
					start = time.time()
					rs = RS.ReinforcementSarsa(state)
					times = rs.setup()
					end = time.time()
					timeAvg += end-start
					setupTime += times[0]
					trainTime += times[1]
					listOfStates = rs.getListOfStates()
					wins = 0
					losses = 0
					for i in range(len(listOfStates)):
						if(player.findNimSum(listOfStates[i]) != 0):
							playing = 1
							board = listOfStates[i][:]
							winBoard = [0] * len(listOfStates[i])
							while(playing):
								move = rs.makeMove(board)
								board[move[1]] = board[move[1]]-move[0]
								if(board == winBoard):
									wins += 1
									break
								move = player.makeMove(board)
								board[move[1]] = board[move[1]]-move[0]
								if(board == winBoard):
									losses += 1
									break
					percent += (wins/(wins+losses)*100)
				timeAvg /= 10
				percent /= 10
				setupTime /= 10
				trainTime /= 10
				line += "setup: " + str(round(setupTime, 3)) + "s\t train: " + str(round(trainTime, 3)) + "s\t total: " + str(round(timeAvg, 3)) + "s\t" + str(int(percent)) + "%\t"
			if(int(sys.argv[6]) == 1):
				timeAvg = 0
				percent = 0
				setupTime = 0
				trainTime = 0
				for i in range(10):
					start = time.time()
					rq = RQ.ReinforcementQlearning(state)
					times = rq.setup()
					end = time.time()
					timeAvg += end-start
					setupTime += times[0]
					trainTime += times[1]
					listOfStates = rq.getListOfStates()
					wins = 0
					losses = 0
					for i in range(len(listOfStates)):
						if(player.findNimSum(listOfStates[i]) != 0):
							playing = 1
							board = listOfStates[i][:]
							winBoard = [0] * len(listOfStates[i])
							while(playing):
								move = rq.makeMove(board)
								board[move[1]] = board[move[1]]-move[0]
								if(board == winBoard):
									wins += 1
									break
								move = player.makeMove(board)
								board[move[1]] = board[move[1]]-move[0]
								if(board == winBoard):
									losses += 1
									break
					percent += (wins/(wins+losses)*100)
				timeAvg /= 10
				percent /= 10
				setupTime /= 10
				trainTime /= 10
				line += "setup: " + str(round(setupTime, 3)) + "s\t train: " + str(round(trainTime, 3)) + "s\t total: " + str(round(timeAvg, 3)) + "s\t" + str(int(percent)) + "%\t"
			if(int(sys.argv[7]) == 1):
				timeAvg = 0
				percent = 0
				setupTime = 0
				trainTime = 0
				for i in range(10):
					start = time.time()
					sss = SS.SpaceSaveSarsa(state)
					times = sss.setup()
					end = time.time()
					timeAvg += end-start
					setupTime += times[0]
					trainTime += times[1]
					listOfStates = sss.getListOfStates()
					wins = 0
					losses = 0
					for i in range(len(listOfStates)):
						if(player.findNimSum(listOfStates[i]) != 0):
							playing = 1
							board = listOfStates[i][:]
							winBoard = [0] * len(listOfStates[i])
							while(playing):
								move = sss.makeMove(board)
								board[move[1]] = board[move[1]]-move[0]
								if(board == winBoard):
									wins += 1
									break
								move = player.makeMove(board)
								board[move[1]] = board[move[1]]-move[0]
								if(board == winBoard):
									losses += 1
									break
					percent += (wins/(wins+losses)*100)
				timeAvg /= 10
				percent /= 10
				setupTime /= 10
				trainTime /= 10
				line += "setup: " + str(round(setupTime, 3)) + "s\t train: " + str(round(trainTime, 3)) + "s\t total: " + str(round(timeAvg, 3)) + "s\t" + str(int(percent)) + "%\t"
			if(int(sys.argv[8]) == 1):
				timeAvg = 0
				percent = 0
				setupTime = 0
				trainTime = 0
				for i in range(10):
					start = time.time()
					ssq = SQ.SpaceSaveQlearning(state)
					times = ssq.setup()
					end = time.time()
					timeAvg += end-start
					setupTime += times[0]
					trainTime += times[1]
					listOfStates = ssq.getListOfStates()
					wins = 0
					losses = 0
					for i in range(len(listOfStates)):
						if(player.findNimSum(listOfStates[i]) != 0):
							playing = 1
							board = listOfStates[i][:]
							winBoard = [0] * len(listOfStates[i])
							while(playing):
								move = ssq.makeMove(board)
								board[move[1]] = board[move[1]]-move[0]
								if(board == winBoard):
									wins += 1
									break
								move = player.makeMove(board)
								board[move[1]] = board[move[1]]-move[0]
								if(board == winBoard):
									losses += 1
									break
					percent += (wins/(wins+losses)*100)
				timeAvg /= 10
				percent /= 10
				setupTime /= 10
				trainTime /= 10
				line += "setup: " + str(round(setupTime, 3)) + "s\t train: " + str(round(trainTime, 3)) + "s\t total: " + str(round(timeAvg, 3)) + "s\t" + str(int(percent)) + "%\t"
			if(int(sys.argv[9]) == 1):
				timeAvg = 0
				percent = 0
				setupTime = 0
				trainTime = 0
				for i in range(10):
					start = time.time()
					ods = ODS.OneDSarsa(state)
					times = ods.setup()
					end = time.time()
					timeAvg += end-start
					setupTime += times[0]
					trainTime += times[1]
					listOfStates = ods.getListOfStates()
					wins = 0
					losses = 0
					for i in range(len(listOfStates)):
						if(player.findNimSum(listOfStates[i]) != 0):
							playing = 1
							board = listOfStates[i][:]
							winBoard = [0] * len(listOfStates[i])
							while(playing):
								move = ods.makeMove(board)
								board[move[1]] = board[move[1]]-move[0]
								if(board == winBoard):
									wins += 1
									break
								move = player.makeMove(board)
								board[move[1]] = board[move[1]]-move[0]
								if(board == winBoard):
									losses += 1
									break
					percent += (wins/(wins+losses)*100)
				timeAvg /= 10
				percent /= 10
				setupTime /= 10
				trainTime /= 10
				line += "setup: " + str(round(setupTime, 3)) + "s\t train: " + str(round(trainTime, 3)) + "s\t total: " + str(round(timeAvg, 3)) + "s\t" + str(int(percent)) + "%\t"
			if(int(sys.argv[10]) == 1):
				timeAvg = 0
				percent = 0
				setupTime = 0
				trainTime = 0
				for i in range(10):
					start = time.time()
					ssss = SSSS.SpaceSaveSarsaSpread(state)
					times = ssss.setup()
					end = time.time()
					timeAvg += end-start
					setupTime += times[0]
					trainTime += times[1]
					listOfStates = ssss.getListOfStates()
					wins = 0
					losses = 0
					for i in range(len(listOfStates)):
						if(player.findNimSum(listOfStates[i]) != 0):
							playing = 1
							board = listOfStates[i][:]
							winBoard = [0] * len(listOfStates[i])
							while(playing):
								move = ssss.makeMove(board)
								board[move[1]] = board[move[1]]-move[0]
								if(board == winBoard):
									wins += 1
									break
								move = player.makeMove(board)
								board[move[1]] = board[move[1]]-move[0]
								if(board == winBoard):
									losses += 1
									break
					percent += (wins/(wins+losses)*100)
				timeAvg /= 10
				percent /= 10
				setupTime /= 10
				trainTime /= 10
				line += "setup: " + str(round(setupTime, 3)) + "s\t train: " + str(round(trainTime, 3)) + "s\t total: " + str(round(timeAvg, 3)) + "s\t" + str(int(percent)) + "%\t"
			line += str(state) + "\n"
			ssstatistics.write(line)