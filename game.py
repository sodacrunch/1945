# 1945
# Version 1.0
# Shoot the enemy planes
# Haroon Khalid

import pygame
import random
import sys

# INITIALIZE PYGAME
pygame.init()

# SET WINDOW CAPTION
pygame.display.set_caption("1945")

# SET WINDOW RESOLUTION
resolution = (320, 480)
screen = pygame.display.set_mode(resolution, 0, 32)

# SET UP LISTS
enemies = []
shots = []
explosions = []
players = []
background = []
waters = []

class Animation:
 
    # data = [ [time, image], [time, image], ...]
 
    def __init__(self, repeat, data): 
        self.data = data
        self.cur_frame = 0
        self.ticks = pygame.time.get_ticks()
        self.ticks_remaining = data[0][0]
        self.pos = [0, 0]
        self.frames = (len(self.data) - 1)
        self.repeat = repeat
        self.pause = 0
 
    def draw(self, dest): 
        old_ticks = self.ticks
        self.ticks = pygame.time.get_ticks() 
        tick_difference = self.ticks - old_ticks 
        self.ticks_remaining -= tick_difference
 
        while (self.ticks_remaining <= 0): 
            self.cur_frame += 1
            
            if self.cur_frame > self.frames and self.repeat == 0:
                self.pause = 1
                break
            
            self.cur_frame %= len(self.data) 
            self.ticks_remaining += self.data[self.cur_frame][0]

        if self.pause == 0:
            dest.blit(self.data[self.cur_frame][1], self.pos)

class Player(object):
    def __init__(self):
        self.image = p1_plane_1
        self.rect = self.image.get_rect()
        self.rect.x = 130
        self.rect.y = 350
        self.flying = Animation(1, [[30, p1_plane_1],[30, p1_plane_2], [30, p1_plane_3]])
        self.anim = self.flying
        self.shots = 0
        self.score = 0
        self.hits = 0
        self.lives = 3
        self.bombs = 3
 
    def draw(self, dest): 
        self.anim.pos = self.rect
        self.anim.draw(dest)
 
    def update(self):
        
        #Get the current key state.
        key = pygame.key.get_pressed()
        
        #Move left/right
        if key[pygame.K_LEFT]:
            self.rect.x -= 5
        if key[pygame.K_RIGHT]:
            self.rect.x += 5
        if key[pygame.K_UP]:
            self.rect.y -= 5
        if key[pygame.K_DOWN]:
            self.rect.y += 5 
            
        self.draw(screen)

class Explosion(object):
    def __init__(self,type):
        self.image = explode_1
        self.rect = self.image.get_rect()
        self.exploding = Animation(0, [[50, explode_1],[50, explode_2],[50, explode_3],[50, explode_4],[50, explode_5],[50, explode_6]])
        self.p1_exploding = Animation(0, [[50, p1_explode_1],[50, p1_explode_2],[50, p1_explode_3],[50, p1_explode_4],[50, p1_explode_5],[50, p1_explode_6],[50, p1_explode_7]])
        self.anim = self.exploding
        self.type = type
 
    def draw(self, dest):
        if self.type == 1:
            self.anim = self.p1_exploding
        self.anim.pos = self.rect
        self.anim.draw(dest)
 
    def update(self):
        self.draw(screen)
        
class Enemy(object):
    def __init__(self):
        self.image = e_plane_1
        self.rect = self.image.get_rect()
        self.rect.x = 130
        self.rect.y = 30
        self.flying = Animation(1, [[30, e_plane_1],[30, e_plane_2], [30, e_plane_3]])
        self.anim = self.flying
 
    def draw(self, dest): 
        self.anim.pos = self.rect
        self.anim.draw(dest)
 
    def update(self):
        if self.rect.y > 100 and self.rect.y < 104:
            create_shot(1, self.rect.x, self.rect.y)
        if self.rect.y > 450:
            enemies.remove(self)
            
        self.rect.y += 3
        self.draw(screen)
        
class Water(object):
    def __init__(self):
        self.image = water_bg_ext
        self.x = 0
        self.y = -32
        
    def update(self):
        if self.y > 0:
            self.y = -32
        self.y += 1
        screen.blit(self.image, (self.x, self.y))
        
class Fire(object):
    def __init__(self, type):
        self.image = fire_1
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        self.firing_1 = Animation(1, [[50, fire_1]])
        self.e_firing = Animation(1, [[50, e_shot]])
        self.anim = self.firing_1
        self.type = type
         
    def draw(self, dest): 
        self.anim.pos = self.rect
        self.anim.draw(dest)
 
    def update(self):
        if self.type == 1:
            self.anim = self.e_firing
            self.rect.y += 5
            self.draw(screen)
        else:
            self.rect.y -= 20
            self.draw(screen)
            
class Background(object):
    def __init__(self):
        self.image_1 = background_1
        self.image_2 = background_2
        self.image_3 = background_3
        self.x = 100
        self.y = 100
        self.image = self.image_1
        
    def update(self):
        if self.y > 480:
            background.remove(self)
            create_background()
        self.y += 0.4
        screen.blit(self.image, (self.x, self.y))
        print str(len(background))
               
