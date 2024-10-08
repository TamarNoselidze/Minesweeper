from tkinter import *
from tkinter.font import Font
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random

root = Tk()       
root.title('Minesweeper')
canvas=Canvas(root, width=540, height=570, background='#aaaaaa')
canvas.grid()

class Square:

    opened=False
    flag=False
    mine=False
    adj_mines=0

    def __init__(self):
        pass

class Board:
    dirs=[(0,1), (0,-1), (1,0), (-1,0), (-1,-1), (-1,1), (1,-1), (1,1)]
    def create_board(self, size):
        board=[]
        for i in range (size):
            row=[]
            for j in range(size):
                square=Square()
                row.append(square)
            board.append(row)
        return board
    
    def mine_generator(self, size, num_mines):
        mines=set()
        while len(mines)<num_mines:
            i=random.randint(0,(size**2-1))
            mines.add(i)

        for mine in mines:
            i=mine//size
            j=mine%size
            self.board[i][j].mine=True

    def content_generator(self, size):
        for x in range(size):
            for y in range(size):
                square=self.board[x][y]
                value=0
                if not square.mine:
                    for dx, dy in self.dirs:
                        if 0<=x+dx<=size-1 and 0<=y+dy<=size-1:
                            new_square=self.board[x+dx][y+dy]    
                            if new_square.mine:
                                value+=1
                    square.adj_mines=value
               

    def __init__(self, size=16, num_mines=40):    
        self.num_flags=num_mines
        self.game_over=False
        self.game_won=False
        self.size=size

        self.board = self.create_board(size)
        self.mine_generator(size, num_mines)
        self.content_generator(size)

board=Board()


def create_canvas():
    # Board
    canvas.create_rectangle(30, 60, 510, 540, fill='#343d52')

    # Vertical lines at intevals of 30
    x0=list(range(30,540,30))
    for i in x0:
        id = canvas.create_line(i, 60, i, 540, width=2, fill='white')

    # Horizontal lines at intevals of 30
    y0=list(range(60,570,30))
    for i in y0:
        id = canvas.create_line(30, i, 510, i, width=2, fill='white')
    
    # N of flags
    canvas.create_rectangle(60, 15, 150, 45, fill='#808588', outline='#808588')
    font=Font(family='Courier 10 Pitch', size=10)
    text=f'Flags: {board.num_flags}'
    canvas.create_text(105, 30, text=text, font=font)

    # Restart Button
    font=Font(family='Courier 10 Pitch', size=10)
    restart_button = Button(root, text='Restart', font=font, command=restart, bg='#808588', height=1, width=9)
    restart_button.place(x=390,y=15)

    # Help Button
    font=Font(family='Arial Black', size=10)
    help_button = Button(root, text='?', command=help, font=font, bg='#193465', height=1, width=3)
    help_button.place(x=255,y=15)

def help():
    popup = tk.Tk()
    popup.wm_title('Help')
    font=Font(family='Courier 10 Pitch', size=10)

    with open('rules.txt') as f:
        rules = f.read()
    label = ttk.Label(popup, text=rules, font=font)
    label.pack(side="top", fill="x", padx=20, pady=40)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()


def restart():
    global board
    canvas.delete('all')
    create_canvas()
    board=Board()
    update_flag(board.num_flags)

def display_content(x,y):
    if board.board[x][y].flag:
        canvas.create_rectangle(x*30+30, y*30+60, x*30+59, y*30+89, fill='#343d52', outline='white')
        board.num_flags+=1
        update_flag(board.num_flags)

    content=board.board[x][y].adj_mines
    colors=['blue', '#0f29d4', '#3CC130', '#F80C0C', '#1f1313', '#FCED10', '#EA5BA9', '#B6F2F0', '#1D4515']
    font=Font(family='Arial Black', size=12)
    canvas.create_rectangle(x*30+30, y*30+60, x*30+59, y*30+89, fill='#aaaaaa', outline='white')
    if content!=0:
        canvas.create_text(x*30+45, y*30+75, text=content, font=font, fill=colors[content])
    board.board[x][y].opened=True

def content_rec_fun(x,y):
    square=board.board[x][y]
    #base case
    if square.opened or square.mine:
        return
    
    display_content(x,y)
        
    #recursive case
    if square.adj_mines==0:
        for dx, dy in board.dirs:
            if 0<=x+dx<board.size and 0<=y+dy<board.size:
                content_rec_fun(x+dx, y+dy)


image1 = Image.open('mine.png')
resize_image1= image1.resize((20, 20))
mine=ImageTk.PhotoImage(resize_image1)

def gameover():
    board.game_over=True
    font=Font(family='Courier 10 Pitch', size=10)
    text="GAME OVER - CLICK 'Restart' TO RESTART THE GAME"
    canvas.create_text(270, 555, text=text, font=font, fill='#ff0000')
    for x in range (16):
        for y in range(16):
            if board.board[x][y].mine:
                color='red'
                if board.board[x][y].flag:
                    color='green'
                canvas.create_rectangle(x*30+30, y*30+60, x*30+59, y*30+89, fill=color, outline='white')
                canvas.create_image(x*30+45, y*30+75, image=mine)

                

def check_win():
    for x in range(16):
        for y in range(16):
            square=board.board[x][y]
            if square.mine and not square.flag:
                return
            if not square.mine and square.flag:
                return

    board.game_won=True        
    font=Font(family='Courier 10 Pitch', size=10)
    text="YOU WON - CLICK 'Restart' TO RESTART THE GAME"
    canvas.create_text(270, 555, text=text, font=font, fill='green')

    for x in range(16):
        for y in range(16):
            content_rec_fun(x,y)

def left_click(event):
    if 30<= event.x<=510 and 60<=event.y<=540:
        if board.game_over==False and board.game_won==False:
            x=round((event.x-45)/30)
            y=round((event.y-75)/30)
            square=board.board[x][y]
        
            if square.opened or square.flag:
                return 
            elif square.mine:
                gameover()
            else:
                content_rec_fun(x,y)
        
        else:
            pass    
    else:
        pass


image2 = Image.open("flag.png")
resize_image2= image2.resize((27, 27))
flag=ImageTk.PhotoImage(resize_image2)

def update_flag(n):
    canvas.create_rectangle(60, 15, 150, 45, fill='#808588', outline='#808588')
    font=Font(family='Courier 10 Pitch', size=10)
    text=f'Flags: {n}'
    canvas.create_text(105, 30, text=text, font=font)

def right_click(event):
    if 30<= event.x<=510 and 60<=event.y<=540:
        if board.game_over==False and board.game_won==False:

            x=round((event.x-45)/30)
            y=round((event.y-75)/30)
            square=board.board[x][y]
            if square.flag:
                canvas.create_rectangle(x*30+30, y*30+60, x*30+59, y*30+89, fill='#343d52', outline='white')
                square.flag=False
                board.num_flags+=1
                update_flag(board.num_flags)

            elif square.opened:
                return

            else:
                canvas.create_image(x*30+45, y*30+75, image=flag)
                square.flag=True
                board.num_flags-=1
                update_flag(board.num_flags)
                if board.num_flags==0:
                    check_win()
            
    else:
        pass

create_canvas()
canvas.bind('<Button-1>', left_click)
canvas.bind('<Button-3>', right_click)

root.mainloop()