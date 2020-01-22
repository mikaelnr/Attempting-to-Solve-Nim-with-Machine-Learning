import time
import sys

import ReinforcementSarsa as RS
import ReinforcementQlearning as RQ
import PerfectPlayer as PP
import SpaceSaveSarsa as SS
import SpaceSaveQlearning as SQ
import OneDSarsa as ODS
import SpaceSaveSarsaSpread as SSSS

if(len(sys.argv) < 5):
	print("Error: too few arguments. Got " + str(len(sys.argv)-1) + ", Expected 4")
elif (len(sys.argv) > 5):
	print("Error: too many arguments. Got, " + str(len(sys.argv)-1) + ", Expected 4")
else:
	#Parsing the input
	startState = list(map(int, sys.argv[3].split(',')))
	trainingType = int(sys.argv[2])
	if(trainingType == 0):
		ml = RS.ReinforcementSarsa(startState)
	elif(trainingType == 1):
		ml = RQ.ReinforcementQlearning(startState)
	elif(trainingType == 2):
		ml = SS.SpaceSaveSarsa(startState)
	elif(trainingType == 3):
		ml = SQ.SpaceSaveQlearning(startState)
	elif(trainingType == 4):
		ml = ODS.OneDSarsa(startState)
	else:
		ml = SSSS.SpaceSaveSarsaSpread(startState)
	ml.setup()
	
	#The code for the reinforcement program playing against the deterministic program, and getting statistics from it.
	if(int(sys.argv[1]) == 0):
		playstatistics = open("playstatistics.txt", "w")
		playstatistics.write(str(trainingType) + "\n")
		player = PP.PerfectPlayer()
		playing = 1
		board = startState[:]
		winBoard = [0] * len(startState)
		#If the reinforcement algo gets the first move it gets to make a move before the loop start.
		if(int(sys.argv[4]) == 1):
			start = time.time()
			move = player.makeMove(board)
			end = time.time()
			moveTime = end-start
			board[move[1]] = board[move[1]]-move[0]
			playstatistics.write("Move by Pre-algo, took " + str(move[0]) + " counters from heap " + str(move[1]+1) + ". New state: " + str(board) + " time used: " + str(round(moveTime, 3)) + "s.\n")
			if(board == winBoard):
				playstatistics.write("Pre-algo is the winner.")
				playing = 0
		#Otherwise the game starts here.
		while(playing):
			start = time.time()
			move = ml.makeMove(board)
			end = time.time()
			moveTime = end-start
			board[move[1]] = board[move[1]]-move[0]
			playstatistics.write("Move by ML, took " + str(move[0]) + " counters from heap " + str(move[1]+1) + ". New state: " + str(board) + " time used: " + str(round(moveTime, 3)) + "s.\n")
			if(board == winBoard):
				playstatistics.write("ML is the winner.")
				break
			start = time.time()
			move = player.makeMove(board)
			end = time.time()
			moveTime = end-start
			board[move[1]] = board[move[1]]-move[0]
			playstatistics.write("Move by Pre-algo, took " + str(move[0]) + " counters from heap " + str(move[1]+1) + ". New state: " + str(board) + " time used: " + str(round(moveTime, 3)) + "s.\n")
			if(board == winBoard):
				playstatistics.write("Pre-algo is the winner.")
				break
	#If the player wants to play against the Reinforcement algo.
	else:
		player = PP.PerfectPlayer()
		playing = 1
		board = startState[:]
		winBoard = [0] * len(startState)
		#If the player wants to start first, they make a move first.
		if(int(sys.argv[4]) == 1):
			move = [-1, -1]
			print("Current board is: " + str(board) + "\n")
			move[1] = int(input("Which heap do you want to remove from? "))-1
			while((move[1] < 0 or move[1] >= len(board)) or board[move[1]] == 0):
				move[1] = int(input("Illegal heap, choose again. "))-1
			move[0] = int(input("How many counters do you wish to remove? "))
			while(move[0] < 1 or move[0] > board[move[1]]):
				move[0] = int(input("Illegal amount, choose again. "))
			board[move[1]] = board[move[1]]-move[0]
			if(board == winBoard):
				print("You are the winner.")
				playing = 0
		#Otherwise the game starts here, with the reinforcement program making the first move.
		while(playing):
			move = ml.makeMove(board)
			board[move[1]] = board[move[1]]-move[0]
			print("Move by ML, took " + str(move[0]) + " counters from heap " + str(move[1]+1) + ".")
			if(board == winBoard):
				print("ML is the winner.")
				break
			move = [-1, -1]
			print("Current board is: " + str(board) + "\n")
			move[1] = int(input("Which heap do you want to remove from? "))-1
			while(move[1] < 0 or move[1] >= len(board) or board[move[1]] == 0):
				move[1] = int(input("Illegal heap, choose again. "))-1
			move[0] = int(input("How many counters do you wish to remove? "))
			while(move[0] < 1 or move[0] > board[move[1]]):
				move[0] = int(input("Illegal amount, choose again. "))
			board[move[1]] = board[move[1]]-move[0]
			if(board == winBoard):
				print("You are the winner.")
				break