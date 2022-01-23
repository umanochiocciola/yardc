#from lvl import GenLevel
from params import *
from cell import cell, afd
import bosses
from terrain import GetTerrain
from menu import menu




log('----------------------- NEW SESSION -------------------------')

def QUIT():
    g.quit()
    exit(0)


def main():
    
    LEVEL = 1
    alive = 1
    carry = (10, 1, 0, 0)
    cells = 0
    
    bossdata = {} # reset bosses
    
    
    LOADED = 0
    try:
        with open("save.json", 'r') as f:
            carry, cells, LEVEL = load_save(json.loads(f.read()))
            LOADED = 1
    
    except:
        print('unable to fetch save file, starting new game...')

    menu(carry, cells, LEVEL)
    
    while 1: # game
        
        if not alive:
            return cells[0].score
        
        if cells:
            carry = (cells[0].hp, cells[0].atk, cells[0].defence, cells[0].score+5)
        
        print(LOADED, carry, LEVEL)
        if not LOADED or not cells:
            LOADED = 0
            
            if LEVEL%10:
                cells = GetLevel(8, 8, cellnumber, cellnumber, LEVEL)
            else:
                try:
                    with open(f"assets/bossrooms/{int(LEVEL/10)}.json", 'r') as f:
                        cells = GetCellsLevel(json.loads(f.read()))
                except json.decoder.JSONDecodeError as e:
                    print('json error cringe\n', e)
                
                except:# Exception as e:
                    #print(e)
                    return 'END'
        
            cells.insert(0, cell(8, 8))
        cells[0].hp, cells[0].atk, cells[0].defence, cells[0].score = carry
        
        if LEVEL == 30:
            cells.append(cell(8, 8, 'gun', fr=-1, solid=0))

        
        mvx = mvy = 0
        
        SELECTED_MAN_CELL = 'wall'
        
        shooting = 0
        
        tic = 0
        movtic = 0
        while 1: # level
            
            for ev in g.event.get():
                if ev.type == g.QUIT:
                    QUIT()
            
                if ev.type == g.KEYDOWN:
                    
                    movtic == -3
                    
                    if ev.key == g.K_ESCAPE:
                        menu(carry, cells, LEVEL)
                    
                    if ev.key == g.K_SPACE:
                        if LEVEL == 30:
                            shooting = 1
                        
                    
                    if ev.key in [g.K_w, g.K_UP, g.K_k] :
                        mvy += -1
                    if ev.key in [g.K_s, g.K_DOWN, g.K_j]:
                        mvy += 1
                    if ev.key in [g.K_a, g.K_LEFT, g.K_h]:
                        mvx += -1
                    if ev.key in [g.K_d, g.K_RIGHT, g.K_l]:
                        mvx += 1
                
                if ev.type == g.KEYUP:
                    
                    if ev.key == g.K_SPACE:
                        shooting = 0
                    
                    if mvx != 0:

                        if ev.key in [g.K_a, g.K_LEFT, g.K_h]:
                            mvx -= -1
                        if ev.key in [g.K_d, g.K_RIGHT, g.K_l]:
                            mvx -= 1
                    
                    if mvy != 0:
                
                        if ev.key in [g.K_w, g.K_UP, g.K_k] :
                            mvy -= -1
                        if ev.key in [g.K_s, g.K_DOWN, g.K_j]:
                            mvy -= 1
           
           
            # so if you press w and k you don't go up twice as fast
            if mvx > 1: mvx = 1
            if mvx <-1: mvx = -1
            if mvy > 1: mvy = 1
            if mvy <-1: mvy = -1
            
           
            #if [i for i in cells if i.type == 'shot'] != []:
            #    print('>)')
            
            # get what cell is the mouse on
            for i in cells:
                mx, my = g.mouse.get_pos()
                if (i.x, i.y) == (int(mx/cellsize), int(my/cellsize)):
                    SELECTED_MAN_CELL = i.type
            
            if shooting and tic%10 == 0:
                cells.append(cell(cells[0].x, cells[0].y, celltype='shot', fr=-1, solid=0))
            
            movtic += 1
            if movtic % 5 == 0:               
                if mvx:
                    cells[0].dir = mvx
                cells[0].xdir = mvx
                cells[0].x += mvx
                #if mvy != 0:
                cells[0].y += mvy
                cells[0].ydir = mvy
        
                if RoomWalls(cells[0], cells):
                    cells[0].x -= mvx
                    cells[0].y -= mvy

            

            if EntityMovement(cells, tic) == 'died':
                alive = 0
                break
            
            dmg = CheckDamage(cells[0], cells)
            if dmg:
                
                
                dmg -= cells[0].defence
                if dmg > 0:
                    cells[0].hp -= dmg
                    if cells[0].hp <= 0:
                        alive = 0
                        break
        
            CheckUpgrades(cells[0], cells) # and apply them
                
                



            if CheckWin(cells[0], cells):
                effect["Door"].play()
                LEVEL += 1
                break
        
            update(cells, LEVEL, SELECTED_MAN_CELL)
            tic += 1
        



