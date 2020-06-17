# Sprite classes for platform game
from settings import *
import pygame as pg
vec = pg.math.Vector2

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.set_colorkey(BLACK)
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (125, 100))
        return image
    def get_image2(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.set_colorkey(BLACK)
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (250, 200))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.sync = False
        self.OnTheRight = True
        self.locked = False
        self.damage = False
        self.dead = False
        self.attacking = False
        self.walking = False
        self.fase = 0
        self.life = 100
        self.atk_dmg = 10
        self.wrong = 0
        self.q = 1
        self.idle = True
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.idle_frames_r[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(36, HEIGHT -60)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self):
        self.idle_frames_r = [self.game.spritesheet.get_image(185, 146, 50, 36),
                            self.game.spritesheet.get_image(245, 146, 50, 36),
                            self.game.spritesheet.get_image(5, 193, 50, 36),
                            self.game.spritesheet.get_image(65, 193, 50, 36)]
        self.walking_r = [self.game.spritesheet.get_image(65, 240, 50, 36),
                            self.game.spritesheet.get_image(185, 240, 50, 36),
                            self.game.spritesheet.get_image(5, 287, 50, 36),
                            self.game.spritesheet.get_image(125, 287, 50, 36),
                            self.game.spritesheet.get_image(245, 287, 50, 36),
                            self.game.spritesheet.get_image(305, 52, 50, 36)]
        self.atck = [self.game.spritesheet.get_image(5, 5, 50, 36),
                            self.game.spritesheet.get_image(65, 5, 50, 36),
                            self.game.spritesheet.get_image(125, 5, 50, 36),
                            self.game.spritesheet.get_image(185, 5, 50, 36),
                            self.game.spritesheet.get_image(245, 5, 50, 36),
                            self.game.spritesheet.get_image(5, 52, 50, 36)]
        self.walking_l = []
        for frame in self.walking_r:
            frame.set_colorkey(BLACK)
            self.walking_l.append(pg.transform.flip(frame, True, False))
        self.idle_frames_l = []
        self.hit = [self.game.spritesheet.get_image(5, 146, 50, 36),
                    self.game.spritesheet.get_image(65, 146, 50, 36),
                    self.game.spritesheet.get_image(125, 146, 50, 36)]
        self.death = [self.game.spritesheet.get_image(65, 52, 50, 36),
                            self.game.spritesheet.get_image(125, 52, 50, 36),
                            self.game.spritesheet.get_image(185, 52, 50, 36),
                            self.game.spritesheet.get_image(245, 52, 50, 36),
                            self.game.spritesheet.get_image(5, 99, 50, 36),
                            self.game.spritesheet.get_image(65, 99, 50, 36),
                            self.game.spritesheet.get_image(125, 99, 50, 36)]
        for frame in self.idle_frames_r:
            frame.set_colorkey(BLACK)
            self.idle_frames_l.append(pg.transform.flip(frame, True, False))

    def jump(self):
        # jump only if standing on a platform
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and not self.locked:
            self.acc.x = -PLAYER_ACC
            self.OnTheRight = False
        if keys[pg.K_RIGHT] and not self.locked:
            self.acc.x = PLAYER_ACC
            self.OnTheRight = True

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.fase += 1
            if self.fase < 4:
                self.pos.x = 36
        if self.pos.x < 20:
            self.pos.x = 20

        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        # show walk animation
        if self.walking:
            if now - self.last_update > 150:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walking_r[self.current_frame]
                else:
                    self.image = self.walking_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # show idle animation
        if not self.jumping and not self.walking and not self.attacking:
            if now - self.last_update > 150:
                if self.OnTheRight:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.idle_frames_r)
                    bottom = self.rect.bottom
                    self.image = self.idle_frames_r[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
                else:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.idle_frames_l)
                    bottom = self.rect.bottom
                    self.image = self.idle_frames_l[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom 
        if self.attacking:
            if not self.sync:
                self.current_frame = -1
                self.sync = True 
            if now - self.last_update > 50:
                self.idle = False
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.atck)
                bottom = self.rect.bottom
                self.image = self.atck[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                if self.current_frame == 5:
                    self.attacking = False
                    self.idle = True
                    self.sync = False
        if self.locked:
                if self.idle:
                    if now - self.last_update > 150:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.idle_frames_r)
                        bottom = self.rect.bottom
                        self.image = self.idle_frames_r[self.current_frame]
                        self.rect = self.image.get_rect()
                        self.rect.bottom = bottom
                if self.damage:
                    if not self.sync:
                        self.current_frame = -1
                        self.sync = True 
                    if now - self.last_update > 100:
                        self.idle = False
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.hit)
                        bottom = self.rect.bottom
                        self.image = self.hit[self.current_frame]
                        self.rect = self.image.get_rect()
                        self.rect.bottom = bottom
                        if self.current_frame == 2:
                            self.damage = False
                            self.idle = True
                            self.sync = False
                if self.dead: 
                    if not self.sync:
                        self.current_frame = -1
                        self.sync = True 
                    if now - self.last_update > 100:
                        self.idle = False
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.death)
                        bottom = self.rect.bottom
                        self.image = self.death[self.current_frame]
                        self.rect = self.image.get_rect()
                        self.rect.bottom = bottom
                        if self.current_frame == 6:
                            self.dead = False
                            self.locked = False
                            self.pos = vec(36, HEIGHT -60)
                            self.idle = True
                            self.sync = False
                            self.life = 100

