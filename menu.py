import pygame as g
from params import *
import json


toggle_music = g.Rect(100, 300, 100, 50)


def dictify_cells(cells):
    if cells == 0:
        return 0 # trying to save not-started-yet game
    
    out = {}
    for i in cells:
        if i.type not in out:
            out[i.type] = []
        
        out[i.type].append((i.x, i.y))

        try: out.pop("blood-hurt")
        except: 0

    return out



def menu(carry, cells, LEVEL):
        
        window.fill((0,0,0))
        window.blit(g.image.load('assets/Background.png'), (int(MENUSIZE/2),0))
        g.display.flip()
        
        MUSIC = 1
        
        
        while 1:
            for ev in g.event.get():
                if ev.type == g.QUIT:
                    g.quit()
                    quit()
                
                if ev.type == g.KEYDOWN:
                    if ev.key == g.K_m:
                        MUSIC = not MUSIC
                        if MUSIC:
                            g.mixer.unpause()                    
                        else:
                            g.mixer.pause()
                    
                    elif ev.key == g.K_o:
                        with open('save.json', 'w') as f:
                            f.write(json.dumps({
                                "cells": dictify_cells(cells),
                                "carry": carry,
                                "level": LEVEL
                            }))
                    
                    else:
                        return
        
        
        clock.tick(60)


