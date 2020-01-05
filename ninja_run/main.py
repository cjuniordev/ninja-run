import pygame
from pygame.locals import *

#CONST
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 450
FLOOR_WIDTH = 2 * SCREEN_WIDTH
FLOOR_HEIGHT = 64
FLOOR_YPOS = SCREEN_HEIGHT - FLOOR_HEIGHT
PLAYER_XPOS = 50

GAME_SPEED = 10
VELOCITY = 10
JUMP = -20
GRAVITY = 1 
FPS = 30


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [
            pygame.transform.scale( (pygame.image.load('img/player/run/Run__000.png').convert_alpha() ), (50, 50) ),
            pygame.transform.scale( (pygame.image.load('img/player/run/Run__001.png').convert_alpha() ), (50, 50) ),
            pygame.transform.scale( (pygame.image.load('img/player/run/Run__002.png').convert_alpha() ), (50, 50) ),
            pygame.transform.scale( (pygame.image.load('img/player/run/Run__003.png').convert_alpha() ), (50, 50) ),
            pygame.transform.scale( (pygame.image.load('img/player/run/Run__004.png').convert_alpha() ), (50, 50) ),
            pygame.transform.scale( (pygame.image.load('img/player/run/Run__005.png').convert_alpha() ), (50, 50) ),
            pygame.transform.scale( (pygame.image.load('img/player/run/Run__006.png').convert_alpha() ), (50, 50) ),
            pygame.transform.scale( (pygame.image.load('img/player/run/Run__007.png').convert_alpha() ), (50, 50) ),
            pygame.transform.scale( (pygame.image.load('img/player/run/Run__008.png').convert_alpha() ), (50, 50) ),
            pygame.transform.scale( (pygame.image.load('img/player/run/Run__009.png').convert_alpha() ), (50, 50) )
        ]

        self.current_image = 0

        self.velocity = VELOCITY

        self.image = pygame.transform.scale( (pygame.image.load('img/player/run/Run__000.png').convert_alpha() ), (50, 50) )
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = PLAYER_XPOS
        self.rect[1] = SCREEN_HEIGHT / 2

    def jump(self):
        self.velocity = JUMP

    def update(self):
        self.current_image = (self.current_image + 1) % 10
        self.image = self.images[self.current_image]

        self.velocity += GRAVITY

        #fall
        if not self.rect[1] >= FLOOR_YPOS - 50: # 50 is ypos the player
           self.rect[1] += self.velocity
        else:
            self.rect[1] = FLOOR_YPOS - 50

    def ypos(self): #this method returned the player's position to set the kunai launch position
        self.player_ypos = self.rect[1]
        return self.player_ypos

