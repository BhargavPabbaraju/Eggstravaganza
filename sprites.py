
import pygame as pg
from random import randint as rand,choice
from settings import *
from math import sin,cos
from pygame.math import Vector2 as vec2

from colors import *


class Spritesheet:
    def __init__(self,file):
        self.sheet = pg.image.load('./Images/%s'%file).convert_alpha()
    
    def get_image(self,r,c,w,h,scale=1):
        surf = pg.Surface((w,h),pg.SRCALPHA)
        surf.blit(self.sheet,(0,0),[c*w,r*h,w,h])
        if scale!=1:
            surf = pg.transform.scale(surf,scale)
        
        return surf
        

sheets={}


class Egg(pg.sprite.Sprite):
    def __init__(self,game,r,c,vel,type='Egg'):
        super().__init__()
        self.type = type
        if 'egg' not in sheets:
            sheets['egg'] = Spritesheet('eggs.png')
        self.width = 64-8
        self.height = 64-8
        self.x = rand(BOUNDARY+self.width,WIDTH-BOUNDARY-self.width)
        self.y = -self.height
        self.vel = vel 
        #self.image = pg.Surface((self.width,self.height))
        #self.image.fill((rand(0,255),rand(0,255),rand(0,255)))
        self.r = r
        self.c = c
        self.game = game
        if self.type=='Egg':
            self.image = sheets['egg'].get_image(self.r,self.c,self.width,self.height)
        elif self.type=='Life':
            self.image = pg.transform.scale(self.game.life,(self.width,self.height))
        else:
            self.image = pg.transform.scale(self.game.bomb,(self.width,self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.start = pg.time.get_ticks()

        
    
    def update(self):
        if not self.game.running:
            return
        if self.y > HEIGHT - BOUNDARY:
            if self.type=='Egg':
                self.game.generate_particles(self.rect.center,self.r,self.c,'triangle')
                self.game.lose_life()
            self.kill()
        
      
       
        t = (pg.time.get_ticks()-self.start)/200
        self.y+=self.vel*t
            
        
        self.rect.y = self.y






class Bubble(pg.sprite.Sprite):
    def __init__(self,game,shooter=False):
        super().__init__()
        self.width = 64
        self.height = 64
        self.game = game
        self.image = pg.Surface((self.width,self.height),pg.SRCALPHA)
        if 'bubble' not in sheets:
            sheets['bubble'] = Spritesheet('bubbles.png')
        self.change_image()
        
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH//2
        self.rect.bottom = HEIGHT-self.height//4 + 8
        self.pos = self.rect.center
        
        self.start = pg.time.get_ticks()
        self.update_thres = 100
        self.shooter = shooter
    
    def make_bubble(self,r,c,pos,vec,vel,image):
        self.r = r
        self.c = c
        self.image = image
        self.pos = pos
        self.vec = vec

        self.rect = self.image.get_rect()
        self.rect.x = WIDTH//2
        self.rect.bottom = HEIGHT-self.height//4 + 8
        
        self.rect.x+= self.vec.x*64*2 +16
        self.rect.y+= self.vec.y*64*2 +16
        
        
            
        #self.rect.y = self.y
       
        
        self.vel = vel
        
    
    def change_image(self):
        self.r = rand(0,2)
        self.c = rand(0,2)
        self.image = sheets['bubble'].get_image(self.r,self.c,self.width,self.height)
    
    def update(self):
        now = pg.time.get_ticks()
        t = (pg.time.get_ticks()-self.start)/200
        if self.shooter:
            return 
        
        self.rect.x+= self.vec.x*self.vel*t
        self.rect.y+= self.vec.y*self.vel*t
          
        
        if self.rect.x<=BOUNDARY or self.rect.x>=WIDTH-BOUNDARY-self.width:
            self.game.generate_particles(self.rect.center,self.r,self.c,'circle')
            self.kill()

        if self.rect.y<=0 or self.rect.y>=HEIGHT:
            self.kill()


class Arrow(pg.sprite.Sprite):
    def __init__(self,game):
        super().__init__()
        self.width = 64*3
        self.height = 64*3
        self.image = pg.Surface((self.width,self.height),pg.SRCALPHA)

       
        #self.image.fill((rand(0,255),rand(0,255),rand(0,255)))
        
        

        self.rect = self.image.get_rect()
        

        pg.draw.line(self.image,(209,130,143),(self.width//2,0),(self.width//2,self.height//3),width=4)
        pg.draw.line(self.image,(209,130,143),(self.width//2,0),(self.width//2-16,16),width=6)
        pg.draw.line(self.image,(209,130,143),(self.width//2,0),(self.width//2+16,16),width=6)
        #self.rect.y = self.y
        self.game = game
        self.start = self.rect.center
        
        self.last_update = pg.time.get_ticks()
        self.update_thres = 100
        self.angle = 0
        self.origImage = self.image
        self.origRect = self.rect
        self.rect.center = self.game.shooter.rect.center
        self.direction = vec2(WIDTH//2,0)
        self.position = (WIDTH//2,HEIGHT-self.height*2)

        

    

    def update(self):
        

        
        self.direction = vec2(pg.mouse.get_pos())-vec2(self.origRect.center)
        self.angle = self.direction.angle_to((0,-1))

        self.image = pg.transform.rotate(self.origImage,self.angle)
        self.rect = self.image.get_rect(center=self.origRect.center)
        self.direction = self.direction.normalize()
        


class Particle(pg.sprite.Sprite):
    def __init__(self,pos,r,c,radius,shape):
        super().__init__()
        self.radius = radius
        self.pos = pos
        self.vec = vec2(rand(0,20)/10-1,rand(0,20)/10-1)
        self.last_update = pg.time.get_ticks()
        self.update_thres = 100
        self.shape = shape
        if self.shape=='circle':
            self.color = choice([(255,255,255)]+bubbleColors[r][c])
        if self.shape=='triangle':
            self.color = choice(eggColors[r][c])
        
        if shape=='bomb':
            self.color = choice(bombColors)
            self.shape = choice(['circle','triangle'])

        self.points = choice([[(0,self.radius*2),(self.radius*2,self.radius*2),(self.radius,self.radius)],#straight
                       [(0,0),(self.radius*2,0),(self.radius,self.radius)],#upside down
                       [(0,0),(0,self.radius*2),(self.radius,self.radius)],#right pointing
                       [(self.radius*2,0),(self.radius*2,self.radius*2),(0,self.radius)],#left pointing
                       ])
        self.update_image()
        
    
    def update_image(self):
        self.image = pg.Surface((self.radius*2,self.radius*2),pg.SRCALPHA)
        if self.shape=='circle':
            pg.draw.circle(self.image,self.color,(self.radius,self.radius),self.radius)
        else:
            pg.draw.polygon(self.image,self.color,self.points)
        self.rect = self.image.get_rect()
        self.rect.center = [int(self.pos[0]),int(self.pos[1])]



    def update(self):
        self.radius -=0.1
        if self.radius<=0:
            self.kill()
        
        self.pos+=self.vec
        self.vec+=vec2(rand(-3,3)/10,rand(-3,3)/10)
    
        self.update_image()
        
        
        

class Text(pg.sprite.Sprite):
    def __init__(self,game,msg,x,y,size=12,color=(0,0,0),typ=None):
        super().__init__()
        self.font = pg.font.Font('./Fonts/PrettyPastel-7K2P.ttf',size)
        self.image = self.font.render(msg,True,color)
        self.rect = self.image.get_rect()
        self.center = (x,y)
        self.rect.center = self.center
        self.game = game
        self.type = typ
        self.color = color
        self.size = size

    
    def update(self):
        if self.type == 'score':
            if self.game.score>999 and self.size>36:
                self.font = pg.font.Font('./Fonts/PrettyPastel-7K2P.ttf',36)
                self.size = 36
            self.image = self.font.render("Score:%d"%self.game.score,True,self.color)
            self.rect = self.image.get_rect()
            self.rect.center = self.center

 

class CapturedEgg(pg.sprite.Sprite):
    def __init__(self,bubble,egg,pos):
        super().__init__()
        self.image = pg.Surface((64,64),pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.alpha = 255
        self.rect.center = pos
        self.image.blit(egg,(0,0))
        self.image.blit(bubble,(0,0))
        self.speed = 5
    
    def update(self):
        if self.alpha<=0:
            self.kill()
        
        self.alpha-=self.speed
        self.image.set_alpha(self.alpha)