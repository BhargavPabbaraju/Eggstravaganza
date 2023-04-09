from sprites import *

class Game:
    def __init__(self):
        
        self.window = pg.display.set_mode((WIDTH,HEIGHT))
        self.clock = pg.time.Clock()
        self.refresh()


    def refresh(self):
        self.running = True
        self.eggs = pg.sprite.Group()
        self.bubbles = pg.sprite.Group()
        self.score = 0
        self.currentEggs =0
        #self.maxEggs = 100
        self.shooter = Bubble(self)
        self.arrow = Arrow(self)


    def draw(self):
        
        #self.all_sprites.update()
        #self.all_sprites.draw(self.window)
        self.bubbles.update()
        self.bubbles.draw(self.window)
        self.eggs.update()
        self.eggs.draw(self.window)
        self.shooter.update()
        self.window.blit(self.shooter.image,self.shooter.rect)


    def check_events(self):
        pass

    def spawn_eggs(self):
        r = rand(1,100)
        if r < 2:
            egg = Egg(self)
            self.eggs.add(egg)
            self.currentEggs+=1
            

    def run(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
            
            self.spawn_eggs()
            self.check_events()
            self.window.fill(-1)
            self.draw()
            pg.display.update()



game = Game()
game.run()