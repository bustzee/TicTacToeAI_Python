import pygame
import numpy as np  
import sys


pygame.init()


#DECLARING OUR CONSTANTS
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (180,180,180)
RED = (255,0,0)
GREEN = (0,255,0)

WIDTH = 300
HEIGHT = 300
GRID_LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLUMNS = 3
SQUARE_SIZE = WIDTH//BOARD_ROWS
CIRCLE_RADIUS = SQUARE_SIZE//3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Tic Tac Toe Game')
screen.fill(BLACK)

board = np.zeros((BOARD_ROWS, BOARD_COLUMNS))



def draw_lines(color=WHITE):
    for i in range(1,BOARD_ROWS):
        pygame.draw.line(screen, color, (0,SQUARE_SIZE*i), (WIDTH, SQUARE_SIZE*i), GRID_LINE_WIDTH)
        pygame.draw.line(screen, color, (SQUARE_SIZE*i,0), (SQUARE_SIZE*i,HEIGHT),GRID_LINE_WIDTH)


def draw_figures(color=WHITE):
    #print("drawing figures")
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS):
            value = board[row][col]
            #print(board[row][col])
            if board[row][col]==1:
                #circle
                print("Circle")
                pygame.draw.circle(screen, color, (int(col*SQUARE_SIZE + SQUARE_SIZE//2), int(row*SQUARE_SIZE + SQUARE_SIZE//2)), CIRCLE_RADIUS,CIRCLE_WIDTH)


            elif board[row][col]==2:
                print("Square")
                pygame.draw.line(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE//4, row*SQUARE_SIZE + SQUARE_SIZE//4), (col*SQUARE_SIZE + 3*SQUARE_SIZE//4, row*SQUARE_SIZE  + 3*SQUARE_SIZE//4), CROSS_WIDTH)
                pygame.draw.line(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE//4, row*SQUARE_SIZE + 3*SQUARE_SIZE//4), (col*SQUARE_SIZE + 3*SQUARE_SIZE//4, row*SQUARE_SIZE  + SQUARE_SIZE//4), CROSS_WIDTH)




def mark_square(row, col, player):

    board[row][col] = player
    print(board[row][col])


def available_square(row, col):
    return board[row][col]==0

def is_board_full(check_board=board):
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLUMNS):
            if check_board[i][j]==0:
                return False
    
    return True


def check_winner(player, check_board=board):
    for j in range(BOARD_COLUMNS):
        if board[0][j] == player and board[1][j] == player and board[2][j] == player:
            return True
    
    for k in range(BOARD_ROWS):
        if board[k][0]==player and board[k][1] == player and board[k][2] == player:
            return True
    
    #check diagonals
        #left diagonal
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    elif board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    # no winner
    return False

#minimax function for AI algorithm
def minimax(minmax_board, depth, isMaximizingPlayer):
    if check_winner(2, minmax_board):
        return float('inf')
    elif check_winner(1, minmax_board):
        return float('-inf')
    elif is_board_full(minmax_board):
        return 0
    
    if isMaximizingPlayer:
        bestscore = -10000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLUMNS):
                if minmax_board[row][col] == 0:
                    # available square
                    minmax_board[row][col] = 2
                    score = minimax(minmax_board, depth + 1, False)
                    minmax_board[row][col] = 0
                    bestscore = max(bestscore, score)

        return bestscore

    else:
        bestscore = 10000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLUMNS):
                if minmax_board[row][col] == 0:
                    # available square
                    minmax_board[row][col] = 1
                    score = minimax(minmax_board, depth + 1, True)
                    minmax_board[row][col] = 0
                    bestscore = min(bestscore, score)

        return bestscore
    
def best_move():
    best_score = -10000
    move = (-1,-1)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                if (score > best_score):
                    best_score = score
                    move = (row, col)
    
    if move != (-1,-1):
        mark_square(move[0], move[1], 2)
        return True
    return False


def restart_game():
    screen.fill(BLACK)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS):
            board[row][col] = 0


draw_lines()
player = 1
game_Over = False


while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
    
        if event.type==pygame.MOUSEBUTTONDOWN and not game_Over:
            mouseX = event.pos[0]//SQUARE_SIZE
            mouseY = event.pos[1]//SQUARE_SIZE
            
            if available_square(mouseY, mouseX):
                print("Square available")
                mark_square(mouseY, mouseX, 1)
                if check_winner(1):
                    game_Over=True
                    
                player = player % 2 + 1

                if not game_Over:
                    if best_move():
                        if check_winner(2):
                            game_Over = True
                            print("AI WON")
                    

                        player = player % 2 + 1

                if not game_Over:
                    if is_board_full(board):
            
                        game_Over = True
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                restart_game()
                game_Over=False
                player=1

     
    if not game_Over:
        draw_figures(WHITE)  
        #print("k")
    else:
        if check_winner(1):
            draw_figures(GREEN)
            draw_lines(GREEN)
        elif check_winner(2):
            draw_figures(RED)
            draw_lines(RED)
        else:
            draw_figures(GRAY)
            draw_lines(GRAY) 
    pygame.display.update()
