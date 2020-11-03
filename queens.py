# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 01:24:23 2020

@author: Edward Yip
"""


import math
import numpy as np
import pygame




ALPH = ["a","b","c","d","e","f","g","h","i","j"]
NUM = [1,2,3,4,5,6,7,8,9,0]
QUEENIMG = pygame.image.load("queen.png")

def queens(position, size):
    global allstep
    allstep = []
    if size == 1:
        return "a1"
    pos_step = []
    
    #making the board
    board = np.empty([size,size],dtype=object)
    global ff
    ff = np.empty([size,size],dtype=object)
    for i in range(size):
        for j in range(size):
            ff[i,j] = str(str(ALPH[j])+str(NUM[:size][-i-1]))
            board[i,j] = "  "
    board_states = []

    #position coordinates
    pos = list(np.where(ff == position))
    if len(pos[0]) == 0:
        return None

    # first queen
    new_queen(position,size,board,board_states,pos_step) 
    board_states.append(np.copy(board))
    

    col_steps = [[i for i in range(size) if i != pos[1]]]
    
    find_spot(size,board,board_states,pos_step,col_steps)
    output = (str(",".join(sorted(pos_step))))
    if len(col_steps) ==0:
        return "There is no solution"
    return allstep
  
def new_queen(new_position,size,board,board_states,pos_step):
    pos_step.append(new_position)
    pos = list(np.where(ff == new_position))

    #row
    for i in range(size):
        board[i,pos[1]]="o "
    
    #column
    for i in range(size):
        board[pos[0],i]="o "
     
    #diagonal1
    if pos[1]-pos[0] >=0:
        np.fill_diagonal(board[:,int(pos[1]-pos[0]):], "o ")
    else:
        np.fill_diagonal(board[int(pos[0]-pos[1]):], "o ")
    #diagonal2
    if pos[0]+pos[1]>=size:
        np.fill_diagonal(board[int(pos[1]-(size-pos[0])+1):,::-1], "o ")
    else:
        np.fill_diagonal(np.fliplr(board[:,:int(pos[1]+pos[0]+1)]), "o ")
    
    board[tuple(pos)]= new_position
    board_states.append(np.copy(board))
    
def find_spot(size,board,board_states,pos_step,col_steps):

    fill = 0
    if len(col_steps) ==0:
        return 
    i = col_steps[-1][0]
    for j in range(size):
        if board[j,i] != "  ":
            continue
        pos_found = str(str(ALPH[i])+str(NUM[:size][-j-1]))
        new_queen(pos_found,size,board,board_states,pos_step)
        fill = 1
        break
    allstep.append(np.copy(board))
            
    if fill == 1:
        if len(pos_step)!=size:
            col_next = [a for a in col_steps[-1] if a !=i]
            col_steps.append(col_next)
            find_spot(size,board,board_states,pos_step,col_steps)
            return
        
    else:
        if len(col_steps)==0:
            return
        del board_states[-1]
        del col_steps[-1]
        board = np.copy(board_states[-1])
        d_spot = list(np.where(ff == pos_step[-1]))
        board[d_spot[0],d_spot[1]]= "# "
        del board_states[-1]
        board_states.append(np.copy(board))
        del pos_step[-1]
        find_spot(size,board,board_states,pos_step,col_steps)
        return

def BoardGen(size):
    board = np.empty([size,size],dtype=object)
    fullboard = np.empty([size,size],dtype=object)
    for i in range(size):
        for j in range(size):
            fullboard[i,j] = str(str(ALPH[j])+str(NUM[:size][-i-1]))
            board[i,j] = "  "
    return board, fullboard

def BoardUpdate(board,done):
    counter = 0
    for i in range(size):
        for j in range(size):
            rect = (70*i+60, 70*j+60, 70, 70)
            spot = pygame.Rect(70*i+85, 70*j+85, 20, 20)
            if counter % 2 == 0:
                pygame.draw.rect(gameDisplay, (240,217,181), rect)
            else:
                pygame.draw.rect(gameDisplay, (181,136,99), rect)
            counter +=1
            
            if board[j,i] == "o ":
                if done !=1:
                    pygame.draw.ellipse(gameDisplay, (20,20,20), spot)
            elif board[j,i] == "# ":
                if done != 1:
                    pygame.draw.rect(gameDisplay, (255,100,100), spot)
            elif board[j,i] != "  ":
                gameDisplay.blit(QUEENIMG,(70*i+60, 70*j+60))
                            
        if size % 2 ==1:
            continue
        counter -=1

framezero = pygame.USEREVENT + 1
FR_ZERO = pygame.event.Event(framezero)
frameone = pygame.USEREVENT + 2
FR_ONE = pygame.event.Event(frameone)
frametwo = pygame.USEREVENT + 3
FR_TWO = pygame.event.Event(frametwo)
framethree = pygame.USEREVENT + 4
FR_THREE = pygame.event.Event(framethree)

game_exit = False
pygame.init()
pygame.event.post(FR_ZERO)

while not game_exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_exit = True
        if event.type == framezero:
            frame = 0
            gameDisplay = pygame.display.set_mode((400,400))
            pygame.display.set_caption("Choose an integer")
            gameDisplay.fill((240,217,181))
            pygame.font.init() 
            myfont = pygame.font.SysFont('Calibri', 25,bold=True)
            sizeqs = myfont.render(str("Enter the board size (1-10):"), True, (0, 0, 0))
            gameDisplay.blit(sizeqs,(60,100))
            num_entry = ""
            
        if frame == 0:
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if num_entry.isnumeric():
                        if 0<int(num_entry)<11:
                            size = int(num_entry)
                            pygame.event.post(FR_ONE)
                        else:
                            error = myfont.render(str(num_entry)+str(" is not between 1-10!!"), True, (0, 0, 0))
                            error_width = int(error.get_width())
                            pygame.draw.rect(gameDisplay, (240,217,181), ((0,130,400,50)))
                            gameDisplay.blit(error,((400-error_width)/2,130))

                    else:
                        error = myfont.render(str(num_entry)+str(" is not an integer!"), True, (0, 0, 0))
                        error_width = int(error.get_width())
                        pygame.draw.rect(gameDisplay, (240,217,181), ((0,130,400,50)))
                        gameDisplay.blit(error,((400-error_width)/2,130))
                
                    num_entry = ''
                    
                elif event.key == pygame.K_BACKSPACE:
                    num_entry = num_entry[:-1]
                else:
                    if len(num_entry)<10:
                        num_entry += event.unicode
                    
            text = myfont.render(num_entry,True,(0,0,0))
            pygame.draw.rect(gameDisplay, (240,217,181), (150,200,200,50))
            gameDisplay.blit(text,(150,200))
            
        if event.type == frameone:
            board , fullboard = BoardGen(size)
            
            gameDisplay = pygame.display.set_mode((size*70+120,size*70+120))
            pygame.display.set_caption("ChessBoard")
            gameDisplay.fill((255,255,255))
            pygame.draw.rect(gameDisplay, (0,0,0), (50, 50, size*70+20, size*70+20))
            
            Choose = myfont.render(str("Choose a position"), True, (0, 0, 0))
            gameDisplay.blit(Choose,(10,10))
            
            BoardUpdate(board,0)
            frame = 1   

        if frame == 1:     
            pygame.draw.rect(gameDisplay, (255,255,255), (size*70,size*70+80,50,50))
            mouse_x , mouse_y = pygame.mouse.get_pos()
            sq_x = ((mouse_x-60) // 70) if ((mouse_x-60) // 70)<size else size-1
            sq_y = ((mouse_y-60) // 70) if ((mouse_y-60) // 70)<size else size-1
            textsurface = myfont.render(str(fullboard[sq_y,sq_x]), True, (100, 100, 100))
            gameDisplay.blit(textsurface,(size*70,size*70+80))
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 60 < mouse_x < size*70+60 and 60 < mouse_y < size*70+60:
                    pygame.draw.rect(gameDisplay, (255,255,255), (10, 10, 200, 35))
                    frame = 2
                    pygame.event.post(FR_TWO)
                    board[sq_y,sq_x]=fullboard[sq_y,sq_x]
                    BoardUpdate(board,0)
  
        if frame == 2:
            q = queens(fullboard[sq_y,sq_x],size)
            if isinstance(q,str):
                no_sol = myfont.render(str("No Solution!"), True, (0, 0, 0))
                gameDisplay.blit(no_sol,(10,10))
            else:
                for i in q:
                    BoardUpdate(i,0)
                    pygame.display.update()
                    pygame.time.delay(50)
                pygame.event.post(FR_THREE)
            frame = 3
            
        if event.type == framethree:
            pygame.time.delay(100)
            BoardUpdate(q[-1],1)
            
        if frame == 3:
           pygame.draw.rect(gameDisplay, (230,230,230),(50,size*70+77,80,30))
           play_again = myfont.render(str("Again?"), True, (0, 0, 0))
           gameDisplay.blit(play_again,(55,size*70+80))
           mouse_x , mouse_y = pygame.mouse.get_pos()
           if event.type == pygame.MOUSEBUTTONDOWN:
                if 65 < mouse_x < 155 and size*70+80 < mouse_y < size*70+125: 
                    pygame.event.post(FR_ZERO)
   
    pygame.display.update()

pygame.quit()
