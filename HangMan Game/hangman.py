import pygame
import sys
from pygame.locals import *
import math
import random
pygame.font.init()

#Setting up the display window
SCREENWIDTH = 1366
SCREENHEIGHT = 768
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('HangMan Game by Lavish Khariwal')
pygame.display.update()

#Global Variables for the game
FPS = 60
BACKGROUND = 'assets/sprites/background.png'
MAIN = 'assets/sprites/main.png'
GAMEOVER = 'assets/sprites/GameOver.png'
GAMEWIN = 'assets/sprites/GameWin.png'
GAME_SPRITES = {}
GAME_SOUNDS = {}
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
RADIUS = 43
GAP = 21
A = 65
Y = chr(90)
Z = chr(91)
LETTER_FONT = pygame.font.SysFont('assets/MyFont/ARCADE.ttf', 78)
DIS_FONT = pygame.font.SysFont('assets/MyFont/ARCADE.ttf', 88)
WORD_FONT = pygame.font.SysFont('assets/MyFont/ARCADE.ttf', 92)
KILL_FONT = pygame.font.SysFont('assets/MyFont/ARCADE.ttf', 50)

#Colours
purple = (98, 24, 131)
pink = (235, 67, 231)

#Game Variables
hangmanStatus=0
with open("assets/dict/Dictionary.txt", "r") as file:
    MyDict = file.read()
    words = list(map(str, MyDict.split()))
keyboard = []
secret_word = random.choice(words)
display_word = ["_ "] * len(secret_word)
INCORRECT_GUESSES = 0
max_incorrect_guesses = 6
startx = 559
starty = 267

