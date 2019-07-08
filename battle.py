# -*- coding: utf-8 -*-
"""
Created on Thu May  2 23:10:34 2019

@author: Cavin 
"""

import pygame
pygame.init() # initialisation 

# window 
win = pygame.display.set_mode((500,480)) # window setting 
pygame.display.set_caption("Cavin's Game") # title of window 

screenwidth = 500 

# basic setting with images 
walkRight = [pygame.image.load('C://data/R1.png'),
             pygame.image.load('C://data/R2.png'),
             pygame.image.load('C://data/R3.png'),
             pygame.image.load('C://data/R4.png'),
             pygame.image.load('C://data/R5.png'),
             pygame.image.load('C://data/R6.png'),
             pygame.image.load('C://data/R7.png'),
             pygame.image.load('C://data/R8.png'),
             pygame.image.load('C://data/R9.png')]
walkLeft = [pygame.image.load('C://data/L1.png'),
             pygame.image.load('C://data/L2.png'),
             pygame.image.load('C://data/L3.png'),
             pygame.image.load('C://data/L4.png'),
             pygame.image.load('C://data/L5.png'),
             pygame.image.load('C://data/L6.png'),
             pygame.image.load('C://data/L7.png'),
             pygame.image.load('C://data/L8.png'),
             pygame.image.load('C://data/L9.png')]
bg = pygame.image.load('C://data/bg.jpg')
char = pygame.image.load('C://data/standing.png')

clock = pygame.time.Clock() 

#bulletSound = pygame.mixer.Sound('bullet.wav')
#hitSound = pygame.mixer.Sound('hit.wav')

music = pygame.mixer.music.load('C://data/music.mp3')
pygame.mixer.music.play(-1)

score = 0

# classifying for optimisation 
class player(object):
    def __init__(self, x, y, width, height): # default variables 
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.vel = 5 
        self.isJump = False 
        self.jumpCount = 10 
        self.left, self.right = False, False 
        self.walkCount = 0 
        self.standing = True 
        self.hitbox = (self.x + 17, self.y + 11, 29, 52) # rectangle(x, y, width, height) 
        
    
    def draw(self,win): 
        if self.walkCount+1 >= 27: 
            self.walkCount = 0 
            
        if not(self.standing): # means not moving?  
            if self.left: 
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y)) # use walkCount as indices 
                self.walkCount += 1
            elif self.right: 
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1 
        else: # if moving? 
            #win.blit(char, (self.x,self.y))
            if self.right: 
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52) 
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2) 

    def hit(self): 
        self.isJump = False # redefine the jump not to let the character go to the bottom 
        self.jumpCount = 10
        self.x = 100
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255,0,0))
        win.blit(text, (250 - (text.get_width()/2),200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

'''
First, you need to realize what blitting is doing. 
Your screen is just a collection of pixels, 
and blitting is doing a complete copy of one set of pixels onto another. 
For example, you can have a surface with an image that you loaded from the hard drive, 
and can display it multiple times on the screen in different positions 
by blitting that surface on top of the screen surface multiple times.

https://stackoverflow.com/questions/17454257/a-bit-confused-with-blitting-pygame
'''
            
class projectile(object):
    def __init__(self, x, y, radius, color, facing): # facing: when the character stands 
        self.x, self.y = x, y 
        self.radius = radius 
        self.color = color 
        self.facing = facing 
        self.vel = 8 * facing 
        
    def draw(self, win): 
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius) 

class enemy(object):
    walkRight = [pygame.image.load('C://data/R1E.png'),
             pygame.image.load('C://data/R2E.png'),
             pygame.image.load('C://data/R3E.png'),
             pygame.image.load('C://data/R4E.png'),
             pygame.image.load('C://data/R5E.png'),
             pygame.image.load('C://data/R6E.png'),
             pygame.image.load('C://data/R7E.png'),
             pygame.image.load('C://data/R8E.png'),
             pygame.image.load('C://data/R9E.png'),
             pygame.image.load('C://data/R10E.png'),
             pygame.image.load('C://data/R11E.png')]
    walkLeft = [pygame.image.load('C://data/L1E.png'),
             pygame.image.load('C://data/L2E.png'),
             pygame.image.load('C://data/L3E.png'),
             pygame.image.load('C://data/L4E.png'),
             pygame.image.load('C://data/L5E.png'),
             pygame.image.load('C://data/L6E.png'),
             pygame.image.load('C://data/L7E.png'),
             pygame.image.load('C://data/L8E.png'),
             pygame.image.load('C://data/L9E.png'),
             pygame.image.load('C://data/L10E.png'),
             pygame.image.load('C://data/L11E.png')]
    
    def __init__(self, x, y, width, height, end):
        self.x, self.y = x, y 
        self.width, self.height = width, height
        self.end = end
        self.path = [self.x, self.end] # keep tracking and stop  
        self.walkCount = 0 
        self.vel = 3 
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10 
        self.visible = True  

    def draw(self, win):
        self.move() 
        if self.visible: 
            if self.walkCount + 1 >= 33: # to change the walking images 
                self.walkCount = 0 
            if self.vel > 0: 
                win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1 
            else: 
                win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1 
                
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10)) # health bar(red) 
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - ((50/10) * (10 - self.health)), 10)) # health bar(green) 
            self.hitbox = (self.x + 17, self.y + 2, 31, 57) 
            #pygame.draw.rect(win, (255,0,0), self.hitbox, 2) 
    
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]: 
                self.x += self.vel
            else: 
                self.vel = self.vel * -1 # change direction 
                self.walkCount = 0 
        else: 
            if self.x - self.vel > self.path[0] :
                self.x += self.vel 
            else: 
                self.vel = self.vel * -1 
                self.walkCount = 0 
    
    def hit(self): 
        if self.health > 1:
            self.health -= 1
        else: 
            self.visible = False # make character invisible if health hits to 0 
        print('Hit!', end=" ") 
        
    
        
