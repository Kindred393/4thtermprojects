import pygame as pg
import random as r
import math
from os import *

#Attribution
####################################################################
# Code created by: Eric Broadbent
# Art Work Credit: "Kenney.nl" @ "www.kenney.nl"
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder>
# licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>

####################################################################



# Game object classes
####################################################################

class Player(pg.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.sheild = 100
        # self.image = pg.Surface((50,40))
        # self.image.fill(GREEN)
        self.image = player_img
        self.image = pg.transform.scale(player_img,(60,48))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = self.rect.width*.85 / 2
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = (WIDTH/2)
        self.rect.bottom = (HEIGHT - (HEIGHT*.05))
        self.speedx = 0
        self.shoot_delay = 250
        self.last_shot = pg.time.get_ticks()
        self.lives = 3
        self.hide_timer = pg.time.get_ticks()
        self.hidden = False

    def hide(self):
        # hide the player temporarily
        self.lives -= 1
        self.hidden = True
        self.hide_timer = pg.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)



    def update(self):
        # unhide if hidden
        if self.hidden and (pg.time.get_ticks() - self.hide_timer >3000):
            self.hidden = False
            self.rect.bottom = (HEIGHT - (HEIGHT*.05))
            self.rect.centerx = (WIDTH / 2)
            self.sheild = 100

        # basic movment side to side
        if keyboard:
            self.speedx = 0
            keystate = pg.key.get_pressed()
            if keystate[pg.K_LEFT] or keystate[pg.K_a]:
                self.speedx = -5
            if keystate[pg.K_RIGHT] or keystate[pg.K_d]:
                self.speedx = 5
            if keystate[pg.K_SPACE] and not self.hidden:
                self.shoot()
        if mouse:
            mousestate = pg.mouse.get_pressed(3)
            if mousestate[0]:
                self.shoot()
            mouse_pos = pg.mouse.get_pos()
            self.rect.centerx = mouse_pos[0]

        # binding ship to screen
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH

        self.rect.x += self.speedx

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            b = Bullet(self.rect.centerx,self.rect.top+1)
            all_sprites.add(b)
            bullet_group.add(b)
            shoot_snd.play()


