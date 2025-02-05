import copy 
solved = False
completedBoard = None

top = [ 1, -1, -1, 2, 1, -1 ]
bottom = [ 2, -1, -1, 2, -1, 3 ]
left = [ 2, 3, -1, -1, -1 ]
right = [ -1, -1, -1, 1, -1 ]
rules = [["L","R","L","R","T","T" ],
		[ "L","R","L","R","B","B" ],
		[ "T","T","T","T","L","R" ],
		[ "B","B","B","B","T","T" ],
		[ "L","R","L","R","B","B" ]]

top = [ -1,-1,-1,-1,0,-1]
bottom = [ 1,-1,-1,2,1,-1 ]
left = [ 3,-1,1,-1,1,3 ]
right = [ 2,-1,-1,-1,-1,3 ]
rules =[['L', 'R', 'L', 'R', 'T', 'T'],
		['L', 'R', 'L', 'R', 'B', 'B'],
		['T', 'L', 'R', 'L', 'R', 'T'],
		['B', 'T', 'L', 'R', 'T', 'B'],
		['T', 'B', 'L', 'R', 'B', 'T'],
		['B', 'L', 'R', 'L', 'R', 'B']]

top = [4, -1, -1, 2, -1, -1, -1, -1]
left = [-1, 1, -1, -1, 4, -1, -1, 4]
right = [2, 2, 2, 4, 4, 3, 3, 4]
bottom = [3, 3, -1, -1, 2, -1, 2, -1]
rules =[['T', 'L', 'R', 'T', 'L', 'R', 'L', 'R'],
		['B', 'L', 'R', 'B', 'T', 'T', 'T', 'T'],
		['L', 'R', 'T', 'T', 'B', 'B', 'B', 'B'],
		['T', 'T', 'B', 'B', 'L', 'R', 'L', 'R'],
		['B', 'B', 'T', 'L', 'R', 'T', 'T', 'T'],
		['T', 'T', 'B', 'L', 'R', 'B', 'B', 'B'],
		['B', 'B', 'T', 'L', 'R', 'L', 'R', 'T'],
		['L', 'R', 'B', 'L', 'R', 'L', 'R', 'B']]

top = [-1, -1, 2, 3, -1, 3, -1, -1]
left = [2, 4, 4, 4, -1, -1, 4, 1]
right = [-1, 4, 4, 4, 3, 3, -1, -1]
bottom = [-1, -1, 2, 4, -1, 4, 4, 4]
rules =[['L', 'R', 'L', 'R', 'L', 'R', 'T', 'T'],
		['L', 'R', 'L', 'R', 'T', 'T', 'B', 'B'],
		['T', 'L', 'R', 'T', 'B', 'B', 'L', 'R'],
		['B', 'T', 'T', 'B', 'L', 'R', 'T', 'T'],
		['T', 'B', 'B', 'T', 'T', 'T', 'B', 'B'],
		['B', 'T', 'T', 'B', 'B', 'B', 'T', 'T'],
		['T', 'B', 'B', 'T', 'T', 'T', 'B', 'B'],
		['B', 'L', 'R', 'B', 'B', 'B', 'L', 'R']]