class Menu(object):
    def __init__(self):
        self.press = Animation(1, [[500, press_start_1],[200, press_start_2]])
        self.anim = self.press
        self.exit = 0
        
    def draw(self, dest): 
        self.anim.pos = (80,250)
        self.anim.draw(dest)
        
    def update(self):
        screen.blit(menu_img, (0,0))
        self.draw(screen)
        pygame.display.flip()
        pygame.time.delay(25)
                
def create_shot(type, x, y):
    if type == 1:
        f = Fire(type)
        f.rect.x = x + 13
        f.rect.y = y + 40
        shots.append(f)
    else:
        f = Fire(type)
        f.rect.x = players[0].rect.x + 17
        f.rect.y = players[0].rect.y - 20
        shots.append(f)
 
def update_shots():
    for f in shots:
        f.update()
        
def update_players():
    for p in players:
        p.update()
        
def create_enemy():
    e = Enemy()
    random.seed()
    e.rect.x = random.randrange(10, 300)
    #e.rect.y = 10    
    e.rect.y = random.randrange(-500, -10)
    enemies.append(e)
 
def update_enemies():
    for e in enemies:
        e.update()           
        
def create_explosion(type, erectx, erecty):
    x = Explosion(type)
    x.rect.x = erectx
    x.rect.y = erecty
    explosions.append(x)
    
def update_explosions():
    for x in explosions:
        if x.exploding.pause == 1:
            explosions.remove(x)
        else:
            x.update()
            
def create_background():
    bg = Background()
    background.append(bg)

def update_background():
    for b in background:
        b.update()
    if len(background) == 0:
        create_background()
        
def create_water():
    w = Water()
    waters.append(w)
def update_water():
    for w in waters:
        w.update()
    if len(waters) == 0:
        create_water()
          
def draw_stats():
    p1_score_text = custom_font.render("PLAYER 1", True, white)
    high_score_text = custom_font.render("HIGH SCORE", True, gold)
    p1_points_text = custom_font.render(str(p1.score), True, light_grey)
    high_score_points = custom_font.render(str(p1.score), True, light_grey)
    p1_bomb_text = custom_font.render(str(p1.bombs), True, light_grey)
    screen.blit(p1_score_text, (10, 5))
    screen.blit(high_score_text, (187, 5))
    screen.blit(p1_points_text, (10, 20))
    screen.blit(high_score_points, (187, 20))
    
    if p1.bombs == 3:
        screen.blit(p1_bomb, (255,455))
        screen.blit(p1_bomb, (275,455))
        screen.blit(p1_bomb, (295,455))
    elif p1.bombs == 2:
        screen.blit(p1_bomb, (275,455))
        screen.blit(p1_bomb, (295,455))
    elif p1.bombs == 1:
        screen.blit(p1_bomb, (295,455))
        
        
    if p1.lives == 3:
        screen.blit(p1_life, (10,455))
        screen.blit(p1_life, (38,455))
        screen.blit(p1_life, (66,455))
    elif p1.lives == 2:
        screen.blit(p1_life, (10,455))
        screen.blit(p1_life, (38,455))
    elif p1.lives == 1:
        screen.blit(p1_life, (10,455))

def check_hit():
    for e in enemies:
        for p in players:
            for f in shots:
                
                if e.rect.colliderect(f.rect):
                    p1.hits += 1
                    p1.score += 100
                    thump_snd.play()
                    create_explosion(0, e.rect.x, e.rect.y)
                    
                    # REMOVE FROM LISTS
                    if e in enemies:
                        enemies.remove(e)
                    if f in shots:
                        shots.remove(f)
                    
                if f.rect.colliderect(p.rect):
                    thump_snd.play()
                    create_explosion(1, p.rect.x, p.rect.y)
                    
                    # REMOVE FROM LISTS
                    if f in shots:
                        shots.remove(f)
                    if p in players:
                        players.remove(p)
                    

# CREATE PLAYER
def create_player():
    print str(len(enemies))
    for e in enemies:
        thump_snd.play()
        create_explosion(0, e.rect.x, e.rect.y)
        if e in enemies:
            enemies.remove(e)
            
    p1 = Player()
    players.append(p1)
                    
# CREATE ENEMIES
def spawn_enemies():
    if len(enemies) < 8:
        create_enemy()
        
def check_plane_hit():
    for e in enemies:
        for p in players:
            if e.rect.colliderect(p.rect):
                thump_snd.play()
                create_explosion(1, p1.rect.x, p1.rect.y)
                create_explosion(0, e.rect.x, e.rect.y)
            
                if e in enemies:
                    enemies.remove(e)
                if p in players:
                    players.remove(p)
                    
# SET UP THE FONT AND COLOR
default_font = pygame.font.get_default_font()
font = pygame.font.SysFont(default_font, 20)
big_font = pygame.font.SysFont(default_font, 26)
custom_font = pygame.font.Font("imagine_font.ttf", 18)
white = (255,255,255)
light_grey = (191,191,191)
gold = (255,215,0)
          
