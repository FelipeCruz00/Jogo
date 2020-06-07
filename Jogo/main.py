# Search of the Sword - Platformer game
import pygame as pg
import random
import os
from settings import *
from sprites import *
from os import path

class Game:
    def __init__(self):
        #initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        gameIcon = pg.image.load('data/images/icone.png')
        pg.display.set_icon(gameIcon)
        self.background_image = pg.image.load("background.png").convert()
        self.clock = pg.time.Clock()
        self.running = True

    #def load_data(self):
        #load high score
        #self.dir = path.dirname(__file__)
        #with open(path.join(self.dir, HS_FILE), 'w') as f:

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()
    
    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # game loop - update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                if self.player.pos.y < hits[0].rect.bottom:
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = 0

    def events(self):
        # game loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.player.jump()
    
    def draw(self):
        # game loop - draw
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        # after drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen'
        start = True
        but = Button("bt1.png", 700, 100, (400,70))
        but2 = Button("bt2.png", 150, 50, (400,160))
        but3 = Button("bt3.png", 150, 50, (400,220))
        while start:
            self.screen.blit(self.background_image, [0, 0])
            but.render(self.screen)
            but2.render(self.screen)
            but3.render(self.screen)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if but2.rect.collidepoint(pg.mouse.get_pos()):
                        start = False
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if but3.rect.collidepoint(pg.mouse.get_pos()):
                        show_options_screen()
            pg.display.flip()
    
    def show_options_screen(self):
        start = True
        while start:
            self.screen.blit(self.background_image, [0, 0])
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if but2.rect.collidepoint(pg.mouse.get_pos()):
                        start = False
            pg.display.flip()

    def show_go_screen(self):
        # game over/continue
        pass
    
g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()