for i, letter in enumerate(LETTERS):
    x = startx + ((GAP +(RADIUS*2)) * (i % 6))
    y = starty + ((i//6) * (GAP + (RADIUS*2)))
    keyboard.append((x, y, letter))
    
               
#Showing Welcome image on the screen        
def welcomeScreen():
      while True:
          for event in pygame.event.get():
              #Quit the Game
              if event.type == QUIT:
                     pygame.quit()
                     sys.exit()
                     
              elif event.type == KEYDOWN and event.key == K_ESCAPE:
                     pygame.quit()
                     sys.exit()
                   
              #Head to the main game    
              elif event.type == KEYDOWN and (event.key == K_TAB):
                     return
              
              #Shows the Welcome Screen
              else:
                     SCREEN.blit(GAME_SPRITES['main'], (0,0))
                     pygame.display.update()
                     FPSCLOCK.tick(FPS)

#Game Win
def GameWin():
    
    while True:
        for event in pygame.event.get():
                   #Quit the game
                   if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                        
                   #Head to the main game    
                   elif event.type == KEYDOWN and (event.key == K_TAB):
                       mainGame()
                   
                   else:
                       
                       text = DIS_FONT.render("THE WORD WAS " + secret_word + "!" , 1, pink)
                       word_x = (SCREENWIDTH - text.get_width())/2
                       SCREEN.blit(GAME_SPRITES['gamewin'], (0,0))
                       SCREEN.blit(text, (word_x , 150)) 
                       pygame.display.update()
                       FPSCLOCK.tick(FPS)
                       
#Game Over
def GameOver():
    
    while True:
            for event in pygame.event.get():
                   #Quit the game
                   if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                        
                   #Head to the main game    
                   elif event.type == KEYDOWN and (event.key == K_TAB):
                        mainGame()
                   
                   else:
                        
                        text = DIS_FONT.render("THE WORD WAS " + secret_word + "!" , 1, pink)
                        word_x = (SCREENWIDTH - text.get_width())/2
                        SCREEN.blit(GAME_SPRITES['gameover'], (0,0))
                        SCREEN.blit(text, (word_x, 150)) 
                        pygame.display.update()
                        FPSCLOCK.tick(FPS)
                        
#Main Game         
def mainGame():
        global INCORRECT_GUESSES
        global running
        running = True
        gameover = False
        gamewin = False
        SCREEN.blit(GAME_SPRITES['background'], (0,0))
            
        #Updating the display
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
        
     
        while running:
              
                for event in pygame.event.get():
                   #Quit the game
                   if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        running = False
                   
                   #Getting mouse position
                   elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        
                        for x,y, letter in keyboard:
                            dis_x = x - mouse_x
                            dis_y = y - mouse_y
                            if abs(dis_x) < RADIUS and abs(dis_y) < RADIUS:
                                keyboard.remove((x, y, letter))
                                
                                # check if the letter is in the secret word
                                if letter in secret_word:
                                    GAME_SOUNDS['correct'].play()
                                    
                                    # update the display with the correctly guessed letter
                                    for i, c in enumerate(secret_word):
                                        if c == letter:
                                            display_word[i] = c
                                    # check if the player has won
                                    if "".join(display_word) == secret_word:
                                        SCREEN.blit(hangers[6], (90, 330))  
                                        pygame.display.update()
                                        
                                        pygame.time.delay(500)
                                        
                                        GAME_SOUNDS['win'].play()
                                        running = False
                                        GameWin()
                                        
                                else:
                                        # increment the number of incorrect guesses
                                        GAME_SOUNDS['incorrect'].play()
                                        INCORRECT_GUESSES += 1
                                        
                                        # check if the player has lost
                                        if INCORRECT_GUESSES == max_incorrect_guesses:
                                               SCREEN.blit(hangers[6], (90, 330))
                                               pygame.display.update()
                                               
                                               pygame.time.delay(500)
                                               GAME_SOUNDS['gameover'].play()
                                               
                                               GameOver()
                                               running=False
                                               
                SCREEN.blit(hangers[INCORRECT_GUESSES], (90, 330))
              
              
                for x, y, letter in keyboard:
                      pygame.draw.circle(SCREEN, purple, (x, y), RADIUS, 70)
                      
                      text = LETTER_FONT.render(letter, 1, pink)
                      SCREEN.blit(text, (x - text.get_width()/2, (y - text.get_height()/2)+2))
                      
                      text = KILL_FONT.render(f"Please Don't", 1, pink)
                      SCREEN.blit(text, (107, 107))
                      
                      text = KILL_FONT.render(f"Kill Him!", 1, pink)
                      SCREEN.blit(text, (107, 142))
                      
                      for i, worddisplayed in enumerate(display_word):
                          
                            word_to_display = WORD_FONT.render(worddisplayed, 1, pink)
                            
                            SCREEN.blit(word_to_display, ((SCREENWIDTH - word_to_display.get_width())/2 + (i*50), 121))
                  
                pygame.display.flip()
                                 

if __name__ == "__main__":
        #Initializing pygame
        pygame.init()
        
        FPSCLOCK = pygame.time.Clock()
        pygame.display.set_caption("HangMan Game by Lavish Khariwal")
        
        #Locating Game Sprites
        GAME_SPRITES['main'] = pygame.image.load(MAIN).convert_alpha()
        GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert_alpha()
        GAME_SPRITES['gameover'] = pygame.image.load(GAMEOVER).convert_alpha()
        GAME_SPRITES['gamewin'] = pygame.image.load(GAMEWIN).convert_alpha()
        
        hangers = [pygame.image.load('assets/sprites/images_hangman0.png').convert_alpha(),
        pygame.image.load('assets/sprites/images_hangman1.png').convert_alpha(),
        pygame.image.load('assets/sprites/images_hangman2.png').convert_alpha(),
        pygame.image.load('assets/sprites/images_hangman3.png').convert_alpha(),
        pygame.image.load('assets/sprites/images_hangman4.png').convert_alpha(),
        pygame.image.load('assets/sprites/images_hangman5.png').convert_alpha(),
        pygame.image.load('assets/sprites/images_hangman6.png').convert_alpha(), ]
        
        hangers[0] = pygame.transform.scale(hangers[0], (350,350))
        hangers[1] = pygame.transform.scale(hangers[1], (350,350))
        hangers[2] = pygame.transform.scale(hangers[2], (350,350))
        hangers[3] = pygame.transform.scale(hangers[3], (350,350))
        hangers[4] = pygame.transform.scale(hangers[4], (350,350))
        hangers[5] = pygame.transform.scale(hangers[5], (350,350))
        hangers[6] = pygame.transform.scale(hangers[6], (350,350))
        
        GAME_SPRITES['backgroud'] = pygame.transform.scale(GAME_SPRITES['background'], (1366, 768))
        GAME_SPRITES['main'] = pygame.transform.scale(GAME_SPRITES['main'], (1366, 768))
        GAME_SPRITES['gameover'] = pygame.transform.scale(GAME_SPRITES['gameover'], (1366, 768))
        GAME_SPRITES['gamewin'] = pygame.transform.scale(GAME_SPRITES['gamewin'], (1366, 768))
        
        #Locating Game Sounds
        GAME_SOUNDS['win'] = pygame.mixer.Sound('assets/audio/win.wav')
        GAME_SOUNDS['gameover'] = pygame.mixer.Sound('assets/audio/gameover.wav')
        GAME_SOUNDS['correct'] = pygame.mixer.Sound('assets/audio/correct.wav')
        GAME_SOUNDS['incorrect'] = pygame.mixer.Sound('assets/audio/incorrect.wav')
        
        #Running all the functions
        while True:
               welcomeScreen()
               mainGame()
               
pygame.quit()
sys.exit()
