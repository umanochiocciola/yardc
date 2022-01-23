import pygame as g
from random import randint, choice

from params import *

afd = {}
entities = {
    #  name    atk hp gold
    "goblin" : (1, 5, 1),
    "rat"    : (1, 2, 0),
    "boar"   : (5, 5, 3),
    "griefer": (1, 1, 3),
    "boulder": (7, 99, 0),
    "boulder2": (12, 99, 0),
    "tanky"  : (5, 30, 5),
    "spike"  : (7, 5, 5),
    
    "boss1"  : (0, 1, 10),
    "boss2"  : (0, 100, 10),
    "boss3"  : (0, 100, 20),
    
}

class cell:
    def __init__(s, x, y, celltype='player', fr=50, solid=1, one_cicle_animation=0):
        # most unintuitively, the bigger is fr, the slower the animation is 
        
        s.x = x
        s.y = y
        s.type = celltype
        s.xdir = 0
        s.ydir = 0
        s.dir = 0
        s.solid = solid
        
        s.oca = one_cicle_animation
        
        s.isEntity = 0
        s.hp = 0
        s.atk = 0
        s.OnKill = 0
        
        if celltype == 'player':
            s.atk = 1
            s.score = 0
            s.defence = 0
        
        if celltype in entities:
            s.isEntity = 1
            s.atk, s.hp, s.OnKill = entities[celltype]
        
        
        if celltype in afd:
            fn = afd[celltype]   # already stored Frame Number for celltype
        else:
            try:
                with open(f'assets/cells/{celltype}.afd', 'r') as f:  # needs to get Frame Number for celltype, stores it for later
                    afd[celltype] = fn = int(f.read())
            except:
                afd[celltype] = fn = 1      # there's no animation frames descriptor and we'll assume there's only one frame
        
        s.fn = fn
        s.frames = [g.transform.scale(g.image.load(f'assets/cells/{celltype}-{i}.png'), (cellsize, cellsize)) for i in range(fn)]
        s.atic   = 0
        s.fr = fr
        s.oneciclefinished = 0
        
        
        s.owntic = 0 # used by some to count stuff
        
        #print(celltype, s.fn)
    
    def render(s, screen):
        #print('rendering', s.type)
        if s.dir > 0:
            screen.blit(g.transform.flip(s.frames[int(s.atic/s.fr)], 1, 0), (s.x*cellsize, s.y*cellsize))
        else:
            screen.blit(s.frames[int(s.atic/s.fr)], (s.x*cellsize, s.y*cellsize))
        
        if s.fr > 0 and not s.oneciclefinished:
            #print(s.type)
            s.atic += 1
            if int(s.atic/s.fr) >= s.fn:
                if s.oca:
                    s.atic -= 1
                    s.oneciclefinished = 1
                else:
                    s.atic = 0


