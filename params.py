import pygame as g
from random import randint, choice
import json
from glob import glob
from threading import Thread
from time import sleep


LOG = 0

def log(*args):
    if not LOG:
        return
    
    out = ''
    for i in args:
        out += str(i)

    with open('log.txt', 'a') as f:
        f.write(out)


g.init()

cellnumber = 25
screensize = 700                  #cellnumber*cellsize
cellsize = int(screensize/cellnumber)

MENUSIZE = 200

title_font = g.font.Font(None, 32)
font = g.font.Font(None, 32)

clock = g.time.Clock()
screen = g.Surface((screensize, screensize))
info =   g.Surface((MENUSIZE, screensize))

window = g.display.set_mode(((screensize+MENUSIZE, screensize)))
g.display.set_caption(f"UpperT@le")

with open('params.json', 'r') as f:
    params = json.loads(f.read())


info_back = g.transform.scale(g.image.load('assets/info-back.png'), (MENUSIZE, screensize))



# all CELLTYPEs that will not have fr=-1
use_animation = {
    #type  fr
    "rat": 20,
    "upgrade": 40,
    'boar' : 20,
    'griefer': 50,
    'boss1' : 50,
    'boss2' : 60,
    
    #'explosion' : 10,
    #'blood-hurt': 10,

}


# all CELLTYPEs that will not block other entities
not_solid = [
    'exit',
    'upgrade',
    'boss2',
    'teleport-enter',
    'teleport-exit',
    #'Xboar',
]




def music_mixer():
    music = []
    for i in glob('assets/music/*'):
        music.append(g.mixer.Sound(i))
    
    while 1:
        channel = choice(music).play()
        while channel.get_busy():
            sleep(1) # we don't mind some delay for less lag
        
        sleep(1)     # since we have a little pause anyway



effect = {}
for i in glob('assets/sound/*'):
    effect[i.strip('assets/sound/').strip('.wav')] = g.mixer.Sound(i)

# to play, effect["name"].play()


Thread(target=music_mixer).start()


bossdata = {} # will be used by bosses to store values

