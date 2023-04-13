from sprites import *
from math import log10
class Game:
    def __init__(self):
        pg.init()
        self.window = pg.display.set_mode((WIDTH,HEIGHT))
        pg.font.init()
        self.clock = pg.time.Clock()
        
        self.weights=[]
        probs={5:8,6:4,7:5,8:4,9:2,10:5,11:3,12:2,13:2,14:1,15:2,90:1}
        for p in probs:
            for i in range(probs[p]):
                self.weights.append(p)
       
        self.life = pg.image.load('./Images/life.png').convert_alpha()
        self.bomb = pg.image.load('./Images/bomb.png').convert_alpha()
        self.bg = pg.image.load('./Images/bg.png').convert_alpha()
        self.refresh()


    def refresh(self):
        self.running = True
        self.eggs = pg.sprite.Group()
        self.bubbles = pg.sprite.Group()
        self.particles = pg.sprite.Group()
        self.fonts = pg.sprite.Group()
        self.shooter = Bubble(self,True)
        self.arrow = Arrow(self)
        self.last_clicked = pg.time.get_ticks()
        self.click_thres = 100
        self.score = 0
        self.lives = 20
        self.finish = False
        self.start = pg.time.get_ticks()
    

    def lose_life(self):
        self.lives=max(0,self.lives-1)
        if self.lives==0:
            self.game_over()

    def game_over(self):
        self.running = False
        self.finish = True
        self.fonts.add(Text(self,'GAME OVER',(WIDTH-len('GAME OVER'))//2,(HEIGHT-72)//2-64,72,(209,177,130)))
        self.fonts.add(Text(self,'Press a key to play again',(WIDTH-len('Press a key to play again'))//2,(HEIGHT-72)//2,36,(209,177,130)))
        
        while self.finish:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
            
                if event.type == pg.KEYDOWN:
                    self.finish = False
                    self.running = True
                    self.refresh()
                    self.run()
        
            self.window.fill(1)
            self.draw()
            pg.display.update()
            self.clock.tick(60)


    def draw(self):
        self.window.blit(self.bg,(0,0))
        
        self.eggs.update()
        self.eggs.draw(self.window)

        self.arrow.update()
        self.window.blit(self.arrow.image,self.arrow.rect)

        self.bubbles.update()
        self.bubbles.draw(self.window)

        self.particles.update()
        self.particles.draw(self.window)

        self.shooter.update()
        self.window.blit(self.shooter.image,self.shooter.rect)

        self.fonts.update()
        self.fonts.draw(self.window)

        
        self.draw_lives()
    
    def draw_lives(self):
        x = BOUNDARY//2
        y = 64
        for i in range(min(self.lives,10)):
            self.window.blit(self.life,(x,y))
            y+=64
        
        x = WIDTH-BOUNDARY//2
        y = 64
        for i in range(max(0,self.lives-10)):
            self.window.blit(self.life,(x,y))
            y+=64

    def check_events(self):
        now = pg.time.get_ticks()

        if pg.mouse.get_pressed()[0] and now-self.last_clicked >self.click_thres:
            #Mouse clicked
            b = Bubble(self)
            b.make_bubble(self.shooter.r,self.shooter.c,self.shooter.pos,self.arrow.direction,rand(7,20)/10,self.shooter.image)
            self.bubbles.add(b)
            self.shooter.change_image()
            self.last_clicked = now
        
        hits = pg.sprite.groupcollide(self.bubbles,self.eggs,False,False)
        for bubble in hits:
            for egg in hits[bubble]:
                if egg.type == 'Life':
                    self.lives = min(self.lives+1,20)
                elif egg.type == 'Bomb':
                    self.generate_particles(egg.rect.center,0,0,'bomb')
                    self.lives = max(0,self.lives-1)
                else:
                    self.score+=1
                    self.particles.add(CapturedEgg(bubble.image,egg.image,egg.rect.center))
                bubble.kill()
                egg.kill()
                if self.lives==0:
                    self.game_over()
                
        
        

    def spawn_eggs(self):
        r = rand(0,100)
        
        if r<choice(self.weights):
            egg = Egg(self,rand(0,3),rand(0,2),rand(1,8)/10)
            self.eggs.add(egg)
        
        now = pg.time.get_ticks()

        if r<2 and now-self.start>2000:
            self.start = now
            self.eggs.add(Egg(self,rand(0,3),rand(0,2),rand(1,8)/10,choice(['Life','Bomb'])))
        
        
    

    def generate_particles(self,pos,r,c,shape):
        r1 = rand(10,50) if shape!='bomb' else rand(20,50)
        r2 = rand(4,18) if shape!='bomb' else rand(8,16)

        for i in range(r1):
            self.particles.add(Particle(pos,r,c,r2,shape))
        

    def run(self):

        self.fonts.add(Text(self,'Score:999',WIDTH-BOUNDARY//2,32,48,(121,118,153),'score'))
        
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
            
            self.spawn_eggs()
            self.check_events()
            self.window.fill(1)
            self.draw()
            pg.display.update()
            self.clock.tick(60)



game = Game()
game.run()