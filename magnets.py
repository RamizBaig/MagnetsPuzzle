import copy, time
solved = False
completedBoard = None

# canPutHorizontally and Vertically and rulesMet are pruning methods for the recursive calls
def canPutPatternHorizontally(rules,i,j,pat):
	if pat == "xx": # dominoe pattern
		if (len(rules)-1-i < top[j]+bottom[j]) or (len(rules)-1-i < top[j+1]+bottom[j+1]): return False # not enough squares for future req
		if len(rules[0])-2 == j and (left[i]>0 or right[i]>0): return False # if last col and req not met
		if len(rules)-1 == i and (top[j]>0 or top[j+1]>0 or bottom[j]>0 or bottom[j+1]>0): return False # last row and req not met
		return True

	if (left[i]==0 or right[i]==0): return False # req previosusly met
	elif (len(rules[0])-j==2) and (left[i]>1 or right[i]>1): return False # req too large
	elif j-1>=0 and rules[i][j-1] == pat[0]: return False # dominoe to the left is not same
	elif i-1>=0 and rules[i-1][j] == pat[0]: return False# dominoe above is not same
	elif i-1>=0 and rules[i-1][j+1] == pat[1]: return False # dominoe above and right is not same as pat end
	elif j+2 < len(rules[0]) and rules[i][j+2] == pat[1]: return False # dominoe to right of right is not same as pat end
		
	if pat == "+-": #dominoes pattern +-
		if (top[j]==0 or bottom[j+1]==0): return False # reqs previously met
		if (len(rules)-1==i) and (top[j]>1 or top[j+1]>0 or bottom[j+1]>1 or bottom[j]>0): return False # last row and req too large
	
	elif pat == "-+": # dominoe pattern -+
		if (bottom[j]==0 or top[j+1]==0): return False # reqs previously met
		if (len(rules)-1==i) and (bottom[j]>1 or bottom[j+1]>0 or top[j+1]>1 or top[j]>0): return False # last row and req too large

	return True

def canPutPatternVertically(rules,i,j,pat): # only ever called on if (i,j) is "T"
	if pat == "xx": # dominoe pattern x/x
		if len(rules)-2-i < top[j]+bottom[j]: return False # if not enough squares to meet reqs
		if len(rules)-2 == i and (top[j]>0 or bottom[j]>0): return False # last row and reqs not met
		if len(rules[0])-1 == j and (left[i]>0 or right[i]>0): return False # last row and reqs not met
		return True

	if (top[j]==0 or bottom[j]==0): return False # reqs alr met
	if (len(rules)-2==i) and (top[j]>1 or bottom[j]>1): return False # reqs too large to meet
	
	if j-1>=0 and rules[i][j-1] == pat[0]: return False # dominoe to the left is not same
	elif i-1>=0 and rules[i-1][j] == pat[0]: return False # dominoe above is not same
	elif j+1 < len(rules[0]) and rules[i][j+1] == pat[0]: return False # dominoe to the right is not the same
 
	if pat == "+-": # dominoe pattern +/-
		if (left[i]==0 or right[i+1]==0): return False # reqs previously met
		if (len(rules[0])-1==j) and (left[i]>1): return False # last row and req cant meet
	
	elif pat == "-+": # dominoe patter -/+
		if (right[i]==0 or left[i+1]==0): return False # req previously met
		if (len(rules[0])-1==j) and (right[i]>1): return False # last row and req cant meet
	
	return True

def rulesMet(rules,i,j): # secondary check, for going over an end peice of a dominoe previpusly place
	if (len(rules[0])-1==j) and (left[i]>0 or right[i]>0): return False # last col and req not met
	if (len(rules)-1==i) and (top[j]>0 or bottom[j]>0): return False # last row and req not met
	return True

def addOrRemoveMagnet(rules,i,j,oppVec,pat,amount=None,reqChangeVec=None): 
    # to add/remove a magnet with any pattern, in any direction, reqChangeVec is a 4tuple of the dif of the 4 direction req vectors
	rules[i][j] = pat[0]
	rules[i+oppVec[0]][j+oppVec[1]] = pat[1]
	if amount:
		top[j+reqChangeVec[0]]+=amount
		left[i+reqChangeVec[1]]+=amount
		right[i+reqChangeVec[2]]+=amount
		bottom[j+reqChangeVec[3]]+=amount