top = [8, 8, 8, -1, -1, 8, -1, 7, 4, -1, 6, -1, 7, 8, -1, -1]
left = [8, -1, 7, -1, -1, -1, -1, 8, -1, -1, -1, 8, 7, 8, 7, 8]
right = [-1, 8, 6, -1, 8, 7, 8, 7, 7, 7, 5, 7, -1, 7, 8, 7]
bottom = [8, 8, 8, 8, 7, 8, 8, -1, 5, -1, -1, -1, 8, 7, -1, 6]
rules =[['L', 'R', 'L', 'R', 'L', 'R', 'L', 'R', 'L', 'R', 'L', 'R', 'L', 'R', 'L', 'R'],
		['T', 'T', 'L', 'R', 'L', 'R', 'L', 'R', 'T', 'L', 'R', 'L', 'R', 'L', 'R', 'T'],
		['B', 'B', 'T', 'L', 'R', 'L', 'R', 'T', 'B', 'L', 'R', 'T', 'T', 'L', 'R', 'B'],
		['L', 'R', 'B', 'L', 'R', 'L', 'R', 'B', 'L', 'R', 'T', 'B', 'B', 'T', 'L', 'R'],
		['T', 'T', 'L', 'R', 'T', 'L', 'R', 'L', 'R', 'T', 'B', 'L', 'R', 'B', 'L', 'R'],
		['B', 'B', 'L', 'R', 'B', 'T', 'L', 'R', 'T', 'B', 'T', 'T', 'T', 'L', 'R', 'T'],
		['T', 'T', 'L', 'R', 'T', 'B', 'L', 'R', 'B', 'T', 'B', 'B', 'B', 'L', 'R', 'B'],
		['B', 'B', 'L', 'R', 'B', 'L', 'R', 'L', 'R', 'B', 'L', 'R', 'L', 'R', 'T', 'T'],
		['T', 'T', 'T', 'T', 'T', 'L', 'R', 'T', 'L', 'R', 'L', 'R', 'L', 'R', 'B', 'B'],
		['B', 'B', 'B', 'B', 'B', 'T', 'T', 'B', 'L', 'R', 'T', 'T', 'T', 'T', 'T', 'T'],
		['T', 'T', 'T', 'L', 'R', 'B', 'B', 'T', 'L', 'R', 'B', 'B', 'B', 'B', 'B', 'B'],
		['B', 'B', 'B', 'L', 'R', 'L', 'R', 'B', 'L', 'R', 'L', 'R', 'T', 'T', 'L', 'R'],
		['T', 'T', 'L', 'R', 'L', 'R', 'L', 'R', 'T', 'T', 'L', 'R', 'B', 'B', 'L', 'R'],
		['B', 'B', 'L', 'R', 'L', 'R', 'L', 'R', 'B', 'B', 'L', 'R', 'L', 'R', 'L', 'R'],
		['L', 'R', 'T', 'L', 'R', 'L', 'R', 'T', 'T', 'T', 'T', 'L', 'R', 'T', 'L', 'R'],
		['L', 'R', 'B', 'L', 'R', 'L', 'R', 'B', 'B', 'B', 'B', 'L', 'R', 'B', 'L', 'R']]

def canPutPatternHorizontally(rules,i,j,pat):
	if pat == "xx":
		if (len(rules)-1-i < top[j]+bottom[j]) or (len(rules)-1-i < top[j+1]+bottom[j+1]): return False
		if len(rules[0])-2 == j and (left[i]>0 or right[i]>0): return False
		if len(rules)-1 == i and (top[j]>0 or top[j+1]>0 or bottom[j]>0 or bottom[j+1]>0): return False
		return True

	if (left[i]==0 or right[i]==0): return False
	if (len(rules[0])-2==j) and (left[i]>1 or right[i]>1): return False	
	if j-1>=0 and rules[i][j-1] == pat[0]: # dominoe to the left is not same
		return False
	elif i-1>=0 and rules[i-1][j] == pat[0]: # dominoe above is not same
		return False
	elif i-1>=0 and rules[i-1][j+1] == pat[1]: # dominoe above and right is not same as pat end
		return False
	elif j+2 < len(rules[0]) and rules[i][j+2] == pat[1]: # dominoe to right of right is not same as pat end
		return False
 
	if pat == "+-":
		if (top[j]==0 or bottom[j+1]==0): return False
		if (len(rules)-1==i) and (top[j]>1 or top[j+1]>0 or bottom[j+1]>1 or bottom[j]>0): return False
	
	elif pat == "-+":
		if (bottom[j]==0 or top[j+1]==0): return False
		if (len(rules)-1==i) and (bottom[j]>1 or bottom[j+1]>0 or top[j+1]>1 or top[j]>0): return False
	
	return True
	
def rulesMet(rules,i,j):
	if (len(rules[0])-1==j) and (left[i]>0 or right[i]>0): return False
	if (len(rules)-1==i) and (top[j]>0 or bottom[j]>0): return False
	return True