def update(cells, LEVEL, man):
    screen.fill((28,9,1))

    for i in cells:
        i.render(screen)
    
    
    screen.blit(font.render(f"level {LEVEL}   ||   hp: {cells[0].hp}  |   atk: {cells[0].atk}   |   def: {cells[0].defence}   |   score: {cells[0].score}", 0, (0,255,0)), (10,10))
    '''s
    GCOLOR = (157,190,0)
    for x in range(cellnumber):
        g.draw.line(screen, GCOLOR, (x*cellsize,0), (x*cellsize,screensize))
    
    for y in range(cellnumber):
        g.draw.line(screen, GCOLOR, (0, y*cellsize), (screensize, y*cellsize))
    '''
    
    info.fill((0,0,0))
    info.blit(info_back, (0,0))
    info.blit(font.render(f' -- {man} --',0,(200,200,200)), (10, 10))
    info.blit(font.render(params['help'].get(man, 'no info avaiable'),0,(200,200,200)), (0, 30))
    
    
    
    window.fill((0,0,0))
    
    window.blit(screen, (0,0))
    window.blit(info, (screensize, 0))
    
    
    g.display.flip()
    clock.tick(60)




## interactables
def CheckWin(pl, cells):
    for i in cells:
        if i.type == 'exit' and (i.x, i.y) == (pl.x, pl.y):
            return 1
    
    return 0


def CheckUpgrades(pl, cells): # and apply them
    for i in cells:
        if i.type == 'upgrade' and (i.x, i.y) == (pl.x, pl.y):
            #use upgrade
            cells.remove(i)
            
            #apply upgrade
            dice = randint(0, 3)
            if dice == 0:
                effect["Heal"].play()
                pl.hp += 1
            if dice == 1:
                effect["Power"].play()
                pl.atk += 1
            if dice == 2:
                effect["Exp"].play()
                pl.score += 1
            if dice == 3:
                effect["Clang"].play()
                pl.defence += 1

            
            return


## other stuff

def RoomWalls(pl, cells):
    pop = 0
    # screen margin
    if pl.x >= cellnumber or pl.x < 0 or pl.y >= cellnumber or pl.y < 0:
        pop = 1

    if not pop:
        # cell collision
        for i in cells:
            if i is pl or (not i.solid): continue
            if (i.x, i.y) == (pl.x, pl.y):
                pop = 1
                break

    return pop


def EntityMovement(cells, tic):

    for i in cells:
        if i.type == 'goblin' and tic%40 == 0:
            randmov(cells, i)
                
        if i.type == 'rat' and tic%20 == 0:
            i.dir = randmov(cells, i)
        
        if i.type == 'blocked-exit':
            open_me = 1
            for j in cells:
                if j.isEntity and j.type != 'player' and j.type != 'boulder':
                   open_me = 0
                   break
            
            if open_me:
                cells.append(cell(i.x, i.y, "exit", fr=-1, solid=0))
                cells.remove(i)
        
        if i.type == 'boar' and tic%30 == 0:
            i.dir = randmov(cells, i)
        
        
        if i.type == 'griefer' and tic%50 == 0:
            cells.append(cell(i.x, i.y, celltype="boulder", fr=-1, solid=0))
            
            # toward player direction, approxed to 8 directions
            cells[-1].xdir = (1-2*(cells[0].x<i.x))*(cells[0].x != i.x)
            cells[-1].ydir = (1-2*(cells[0].y<i.y))*(cells[0].y != i.y)


        if i.type == 'boulder' and tic%10 == 0:
            #print(i.xdir, i.ydir)
            i.x += i.xdir
            i.y += i.ydir
            
            fucked = 0
            for j in cells:
                if j.type == 'shot' and (i.x, i.y) == (j.x, j.y):
                    cells.remove(j)
                    cells.remove(i)
                    fucked = 1
                    break
            if fucked:
                continue
            
            if i.x >= cellnumber or i.y >= cellnumber or i.x < 0 or i.y < 0:
                cells.remove(i)
                continue
            
        
        if i.type == 'tanky':
            i.dir = 1-2*(cells[0].x < i.x)
            if randint(1, 100) == 1:
                randmov(cells, i)
        
        if i.type == 'spike':
            i.dir = 1-2*(cells[0].x < i.x)
            if randint(1, 20) == 1:
                randmov(cells, i)
        
        
        
        if i.type == 'boss1':
            bosses.boss_1(cells, i)
        
        if i.type == 'boss2' and tic%10==0:
            bosses.boss_2(cells, i)
        
        
        if i.type == 'Xboar' and tic%30 == 0:
            i.xdir = (1-2*(cells[0].x<i.x))*(cells[0].x != i.x)
            i.ydir = (1-2*(cells[0].y<i.y))*(cells[0].y != i.y)
            
            i.x += i.xdir
            i.y += i.ydir
            
            for j in cells:
                if j is i:
                    continue
                
                if j.type == 'Xboar' and (j.x, j.y) == (i.x, i.y):
                    i.x -= i.xdir
                    i.y -= i.ydir
                    break
            
            i.owntic += 1
            
            if (i.x, i.y) == (cells[0].x, cells[0].y) or i.owntic == 50:
                cells.append(cell(i.x, i.y, celltype="explosion", fr=5, solid=0, one_cicle_animation=1))
                cells.remove(i)
            
            
        
        
        if i.type == 'explosion':
            if i.oneciclefinished:
                ret = 0
                if (i.x, i.y) == (cells[0].x, cells[0].y):
                    cells[0].hp -= 15
                    if cells[0].hp <= 0:
                        ret = 'died'
                cells.remove(i)
                if ret: return ret
        
        
        if i.type == 'teleport-enter':
            for j in cells:
                if j.type == 'teleport-exit':
                    cells[0].x, cells[0].y = j.x, j.y
                    cells.remove(i)
                    break
        
        
        if i.type == 'bomb':
            if tic%10 == 0:
                i.y += i.ydir
            
            for j in cells:
                if (i.x, i.y) == (j.x, j.y) and (j.type not in ['wall', 'bomb'] or i.y > cellnumber-4):
                    cells.remove(i)
                    if j.type not in ['player', 'bomb', 'blocked-exit']\
                       and j.type != 'wall': # remove this last condition part to spice up
                        cells.remove(j)
                    cells.append(cell(i.x, i.y, 'explosion', fr=5, solid=0, one_cicle_animation=1))
                    break
                    
            
            
            if i.x >= cellnumber or i.y >= cellnumber or i.x < 0 or i.y < 0:
                cells.remove(i)
                continue
        
        
        if i.type == 'boss3':
            bosses.boss_3(cells, i)
        
        
        if i.type == 'gun':
            i.x, i.y = cells[0].x, cells[0].y
        
        if i.type == 'shot' and tic%3==0:
            i.y -= 1
            if i.y <= 0:
                cells.remove(i)
                continue
        
        
        
            


