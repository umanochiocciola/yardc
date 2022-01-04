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
    #print(data)
    if data['shot'] <= 32:
        if data['last']==0:
            data['last'] = randint(20, 100)
            data['shot'] += 2
            #print(' attacked')
            cells.append(cell(randint(6, 10), 2, celltype="boulder", fr=-1))
            cells[-1].ydir = 1
            cells[-1].atk = 10
            
            cells.append(cell(randint(6, 10), 14, celltype="boulder", fr=-1))
            cells[-1].ydir = -1
            cells[-1].atk = 10
            
        else:
            data['last'] -= 1
    
    
    else:
        for i in cells:
            if i.type == 'wall?':
                cells.remove(i)
    
    
    
        
            
    