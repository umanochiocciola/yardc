import pygame as g
from random import randint, choice
import json


g.init()

cellnumber = 25
screensize = 700                  #cellnumber*cellsize
cellsize = int(screensize/cellnumber)

title_font = g.font.Font(None, 32)
font = g.font.Font(None, 32)

clock = g.time.Clock()
screen = g.display.set_mode((screensize, screensize))#, g.FULLSCREEN)
g.display.set_caption(f"UpperT@le")

with open('params.json', 'r') as f:
    params = json.loads(f.read())



# all CELLTYPEs that will not have fr=-1
use_animation = {
    #type  fr
    "rat": 20,
    "upgrade": 40,
    'boar' : 20,
    'griefer': 50,
    #'blood-hurt': 60

}


# all CELLTYPEs that will not block other entities
not_solid = [
    'exit',
    'upgrade',
]


music = {
    "main": g.mixer.Sound("assets/music/poppy.wav")
}

music["main"].play(-1)