# main variables 
#x, y = 50, 400 # top-left: (0,0) // bottom-right: (500,500) 
#width, height = 64, 64  
#vel = 5 # velocity(rate of moving the position for each coord) 
#isJump = False 
#jumpCount = 10 
#left, right = False, False
#walkCount = 0 

# define function for characters and background 
def redrawGameWindow():
    #global walkCount # global variable 
    win.blit(bg, (0,0))
    text = font.render('Score: ' + str(score), 1, (0,0,0)) 
    win.blit(text, (350, 10)) # put the text on the screen just like characters 
    man.draw(win) # inheritance 
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    
    pygame.display.update() 

# mainloop 
font = pygame.font.SysFont('comicsans', 30, True) # SysFont(name, size, bold=False, italic=False) 
man = player(300, 410, 64, 64)
goblin = enemy(100, 410, 64, 64, 450)
shootLoop = 0 
bullets = [] 
run = True 
while run:
    #pygame.time.delay(50) # clock in a game 
    clock.tick(27) # frame rate(fps?) 

    if goblin.visible == True: # set this if statement to avoid the collision after goblin becomes invisible 
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                score -= 5 
    
    if shootLoop > 0: # make timedelay between each shot 
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
            
    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]: # y-coord 
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]: # x-coord 
                goblin.hit() 
                score += 1 
                bullets.pop(bullets.index(bullet)) # delete the bullet 
                
            
        if bullet.x < 500 and bullet.x > 0: # possible amount of shots 
            bullet.x += bullet.vel
        else: # not shown on the screen 
            bullets.pop(bullets.index(bullet)) # remove bullets 
            
    keys = pygame.key.get_pressed() 
    
    if keys[pygame.K_SPACE] and shootLoop == 0: 
        if man.left:
            facing = -1 
        else: 
            facing = 1
        if len(bullets) < 5: 
            bullets.append(projectile(round(man.x + man.width//2), round(man.y + man.height//2), 6, (0,0,0), facing))
            
        shootLoop = 1
    
    if keys[pygame.K_LEFT] and man.x > man.vel: # set boundaries 
        man.x -= man.vel # moves left by the amount of vel 
        man.left, man.right = True, False 
        man.standing = False # isn't indeed walking? 
    elif keys[pygame.K_RIGHT] and man.x < 500-man.width-man.vel: 
        man.x += man.vel 
        man.left, man.right = False, True 
        man.standing = False 
    else: 
        man.standing = True 
        #man.left, man.right = False, False 
        man.walkCount = 0 
        
    if not(man.isJump):
        #if keys[pygame.K_UP] and y > vel:
        #    y -= vel # y-cord approached to 0(moves upward)
        #if keys[pygame.K_DOWN] and y < 500-height-vel:
        #    y += vel 
        if keys[pygame.K_UP]:
            man.isJump = True 
            man.left, man.right = False, False 
            man.walkCount = 0 
            
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1 # allows to go downward after jumping  
            man.y -= (man.jumpCount**2)*.5*neg # square function(jump downward by the amount of square)
            man.jumpCount -= 1 
        else:
            man.isJump = False
            man.jumpCount = 10 
    
    redrawGameWindow() 
    
    #win.fill((0,0,0)) # remove trails 
    
    # draw characters 
    #pygame.draw.rect(win, (255, 0, 0), (x, y, width, height)) # rgb 
    #pygame.display.update() # show the character on the window 
            
pygame.quit() 
