from sprites import *

class Game:
    def __init__(self):
        pg.init()
        self.window = pg.display.set_mode((WIDTH,HEIGHT))
        pg.font.init()
        self.clock = pg.time.Clock()
        self.bg = pg.image.load('./Images/bg.png').convert_alpha()
        self.refresh()


    def refresh(self):
        self.running = True
        self.eggs = pg.sprite.Group()
        self.bubbles = pg.sprite.Group()
        self.particles = pg.sprite.Group()
        self.fonts = pg.sprite.Group()
        self.score = 0
        self.currentEggs =0
        #self.maxEggs = 100
        self.shooter = Bubble(self,True)
        self.arrow = Arrow(self)
        self.last_clicked = pg.time.get_ticks()
        self.click_thres = 200
        self.score = 0
        self.lives = 20
        self.life = Life()
        self.finish = False
    

    def lose_life(self):
        self.lives=max(0,self.lives-1)
        if self.lives==0:
            self.game_over()

    def game_over(self):
        self.running = False
        self.finish = True
        self.fonts.add(Text(self,'GAME OVER',(WIDTH-len('GAME OVER'))//2,(HEIGHT-72)//2,72,(209,177,130)))
        
        while self.finish:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
            
           
            self.check_events()
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
            self.window.blit(self.life.image,(x,y))
            y+=64
        
        x = WIDTH-BOUNDARY//2
        y = 64
        for i in range(max(0,self.lives-10)):
            self.window.blit(self.life.image,(x,y))
            y+=64

    def check_events(self):
        now = pg.time.get_ticks()

        if not self.running:
            return
        if pg.mouse.get_pressed()[0] and now-self.last_clicked >self.click_thres:
            #Mouse clicked
            b = Bubble(self)
            b.make_bubble(self.shooter.r,self.shooter.c,self.shooter.pos,self.arrow.direction,rand(1,20)/10,self.shooter.image)
            self.bubbles.add(b)
            self.shooter.change_image()
            self.last_clicked = now
        
        hits = pg.sprite.groupcollide(self.bubbles,self.eggs,False,False)
        for bubble in hits:
            for egg in hits[bubble]:
            #bubble.kill()
                egg.kill()
                self.score+=1
        
        

    def spawn_eggs(self):
        r = rand(1,100)
        if r < 5:
            egg = Egg(self,rand(0,3),rand(0,2),rand(1,8)/10)
            self.eggs.add(egg)
            self.currentEggs+=1
    

    def generate_particles(self,pos,r,c,shape):
        for i in range(rand(5,20)):
            self.particles.add(Particle(pos,r,c,rand(2,18),shape))

    def run(self):

        self.fonts.add(Text(self,'Score:999',WIDTH-BOUNDARY//2,32,32,(121,118,153),'score'))
        
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