def canPutPatternVertically(rules,i,j,pat): # only ever called on if (i,j) is "T"
	if pat == "xx":
		if len(rules)-2-i < top[j]+bottom[j]: return False
		if len(rules)-2 == i and (top[j]>0 or bottom[j]>0): return False
		if len(rules[0])-1 == j and (left[i]>0 or right[i]>0): return False
		return True

	if (top[j]==0 or bottom[j]==0): return False
	if (len(rules)-2==i) and (top[j]>1 or bottom[j]>1): return False
	
	if j-1>=0 and rules[i][j-1] == pat[0]: # dominoe to the left is not same
		return False
	elif i-1>=0 and rules[i-1][j] == pat[0]: # dominoe above is not same
		return False
	elif j+1 < len(rules[0]) and rules[i][j+1] == pat[0]: # dominoe to the right is not the same
		return False
 
	if pat == "+-":
		if (left[i]==0 or right[i+1]==0): return False
		if (len(rules[0])-1==j) and (left[i]>1): return False
	
	elif pat == "-+":
		if (right[i]==0 or left[i+1]==0): return False
		if (len(rules[0])-1==j) and (right[i]>1): return False
	
	return True

def addOrRemoveMagnet(rules,i,j,oppVec,pat,amount=None,reqChangeVec=None):
	rules[i][j] = pat[0]
	rules[i+oppVec[0]][j+oppVec[1]] = pat[1]
	if amount:
		top[j+reqChangeVec[0]]+=amount
		left[i+reqChangeVec[1]]+=amount
		right[i+reqChangeVec[2]]+=amount
		bottom[j+reqChangeVec[3]]+=amount

def solveMagnets(rules,i,j):
	global solved, completedBoard
	if solved:
		return
	
	if i == len(rules) and j == 0: # complete
		solved = True
		completedBoard=copy.deepcopy(rules)
	
	elif j >= len(rules[0]):
		solveMagnets(rules,i+1,0)

	else: # normal solving cases
		if rules[i][j] == "L": # solving a horizontal dominoe
			if canPutPatternHorizontally(rules,i,j,"+-"): # tries putting a +- dominoe (horizontal)
				addOrRemoveMagnet(rules,i,j,(0,1),"+-",-1,(0,0,0,1))
				solveMagnets(rules,i,j+2)
				addOrRemoveMagnet(rules,i,j,(0,1),"LR",1,(0,0,0,1))
			
			if canPutPatternHorizontally(rules,i,j,"-+"): # tries putting a -+ dominoe (horizontal)
				addOrRemoveMagnet(rules,i,j,(0,1),"-+",-1,(1,0,0,0))
				solveMagnets(rules,i,j+2)
				addOrRemoveMagnet(rules,i,j,(0,1),"LR",1,(1,0,0,0))
			
			if canPutPatternHorizontally(rules,i,j,"xx"): # tries putting a xx dominoe(horizontal)
				addOrRemoveMagnet(rules,i,j,(0,1),"xx")
				solveMagnets(rules,i,j+2)
				addOrRemoveMagnet(rules,i,j,(0,1),"LR")

		elif rules[i][j] == "T": # solving a vertical dominoe
			if canPutPatternVertically(rules,i,j,"+-"): # tries putting a +/- dominoe (vertical)
				addOrRemoveMagnet(rules,i,j,(1,0),"+-",-1,(0,0,1,0))
				if rulesMet(rules,i,j):solveMagnets(rules,i,j+1)
				addOrRemoveMagnet(rules,i,j,(1,0),"TB",1,(0,0,1,0))
				
			if canPutPatternVertically(rules,i,j,"-+"): # tries putting a -/+ dominoe (vertical)
				addOrRemoveMagnet(rules,i,j,(1,0),"-+",-1,(0,1,0,0))
				if rulesMet(rules,i,j):solveMagnets(rules,i,j+1)
				addOrRemoveMagnet(rules,i,j,(1,0),"TB",1,(0,1,0,0))
			if canPutPatternVertically(rules,i,j,"xx"): # tries putting a x/x dominoe (vertical)
				addOrRemoveMagnet(rules,i,j,(1,0),"xx")
				if rulesMet(rules,i,j):solveMagnets(rules,i,j+1)
				addOrRemoveMagnet(rules,i,j,(1,0),"TB")
				
		else:
			if rulesMet(rules,i,j): solveMagnets(rules,i,j+1)

def printBoard(arr):
	print()
	print("Top: {}\nLeft: {}\nRight: {}\nBottom: {}".format(top, left, right, bottom))
	for line in arr:
		print(" ".join(line))
  
def main():
	printBoard(rules)
	solveMagnets(rules,0,0)
	print(completedBoard)
	if solved:
		printBoard(completedBoard)
	else:
		print("wasnt solved")
main()
