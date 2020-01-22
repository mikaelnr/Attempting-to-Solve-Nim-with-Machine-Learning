import time
import sys
import ReinforcementSarsa as RS
import ReinforcementQlearning as RQ
import PerfectPlayer as PP
import SpaceSaveSarsa as SS
import SpaceSaveQlearning as SQ
import OneDSarsa as ODS
import SpaceSaveSarsaSpread as SSS

if(len(sys.argv) < 6):
	print("Error: too few arguments. Got " + str(len(sys.argv)-1) + ", Expected 5")
elif (len(sys.argv) > 6):
	print("Error: too many arguments. Got, " + str(len(sys.argv)-1) + ", Expected 5")
else:
	#Parsing the input.
	heapSizeLower = int(sys.argv[1])
	heapSizeUpper = int(sys.argv[2])
	heapAmountLower = int(sys.argv[3])
	heapAmountUpper = int(sys.argv[4])
	trainingType = int(sys.argv[5])
	player = PP.PerfectPlayer()
	ssstatistics = open("episodestatistics.txt", "w")
	#The desired percentage winrate, which terminates the program.
	goal = 90
	ssstatistics.write("Type: " + str(trainingType) + " ,percentage goal: " + str(goal) + "%\n")
	for heapSize in range(heapSizeLower, heapSizeUpper+1):
		for heapAmount in range(heapAmountLower, heapAmountUpper+1):
			state = [heapSize] * heapAmount
			print(state)
			#Settings for the programs to train.
			amountEpisodes = 10
			epsilon = 0.1
			mu = 0.5
			gamma = 0.5
			totalTime = 0
			start = time.time
			#The selection of the correct program to run.
			if(trainingType == 0):
				ml = RS.ReinforcementSarsa(state)
			elif(trainingType == 1):
				ml = RQ.ReinforcementQlearning(state)
			elif(trainingType == 2):
				ml = SS.SpaceSaveSarsa(state)
			elif(trainingType == 3):
				ml = SQ.SpaceSaveQlearning(state)
			elif(trainingType == 4):
				ml = ODS.OneDSarsa(state)
			else:
				ml = SSS.SpaceSaveSarsaSpread(state)
			ml.setup(1)
			end = time.time()
			listOfStates = ml.getListOfStates()
			totalTime += end - start
			stillTraining = 1
			totalEpisodes = 0
			#This loop runs until the percentage winrate is equal or higher than the desired goal.
			while(stillTraining):
				start = time.time()
				ml.train(amountEpisodes, epsilon, mu, gamma)
				end = time.time()
				totalTime += end-start
				wins = 0
				losses = 0
				"""Unlike in the program Run.py the statistics aren't repeated ten times. Quite understandably, this would not work here,
				because the desire is one properly trained program, not ten alright ones."""
				for i in range(len(listOfStates)):
					if(player.findNimSum(listOfStates[i]) != 0):
						playing = 1
						board = listOfStates[i][:]
						winBoard = [0] * len(listOfStates[i])
						while(playing):
							move = ml.makeMove(board)
							board[move[1]] = board[move[1]]-move[0]
							if(board == winBoard):
								wins += 1
								break
							move = player.makeMove(board)
							board[move[1]] = board[move[1]]-move[0]
							if(board == winBoard):
								losses += 1
								break
				totalEpisodes += amountEpisodes
				percent = (wins//(wins+losses)*100)
				if(percent >= goal):
					stillTraining = 0
			ssstatistics.write("Time used: " + str(round(totalTime, 3)) + "s, Episodes used: " + str(totalEpisodes) + ", " + str(state) + "\n")