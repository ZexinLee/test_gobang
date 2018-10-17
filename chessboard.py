import tkinter as tk
from tkinter import *
from tkinter import EventType
from tkinter import Event
import numpy as np
from chessboard_tools import *
import model6
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0

class Chessboard(object):
    def __init__(self, chessboard_size):
        # information of players
        self.chessboard_size = chessboard_size
        self.chessboard_info = self.init_board_info()
        self.player = COLOR_BLACK
        self.bla_start_pos = [235, 235]
        self.whi_chessed = []
        self.bla_chessed = []

        # game states
        self.isStarted = False
        self.someoneWin = COLOR_NONE

        self.window = Tk()
        self.window.title('GoBang Game')
        self.window.geometry("600x470+80+80")
        self.window.resizable(0, 0)
        self.can = Canvas(self.window, bg='#EEE8AC', width=470, height=470)
        self.draw_board()
        self.can.grid(row=0, column=0)
        self.var = IntVar()
        self.var.set(COLOR_BLACK)
        
        # AI
        self.AI = model6.AI(self.chessboard_size, COLOR_WHITE, 1)
        self.AI2 = model6.AI(self.chessboard_size, COLOR_BLACK, 1)

        # Record Last chess
        self.lastChess = []
        self.lastPlayer = self.player



    # configuring the layout
    def draw_board(self):
        '''Draw the chess board'''
        for row in range(self.chessboard_size):
            if row == 0 or row == self.chessboard_size-1:
                self.can.create_line((25, 25+row*30),(445,25+row*30), width = 2)
            else:
                self.can.create_line((25, 25+row*30), (445, 25+row*30), width = 1)
        for col in range(self.chessboard_size):
            if col == 0 or col == self.chessboard_size-1:
                self.can.create_line((25+col*30, 25),(25+col*30, 445), width = 2)
            else:
                self.can.create_line((25+col*30, 25),(25+col*30, 445), width = 1)
        self.can.create_oval(112, 112, 118, 118, fill="black")
        self.can.create_oval(352, 112, 358, 118, fill="black")
        self.can.create_oval(112, 352, 118, 358, fill="black")
        self.can.create_oval(232, 232, 238, 238, fill="black")
        self.can.create_oval(352, 352, 358, 358, fill="black")
    
    def init_board_info(self):
        return np.zeros((self.chessboard_size, self.chessboard_size))

    def place_btns(self):
        b1 = Button(self.window, text= '开始游戏', command = self.start_button)
        b1.place(relx=0, rely=0, x=495, y=100)

        b2 = Button(self.window, text = '重置', command = self.reset_button)
        b2.place(relx=0, rely=0, x=495, y=150)

        b3 = Radiobutton(self.window, text = '玩家先', variable=self.var, value=COLOR_BLACK, command=self.selectColor)
        b3.place(relx=0, rely=0, x=495, y=250)

        b4 = Radiobutton(self.window, text = 'AI先', variable=self.var, value=COLOR_WHITE, command=self.selectColor)
        b4.place(relx=0, rely=0, x=495, y=300)

        self.can.bind("<Button-1>", lambda x: self.chess(x))
    
    # define the function of the button
    def start_button(self):
        if self.isStarted == False:
            self.isStarted = True
            self.AI = model6.AI(self.chessboard_size, (-1)*self.player, 1)
            self.someoneWin = COLOR_NONE

            if self.player == COLOR_WHITE:
                self.AI.color = COLOR_BLACK
                self.AI2.color = COLOR_WHITE
                print('Computer first')
                self.AI.go(self.chessboard_info)
                self.draw_a_chess(self.AI.candidate_list[0][0],self.AI.candidate_list[0][0],self.AI.color)
                self.draw_chessed()
                self.check_win()


            #     self.AI.go(self.chessboard_info)
            #     self.check_win()
            #     self.draw_a_chess(self.AI.candidate_list[0][0],self.AI.candidate_list[0][1],self.AI.color)
            #     self.draw_chessed()
            #     while(self.someoneWin == COLOR_NONE):
            #         self.AI2.go(self.chessboard_info)
            #         self.draw_a_chess(self.AI2.candidate_list[0][0],self.AI2.candidate_list[0][1],self.AI2.color)
            #         self.draw_chessed()
            #         self.check_win()
            #         self.AI.go(self.chessboard_info)
            #         self.draw_a_chess(self.AI.candidate_list[0][0],self.AI.candidate_list[0][1],self.AI.color)
            #         self.draw_chessed()
            #         self.check_win()
            #         time.sleep(1)
            # else:
            #     self.AI.color = COLOR_WHITE
            #     self.AI2.color = COLOR_BLACK
            #     self.AI2.go(self.chessboard_info)
            #     self.draw_a_chess(self.AI2.candidate_list[0][0],self.AI2.candidate_list[0][1],self.AI2.color)
            #     self.draw_chessed()
            #     self.check_win()
            #     while(self.someoneWin == COLOR_NONE):
            #         self.AI.go(self.chessboard_info)
            #         self.draw_a_chess(self.AI.candidate_list[0][0],self.AI.candidate_list[0][1],self.AI.color)
            #         self.draw_chessed()
            #         self.check_win()
            #         self.AI2.go(self.chessboard_info)
            #         self.draw_a_chess(self.AI2.candidate_list[0][0],self.AI2.candidate_list[0][1],self.AI2.color)
            #         self.draw_chessed()
            #         self.check_win()
            #         time.sleep(1)
    
    def reset_button(self):
        self.someoneWin = COLOR_NONE
        self.isStarted = False
        self.whi_chessed.clear()
        self.bla_chessed.clear()
        self.chessboard_info = self.init_board_info()
        label = Label(self.window, text="reset game", background="#F0F0F0", font=("ËÎÌå", 15, "bold"))
        label.place(relx=0, rely=0, x=480, y=40)
        self.can.delete('all')
        self.draw_board()
        self.can.grid(row=0, column = 0)
        self.AI = model6.AI(self.chessboard_size, COLOR_WHITE, 1)
        
    def selectColor(self):
        '''Select chess color'''
        if self.var.get() == COLOR_BLACK:
            self.player = COLOR_BLACK
            self.AI.color = COLOR_WHITE
            self.AI2.color = COLOR_BLACK
        elif self.var.get() == COLOR_WHITE:
            self.player = COLOR_WHITE
            self.AI.color = COLOR_BLACK
            self.AI2.color = COLOR_WHITE
        else:
            pass
        return
              

    # place chess operation and draw chesses
    def draw_a_chess(self, x, y, player=None):
        self.lastChess = [x, y]
        self.lastPlayer = player
        '''draw a chess on the board'''
        px, py = pos_in_board(x, y)
        oval = pos_to_draw(px, py)

        # print(oval)

        if player == COLOR_BLACK:
            self.can.create_oval(oval, fill = 'black')
            self.bla_chessed.append([x, y, 0])
            self.chessboard_info[x][y] = COLOR_BLACK
        elif player == COLOR_WHITE:
            self.can.create_oval(oval, fill = 'white')
            self.bla_chessed.append([x, y, 1])
            self.chessboard_info[x][y] = COLOR_WHITE
        else:
            print(AttributeError('please choose player'))
        return
    

    def no_in_chessed(self, pos):
        return self.chessboard_info[pos[0]][pos[1]]==COLOR_NONE

    def draw_chessed(self):
        if len(self.whi_chessed) != 0:
            for tmp in self.whi_chessed:
                oval = pos_to_draw(*tmp[0:2])
                self.can.create_oval(oval, full='white')
        
        if len(self.bla_chessed) != 0:
            for tmp in self.whi_chessed:
                oval = pos_to_draw(*tmp[0:2])
                self.can.create_oval(oval, full='black')

    def chess(self, event):
        if self.someoneWin != COLOR_NONE or self.isStarted == False:
            return
        ex = event.y
        ey = event.x
        # print("%d %d" %(ex, ey))
        if not click_in_board(ex, ey):
            return
        
        neibor_po = get_nearest_po(ex, ey)
        # print(neibor_po)
        if self.no_in_chessed(neibor_po):
            self.draw_a_chess(neibor_po[0], neibor_po[1], self.player)
            self.check_win()
            if self.someoneWin == COLOR_NONE:
                # print("before: ", self.AI.chessboard)
                self.AI.go(self.chessboard_info)
                # print("after: ", self.AI.chessboard)
                self.draw_a_chess(self.AI.candidate_list[0][0], self.AI.candidate_list[0][1], self.AI.color)
                self.check_win()
                # print("after 2 : ", self.AI.chessboard)


    # Check whether someone win

    def check_win(self):
        '''Check whether someone win, return boolean value'''
        if self.have_five() == True:
            color = self.lastPlayer
            text = 'Black Win!' if color == COLOR_BLACK else 'White Win!'
            label = Label(self.window, text= text, background='#FFF8DC', font=("ËÎÌå", 15, "bold"))
            label.place(relx=0, rely=0, x=480, y=40)
            self.someoneWin = color

    def have_five(self):
        con_chesses = 0
        # print('last!!')
        # print(self.lastChess)

        x_min = max(0, self.lastChess[0]-4)
        x_max = min(self.chessboard_size-1, self.lastChess[0]+4)
        y_min = max(0, self.lastChess[1]-4)
        y_max = min(self.chessboard_size-1, self.lastChess[1]+4)
            
        x = self.lastChess[0]
        y = self.lastChess[1]
        col = self.lastPlayer
        # ºá
        con_chesses = 1
        for i in range(1,5):
            if x-i>=0 and self.chessboard_info[x-i][y] == col:
                con_chesses += 1
            else:
                break
        for i in range(1,5):
            if x+i < self.chessboard_size and self.chessboard_info[x+i][y] == col:
                con_chesses += 1
            else:
                break
        # print(con_chesses)
        if con_chesses >=5:
            return True
        else:
            con_chesses = 1
        
        # Êú
        for i in range(1,5):
            if y-i>=0 and self.chessboard_info[x][y-i] == col:
                con_chesses += 1
            else:
                break
        for i in range(1,5):
            if y+i < self.chessboard_size and self.chessboard_info[x][y+i] == col:
                con_chesses += 1
            else:
                break
        # print(con_chesses)
        if con_chesses >=5:
            return True
        else:
            con_chesses = 1
        # ×ó
        for i in range(1,5):
            if x-i>=0 and y-i>=0 and self.chessboard_info[x-i][y-i] == col:
                con_chesses += 1
            else:
                break
        for i in range(1,5):
            if x+i < self.chessboard_size and y+i < self.chessboard_size and self.chessboard_info[x+i][y+i] == col:
                con_chesses += 1
            else:
                break
        # print(con_chesses)
        if con_chesses >=5:
            return True
        else:
            con_chesses = 1
        # ÓÒ
        for i in range(1,5):
            if x-i>=0 and y+i < self.chessboard_size and self.chessboard_info[x-i][y+i] == col:
                con_chesses += 1
            else:
                break
        for i in range(1,5):
            if x+i < self.chessboard_size and y-i>=0 and self.chessboard_info[x+i][y-i] == col:
                con_chesses += 1
            else:
                break
        # print(con_chesses)
        if con_chesses >=5:
            return True
        else:
            return False


    def start(self):
        self.place_btns()
        self.window.mainloop()
if __name__ == '__main__':
    f = Chessboard(15)
    f.start()

