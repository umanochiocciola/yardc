from params import *
from cell import cell
from random import randint, choice
    

def boss_1(cells, boss):
    if 'boss1' not in bossdata:
        bossdata['boss1'] = {
            
            "shot": 0,
            "last": 0
            
            }
    
    data = bossdata['boss1']
    log(data)
    #print(data)
    if data['shot'] <= 32:
        if data['last']==0:
            data['last'] = randint(30, 60)
            data['shot'] += 1
            
            vdir = choice([0, 1])
            
            cells.append(cell(randint(6, 10), 2+12*vdir, celltype="boulder", fr=-1))
            cells[-1].ydir = 1-2*vdir 
            cells[-1].atk = 10

            
        else:
            data['last'] -= 1
    
    
    else:
        for i in cells:
            if i.type == 'fake-wall':
                cells.remove(i)
    
    
    
def boss_2(cells, boss):
    if 'boss2' not in bossdata:
        bossdata['boss2'] = {
            "phase": 0,
            "deployed": 0,
            "stood": 0,
            "target" : (boss.x, boss.y),
            
            }
    
    data = bossdata['boss2']
    
    #print(data['phase'])
    
    if data['phase']:
        
        data['stood'] += 1
        if data['stood'] >= 200:
            data['phase'] = 0
            data['stood'] = 0
    
    else:
        
        if (boss.x, boss.y) == data["target"]:
            data["target"] = (randint(0, cellnumber-1), randint(0, cellnumber-1))
            
            placeable = 1
            for i in cells:
                if (i.x, i.y) == (boss.x, boss.y) and i.solid:
                    placeable = 0
                    break
            
            if placeable:
                cells.append(cell(boss.x, boss.y, celltype="Xboar", fr=use_animation['boar'], solid=0))
                data['deployed'] += 1
                if data['deployed'] == randint(5, 10):
                    data['deployed'] = 0
                    data['phase'] = 1
        
        else:
            
            tx, ty = data["target"]
            
            #print(tx, ty, ' ', boss.x, boss.y)
            
            boss.x += (1-2*(tx<boss.x))*(tx != boss.x)
            boss.y += (1-2*(ty<boss.y))*(ty != boss.y)
            



def boss_3(cells, boss):
    
    for i in cells:
        if i.type == 'teleport-enter':
            return
    
    for i in cells:
        if i.type == 'fake-wall':
            cells.remove(i)
    
    
    
    
    if 'boss3' not in bossdata:
        bossdata['boss3'] = {
            "shield": 1,
            "unshielded": 0,
            
            "show shield": 0,
            
            }
    
    data = bossdata['boss3']
    
    #print(data)
    
    if data['shield']>1:
        data['shield'] -= 1
        
        if not data['show shield']:
            data['show shield'] = 1
            cells.append(cell(boss.x, boss.y, 'shield', fr=-1))
        
    else:
        if data['unshielded']:
            data['unshielded'] -= 1    
        elif data['shield']:
            data['shield'] = 0
            data['show shield'] = 0
            for i in cells:
                if i.type == 'shield':
                    cells.remove(i)
                    break
            
            data['unshielded'] = randint(100, 300)
        
        else:
            data['shield'] = randint(100, 300)
            
        # move    
        
        if not randint(0, 50):
            boss.x += choice([-1, 1])
            if boss.x >= cellnumber-8:
                boss.x -= 1
            if boss.x < 8:
                boss.x += 1
                
        
        # check shot
        for i in cells:
            if i.type == 'shot' and (i.x, i.y) == (boss.x, boss.y):
                boss.hp -= 1
                if boss.hp <= 0:
                    cells.remove(boss)
                    return

    
    if not randint(0, 20+10*bool(data["unshielded"])):
        cells.append(cell(randint(6, cellnumber-7), 10, 'boulder', fr=-1))
        cells[-1].ydir = 1
        cells[-1].atk = 10
    
    if not randint(0, 20+bool(data["unshielded"])):
        cells.append(cell(randint(6, cellnumber-7), 10, 'bomb', fr=-1))
        cells[-1].ydir = 1
    







