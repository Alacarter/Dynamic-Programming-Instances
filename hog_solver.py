import math

def HogSolver(y, t, opt_table = {}, change_opt_table_permissions = 0):
	bestNumDiceToRoll = 0
	def H(y, t, table, s = 0):
		# H(y, t, s) = optimal probability you win given it's your turn and the score is y (your) to t (theirs), 
		# and s is 0 if scores not swapped yet in that round
		nonlocal bestNumDiceToRoll
		if t > 1 and y > 1 and (t % y == 0 or y % t == 0) and s == 0:
			if (t, y, 1) not in table:
				table[(t, y, 1)] = H(t, y, table, 1)
			return table[(t, y, 1)]
		elif y >= 100:
			return 1
		elif t >= 100:
			return 0
		else:
			freebacon_score = 1 + max(t % 10, (t // 10) % 10)
			if (t, y + freebacon_score, 0) not in table:
				table[(t, y + freebacon_score, 0)] = H(t, y + freebacon_score, table)
			maxWinProb = 1 - table[(t, y + freebacon_score, 0)] # rolling 0 (free bacon)
			#bestNumDiceToRoll = 0 #nonlocal declared outside of function
			for numDiceToRoll in range (1, 11):
				#iterate over rolling 1 to 10 dice. Calculate probabilities of winning.
				winProb_rolling_i_dice = 1 - opp_win_prob_if_you_roll(numDiceToRoll, y, t, table)
				if winProb_rolling_i_dice > maxWinProb:
					maxWinProb = winProb_rolling_i_dice
					bestNumDiceToRoll = numDiceToRoll
			table[(y, t, 0)] = maxWinProb
			if change_opt_table_permissions:
				opt_table[(y, t)] = bestNumDiceToRoll
			return maxWinProb
	
	def opp_win_prob_if_you_roll(numDice, y, t, table):
		numPigOutPermutations = [0, 1, 11, 91, 671, 4651, 31031, 201811, 1288991, 8124571, 50700551]
		npop = numPigOutPermutations

		numPos = [[] for _ in range(11)]
		numPos[1] = [0, npop[1], 1, 1, 1, 1, 1]
		numPos[2] = [0, npop[2], 0, 0, 1, 2, 3, 4, 5, 4, 3, 2, 1]
		numPos[3] = [0, npop[3], 0, 0, 0, 0, 1, 3, 6, 10, 15, 18, 19, 18, 15, 10, 6, 3, 1]
		numPos[4] = [0, npop[4], 0, 0, 0, 0, 0, 0, 1, 4, 10, 20, 35, 52, 68, 80, 85, 80, 68, 52, 35, 20, 10, 4, 1]
		numPos[5] = [0, npop[5], 0, 0, 0, 0, 0, 0, 0, 0, 1, 5, 15, 35, 70, 121, 185, 255, 320, 365, 381, 365, 320, 255, 185, 121, 70, 35, 15, 5, 1]
		numPos[6] = [0, npop[6], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 6, 21, 56, 126, 246, 426, 666, 951, 1246, 1506, 1686, 1751, 1686, 1506, 1246, 951, 666, 426, 246, 126, 56, 21, 6, 1]
		numPos[7] = [0, npop[7], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 7, 28, 84, 210, 455, 875, 1520, 2415, 3535, 4795, 6055, 7140, 7875, 8135, 7875, 7140, 6055, 4795, 3535, 2415, 1520, 875, 455, 210, 84, 28, 7, 1]
		numPos[8] = [0, npop[8], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 8, 36, 120, 330, 784, 1652, 3144, 5475, 8800, 13140, 18320, 23940, 29400, 34000, 37080, 38165, 37080, 34000, 29400, 23940, 18320, 13140, 8800, 5475, 3144, 1652, 784, 330, 120, 36, 8, 1]
		numPos[9] = [0, npop[9], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 9, 45, 165, 495, 1278, 2922, 6030, 11385, 19855, 32211, 48879, 69675, 93600, 118800, 142740, 162585, 175725, 180325, 175725, 162585, 142740, 118800, 93600, 69675, 48879, 32211, 19855, 11385, 6030, 2922, 1278, 495, 165, 45, 9, 1]
		numPos[10] = [0, npop[10], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 10, 55, 220, 715, 1992, 4905, 10890, 22110, 41470, 72403, 118360, 182005, 264220, 363165, 473694, 587400, 693450, 780175, 837100, 856945, 837100, 780175, 693450, 587400, 473694, 363165, 264220, 182005, 118360, 72403, 41470, 22110, 10890, 4905, 1992, 715, 220, 55, 10, 1]

		if (t, y+1, 0) not in table:
			table[(t, y+1, 0)] = H(t, y + 1, table)
		prob_sum = numPigOutPermutations[numDice] * table[(t, y+1, 0)]
		for outcome in range(2 * numDice, 6 * numDice + 1):
			if (t, y+outcome, 0) not in table:
				table[(t, y+outcome, 0)] = H(t, y + outcome, table)
			prob_sum += numPos[numDice][outcome] * table[(t, y+outcome, 0)]
		prob_sum = prob_sum / 6**numDice
		return prob_sum
	
	def nCr(n,r):
			f = math.factorial
			return int(f(n) / f(r) / f(n-r))

	def numPigOutPermutations(numDice):
		# Calculates number of dice permutations that yield PigOut (at least 1 dice is 1)
		numPermutations = 0
		for i in range(1, numDice + 1):
			numPermutations += nCr(numDice, i) * 5**(numDice - i)
		return numPermutations

	def numPossibilities(numDice, outcome):
		def cbib(n, k):
			#constrained balls in bins. Each bin must have between 2 to 6 balls. Each bin = one dice.
			if n == 0 and k == 0:
				return 1
			elif n <= 0 or k <= 0:
				return 0
			else:
				numWays = 0
				for i in range(2, 7):
					numWays += cbib(n - i, k - 1)
				return numWays
		return cbib(outcome, numDice)
	H(y, t, {}, 1)
	return bestNumDiceToRoll

def createOptTable():
	f = open("hog_optimal_moves_table.txt", "r") #added Dec 2018
	opt_table = eval(f.read()) #added Dec 2018
	opt_table_copy = dict(opt_table)
	f.close()
	for i in range(100):
		for j in range(100):
			if (i, j) not in opt_table:
				opt_table[(i, j)] = HogSolver(i, j, opt_table_copy)
				print("(" + str(i) + ", " + str(j) + ")", opt_table[(i, j)])
				print("opt_table length:", len(opt_table))
	print(opt_table)
	g = open('hog_complete_optimal_moves_table.txt', 'w')
	g.write(str(opt_table))

#createOptTable()
