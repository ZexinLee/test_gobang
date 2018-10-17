import model4
import numpy as np

chessboard = np.zeros((15, 15), dtype=np.int)
ai = model4.AI(15, -1, 5)
print(ai.candidate_list)
# chessboard[8][9] = -1
# chessboard[6][5] = 1

while True:
	step = ai.go(chessboard)
	print(ai.candidate_list)
	chessboard[ai.candidate_list[0][0]][ai.candidate_list[0][1]] = -1
	print(chessboard)
	str = input().split(' ')
	x = int(str[0])
	y = int(str[1])
	chessboard[x][y] = 1
	# print(chessboard)