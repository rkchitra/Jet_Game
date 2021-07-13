import pygame
import decimal
#import random for random numbers
import random
from pygame.locals import (K_UP,K_DOWN,K_LEFT,K_RIGHT,K_ESCAPE,QUIT,KEYDOWN,RLEACCEL)

#player object
class Player(pygame.sprite.Sprite) :
    def __init__(self) :
        super(Player,self).__init__()
        self.surf = pygame.image.load("jet.png").convert()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.surf.get_rect()
        self.d = 5
    
    def update(self,keys_pressed) :
        if keys_pressed[K_UP] :
            self.rect.move_ip(0,-self.d)
            move_up_sound.play()
        if keys_pressed[K_DOWN] :
            self.rect.move_ip(0,self.d)
            move_down_sound.play()
        if keys_pressed[K_LEFT] :
            self.rect.move_ip(-self.d,0)
        if keys_pressed[K_RIGHT] :
            self.rect.move_ip(self.d,0)

        #check for boundaries
        if self.rect.left <= 0 :
            self.rect.left = 2
        if self.rect.right >= SCREEN_WIDTH :
            self.rect.right = SCREEN_WIDTH-2
        if self.rect.top <= 0 :
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT :
            self.rect.bottom = SCREEN_HEIGHT-2

class Enemy(pygame.sprite.Sprite) :
    def __init__(self) :
        super(Enemy,self).__init__()
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect = surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20,SCREEN_WIDTH + 100),
                random.randint(0,SCREEN_HEIGHT - 2),
            )
        )
        self.speed = random.randint(2,5)
    
    def update(self) :
        self.rect.move_ip(-self.speed,0)
        if self.rect.right < 0 :
            self.kill()

class Cloud(pygame.sprite.Sprite) :
    def __init__(self) :
        super(Cloud,self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH+20,SCREEN_WIDTH+100),
                random.randint(0,SCREEN_HEIGHT-2),
            )
        )
        self.speed = 5
    
    def update(self) :
        self.rect.move_ip(-self.speed,0)
        if self.rect.right < 0 :
            self.kill()


pygame.mixer.init()

pygame.init()

pygame. display. set_caption('Jet Game')
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)


pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1)

move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("collision.ogg")

clock = pygame.time.Clock()



#set up the drawing window 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

#custom event to create enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY,250)

#custom event to add clouds 
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD,500)

#player 
player = Player()

enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)




#game loop
running = True

while running :
    for event in pygame.event.get() :
        if event.type == QUIT :
            running = False
        elif event.type == KEYDOWN :
            if event.key == K_ESCAPE :
                running = False
        elif event.type == ADDENEMY :
            #create new enemy
            enemy = Enemy()
            enemies.add(enemy)
            all_sprites.add(enemy)
        elif event.type == ADDCLOUD :
            #create cloud 
            cloud = Cloud()
            clouds.add(cloud)
            all_sprites.add(cloud)
    
    #get keys pressed
    keys_pressed = pygame.key.get_pressed()

    screen.fill((255,255,255))

    #create a surface 
    surf = pygame.Surface((50,50))
    clouds.update()
    player.update(keys_pressed)
    enemies.update()
    
    #sky blue color
    screen.fill((135, 206, 250))

    rect = surf.get_rect()

    for entity in all_sprites :
        screen.blit(entity.surf,entity.rect)
    
    if pygame.sprite.spritecollideany(player,enemies) :
        #if player collides with an enemy
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()
        player.kill()
        running = False

    pygame.display.flip()
    clock.tick(60)
pygame.mixer.music.stop()
pygame.mixer.quit()