class Bullet(pg.sprite.Sprite):
    def __init__(self,x,y):
        super(Bullet, self).__init__()
        # self.image = pg.Surface((5,10))
        # self.image.fill(BLUE)
        self.image = bullet_img
        self.image = pg.transform.scale(self.image, (15, 30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed = -10


    def update(self):
        self.rect.y += self.speed
        # kill bullet when bottom <0
        if self.rect.bottom < 0:
            self.kill()


class Star(pg.sprite.Sprite):
    def __init__(self):
        super(Star,self).__init__()
        self.size =r.randint(1,7)
        self.image = pg.Surface((self.size, self.size))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.x = r.randint(5,WIDTH-5)
        self.y = r.randint(-1000,HEIGHT)
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy

        if self.rect.top > HEIGHT:
            self.x = r.randint(5, WIDTH - 5)
            self.y = r.randint(-1000, 0)
            self.rect.center = (self.x,self.y)


class NPC(pg.sprite.Sprite):
    def __init__(self):
        super(NPC, self).__init__()
        # self.image = pg.Surface((25,25))
        # self.image.fill(RED)
        self.image_orig = r.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()

        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *.75 /2)
        # pg.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.rect.centerx = (WIDTH/2)
        self.rect.top = 0
        self.rsx = r.randint(-5, 5)
        self.rsy = r.randint(1, 10)
        self.speedx = self.rsx
        self.speedy = self.rsy
        self.rot = 0
        self.rot_speed = r.randint(-8,8)
        self.last_update = pg.time.get_ticks()

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 60:
            self.last_update = now
            # do the rotation
            self.rot = (self.rot+self.rot_speed)%360
            new_image = pg.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.center = old_center


    def update(self):

        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.top >= HEIGHT + 20 or self.rect.left >= WIDTH + 10 or self.rect.right <= -10:
            self.rsx = r.randint(-5, 5)
            self.rsy = r.randint(1, 10)
            self.speedx = self.rsx
            self.speedy = self.rsy
            newposx = r.randint(15, WIDTH - 15)
            newposy = r.randint(10, 25) * -1
            self.rect.center = (newposx, newposy)

    def spawn(self):
        npc = NPC()
        print("spawn npc")
        npc_group.add(npc)
        all_sprites.add(npc)

class Explosion(pg.sprite.Sprite):
    def __init__(self,center,size):
        super(Explosion, self).__init__()
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center



####################################################################

#game functions
####################################################################
def draw_text(surf,text,size,x,y,color):
    font = pg.font.Font(font_name,size)
    text_surface = font.render(text,True,color)
    text_rect = text_surface.get_rect()
    text_rect.midtop=(x,y)
    surf.blit(text_surface,text_rect)

def draw_bar(surf,x,y,pct):
    if pct < 0:
        pct = 0
    bar_len = 180
    bar_height = 40
    fill = (pct/100)*bar_len
    outline_rect = pg.Rect(x,y,bar_len,bar_height)
    fill_rect = pg.Rect(x,y,fill,bar_height)
    pg.draw.rect(surf,GREEN,fill_rect)
    pg.draw.rect(surf,WHITE,outline_rect,4)

def draw_lives(surf,x,y,lives,img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x+30 * i
        img_rect.y = y
        surf.blit(img,img_rect)





####################################################################

# Game Constants
####################################################################
HEIGHT = 900
WIDTH = 600
FPS = 60

# Colors (R,G,B)
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)

title = "Shmup"
font_name = pg.font.match_font("arial")
mouse = False
keyboard = True

####################################################################

# folder variables
####################################################################
game_folder = path.dirname(__file__)
imgs_folder = path.join(game_folder,"imgs")
scores_folder = path.join(game_folder,"scores")
snds_folder = path.join(game_folder,"snds")
player_img_folder = path.join(imgs_folder,"player_imgs")
enemy_img_folder = path.join(imgs_folder,"enemy_imgs")
background_img_folder = path.join(imgs_folder,"background_imgs")
animation_folder = path.join(imgs_folder,"animation")
player_animation_folder = path.join(animation_folder,"player_animation")
npc_animation_folder = path.join(animation_folder,"npc_animation")
####################################################################

####################################################################

# initialize pygame and create window
####################################################################
pg.init()
pg.mixer.init()

screen = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption(title)
clock = pg.time.Clock()
####################################################################

# load imgs
####################################################################
#back grond img loaded
background = pg.image.load(path.join(background_img_folder,"starfield.png")).convert()
background = pg.transform.scale(background,(WIDTH,HEIGHT))
background_rect = background.get_rect()
#player img loaded
player_img = pg.image.load(path.join(player_img_folder,"player1Ship.png")).convert()
player_mini_img = pg.transform.scale(player_img,(25,19))
player_mini_img.set_colorkey(BLACK)

npc_img = pg.image.load(path.join(enemy_img_folder,"img_1.png")).convert()
bullet_img = pg.image.load(path.join(player_img_folder,"bullet_img.png")).convert()
meteor_images = []
meteor_list =['meteorBrown_big1.png','meteorBrown_big3.png','meteorBrown_big2.png','meteorBrown_big4.png',
              'meteorBrown_med1.png','meteorBrown_med3.png',
              'meteorBrown_small1.png','meteorBrown_small2.png',
              'meteorBrown_tiny1.png','meteorBrown_tiny2.png',
              'meteorGrey_big1.png','meteorGrey_big2.png','meteorGrey_big3.png','meteorGrey_big4.png',
              'meteorGrey_med1.png','meteorGrey_med2.png',
              'meteorGrey_small1.png','meteorGrey_small2.png',
              'meteorGrey_tiny1.png','meteorGrey_tiny2.png']
for img in meteor_list:
    meteor_images.append(pg.image.load(path.join(enemy_img_folder,img)))

# load explostion animation imgs
explosion_anim = {}
explosion_anim["lg"] = []
explosion_anim["sm"] = []
explosion_anim["player"] = []
for i in range(0,9):
    fn = "regularExplosion0{}.png".format(i)
    img = pg.image.load(path.join(npc_animation_folder,fn)).convert()
    img.set_colorkey(BLACK)
    img_lg = pg.transform.scale(img,(100,100))
    img_sm = pg.transform.scale(img, (40, 40))
    explosion_anim["sm"].append(img_sm )
    explosion_anim["lg"].append(img_lg )
    # adding player explostion
    fn = "sonicExplosion0{}.png".format(i)
    img = pg.image.load(path.join(player_animation_folder, fn)).convert()
    img.set_colorkey(BLACK)
    explosion_anim["player"].append(img)


####################################################################
#load sounds
####################################################################
shoot_snd = pg.mixer.Sound(path.join(snds_folder,"pew (1).wav"))
expl_sounds = []
for snd in ['expl3 (1).wav', 'expl6 (1).wav']:
    expl_sounds.append(pg.mixer.Sound(path.join(snds_folder, snd)))

pg.mixer.music.load(path.join(snds_folder,"tgfcoder-FrozenJam-SeamlessLoop (1).ogg"))
pg.mixer.music.set_volume(1)
pg.mixer.music.play(loops=-1)
####################################################################

# create Sprite groups
####################################################################
all_sprites = pg.sprite.Group()
players_group = pg.sprite.Group()
npc_group = pg.sprite.Group()
bullet_group = pg.sprite.Group()
star_group = pg.sprite.Group()

####################################################################

# create Game Objects
####################################################################
for i in range(25):
    star = Star()
    star_group.add(star)



player = Player()


for i in range(10):
    npc = NPC()
    npc_group.add(npc)



####################################################################

#add objects to sprite groups
####################################################################
players_group.add(player)


for i in star_group:
    all_sprites.add(i)

for i in players_group:
    all_sprites.add(i)

for i in npc_group:
    all_sprites.add(i)




####################################################################


# Game Loop
###################
#game update Variables
########################################
playing = True
score = 0

########################################
################################################################
while playing:
    # timing
    ##################################################
    clock.tick(FPS)
    ##################################################

    # collecting Input
    ##################################################

    # Quiting the game when we hit the x
    for event in pg.event.get():
        if event.type ==pg.KEYDOWN:
            # if event.key == pg.K_SPACE:
            #     player.shoot()
            if event.key == pg.K_ESCAPE:
                playing = False
        if event.type == pg.QUIT:
            playing = False

    ##################################################
    # Updates
    ##################################################
    all_sprites.update()

    # if NPC hits player
    hits = pg.sprite.spritecollide(player,npc_group,True,pg.sprite.collide_circle)
    for hit in hits:
        # playing = False
        npc.spawn()
        r.choice(expl_sounds).play()
        player.sheild -= hit.radius*2
        exlp = Explosion(hit.rect.center, "sm")
        all_sprites.add(exlp)
        if player.sheild <= 0:
            death_expl = Explosion(player.rect.center,"player")
            all_sprites.add(death_expl)
            player.hide()

            if player.lives <= 0  : #and not death_expl.alive() need to fix
                playing = False

    # if bullet his npc
    hits = pg.sprite.groupcollide(npc_group,bullet_group,True,True )
    for hit in hits:
        score += 50 - hit.radius
        exlp = Explosion(hit.rect.center,"lg")
        all_sprites.add(exlp)
        npc.spawn()
        r.choice(expl_sounds).play()




    ##################################################
    # Render
    ##################################################

    screen.fill(BLACK)
    screen.blit(background,background_rect)

    all_sprites.draw(screen)
    #draw hud
    draw_text(screen,"Score: "+str(score),40, WIDTH/2,10,WHITE)
    draw_bar(screen, 5, 10, player.sheild)
    draw_lives(screen, WIDTH-100, 10, player.lives, player_mini_img)

    pg.display.flip()
    ##################################################


pg.quit()
################################################################
#####################





