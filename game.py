#from lvl import GenLevel
from params import *
from cell import cell, afd
from terrain import GetTerrain
from menu import menu

def QUIT():
    g.quit()
    exit(0)


def main():
    LEVEL = 1
    alive = 1
    carry = (10, 1, 0, 0)
    cells = 0
    
    while 1: # game
        if cells:
            carry = (cells[0].hp, cells[0].atk, cells[0].defence, cells[0].score)
        
        
        if LEVEL%10:
            cells = GetLevel(8, 8, cellnumber, cellnumber, LEVEL)
        else:
            try:
                with open(f"assets/bossrooms/{int(LEVEL/10)}.json", 'r') as f:
                    cells = GetCellsLevel(json.loads(f.read()))
            except json.decoder.JSONDecodeError as e:
                print('json error cringe\n', e)
            
            except:
                return 'END'
    
        cells.insert(0, cell(8, 8))
        cells[0].hp, cells[0].atk, cells[0].defence, cells[0].score = carry
            
        if not alive:
            return LEVEL
        
        mvx = mvy = 0
        
        tic = 0
        movtic = 0
        while 1: # level
            
            for ev in g.event.get():
                if ev.type == g.QUIT:
                    QUIT()
            
                if ev.type == g.KEYDOWN:
                    
                    movtic == -3
                    
                    if ev.key == g.K_w:
                        mvy += -1
                    if ev.key == g.K_s:
                        mvy += 1
                    if ev.key == g.K_a:
                        mvx += -1
                    if ev.key == g.K_d:
                        mvx += 1
                
                if ev.type == g.KEYUP:
                    
                    if mvy != 0:
                    
                        if ev.key == g.K_w:
                            mvy -= -1
                        if ev.key == g.K_s:
                            mvy -= 1
                    
                    if mvx != 0:
                
                        if ev.key == g.K_a:
                            mvx -= -1
                        if ev.key == g.K_d:
                            mvx -= 1
            
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

            

            EntityMovement(cells, tic)
            
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
                LEVEL += 1
                break
        
            update(cells, LEVEL)
            tic += 1
        



def update(cells, LEVEL):
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
            dice = randint(0, 4)
            if dice == 0:
                pl.hp += randint(1,5)
            if dice == 1:
                pl.atk += randint(1,5)
            if dice == 2:
                pl.score += randint(1,5)
            if dice == 3:
                pl.defence += randint(1,5)

            
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
            for i in cells:
                if i.isEntity and i.type != 'player':
                   open_me = 0
                   break
            
            if open_me:
                cells.append(cell(i.x, i.y, "exit", fr=-1, solid=0))
                cells.remove(i)
        
        if i.type == 'boar' and tic%30 == 0:
            i.dir = randmov(cells, i)
        
        
        if i.type == 'griefer' and tic%50 == 0:
            cells.append(cell(i.x, i.y, celltype="boulder", fr=-1, solid=0))
            cells[-1].xdir = (1-2*(cells[0].x<i.x))*(cells[0].x != i.x)
            cells[-1].ydir = (1-2*(cells[0].y<i.y))*(cells[0].y != i.y)


        if i.type == 'boulder' and tic%10 == 0:
            i.x += i.xdir
            i.y += i.ydir
            
            if i.x >= cellnumber or i.y >= cellnumber or i.x < 0 or i.y < 0:
                cells.remove(i)
                continue
        
        if i.type == 'tanky':
            i.dir = 1-2*(cells[0].x < i.x)
            if randint(1, 100) == 1:
                randmov(cells, i)
            
            


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
            i.hp -= pl.atk
            cells.append(cell(i.x, i.y, "blood-hurt", fr=10, solid=0, one_cicle_animation=1))
            i.x -= pl.xdir
            i.y -= pl.ydir
            if i.hp <= 0:
                cells.remove(i)
            
            else:
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




def GameOver(lvl):
    
    while 1:
        for ev in g.event.get():
            if ev.type == g.QUIT:
                g.quit()
                exit(0)
            
            if ev.type == g.KEYDOWN:
                return
                
            
        screen.fill((50, 0, 0))
        
        if lvl == 'END':
        
            screen.blit(title_font.render("Congrats!", 0, (0, 255, 0)), (200, 100))
            screen.blit(font.render(f"You reached an end! New stuff soon! Go do something else now!", 0, (0, 255, 0)), (150, 200))
        
        else:
            screen.blit(title_font.render("Game Over!", 0, (0, 255, 0)), (100, 100))
            screen.blit(font.render(f"Score: {lvl}", 0, (0, 255, 0)), (200, 200))
        
        screen.blit(font.render(f"press any key", 0, (0, 255, 0)), (200, 300))
        
        g.display.flip()
        clock.tick(60)




while 1:
    menu()
    GameOver(main())