def solveMagnets(rules,i,j): # recusive backtracing aproach
	global solved, completedBoard
	if solved:
		return
	if i == len(rules) and j == 0: # complete
		solved = True
		completedBoard=copy.deepcopy(rules)
	elif j >= len(rules[0]): # off the board on right
		solveMagnets(rules,i+1,0)

	else: # normal solving cases
		if rules[i][j] == "L": # solving a horizontal dominoe
			if canPutPatternHorizontally(rules,i,j,"xx"): # tries putting a xx dominoe(horizontal)
				addOrRemoveMagnet(rules,i,j,(0,1),"xx")
				solveMagnets(rules,i,j+2)
				addOrRemoveMagnet(rules,i,j,(0,1),"LR")
			if canPutPatternHorizontally(rules,i,j,"+-"): # tries putting a +- dominoe (horizontal)
				addOrRemoveMagnet(rules,i,j,(0,1),"+-",-1,(0,0,0,1))
				solveMagnets(rules,i,j+2)
				addOrRemoveMagnet(rules,i,j,(0,1),"LR",1,(0,0,0,1))
			if canPutPatternHorizontally(rules,i,j,"-+"): # tries putting a -+ dominoe (horizontal)
				addOrRemoveMagnet(rules,i,j,(0,1),"-+",-1,(1,0,0,0))
				solveMagnets(rules,i,j+2)
				addOrRemoveMagnet(rules,i,j,(0,1),"LR",1,(1,0,0,0))
			
		elif rules[i][j] == "T": # solving a vertical dominoe
			if canPutPatternVertically(rules,i,j,"xx"): # tries putting a x/x dominoe (vertical)
				addOrRemoveMagnet(rules,i,j,(1,0),"xx")
				if rulesMet(rules,i,j):solveMagnets(rules,i,j+1)
				addOrRemoveMagnet(rules,i,j,(1,0),"TB")
			if canPutPatternVertically(rules,i,j,"+-"): # tries putting a +/- dominoe (vertical)
				addOrRemoveMagnet(rules,i,j,(1,0),"+-",-1,(0,0,1,0))
				if rulesMet(rules,i,j):solveMagnets(rules,i,j+1)
				addOrRemoveMagnet(rules,i,j,(1,0),"TB",1,(0,0,1,0))
			if canPutPatternVertically(rules,i,j,"-+"): # tries putting a -/+ dominoe (vertical)
				addOrRemoveMagnet(rules,i,j,(1,0),"-+",-1,(0,1,0,0))
				if rulesMet(rules,i,j):solveMagnets(rules,i,j+1)
				addOrRemoveMagnet(rules,i,j,(1,0),"TB",1,(0,1,0,0))
		else:
			if rulesMet(rules,i,j): solveMagnets(rules,i,j+1)

def printBoard(arr): # printing board state
	print("\nTop: {}\nLeft: {}\nRight: {}\nBottom: {}".format(top, left, right, bottom))
	for line in arr:
		print(" ".join(line))
  
def parseMagnet_Board():
	boards=[]
	with open("magnetBoards.txt", "r") as file:
		for line in file:
			dimensions, data = line.split(":")
			rows, cols = map(int, dimensions.split("x"))
			parts = data.split(",")
   
			top = [int(c) if c != '.' else -1 for c in parts[0]]
			left = [int(c) if c != '.' else -1 for c in parts[1]]
			bottom = [int(c) if c != '.' else -1 for c in parts[2]]
			right = [int(c) if c != '.' else -1 for c in parts[3]]
			
			boardData = parts[4]
			rules = [[boardData[i * cols + j] for j in range(cols)] for i in range(rows)]
			boards.append((rules,top,left,right,bottom))
	return boards

def main(): # function to run
	global rules, top, left, right, bottom, solved
	boards = parseMagnet_Board()
	boardNum=None
 
	while (boardNum!="-1"):
		boardNum=input("-1: to exit\n0: 5x6 given board\n1-4: Not yet added\n5-8: 4x4 boards\n9-12: 8x8 boards\n13-16: 16x16 boards\nFYI, first 2 of a sequence are 'easy' and last 2 are 'tricky', but all 4x4 are easy")
		(rules, top, left, right, bottom) = boards[int(boardNum)]
		printBoard(rules)
		startTime = time.time()
		solveMagnets(rules,0,0)
		if solved:
			printBoard(completedBoard)
			solved=False
		else:
			print("wasnt solved")
		endTime = time.time()
		print("Time taken:",endTime-startTime, "seconds")
main()