def randmov(cells, i):
    
    if randint(0,1):
        mvy = 0
        mvx = randint(-1, 1)
        if not mvx:
            mvy = randint(-1, 1)
    else:
        mvx = 0
        mvy = randint(-1, 1)
        if not mvy:
            mvx = randint(-1, 1)    

    i.x += mvx
    i.y += mvy
    
    if RoomWalls(i, cells):
        i.x -= mvx
        i.y -= mvy
    
    return mvx


            
    
def CheckDamage(pl, cells):
    for i in cells:
        if i is pl or (not i.isEntity): continue
        if (i.x, i.y) == (pl.x, pl.y+pl.ydir) or (i.x, i.y)==(pl.x+pl.xdir, pl.y):

            effect["Crunch"].play()
            
            i.hp -= pl.atk
            cells.append(cell(i.x, i.y, "blood-hurt", fr=10, solid=0, one_cicle_animation=1))
            i.x -= pl.xdir
            i.y -= pl.ydir
            if i.hp <= 0:
                cells.remove(i)
                pl.score += i.OnKill
            return i.atk

def GetLevel(*args):
    
    #lvl = GenLevel()
    #print(lvl); g.quit(); exit(0)
    lvl = GetTerrain(*args)
    return GetCellsLevel(lvl)

def GetCellsLevel(lvl):
    cells = []
    for celltype, positions in lvl.items():
        #print('celltype:', celltype, '\n\tpositions:', positions)#; g.quit(); exit(0)
        for pos in positions:
            x, y = pos
            #try: x, y = pos
            #except:
                #print(positions); g.quit(); exit(0)
        
            cells.append(cell(x, y, celltype, fr=use_animation.get(celltype, -1), solid=(celltype not in not_solid) ))
            #print(celltype, f'@ {x}, {y}')

    return cells



def load_save(save):
    carry = tuple(save['carry'])
    LEVEL = save['level']
    
    raw_cells = save['cells']
    cells = GetCellsLevel(raw_cells)
    
    return carry, cells, LEVEL





def GameOver(lvl):
    
    tic = 0
    while 1:
        for ev in g.event.get():
            if ev.type == g.QUIT:
                g.quit()
                exit(0)
            
            if ev.type == g.KEYDOWN and tic >= 50:
                return
                
            
        window.fill((50, 0, 0))
        
        if lvl == 'END':
        
            window.blit(title_font.render("Congrats!", 0, (0, 255, 0)), (200, 100))
            window.blit(font.render(f"You reached an end! New stuff soon! Go do something else now!", 0, (0, 255, 0)), (150, 200))
        
        else:
            window.blit(title_font.render("Game Over!", 0, (0, 255, 0)), (100, 100))
            window.blit(font.render(f"Score: {lvl}", 0, (0, 255, 0)), (200, 200))
        
        window.blit(font.render(f"press any key", 0, (0, 255, 0)), (200, 300))
        
        g.display.flip()
        clock.tick(60)
        tic += 1







while 1:
    GameOver(main())