# LOAD GRAPHICS
sprite_sheet_file = '1945_sprite_sheet.png'
sprite_sheet = pygame.image.load(sprite_sheet_file).convert()
sprite_sheet.set_colorkey((0, 67, 171))
p1_plane_1 = sprite_sheet.subsurface(4, 400, 65, 65)
p1_plane_2 = sprite_sheet.subsurface(70, 400, 65, 65)
p1_plane_3 = sprite_sheet.subsurface(136, 400, 65, 65)
e_plane_1 = sprite_sheet.subsurface(202, 466, 32, 32)
e_plane_2 = sprite_sheet.subsurface(235, 466, 32, 32)
e_plane_3 = sprite_sheet.subsurface(268, 466, 32, 32)
explode_1 = sprite_sheet.subsurface(70, 169, 32, 32)
explode_2 = sprite_sheet.subsurface(103, 169, 32, 32) 
explode_3 = sprite_sheet.subsurface(137, 169, 31, 32) # coordinate is off 1 pixel?
explode_4 = sprite_sheet.subsurface(169, 169, 32, 32)
explode_5 = sprite_sheet.subsurface(202, 169, 32, 32)
explode_6 = sprite_sheet.subsurface(235, 169, 32, 32)
p1_explode_1 = sprite_sheet.subsurface(4, 301, 65, 65)
p1_explode_2 = sprite_sheet.subsurface(70, 301, 65, 65)
p1_explode_3 = sprite_sheet.subsurface(136, 301, 65, 65)
p1_explode_4 = sprite_sheet.subsurface(202, 301, 65, 65)
p1_explode_5 = sprite_sheet.subsurface(268, 301, 65, 65)
p1_explode_6 = sprite_sheet.subsurface(334, 301, 65, 65)
p1_explode_7 = sprite_sheet.subsurface(400, 301, 65, 65)
press_start_1 = sprite_sheet.subsurface(414, 544, 158, 22)
press_start_2 = sprite_sheet.subsurface(4, 546, 1, 1)
e_shot = sprite_sheet.subsurface(280, 148, 9, 9)
score = sprite_sheet.subsurface(572, 178, 63, 17)
fire_1 = sprite_sheet.subsurface(37, 169, 32, 32)
p1_bomb = sprite_sheet.subsurface(279, 272, 11, 22)
p1_life = sprite_sheet.subsurface(206, 274, 23, 18)
background_1 = sprite_sheet.subsurface(103, 499, 64, 65)
background_2 = sprite_sheet.subsurface(168, 499, 23, 18)
background_3 = sprite_sheet.subsurface(233, 500, 23, 18)
menu_graphic = 'menu.png'
water_bg = 'waterbgext.png'
water_bg_ext = pygame.image.load(water_bg).convert()
menu_img = pygame.image.load(menu_graphic).convert()
p1_plane_1.set_colorkey((0, 67, 171))
p1_plane_2.set_colorkey((0, 67, 171))
p1_plane_3.set_colorkey((0, 67, 171))
e_plane_1.set_colorkey((0, 67, 171))
e_plane_2.set_colorkey((0, 67, 171))
e_plane_3.set_colorkey((0, 67, 171))
explode_1.set_colorkey((0, 67, 171))
explode_2.set_colorkey((0, 67, 171))
explode_3.set_colorkey((0, 67, 171))
explode_4.set_colorkey((0, 67, 171))
explode_5.set_colorkey((0, 67, 171))
explode_6.set_colorkey((0, 67, 171))
score.set_colorkey((0, 0, 0))
fire_1.set_colorkey((0, 67, 171))
e_shot.set_colorkey((0, 67, 171))

# LOAD SOUNDS
fusion_snd = pygame.mixer.Sound('fusion.ogg')
shot_snd = pygame.mixer.Sound('shot.ogg')
thump_snd = pygame.mixer.Sound('thump.ogg')
cannon_snd = pygame.mixer.Sound('cannon.ogg')
start_snd = pygame.mixer.Sound('start.ogg')
pygame.mixer.music.load('music_1.ogg')
play_musc = 1

            
# CREATE PLAYER
p1 = Player()
players.append(p1)

# CREATE MENU
menu_screen = Menu()
menu_screen.exit = 0


# MAIN MENU LOOP
while menu_screen.exit == 0:
    for event in pygame.event.get():
        key = pygame.key.get_pressed()
    
        if key[pygame.K_RETURN]:
            menu_screen.exit = 1
            start_snd.play()
            break
    menu_screen.update()

# MAIN GAME LOOP
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if len(players) > 0:
                if event.key == pygame.K_SPACE:
                    shot_snd.play()
                    create_shot(0, p1.rect.x, p1.rect.y)
                    p1.shots += 1
                if event.key == pygame.K_LCTRL:
                    p1.bombs -= 1

            if event.key == pygame.K_F1:
                if len(players) == 0:
                    create_player()
                                    

    if play_musc == 1:
        pygame.mixer.music.play()
    play_musc = 0
    screen.fill((0,67,171))
    #update_background()
    update_water()    
    update_players()
    spawn_enemies()
    update_enemies()
    update_shots()
    update_explosions()
    check_hit()
    check_plane_hit()
    draw_stats()
    pygame.display.flip()
    pygame.time.delay(25)
