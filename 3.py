#!/usr/bin/python

current_point = []
current_vector = []

def next_move(posr, posc, board):
	
	global current_point
	global current_vector
	
	m = n * n
	vectors = []
	distance = []
	
	#Test if current point is dirty
	#Get next instruction
	if current_point != [] :
		if current_point != "d" :
			
	#If current_point is set AND is dirty
	
	
	#If current point isn't set OR isn't dirty
	#Get vectors for every point
	for i in xrange(0,m):
        x = i % n
        y = i / n
        m_x = posr
        m_y = posc
        if grid[y][x] == "d" :
            d_x = x
            d_y = y
			vector_x = m_x - p_x
			vector_y = m_y - p_y
			vectors.append(vector_x, vector_y)
    
	#Calculate closest point
	for v in vectors :
		distance.append(abs(v[0]) + abs(v[1]))
	d.sort()
	
	#Output the correct instruction
    if current_vector[0] > 0 :
        print "LEFT"
		current_vector[0] -= 1
		return
    if current_vector[0] < 0 :
        print "RIGHT"
		current_vector[0] += 1
		return
    if current_vector[1] > 0 :
        print "UP"
		current_vector[1] -= 1
		return
    if current_vector[1] < 0 :
        print "DOWN"
		current_vector[1] += 1
		return
	if current_vector[0] == 0 and current_vector[1] == 0 :
		print "CLEAN"
		current_point = []
		current_vector = []
		return
	return
	
if __name__ == "__main__":
    pos = [int(i) for i in raw_input().strip().split()]
    board = [[j for j in raw_input().strip()] for i in range(5)]
    next_move(pos[0], pos[1], board)
