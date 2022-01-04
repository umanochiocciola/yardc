from params import *
from cell import cell, afd

g.mixer.pause()

def GetTerrain():
    
    cells = []
    TYPE = 0
    types = ['wall', 'exit', 'wall?', 'blocked-exit', 'goblin', 'rat', 'boar', 'sokoban', 'griefer', 'tanky', 'spike', 'boss1']
    one = 1
    while one:
        for ev in g.event.get(): 
            
            if ev.type == g.QUIT:
                one = 0
                
            if ev.type == g.MOUSEBUTTONDOWN:
                x, y = g.mouse.get_pos()
                x = int(x/cellsize)
                y = int(y/cellsize)
                
                
                if (x, y) != (8, 8): # not spawn point
                        
                    
                    if ev.button in [1, 3]: # left and right
                        for i in cells:
                            if (i.x, i.y) == (x, y):
                                cells.remove(i)
                                break
                        
                        if ev.button == 1: # left
                            cells.append(cell(x, y, celltype=types[TYPE], fr=use_animation.get(types[TYPE], -1), solid=1*(types[TYPE] not in not_solid)))
                
                        
                
                
            if ev.type == g.KEYDOWN:
                if ev.key == g.K_RIGHT:
                    TYPE = (TYPE + 1) % len(types) 
                if ev.key == g.K_LEFT:
                    TYPE = (TYPE - 1) % len(types)
                
                if ev.key == g.K_RETURN:
                    one = 0
            
            
        update(cells, types[TYPE])       
    
    
    out = {}
    for i in cells:
        if i.type not in out:
            out[i.type] = []
        out[i.type].append((i.x, i.y))

    
    return out
    
def update(cells, selected):
    screen.fill((28,9,1))

    for i in cells:
        i.render(screen)
    
    GCOLOR = (157,190,0)
    for x in range(cellnumber):
        g.draw.line(screen, GCOLOR, (x*cellsize,0), (x*cellsize,screensize))
    
    for y in range(cellnumber):
        g.draw.line(screen, GCOLOR, (0, y*cellsize), (screensize, y*cellsize))
    
    
    screen.blit(font.render(f'selected: {selected}', 0, (0, 255, 0)), (10,10))
    
    g.display.flip()
    clock.tick(60)





cont = GetTerrain()
with open('out.json', 'w') as f:
    f.write(json.dumps(cont))

g.quit()