class Entity(pg.sprite.Sprite):
    def __init__(self, game, life, at):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.stop = True
        self.life = life
        self.atk_dmg = at
        self.damage = False
        self.sync = False
        self.idle = True
        self.dead = False
        self.attacking = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.idle_frames[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(720, HEIGHT -40)

    def load_images(self):
        self.i = [self.game.inimigo.get_image2(5, 365, 100, 80),
                            self.game.inimigo.get_image2(115, 365, 100, 80),
                            self.game.inimigo.get_image2(225, 365, 100, 80),
                            self.game.inimigo.get_image2(335, 95, 100, 80),
                            self.game.inimigo.get_image2(335, 185, 100, 80),
                            self.game.inimigo.get_image2(335, 275, 100, 80)]
        self.idle_frames = []
        for frame in self.i:
            frame.set_colorkey(BLACK)
            self.idle_frames.append(pg.transform.flip(frame, True, False))
        self.h = [self.game.inimigo.get_image2(115, 275, 100, 80),
                    self.game.inimigo.get_image2(225, 275, 100, 80),
                    self.game.inimigo.get_image2(335, 5, 100, 80)]
        self.hit = []
        for frame in self.h:
            frame.set_colorkey(BLACK)
            self.hit.append(pg.transform.flip(frame, True, False))
        self.d = [self.game.inimigo.get_image2(5, 185, 100, 80),
                     self.game.inimigo.get_image2(115, 185, 100, 80),
                     self.game.inimigo.get_image2(5, 275, 100, 80)]
        self.death = []
        for frame in self.d:
            frame.set_colorkey(BLACK)
            self.death.append(pg.transform.flip(frame, True, False))
        self.a = [self.game.inimigo.get_image2(5, 5, 100, 80),
                       self.game.inimigo.get_image2(115, 5, 100, 80),
                       self.game.inimigo.get_image2(225, 5, 100, 80),
                       self.game.inimigo.get_image2(5, 95, 100, 80),
                       self.game.inimigo.get_image2(115, 95, 100, 80),
                       self.game.inimigo.get_image2(225, 95, 100, 80)]
        self.attack = []
        for frame in self.a:
            frame.set_colorkey(BLACK)
            self.attack.append(pg.transform.flip(frame, True, False))

    def update(self):
        self.animate()

        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        # show idle animation
        if not self.dead and self.stop:
            if self.idle:
                if now - self.last_update > 150:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                        bottom = self.rect.bottom
                        self.image = self.idle_frames[self.current_frame]
                        self.rect = self.image.get_rect()
                        self.rect.bottom = bottom
            if self.attacking:
                if not self.sync:
                    self.current_frame = -1
                    self.sync = True 
                if now - self.last_update > 50:
                    self.idle = False
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.attack)
                    bottom = self.rect.bottom
                    self.image = self.attack[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
                    if self.current_frame == 5:
                        self.attacking = False
                        self.idle = True
                        self.sync = False
            if self.damage:
                if not self.sync:
                    self.current_frame = -1
                    self.sync = True 
                if now - self.last_update > 100:
                    self.idle = False
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.hit)
                    bottom = self.rect.bottom
                    self.image = self.hit[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
                    if self.current_frame == 2:
                        self.damage = False
                        self.idle = True
                        self.sync = False
        if self.dead:
            if not self.sync:
                self.current_frame = -1
                self.sync = True 
                self.stop = False
            if self.stop == False:
                if now - self.last_update > 100:
                    self.idle = False
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.death)
                    bottom = self.rect.bottom
                    self.image = self.death[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
                    if self.current_frame == 2:
                        self.stop = True

class Boss(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.stop = True
        self.life = 120
        self.atk_dmg = 60
        self.damage = False
        self.sync = False
        self.idle = True
        self.dead = False
        self.attacking = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.idle_frames[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(720, HEIGHT -40)

    def load_images(self):
        self.idle_frames = [self.game.boss_spritesheet.get_image2(121, 121, 48, 48),
                            self.game.boss_spritesheet.get_image2(179, 5, 48, 48),
                            self.game.boss_spritesheet.get_image2(179, 63, 48, 48),
                            self.game.boss_spritesheet.get_image2(179, 121, 48, 48)]
        self.hitt = [self.game.boss_spritesheet.get_image2(63, 179, 48, 48),
                    self.game.boss_spritesheet.get_image2(121, 179, 48, 48)]
        self.deathh = [self.game.boss_spritesheet.get_image2(5, 179, 48, 48)]
        self.attack = [self.game.boss_spritesheet.get_image2(5, 63, 48, 48),
                       self.game.boss_spritesheet.get_image2(63, 63, 48, 48),
                       self.game.boss_spritesheet.get_image2(121, 63, 48, 48),
                       self.game.boss_spritesheet.get_image2(5, 121, 48, 48),
                       self.game.boss_spritesheet.get_image2(63, 121, 48, 48)]

    def update(self):
        self.animate()

        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        # show idle animation
        if not self.dead and self.stop:
            if self.idle:
                if now - self.last_update > 150:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                        bottom = self.rect.bottom
                        self.image = self.idle_frames[self.current_frame]
                        self.rect = self.image.get_rect()
                        self.rect.bottom = bottom
            if self.attacking:
                if not self.sync:
                    self.current_frame = -1
                    self.sync = True 
                if now - self.last_update > 50:
                    self.idle = False
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.attack)
                    bottom = self.rect.bottom
                    self.image = self.attack[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
                    if self.current_frame == 4:
                        self.attacking = False
                        self.idle = True
                        self.sync = False
            if self.damage:
                if not self.sync:
                    self.current_frame = -1
                    self.sync = True 
                if now - self.last_update > 50:
                    self.idle = False
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.hitt)
                    bottom = self.rect.bottom
                    self.image = self.hitt[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
                    if self.current_frame == 1:
                        self.damage = False
                        self.idle = True
                        self.sync = False
        if self.dead:
            if not self.sync:
                self.current_frame = -1
                self.sync = True 
                self.stop = False
            if self.stop == False:
                if now - self.last_update > 5:
                    self.idle = False
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.deathh)
                    bottom = self.rect.bottom
                    self.image = self.deathh[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
                    self.stop = True

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, image):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load(image).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class Button:
    def __init__(self, image, w, h, dest):
        self.image = pg.image.load(image).convert()
        self.image = pg.transform.scale(self.image, (w,h))
        self.rect = self.image.get_rect()
        self.rect.center = dest
    def render(self, screen):
        screen.blit(self.image, self.rect)