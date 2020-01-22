import MakeData as MD
import PerfectPlayer as PP
import numpy as np
import mlp
import sys
import time

if(len(sys.argv) < 5):
	print("Error: too few arguments. Got " + str(len(sys.argv)-1) + ", Expected 4")
elif (len(sys.argv) > 5):
	print("Error: too many arguments. Got, " + str(len(sys.argv)-1) + ", Expected 4")
else:
	#Parsing the input.
	heapSizeLower = int(sys.argv[1])
	heapSizeUpper = int(sys.argv[2])
	heapAmountLower = int(sys.argv[3])
	heapAmountUpper = int(sys.argv[4])
	f = open("mlpstatistics.txt", "w")
	filename = "CorrectMoves.txt"
	player = PP.PerfectPlayer()
	#The loop that defines the start-states from which the programs will be run.
	for heapSize in range(heapSizeLower, heapSizeUpper+1):
		for heapAmount in range(heapAmountLower, heapAmountUpper+1):
			"""The Supervised learning program is run 10 times for each start-state, and plays against the perfect player each time,
			to get a winrate for statistics. The time used is also written to file as statistics. The data used is the same for a given state,
			but it is sorted differently for each time."""
			state = [heapSize] * heapAmount
			print(state)
			md = MD.MakeData()
			md.setup(state)
			timeAvg = 0
			percent = 0
			for i in range(10):
				#sorting and separating the data into the needed categories.
				data = np.loadtxt(filename)

				stateLen = len(data[0]) 

				boards = data[::2]
				moves = data[1::2]

				order = list(range(np.shape(boards)[0]))
				np.random.shuffle(order)
				boards = boards[order,:]
				moves = moves[order,:]

				train = boards[::2]
				trainTargets = moves[::2]

				valid = boards[1::4]
				validTargets = moves[1::4]

				test = boards[3::4]
				testTargets = moves[3::4]

				hidden = len(state)+10
				
				start = time.time()
				net = mlp.mlp(hidden, stateLen)
				net.earlystopping(train, trainTargets, valid, validTargets)
				end = time.time()
				timeAvg += end-start
				listOfStates = md.getStates()
				wins = 0
				losses = 0
				for i in range(len(listOfStates)):
					if(player.findNimSum(listOfStates[i]) != 0):
						playing = 1
						board = listOfStates[i][:]
						winBoard = [0] * len(listOfStates[i])
						while(playing):
							move = net.makeMove(board)
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
			line = "Time used:" + str(round(timeAvg, 3)) + "s Winrate/sucessrate: " + str(int(percent)) + "\\% "
			line += str(state) + "\n"
			f.write(line)