class Kunai(pygame.sprite.Sprite):

    def __init__(self, ypos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.flip(pygame.transform.scale( (pygame.image.load('img/player/weapon/Kunai.png').convert_alpha()), (50, 25) ), False, False)
        
        self.rect = self.image.get_rect()
        self.rect[0] = PLAYER_XPOS
        self.rect[1] = ypos

        self.velocity = GAME_SPEED

    def update(self):
        self.rect[0] += self.velocity

def create_kunai(ypos):
    other_kunai = Kunai(ypos)
    kunai_group.add(other_kunai)


class Enemy(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [
            pygame.transform.flip(pygame.transform.scale( (pygame.image.load('img/enemy/zombie/male/walk/Walk_001.png').convert_alpha() ), (50, 50) ), True, False), 
            pygame.transform.flip(pygame.transform.scale( (pygame.image.load('img/enemy/zombie/male/walk/Walk_002.png').convert_alpha() ), (50, 50) ), True, False),
            pygame.transform.flip(pygame.transform.scale( (pygame.image.load('img/enemy/zombie/male/walk/Walk_003.png').convert_alpha() ), (50, 50) ), True, False),
            pygame.transform.flip(pygame.transform.scale( (pygame.image.load('img/enemy/zombie/male/walk/Walk_004.png').convert_alpha() ), (50, 50) ), True, False),
            pygame.transform.flip(pygame.transform.scale( (pygame.image.load('img/enemy/zombie/male/walk/Walk_005.png').convert_alpha() ), (50, 50) ), True, False),
            pygame.transform.flip(pygame.transform.scale( (pygame.image.load('img/enemy/zombie/male/walk/Walk_006.png').convert_alpha() ), (50, 50) ), True, False),
            pygame.transform.flip(pygame.transform.scale( (pygame.image.load('img/enemy/zombie/male/walk/Walk_007.png').convert_alpha() ), (50, 50) ), True, False),
            pygame.transform.flip(pygame.transform.scale( (pygame.image.load('img/enemy/zombie/male/walk/Walk_008.png').convert_alpha() ), (50, 50) ), True, False),
            pygame.transform.flip(pygame.transform.scale( (pygame.image.load('img/enemy/zombie/male/walk/Walk_009.png').convert_alpha() ), (50, 50) ), True, False),
            pygame.transform.flip(pygame.transform.scale( (pygame.image.load('img/enemy/zombie/male/walk/Walk_010.png').convert_alpha() ), (50, 50) ), True, False)
        ]

        self.current_image = 0

        self.velocity = GAME_SPEED

        self.image = pygame.transform.flip(pygame.transform.scale( (pygame.image.load('img/enemy/zombie/male/walk/Walk_001.png').convert_alpha() ), (50, 50) ), True, False)
        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH + 50 #for the enemy create off screen
        self.rect[1] = FLOOR_YPOS - 50 #50 width of enemy

    def update(self):
        self.current_image = (self.current_image + 1) % 10
        self.image = self.images[self.current_image]

        self.rect[0] -= self.velocity

class Floor(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('img/blocks/floor.png')
        self.image = pygame.transform.scale(self.image, (FLOOR_WIDTH, FLOOR_HEIGHT))
        
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = FLOOR_YPOS

    def update(self):
        self.rect[0] -= GAME_SPEED


def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

    
def game(screen, player_group, kunai_group, enemy_group, floor_group, clock, FPS):
    throw_kunai = False
    i = 0
    while True:
        clock.tick(FPS)
        

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if player.rect[1] >= FLOOR_YPOS - 50:
                        player.rect[1] -= 2
                        player.jump()
                if event.key == K_RIGHT:
                    throw_kunai = True
                    i += 1
                    if i > 1:
                        player_ypos = player.ypos()
                        create_kunai(player_ypos)

        if pygame.sprite.pygame.sprite.groupcollide(kunai_group, enemy_group, False, False, pygame.sprite.collide_mask):
            enemy_group.remove(enemy_group.sprites()[0])
            kunai_group.remove(kunai_group.sprites()[0])
            
            throw_kunai = False

            other_enemy = Enemy()
            enemy_group.add(other_enemy)

        if is_off_screen(kunai_group.sprites()[0]):
            #kunai_group.pygame.sprite.remove(kunai_group.sprites()[0])
            kunai_group.remove(kunai_group.sprites()[0])
            throw_kunai = False

        if is_off_screen(enemy_group.sprites()[0]):
            enemy_group.remove(enemy_group.sprites()[0])

            other_enemy = Enemy()
            enemy_group.add(other_enemy)

        if is_off_screen(floor_group.sprites()[0]):
            floor_group.remove(floor_group.sprites()[0])
            
            other_floor = Floor(FLOOR_WIDTH -20)
            floor_group.add(other_floor)

        screen.fill((0, 0, 0))

        player_group.update()
        if throw_kunai:
            kunai_group.update()
        enemy_group.update()
        floor_group.update()

        player_group.draw(screen)
        if throw_kunai:
            kunai_group.draw(screen)
        enemy_group.draw(screen)
        floor_group.draw(screen)

        '''
        if pygame.sprite.pygame.sprite.groupcollide(player_group, enemy_group, False, False, pygame.sprite.collide_mask):
            screen.blit(game_over_screen, (0, 0))
        '''
        pygame.display.update()


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Plataforma')

game_over_screen = pygame.image.load('img/screens/game_over_screen.png')

#create instance of player
player_group = pygame.sprite.Group()
player = Player()
player_group.add(player)

kunai_group = pygame.sprite.Group()
kunai = Kunai(player.rect[1])
kunai_group.add(kunai)

enemy_group = pygame.sprite.Group()
enemy = Enemy()
enemy_group.add(enemy)

floor_group = pygame.sprite.Group()
for i in range(2):
    floor = Floor(FLOOR_WIDTH * i)
    floor_group.add(floor)

clock = pygame.time.Clock()


#call the function game and pass params
game(screen, player_group, kunai_group, enemy_group, floor_group, clock, FPS)