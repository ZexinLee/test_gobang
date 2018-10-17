# Author:LZX
import numpy as np
import random
import time

COLOR_BLACK=-1
COLOR_WHITE=1
COLOR_NONE=0
SEARCH_DEPTH=1

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
    def first_chess(self):
        assert self.color == COLOR_BLACK
        self.candidate_list.clear()
        #==================================================================
        #Here you can put your first piece
        #for example, you can put your piece on sun（天元）
        self.candidate_list.append((self.chessboard_size//2,self.chessboard_size//2))
        
    def nearby_chess(self, x, y, chessboard):
        # empty and in 2 steps
        flag = False
        if(chessboard[x][y] == COLOR_NONE):
            for i in range(x - 2 if x - 2 >= 0 else 0,x + 3 if x + 3 <= self.chessboard_size else self.chessboard_size):
                for j in range(y - 2 if y - 2 >= 0 else 0,y + 3 if y + 3 <= self.chessboard_size else self.chessboard_size):
                    if(chessboard[i][j] != COLOR_NONE):
                        flag = True
        return flag

    def evaluate_all_chessboard(self, chessboard, color):
        max_points = np.zeros((self.chessboard_size, self.chessboard_size))
        for row in range(self.chessboard_size):
            for col in range(self.chessboard_size):
                if(chessboard[row][col] == COLOR_NONE):
                    max_points[row][col] = self.evaluate_point(chessboard, row, col, self.color)
                    # min_points[row][col] = self.evaluate_point(chessboard, row, col, -self.color)
                elif(chessboard[row][col] == self.color):
                    max_points[row][col] = self.evaluate_point(chessboard, row, col, self.color)
                    # min_points[row][col] = 0
                else:
                    max_points[row][col] = 0
                    # min_points[row][col] = self.evaluate_point(chessboard, row, col, -self.color)
                    # min_points[row][col] = self.evaluate_point(chessboard, row, col, -self.color)
        max_points = (max_points.flatten()).tolist()
        # min_points = (min_points.flatten()).tolist()
        # return max_points,min_points
        return max_points

    #单点评估
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
                        empty += count
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
        # print(result)
        return result

    #用于单点评估调用
    def count_find_score(self, count, block, empty=-1):
        # print("count:{a},block={b},empty={c}".format(a=count,b=block,c=empty))
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

    #计算全局分数
    def evaluate_board(self, color):
        max_points = self.evaluate_all_chessboard(chessboard, color=color)
        if(len(max_points) > 0):
            if(color == self.color):
                value = sum(max_points)
        else:
            value = 0

        return value

    def minmax(self, deep, alpha=-float("inf"), beta=float("inf"), color, step=None, steps=None, spread=None):       
        empty_place = np.where(self.board == COLOR_NONE)
        empty_place = list(zip(empty_place[0], empty_place[1]))
        
        for i in range(len(empty_place)):
            self.board[i[0]][i[1]] = color
            # steps = [i]
            # v = r(deep-1, beta, alpha, -color, 1, steps.slice(0), 0)
            v = r(deep-1, beta, alpha, -color)
            #更新alpha值
            alpha = alpha if (alpha >= v.score)
            self.board[i[0]][i[1]] = COLOR_NONE
            # p.v=v
        return alpha

    def r(self, deep, alpha, beta, color, step=None, steps=None, spread=None):
        value = evaluate_board(color)

        leaf = [value, step, steps]

        count += 1
        if(deep <= 0 or value >= FIVE or value <= -FIVE):
            return leaf

        best = [float("-inf"), step, steps]

        #启发式函数
        # points = board.gen(color, board.count > 10 ? step > 1 : step > 3, step > 1)
        points = np.where(self.board == COLOR_NONE)
        points = list(zip(points[0], points[1]))

        # if(!points.length):
        #     return leaf

        for i in range(len(points)):
            p = points[i]
            self.board[p[0]][p[1]] = color

            # _steps = steps.slice(0)
            # _steps.push(p)

            v = r(_deep, beta, alpha, -color, step + 1, _steps, _spread)
            # v.score *= -1
            v[0] *= -1

            # board.remove(p)
            self.board[p[0]][p[1]] = COLOR_NONE

            if(v.score > best.score):
                best = v
            alpha = alpha if alpha >= best.score else best.score

            #beta剪枝
            if(v.score >= beta):
                # ABcut += 1
                print("ABcut")
                v[0] = float("inf")-1
                v.abcut = 1
                return v

        return best
    # The input is current chessboard.
    
    def get_result(candidates, role, deep):
        bestScore = float("-inf")
        for i in range(2, deep+1, 2):
            bestScore = minmax(candidates, role, i, MIN, MAX)
            if(bestScore >= FIVE):
                break

        # candidate.sort()
          #       candidates.sort(function (a,b) {
          #   if (math.equal(a.score,b.score)) {
          #     // 大于零是优势，尽快获胜，因此取步数短的
          #     // 小于0是劣势，尽量拖延，因此取步数长的
          #     if (a.score >= 0) {
          #       if (a.step !== b.step) return a.step - b.step
          #       else return b.score - a.score // 否则 选取当前分最高的（直接评分)
          #     }
          #     else {
          #       if (a.step !== b.step) return b.step - a.step
          #       else return b.score - a.score // 否则 选取当前分最高的（直接评分)
          #     }
          #   }
          #   else return (b.score - a.score)
          # })

        # 排序获得最优结果
        result = candidates[0]
        return result

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
        # first at sun
        if(len(idx) == self.chessboard_size ** 2):
            self.first_chess()
            return;

        new_pos = self.minmax(deep=SEARCH_DEPTH,color=self.color)
        print("new pos is :",new_pos)
        #==============Find new pos========================================
        # Make sure that the position of your decision in chess board is empty.
        #If not, return error.
        assert chessboard[new_pos[0],new_pos[1]]==0
        #Add your decision into candidate_list, Records the chess board
        self.candidate_list.append(new_pos)
        time2 = time.time()
        print(time2 - time1)

