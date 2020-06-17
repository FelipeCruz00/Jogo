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
        gameIcon = pg.image.load('icone.png')
        pg.display.set_icon(gameIcon)
        self.mx = 0
        self.my = 0
        self.correct_again = False
        self.stack = 1
        self.atual = 0
        self.seta = Button("go_back.png", 160, 160, (200,200))
        self.choice = ""
        self.ans1 = pg.Rect(0,125,400,50)
        self.ans2 = pg.Rect(0,200,400,50)
        self.ans3 = pg.Rect(0,275,400,50)
        self.ans4 = pg.Rect(0,350,400,50)
        self.mus = pg.Rect(200,300,320,320)
        self.back = pg.Rect(0,0,32,32)
        self.jump_sound = pg.mixer.Sound("jump.wav")
        self.game_music = pg.mixer.Sound("music.wav")
        self.correct_choice = pg.mixer.Sound("correct_answer.wav")
        self.wrong_choice = pg.mixer.Sound("wrong_answer.wav")
        self.game_music.set_volume(0.4)
        self.game_music.play(-1)
        self.background_image = pg.image.load("background.png").convert()
        self.clock = pg.time.Clock()
        self.running = True
        self.sound = True
        self.score = 0
        self.load_hs()
        self.load_data()

    def load_hs(self):
        # load high score
        with open("highscore.txt", 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
    
    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.boss_group = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.mob = Entity(self, 20, 40)
        self.all_sprites.add(self.mob)
        self.mob.add(self.mobs)
        self.boss = Boss(self)
        self.boss_group.add(self.boss)
        self.p1 = Platform(self, 0, HEIGHT - 60, "grass1.png")
        self.all_sprites.add(self.p1)
        self.platforms.add(self.p1)
        self.game = True
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
        # Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            lowest = hits[0]
            for hit in hits:
                if hit.rect.bottom > lowest.rect.bottom:
                    lowest = hit
            if self.player.pos.y < lowest.rect.centery:
                self.player.pos.y = lowest.rect.top
                self.player.vel.y = 1
                self.player.jumping = False
        if pg.sprite.spritecollide(self.player, self.mobs, False) and not self.player.locked and self.player.pos.x > 620:
            self.player.locked = True
        if pg.sprite.spritecollide(self.player, self.boss_group, False) and not self.player.locked and self.player.pos.x > 600:
            self.player.locked = True

    def events(self):
        # game loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT or self.player.fase > 3:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN and not self.player.locked:
                if event.key == pg.K_UP:
                    if self.sound:
                        self.jump_sound.play()
                    self.player.jump()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and not (self.player.fase >= 0 or self.player.fase <= 3):
                    if self.seta.rect.collidepoint(pg.mouse.get_pos()):
                        self.show_start_screen()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.player.locked:
                if self.ans1.collidepoint(pg.mouse.get_pos()):
                    self.choice = "A"
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.player.locked:
                if self.ans2.collidepoint(pg.mouse.get_pos()):
                    self.choice = "B"
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.player.locked:
                if self.ans3.collidepoint(pg.mouse.get_pos()):
                    self.choice = "C"
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.player.locked:
                if self.ans4.collidepoint(pg.mouse.get_pos()):
                    self.choice = "D"
            if self.choice == CORRECT[self.player.q - 1] and event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.sound:
                self.correct_choice.play()
            if self.choice != CORRECT[self.player.q - 1] and event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.sound:
                self.wrong_choice.play()
    
    def load_data(self):
        # load spritesheet
        self.spritesheet = Spritesheet(SPRITESHEET)
        self.inimigo = Spritesheet("inimigo.png")
        self.boss_spritesheet = Spritesheet("boss.png")
    
    def draw(self):
        # game loop - draw
        font = pg.font.Font("pixeboy.ttf", 32)
        if self.player.fase == 0:
            self.background_image = pg.image.load("bg_fase1.png").convert()
            self.background_image = pg.transform.scale( self.background_image, (800, 600))
        if self.player.fase == 1:
            self.background_image = pg.image.load("bg_fase2.png").convert()  
            self.background_image = pg.transform.scale( self.background_image, (800, 600))
            self.p1.image = pg.image.load("grass2.png").convert()  
            self.p1.image.set_colorkey(WHITE)
        if self.player.fase == 2:
            self.background_image = pg.image.load("bg_fase3.png").convert()
            self.background_image = pg.transform.scale( self.background_image, (800, 600))
            self.p1.image = pg.image.load("grass3.png").convert()  
            if pg.sprite.spritecollide(self.player, self.mobs, False) and self.mob.dead and self.mob.stop:
                pg.sprite.spritecollide(self.player, self.mobs, True)
        if self.player.fase == 3:
            self.background_image = pg.image.load("bg_fase4.png").convert()
            self.background_image = pg.transform.scale(self.background_image, (800, 600))
            self.p1.image = pg.image.load("grass4.png").convert() 
            self.p1.image.set_colorkey(WHITE) 
        self.screen.blit(self.background_image, [0, 0])
        self.check_update()
        self.all_sprites.draw(self.screen)
        hs = font.render("Pontuacao: " + str(self.score), False, WHITE)
        self.screen.blit(hs,(320,10))
        if self.player.locked:
            self.combat()
        # after drawing everything, flip the display
        pg.display.flip()
    
    def draw_text(self):
        font = pg.font.Font("pixeboy.ttf", 22)
        if self.player.fase == 3 or self.player.fase == 2:
            question = font.render(Q[self.player.q - 1], False, WHITE)
            anws1 = font.render(A[self.player.q - 1], False, WHITE)
            anws2 = font.render(B[self.player.q - 1], False, WHITE)
            anws3 = font.render(C[self.player.q - 1], False, WHITE)
            anws4 = font.render(D[self.player.q - 1], False, WHITE)
        else:
            question = font.render(Q[self.player.q - 1], False, BLACK)
            anws1 = font.render(A[self.player.q - 1], False, BLACK)
            anws2 = font.render(B[self.player.q - 1], False, BLACK)
            anws3 = font.render(C[self.player.q - 1], False, BLACK)
            anws4 = font.render(D[self.player.q - 1], False, BLACK)
        if self.player.fase != 3 and not self.mob.dead and not self.player.dead:
            mob = font.render("Vida: " + str(self.mob.life), False, RED)
            self.screen.blit(mob,(690, HEIGHT -180))
            life = font.render("Vida: " + str(self.player.life), False, RED)
            self.screen.blit(life,(615,HEIGHT -160))
        if self.player.fase == 3 and not self.boss.dead and not self.player.dead:
            boss = font.render("Vida: " + str(self.boss.life), False, RED)
            self.screen.blit(boss,(690, HEIGHT -220))
            life = font.render("Vida: " + str(self.player.life), False, RED)
            self.screen.blit(life,(590, HEIGHT -160))
        self.screen.blit(question,(10,72))
        self.screen.blit(anws1,(10,147))
        self.screen.blit(anws2,(10,222))
        self.screen.blit(anws3,(10,297))
        self.screen.blit(anws4,(10,372))

    def combat(self):
        self.draw_text()
        if CORRECT[self.player.q - 1] == "A":
            if self.choice == "A":
                if self.player.fase == 3:
                    self.player.attacking = True
                    self.boss.damage = True
                    self.player.q += 1
                    self.boss.life -= self.player.atk_dmg + 20
                    self.correct_again = True
                    self.score += 100
                else:
                    self.player.attacking = True
                    self.mob.damage = True
                    self.player.q += 1
                    self.mob.life -= self.player.atk_dmg
                    self.score += 100
            if self.choice == "B" or self.choice == "C" or self.choice == "D":
                self.player.wrong += 1
        if CORRECT[self.player.q - 1] == "B":
            if self.choice == "B":
                if self.player.fase == 3:
                    self.player.attacking = True
                    self.boss.damage = True
                    self.player.q += 1
                    self.boss.life -= self.player.atk_dmg + 20
                    self.correct_again = True
                    self.score += 100
                else:
                    self.player.attacking = True
                    self.mob.damage = True
                    self.player.q += 1
                    self.mob.life -= self.player.atk_dmg
                    self.score += 100
            if self.choice == "A" or self.choice == "C" or self.choice == "D":
                self.player.wrong += 1
        if CORRECT[self.player.q - 1] == "C":
            if self.choice == "C":
                if self.player.fase == 3:
                    self.player.attacking = True
                    self.boss.damage = True
                    self.player.q += 1
                    self.boss.life -= self.player.atk_dmg + 20
                    self.correct_again = True
                    self.score += 100
                else:
                    self.player.attacking = True
                    self.mob.damage = True
                    self.player.q += 1
                    self.mob.life -= self.player.atk_dmg
                    self.score += 100
            if self.choice == "B" or self.choice == "A" or self.choice == "D":
                self.player.wrong += 1
        if CORRECT[self.player.q - 1] == "D":
            if self.choice == "D":
                if self.player.fase == 3:
                    self.player.attacking = True
                    self.boss.damage = True
                    self.player.q += 1
                    self.boss.life -= self.player.atk_dmg + 20
                    self.correct_again = True
                    self.score += 100
                else:
                    self.player.attacking = True
                    self.mob.damage = True
                    self.player.q += 1
                    self.mob.life -= self.player.atk_dmg
                    self.score += 100
            if self.choice == "B" or self.choice == "A" or self.choice == "C":
                self.player.wrong += 1
        self.choice = ""
        if self.player.q == 14:
            self.player.q = 1
        if self.player.wrong == 3 and not self.player.fase == 3:
            self.mob.attacking = True
            self.player.damage = True
            self.player.life -= self.mob.atk_dmg
            self.player.wrong = 0
        if self.player.wrong == 3 and self.player.fase == 3:
            self.boss.attacking = True
            self.player.damage = True
            self.player.life -= self.boss.atk_dmg
            self.player.wrong = 0
        if self.player.life <= 0 and not self.player.fase == 3:
            self.player.damage = False
            self.player.dead = True
            self.mob.life = 20
        if self.player.life <= 0 and self.player.fase == 3:
            self.player.damage = False
            self.player.dead = True
            self.boss.life = 120
        if self.mob.life <= 0:
            self.mob.dead = True
            self.player.locked = False
        if self.boss.life <= 0:
            self.boss.dead = True
            self.player.locked = False

    def check_update(self):
        if self.atual != self.player.fase:
            self.mob.life = 20
            self.mob.dead = False
            self.mob.idle = True
            self.atual += 1
            self.player.wrong = 0
        if self.player.fase == 3 and not self.all_sprites.has(self.boss):
            self.all_sprites.add(self.boss)
            self.game_music.stop()
            self.game_music = pg.mixer.Sound("boss_music.wav")
            if self.sound:
                self.game_music.play(-1)
        
    
    def show_start_screen(self):
        # game splash/start screen'
        start = True
        but = Button("bt1.png", 700, 100, (400,70))
        but2 = Button("bt2.png", 150, 50, (400,160))
        but3 = Button("bt3.png", 150, 50, (400,230))
        but4 = Button("bt4.png", 150, 50, (400,300))
        while start:
            self.screen.blit(self.background_image, [0, 0])
            but.render(self.screen)
            but2.render(self.screen)
            but3.render(self.screen)
            but4.render(self.screen)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if but2.rect.collidepoint(pg.mouse.get_pos()):
                        start = False
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if but3.rect.collidepoint(pg.mouse.get_pos()):
                        self.show_options_screen()
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if but4.rect.collidepoint(pg.mouse.get_pos()):
                        self.show_rank_screen()
            pg.display.flip()
    
    def show_options_screen(self):
        start = True
        sound = True
        self.seta = Button("go_back.png", 160, 160, (200,200))
        sound_on = Button("sound_on.png", 160, 160, (400,200))
        sound_off = Button("sound_off.png", 160, 160, (600,200))
        while start:
            self.screen.blit(self.background_image, [0, 0])
            sound_on.render(self.screen)
            sound_off.render(self.screen)
            self.seta.render(self.screen)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if sound_on.rect.collidepoint(pg.mouse.get_pos()):
                        self.sound = True
                        self.game_music.play(-1)
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if sound_off.rect.collidepoint(pg.mouse.get_pos()):
                        self.sound = False
                        self.game_music.stop()
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if self.seta.rect.collidepoint(pg.mouse.get_pos()):
                        start = False
            pg.display.flip()
    
    def show_rank_screen(self):
        font = pg.font.Font("pixeboy.ttf", 60)
        start = True
        self.seta = Button("go_back.png", 32, 32, (16,16))
        fundo = pg.image.load("hs.png").convert()
        while start:
            self.screen.blit(self.background_image, [0, 0])
            self.seta.render(self.screen)
            self.screen.blit(fundo, (20,240))
            hs = font.render("Pontuacao maxima: " + str(self.highscore), False, BLACK)
            self.screen.blit(hs,(45,285))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if self.seta.rect.collidepoint(pg.mouse.get_pos()):
                        start = False
            pg.display.flip()

    def show_go_screen(self):
        if self.score > self.highscore:
            self.highscore = self.score
            with open("highscore.txt", 'w') as f:
                f.write(str(self.score))
        font = pg.font.Font("pixeboy.ttf", 40)
        self.game_music.stop()
        end = False
        self.background_image = pg.image.load("end_scene.png").convert()
        self.background_image = pg.transform.scale(self.background_image, (800,600))
        title = font.render("Obrigado por jogar nosso jogo!", False, WHITE)
        while not end:
            self.screen.blit(self.background_image, [0, 0])
            self.screen.blit(title,(143,270))
            end = True
            pg.display.flip()
        pg.time.wait(5000)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
g.show_go_screen()

pg.quit()