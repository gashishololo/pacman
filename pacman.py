import sys
import pygame
from pygame.locals import *
from math import floor
import random


def init_window():
    pygame.init()
    pygame.display.set_mode((512, 512))
    pygame.display.set_caption('Pacman')


class Map:
    def __init__(self,x,y):
        self.map=[[list()]*x for i in range(y)]
    def get(self,x,y):
        return self.map[x][y]
    def moveTo(self, obj, new_x, new_y):
                point = self.map[obj.x][obj.y]
                if obj in point:
                        point.remove(obj)
                        self.map[new_x][new_y].add(obj)
                        obj.set_ccord(obj.x,obj.y)
                        return True
                return False


def draw_background(scr, img=None):
    if img:
        scr.blit(img, (0, 0))
    else:
        bg = pygame.Surface(scr.get_size())
        bg.fill((0, 0, 0))
        scr.blit(bg, (0, 0))


class GameObject(pygame.sprite.Sprite):
    def __init__(self, img, x, y, tile_size, map_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.screen_rect = None
        self.x = 0
        self.y = 0
        self.tick = 0
        self.tile_size = tile_size
        self.map_size = map_size
        self.set_coord(x, y)

    def set_coord(self, x, y):
        self.x = x
        self.y = y
        self.screen_rect = Rect(floor(x) * self.tile_size, floor(y) * self.tile_size, self.tile_size, self.tile_size )

    def game_tick(self):
        self.tick += 1

    def draw(self, scr):
        scr.blit(self.image, (self.screen_rect.x, self.screen_rect.y))


class Ghost(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/ghost.png', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 1
        map.map[x][y]='g'

    def game_tick(self):
        super(Ghost, self).game_tick()
        if  self.direction == 0:
            self.direction = random.randint(1, 4)
        t=0
        if self.x==pacman.x and self.y>pacman.y and pacman.bonys!='m':
            for i in range(pacman.y,self.y):
                if map.map[self.x][i]=='w' or map.map[self.x][i]=='rw':
                    t=1
            if t==0:
                self.direction=4
        elif self.x==pacman.x and self.y<pacman.y and pacman.bonys!='m':
            for i in range(self.y,pacman.y):
                if map.map[self.x][i]=='w' or map.map[self.x][i]=='rw':
                    t=1
            if t==0:
                self.direction=2
        elif self.x>pacman.x and self.y==pacman.y and pacman.bonys!='m':
            for i in range(pacman.x,self.x):
                if map.map[i][self.y]=='w' or map.map[i][self.y]=='rw':
                    t=1
            if t==0:
                self.direction=3
        elif self.x<pacman.x and self.y==pacman.y and pacman.bonys!='m':
            for i in range(self.x,pacman.x):
                if map.map[i][self.y]=='w' or map.map[i][self.y]=='rw':
                    t=1
            if t==0:
                self.direction=1
        if self.direction == 1 and self.tick%2==0 :
            self.x += self.velocity
            if self.x > self.map_size-1:
                self.x = self.map_size-1
                self.direction = random.randint(1, 4)
            elif map.map[self.x][self.y]=='w' or map.map[self.x][self.y]=='rw':
                self.x-=self.velocity
                self.direction = random.randint(1, 4)
            else:
                map.map[self.x][self.y]='g'
                map.map[self.x-self.velocity][self.y]=''
        elif self.direction == 2 and self.tick%2==0:
            self.y += self.velocity
            if self.y > self.map_size-1:
                self.y = self.map_size-1
                self.direction = random.randint(1, 4)
            elif map.map[self.x][self.y]=='w' or map.map[self.x][self.y]=='rw' :
                self.y-=self.velocity
                self.direction = random.randint(1, 4)
            else:
                map.map[self.x][self.y]='g'
                map.map[self.x][self.y-self.velocity]=''
        elif self.direction == 3 and self.tick%2==0:
            self.x -= self.velocity
            if self.x < 0:
                self.x = 0
                self.direction = random.randint(1, 4)
            elif map.map[self.x][self.y]=='w' or map.map[self.x][self.y]=='rw':
                self.x+=self.velocity
                self.direction = random.randint(1, 4)
            else:
                map.map[self.x][self.y]='g'
                map.map[self.x+self.velocity][self.y]=''
        elif self.direction == 4 and self.tick%2==0:
            self.y -= self.velocity
            if self.y < 0 :
                self.y = 0
                self.direction = random.randint(1, 4)
            elif map.map[self.x][self.y]=='w' or map.map[self.x][self.y]=='rw':
                self.y+=self.velocity
                self.direction = random.randint(1, 4)
            else:
                map.map[self.x][self.y]='g'
                map.map[self.x][self.y+self.velocity]=''
        self.set_coord(self.x, self.y)


class Pacman(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/pacmanright.png', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 1
        map.map[self.x][self.y]='p'
        self.bonys=''
        self.timer=0


    def game_tick(self):
        if self.bonys=='':
            self.timer=0
        if (self.bonys=='s' or self.bonys=='i'or self.bonys=='y' or self.bonys=='m') and self.timer<=60:
            self.timer+=1
        else:
            self.bonys=''
            self.timer=0
        super(Pacman, self).game_tick()

        if self.direction == 1 and self.tick%2==0 :
            self.x += self.velocity
            if self.x > self.map_size-1:
                self.x = self.map_size-1
            elif map.map[self.x][self.y]=='w' and self.bonys!='y':
                self.x-=self.velocity
            else:
                map.map[self.x][self.y]='p'
                map.map[self.x-self.velocity][self.y]=''
        elif self.direction == 2 and self.tick%2==0:
            self.y +=self.velocity
            if self.y > self.map_size-1:
                self.y = self.map_size-1
            elif map.map[self.x][self.y]=='w' and self.bonys!='y':
                self.y-=self.velocity
            else:
                map.map[self.x][self.y]='p'
                map.map[self.x][self.y-self.velocity]=''
        elif self.direction == 3 and self.tick%2==0 :
            self.x -= self.velocity
            if self.x < 0 :
                self.x = 0
            elif map.map[self.x][self.y]=='w' and self.bonys!='y':
                self.x+=self.velocity
            else:
                map.map[self.x][self.y]='p'
                map.map[self.x+self.velocity][self.y]=''
        elif self.direction ==  4 and self.tick%2==0 :
            self.y -= self.velocity
            if self.y < 0:
                self.y = 0
            elif map.map[self.x][self.y]=='w' and self.bonys!='y':
                self.y+=self.velocity
            else:
                map.map[self.x][self.y]='p'
                map.map[self.x][self.y+self.velocity]=''

        self.set_coord(self.x, self.y)


def process_events(events, pacman):
    for event in events:
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                pacman.direction = 3
                pacman.image=pygame.image.load('./resources/pacmanleft.png')
            elif event.key == K_RIGHT:
                pacman.direction = 1
                pacman.image=pygame.image.load('./resources/pacmanright.png')
            elif event.key == K_UP:
                pacman.image=pygame.image.load('./resources/pacmanup.png')
                pacman.direction = 4
            elif event.key == K_DOWN:
                pacman.image=pygame.image.load('./resources/pacmandown.png')
                pacman.direction = 2
            elif event.key == K_SPACE:
                pacman.direction = 0


class Wall(GameObject):
    def __init__(self, x, y,r, tile_size, map_size):
        GameObject.__init__(self, './resources/wall.png', x, y, tile_size, map_size)
        if r=='n':
           map.map[x][y]='w'
        else:
            map.map[x][y]='rw'
            self.image=pygame.image.load('./resources/rwall.png')


class Food(GameObject):
    def  __init__(self,x,y,tile_size, map_size):
        GameObject.__init__(self, './resources/b.png', x, y, tile_size, map_size)


class Bonys(GameObject):
    def  __init__(self,x,y,b, img,tile_size, map_size):
        GameObject.__init__(self, img, x, y, tile_size, map_size)
        self.b=b


if __name__ == '__main__':
    input=open('input.txt','r')
    init_window()
    tile_size =32
    map_size =16
    walls=[]
    ghosts=[]
    food=[]
    bonys=[]
    map=Map(map_size,map_size)
    for i in range(map_size+1):
        for j in range(map_size+1):
            a=input.read(1)
            print(a)
            if a=='n':
                walls.append(Wall(j, i, 'n', tile_size, map_size))
            elif a=='r':
                walls.append(Wall(j, i, 'rw', tile_size, map_size))
            elif a=='f':
                food.append(Food(j,i,tile_size,map_size))
            elif a=='g':
                ghosts.append(Ghost(j, i, tile_size, map_size))
            elif a=='s':
                bonys.append(Bonys(j,i,'s',"./resources/s.png",tile_size,map_size))
            elif a=='i':
                bonys.append(Bonys(j,i,'i',"./resources/i.png",tile_size,map_size))
            elif a=='y':
                bonys.append(Bonys(j,i,'y',"./resources/y.png",tile_size,map_size))
            elif a=='m':
                bonys.append(Bonys(j,i,'m',"./resources/m.png",tile_size,map_size))
            elif a=='p':
                pacman = Pacman(j, i, tile_size, map_size)
    background = pygame.image.load("./resources/background.png")
    screen = pygame.display.get_surface()

    while 1:
        process_events(pygame.event.get(), pacman)
        pygame.time.delay(100)
        pacman.game_tick()
        draw_background(screen, background)
        i=0
        while i<len(walls):
            walls[i].draw(screen)
            if walls[i].x==pacman.x and walls[i].y==pacman.y:
                walls.pop(i)
            else:
                i+=1
        j=0
        while j<len(food):
            food[j].draw(screen)
            if food[j].x==pacman.x and food[j].y==pacman.y:
                food.pop(j)
            else:
                j+=1
        k=0
        while k<len(bonys):
            bonys[k].draw(screen)
            if bonys[k].x==pacman.x and bonys[k].y==pacman.y:
                if bonys[k].b=='s':
                    pacman.bonys='s'
                elif bonys[k].b=='i':
                    pacman.bonys='i'
                elif bonys[k].b=='m':
                    pacman.bonys='m'
                else:
                    pacman.bonys='y'
                pacman.timer=0
                bonys.pop(k)
            else:
                k+=1
        if len(food)==0:
            sys.exit(0)
        pacman.draw(screen)
        g=0
        while g<len(ghosts):
            ghosts[g].game_tick()
            ghosts[g].draw(screen)
            if pacman.x==ghosts[g].x and ghosts[g].y==pacman.y and pacman.bonys=='s':
                ghosts.pop(g)
            elif ghosts[g].x==pacman.x and ghosts[g].y==pacman.y and pacman.bonys!='i':
                sys.exit(0)
            else:
                g+=1
        pygame.display.update()
