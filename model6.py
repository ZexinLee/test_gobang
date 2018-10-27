# Author:LZX
import numpy as np
import random
import time

COLOR_BLACK=-1
COLOR_WHITE=1
COLOR_NONE=0

FIVE=10000000
FOUR=100000
THREE=1000
TWO=100
ONE=10
BLOCK_FOUR=10000
BLOCK_THREE=100
BLOCK_TWO=10
BLOCK_ONE=1

random.seed(0)
#don't change the class name
class AI(object):
    #chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        #You are white or black
        self.color = color
        #the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need add your decision into your candidate_list. System will get the end of your candidate_list as your decision .
        self.candidate_list = []
        self.board = []

    # If your are the first, this function will be used.
    def first_black(self):
        # first black to put at sun
        assert self.color == COLOR_BLACK
        self.candidate_list.clear()
        self.candidate_list.append((self.chessboard_size//2,self.chessboard_size//2))

    def second_black(self)->bool:
        # second black to confirm win formula
        assert self.color == COLOR_BLACK
        self.candidate_list.clear()
        sun = (self.chessboard_size//2,self.chessboard_size//2)
        # 花月(Hua Yue)
        if(self.board[sun[0] - 1][sun[1]] == COLOR_WHITE):
            self.candidate_list.append((sun[0] - 1,sun[1] - 1))
            print("花月1")
        if(self.board[sun[0]][sun[1] - 1] == COLOR_WHITE):
            self.candidate_list.append((sun[0] - 1,sun[1] - 1))
            print("花月2")
        if(self.board[sun[0]][sun[1] + 1] == COLOR_WHITE):
            self.candidate_list.append((sun[0] + 1,sun[1] + 1))
            print("花月3")
        if(self.board[sun[0] + 1][sun[1]] == COLOR_WHITE):
            self.candidate_list.append((sun[0] + 1,sun[1] + 1))
            print("花月4")
        # 浦月(Pu Yue)
        if(self.board[sun[0] - 1][sun[1] - 1] == COLOR_WHITE):
            self.candidate_list.append((sun[0] - 1,sun[1] + 1))
            print("浦月1")
        if(self.board[sun[0] - 1][sun[1] + 1] == COLOR_WHITE):
            self.candidate_list.append((sun[0] - 1,sun[1] - 1))
            print("浦月2")
        if(self.board[sun[0] + 1][sun[1] - 1] == COLOR_WHITE):
            self.candidate_list.append((sun[0] + 1,sun[1] + 1))
            print("浦月3")
        if(self.board[sun[0] + 1][sun[1] + 1] == COLOR_WHITE):
            self.candidate_list.append((sun[0] - 1,sun[1] + 1))
            print("浦月4")
        if(len(self.candidate_list)==0):
            print("对面太菜了，随便下")
            test_list = [(self.chessboard_size//2 - 1,self.chessboard_size//2 - 1),
                (self.chessboard_size//2 - 1,self.chessboard_size//2 + 1),
                (self.chessboard_size//2 + 1,self.chessboard_size//2 - 1),
                (self.chessboard_size//2 + 1,self.chessboard_size//2 + 1),
            ]
            white_point = np.where(self.board == COLOR_WHITE)
            white_point = list(zip(white_point[0], white_point[1]))
            for pos in test_list:
                delta_x1 = self.chessboard_size//2 - pos[0]
                delta_y1 = self.chessboard_size//2 - pos[1]
                delta_x2 = white_point[0][0] - self.chessboard_size//2
                delta_y2 = white_point[0][1] - self.chessboard_size//2
                if(delta_x1/delta_x2 != delta_y1/delta_y2):
                    self.candidate_list.append(pos)
                    break
            # self.candidate_list.append((sun[0] + 1,sun[1] + 1))


    def nearby_chess(self, x, y, chessboard):
        # empty and in 2 steps
        flag = False
        if(chessboard[x][y] == COLOR_NONE):
            for i in range(x - 2 if x - 2 >= 0 else 0,x + 3 if x + 3 <= self.chessboard_size else self.chessboard_size):
                for j in range(y - 2 if y - 2 >= 0 else 0,y + 3 if y + 3 <= self.chessboard_size else self.chessboard_size):
                    if(chessboard[i][j] != COLOR_NONE):
                        flag = True
        return flag

    def evaluate_all_chessboard(self, chessboard):
        # print(self.board)
        max_points = np.zeros((self.chessboard_size, self.chessboard_size))
        min_points = np.zeros((self.chessboard_size, self.chessboard_size))
        for row in range(self.chessboard_size):
            for col in range(self.chessboard_size):
                if(chessboard[row][col] == COLOR_NONE):
                    max_points[row][col] = self.evaluate_point(chessboard, row, col, self.color)
                    min_points[row][col] = self.evaluate_point(chessboard, row, col, -self.color)
                # elif(chessboard[row][col] == self.color):
                    # max_points[row][col] = self.evaluate_point(chessboard, row, col, self.color)
                    # min_points[row][col] = 0
                else:
                    max_points[row][col] = -1
                    min_points[row][col] = -1
                    # min_points[row][col] = self.evaluate_point(chessboard, row, col, -self.color)
        max_points = (max_points.flatten()).tolist()
        min_points = (min_points.flatten()).tolist()
        #max_points = list(map(lambda x:(10 * x) if (x > 1.5 * THREE and x < BLOCK_FOUR) else (x), max_points))
        #min_points = list(map(lambda x:(10 * x) if (x > 2 * THREE and x < BLOCK_FOUR) else (x), min_points))
        return max_points,min_points

    def evaluate_point(self, chessboard, x, y, color, direction=0):
        result = 0
        length = self.chessboard_size
        
        if(direction == 0 or direction == 1):
            # reset
            count, block, empty, secondCount = 1, 0, -1, 0
            i = y
            while(True):
                i += 1
                if(i >= length):
                    block += 1
                    break
                t = chessboard[x][i]
                if(t == COLOR_NONE):
                    if(empty == -1 and i < length-1 and chessboard[x][i+1] == color):
                        empty = count
                        continue
                    else:
                        break
                if(t == color):
                    count += 1
                    continue
                else:
                    block += 1
                    break
            i = y
            while(True):
                i -= 1
                if(i < 0):
                    block += 1
                    break
                t = chessboard[x][i]
                if(t == COLOR_NONE):
                    if(empty == -1 and i > 0 and chessboard[x][i-1] == color):
                        empty = 0
                        continue
                    else:
                        break
                if(t == color):
                    secondCount += 1
                    if(empty != -1):
                        empty += 1
                    continue
                else:
                    block += 1
                    break
            count += secondCount
            result += self.count_find_score(count, block, empty)
        
        if(direction == 0 or direction == 2):
            count, block, empty, secondCount = 1, 0, -1, 0
            i = x
            while(True):
                i += 1
                if(i >= length):
                    block += 1
                    break
                t = chessboard[i][y]
                if(t == COLOR_NONE):
                    if(empty == -1 and i < length - 1 and chessboard[i+1][y] == color):
                        empty = count
                        continue
                    else:
                        break
                if(t == color):
                    count += 1
                    continue
                else:
                    block += 1
                    break
            i = x
            while(True):
                i -= 1
                if(i < 0):
                    block += 1
                    break
                t = chessboard[i][y]
                if(t == COLOR_NONE):
                    if(empty == -1 and i > 0 and chessboard[i-1][y] == color):
                        empty = 0
                        continue
                    else:
                        break
                if(t == color):
                    secondCount += 1
                    if(empty != -1):
                        empty += 1
                    continue
                else:
                    block += 1
                    break
            count += secondCount
            result += self.count_find_score(count, block, empty)
        
        if(direction == 0 or direction == 3):
            count, block, empty, secondCount = 1, 0, -1, 0
            i = 0
            while(True):
                i += 1
                tx = x + i
                ty = y + i
                if(tx >= length or ty >= length):
                    block += 1
                    break
                t = chessboard[tx][ty]
                if(t == COLOR_NONE):
                    if(empty == -1 and (tx < length - 1 and ty < length - 1) and chessboard[tx+1][ty+1]):
                        empty = count
                        continue
                    else:
                        break
                if(t == color):
                    count += 1
                    continue
                else:
                    block += 1
                    break
            i = 0
            while(True):
                i += 1
                tx = x - i
                ty = y - i
                if(tx < 0 or ty < 0):
                    block += 1
                    break
                t = chessboard[tx][ty]
                if(t == COLOR_NONE):
                    if(empty == -1 and (tx > 0  and ty > 0) and chessboard[tx-1][ty-1] == color):
                        empty = 0
                        continue
                    else:
                        break
                if(t == color):
                    secondCount += 1
                    if(empty != -1):
                        empty += 1
                    continue
                else:
                    block += 1
                    break
            count += secondCount
            result += self.count_find_score(count, block, empty)

        if(direction == 0 or direction == 4):
            count, block, empty, secondCount = 1, 0, -1, 0
            i = 0
            while(True):
                i += 1
                tx = x + i 
                ty = y - i
                if(tx < 0 or ty < 0 or tx >= length or ty >= length):
                    block += 1
                    break
                t = chessboard[tx][ty]
                if(t == COLOR_NONE):
                    if(empty == -1 and (tx < length - 1 and ty > 0) and chessboard[tx+1][ty-1] == color):
                        empty = count
                        continue
                    else:
                        break
                if(t == color):
                    count += 1
                    continue
                else:
                    block += 1
                    break
            i = 0
            while(True):
                i += 1
                tx = x - i
                ty = y + i
                if(tx < 0 or ty < 0 or tx >= length or ty >= length):
                    block += 1
                    break
                t = chessboard[tx][ty]
                if(t == COLOR_NONE):
                    if(empty == -1 and (tx > 0 and ty < length - 1) and chessboard[tx - 1][ty + 1] == color):
                        empty = 0
                        continue
                    else:
                        break
                if(t == color):
                    secondCount += 1
                    if(empty != -1):
                        empty += 1
                    continue
                else:
                    block += 1
                    break
            count += secondCount
            result += self.count_find_score(count, block, empty)

        #print("pos:",x,y)
        # print("pos:",x,y)
        # print(result)
        return result

    def count_find_score(self, count, block, empty=-1):
        # print("count:{a},block={b},empty={c}".format(a=count,b=block,c=empty), end='')
        #if(empty == None):
        #    empty = 0
        #print(count, block, empty)
        if(empty < 0):
            if(count >= 5):
                return FIVE
            if(block == 0):
                if(count == 1):
                    return ONE
                if(count == 2):
                    return TWO
                if(count == 3):
                    return THREE
                if(count == 4):
                    return FOUR
            if(block == 1):
                if(count == 1):
                    return BLOCK_ONE
                if(count == 2):
                    return BLOCK_TWO
                if(count == 3):
                    return BLOCK_THREE
                if(count == 4):
                    return BLOCK_FOUR
        elif(empty == 0 or empty == 1 or empty == count - 1):
            if(count >= 6):
                return FIVE
            if(block == 0):
                if(count == 2):
                    return TWO/2
                if(count == 3):
                    return THREE
                if(count == 4):
                    return BLOCK_FOUR
                if(count == 5):
                    return FOUR
            if(block == 1):
                if(count == 2):
                    return BLOCK_TWO
                if(count == 3):
                    return BLOCK_THREE
                if(count == 4):
                    return BLOCK_FOUR
                if(count == 5):
                    return BLOCK_FOUR
        elif(empty == 2 or empty == count - 2):
            if(count >= 7):
                return FIVE
            if(block == 0):
                if(count == 3):
                    return THREE
                if(count == 5 or count == 4):
                    return BLOCK_FOUR
                if(count == 6):
                    return FOUR
            if(block == 1):
                if(count == 3):
                    return BLOCK_THREE
                if(count == 4):
                    return BLOCK_FOUR
                if(count == 5):
                    return BLOCK_FOUR
                if(count == 6):
                    return FOUR
            if(block == 2):
                if(count == 4 or count == 5 or count == 6):
                    return BLOCK_FOUR
        elif(empty == 3 or empty == count - 3):
            if(count >= 8):
                return FIVE
            if(block == 0):
                if(count == 4 or count == 5):
                    return THREE
                if(count == 6):
                    return BLOCK_FOUR
                if(count == 7):
                    return FOUR
            if(block == 1):
                if(count == 4 or count == 5 or count == 6):
                    return BLOCK_FOUR
                if(count == 7):
                    return FOUR
            if(block == 2):
                if(count == 4 or count == 5 or count == 6 or count == 7):
                    return BLOCK_FOUR
        elif(empty == 4 or empty == count - 4):
            if(count >= 9):
                return FIVE
            if(block == 0):
                if(count == 5 or count == 6 or count == 7 or count == 8):
                    return FOUR
            if(block == 1):
                if(count == 4 or count == 5 or count == 6 or count == 7):
                    return BLOCK_FOUR
                if(count == 8):
                    return FOUR
            if(block == 2):
                if(count == 5 or count == 6 or count == 7 or count == 8):
                    return BLOCK_FOUR
        elif(empty == 5 or empty == count - 5):
            return FIVE

        return 0
    # The input is current chessboard.

    def make_decision(self):
        max_value, min_value = self.evaluate_all_chessboard(self.board)
        # print(max_value)
        # print(min_value)
        if(max(max_value) >= FIVE):
            #win directly
            new_pos = (max_value.index(max(max_value))//self.chessboard_size, max_value.index(max(max_value))%self.chessboard_size)
        elif(max(min_value) >= FIVE):
            #defend opposie five
            new_pos = (min_value.index(max(min_value))//self.chessboard_size, min_value.index(max(min_value))%self.chessboard_size)
        elif(max(max_value) >= FOUR):
            #attack alive four
            new_pos = (max_value.index(max(max_value))//self.chessboard_size, max_value.index(max(max_value))%self.chessboard_size)
        elif(max(min_value) >= FOUR):
            #defend alive four
            #begin to think attack points
            defend_list = []
            for i in range(len(min_value)):
                if(min_value[i] >= FOUR):
                    defend_list.append((i//self.chessboard_size, i%self.chessboard_size))
            temp = float("inf")
            new_pos = defend_list[0]
            for pos in defend_list:
                self.board[pos[0]][pos[1]] = self.color
                tmax, tmin = self.evaluate_all_chessboard(self.board)
                if(max(tmin) <= temp):
                    temp = max(tmin)
                    new_pos = pos
                self.board[pos[0]][pos[1]] = COLOR_NONE
            # new_pos = (min_value.index(max(min_value))//self.chessboard_size, min_value.index(max(min_value))%self.chessboard_size)
        elif(max(max_value) >= BLOCK_FOUR + THREE):
            #attack by block four+more than an alive three
            new_pos = (max_value.index(max(max_value))//self.chessboard_size, max_value.index(max(max_value))%self.chessboard_size)
        elif(max(max_value) >= 2 * THREE and max(max_value) < BLOCK_FOUR):
            #attack two three
            new_pos = (max_value.index(max(max_value))//self.chessboard_size, max_value.index(max(max_value))%self.chessboard_size)
        elif(max(max_value) < BLOCK_FOUR + THREE and max(max_value) >= BLOCK_FOUR and max(min_value) >= 2 * THREE and max(min_value) < BLOCK_FOUR):
            #defend when only can block four but opposite has two three(not block four)
            #attack can not hit but in dangerous
            defend_list = []
            for i in range(len(min_value)):
                if(min_value[i] >= 2 * THREE and min_value[i] < BLOCK_FOUR):
                    defend_list.append((i//self.chessboard_size, i%self.chessboard_size))
            for i in range(len(max_value)):
                if(max_value[i] < BLOCK_FOUR + THREE and max_value[i] >= BLOCK_FOUR):
                    defend_list.append((i//self.chessboard_size, i%self.chessboard_size))
            temp = float("inf")
            new_pos = defend_list[0]
            for pos in defend_list:
                self.board[pos[0]][pos[1]] = self.color
                tmax, tmin = self.evaluate_all_chessboard(self.board)
                if(max(tmin) <= temp):
                    if(not(max(tmin) >= FOUR or (max(tmin) >= 2 * THREE and max(tmin) < BLOCK_FOUR) or (max(tmin) >= BLOCK_FOUR + THREE))):
                        temp = max(tmin)
                        new_pos = pos
                self.board[pos[0]][pos[1]] = COLOR_NONE
            #new_pos = (min_value.index(max(min_value))//self.chessboard_size, min_value.index(max(min_value))%self.chessboard_size)
        elif(max(max_value) < BLOCK_FOUR and max(min_value) >= 2 * THREE):
            #defend two three
            new_pos = (min_value.index(max(min_value))//self.chessboard_size, min_value.index(max(min_value))%self.chessboard_size)
        #elif(max(min_value) >= THREE):
         #   new_pos = (min_value.index(max(min_value))//self.chessboard_size, min_value.index(max(min_value))%self.chessboard_size)
        #elif(max(max_value) >= THREE):
         #   new_pos = (max_value.index(max(max_value))//self.chessboard_size, max_value.index(max(max_value))%self.chessboard_size)
        #此处还要写对连二的判断
        elif(self.color == COLOR_WHITE):
            if(max(max_value) >= 1.15 * max(min_value)):
                #attack when holding advantage
                new_pos = (max_value.index(max(max_value))//self.chessboard_size, max_value.index(max(max_value))%self.chessboard_size)
            else:
                #defend
                new_pos = (min_value.index(max(min_value))//self.chessboard_size, min_value.index(max(min_value))%self.chessboard_size)
        else:
            if(max(max_value) >= 0.8 * max(min_value)):
                #attack when holding advantage
                new_pos = (max_value.index(max(max_value))//self.chessboard_size, max_value.index(max(max_value))%self.chessboard_size)
            else:
                #defend
                new_pos = (min_value.index(max(min_value))//self.chessboard_size, min_value.index(max(min_value))%self.chessboard_size)
        return new_pos

    def go(self, chessboard):
        # Clear candidate_list
        time1 = time.time()
        self.candidate_list.clear()
        #==================================================================
        #To write your algorithm here
        #Here is the simplest sample:Random decision

        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        self.board = chessboard

        '''
            Black_first win directly
            花月(Hua Yue)
            浦月(Pu Yue)
        '''
        if(len(idx) == self.chessboard_size ** 2):
            self.first_black()
            return
        if(len(idx) == self.chessboard_size ** 2 - 2):
            self.second_black()
            return

       
        new_pos = self.make_decision()
        print("new pos is :",new_pos)
        #==============Find new pos========================================
        # Make sure that the position of your decision in chess board is empty.
        #If not, return error.
        assert chessboard[new_pos[0],new_pos[1]]==0
        #Add your decision into candidate_list, Records the chess board
        self.candidate_list.append(new_pos)
        time2 = time.time()
        # print(time2 - time1)

