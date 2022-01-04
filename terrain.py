import random as r

def DEBUG(stuff):
    #print(stuff)
    0


spawnrate = {
    # enemy    ( max times to be spawned     min level     max level{-1=no limit} )
    "goblin" : (3, 0, -1),
    "rat"    : (6, 0, -1),
    "boar"   : (5, 10, -1),
    "griefer": (3, 15, -1),
    "tanky"  : (3, 20, -1),
    "spike"  : (4, 20, -1)
    
    
}




def GetTerrain(ox, oy, maxX, maxY, lvl):
    
    #with open('cringe', 'w') as f: f.write('----------\n')
    
    walls = []
    for y in range(maxY):
        walls.extend([(x, y) for x in range(maxX)])
    #print(walls)
    
    # start position is (ox, oy)
    # generate 5x5 starting room centered in (20, 10)
    DEBUG('first room')
    carve_room(walls, ox-2, oy-2, 5, 5)
    
    # create paths paths to random points
    DEBUG('first paths')
    pathed = path_out(ox, oy, maxX, maxY)
    all_paths = []; all_paths.extend(pathed)
    
    new_pathed = []
    
    rooms = [(ox, oy)]
    
    for i in range(4):
        for x, y in pathed:
            
            if not r.randint(0,5):
            #if not r.randint(0, 5):
                DEBUG('carving new room')
                carve_room(walls, x, y, r.randint(2, 10), r.randint(2, 6))

            else:
                DEBUG(f'path branch number {i}')
                new_pathed = path_out(x, y, maxX, maxY, low=1, high=4)
                
        all_paths.extend(new_pathed)
        pathed = new_pathed
    
    
    for path in all_paths:
        try: walls.remove(path)
        except: 0 #tile already carved
    
    
    
    upgrades = []
    for i in range(r.randint(0, 4)):
        upgrades.append(r.choice(all_paths))
    
    
    
    end = r.choice(all_paths)
    
    OUT = {"wall": walls, "exit": [end], "upgrade": upgrades}
    
    for i in spawnrate:
        chance, m, M = spawnrate[i]
        
        #print('spawning', i+'s')
        
        if lvl >= m and (lvl < M or M==-1):
            cat = []
            for j in range(r.randint(0, chance)):
                cat.append(r.choice(all_paths))
            
            #print(cat)
            
            OUT[i] = cat
    
    
    return OUT

    
def carve_room(out, x, y, w, h):
    while x+w >= len(out[0]):
        w-=1
    for i in range(h):
        if y+i < len(out):
            try:
                [out.remove((x+j, y+i)) for j in range(w)]
            except: 0 #tile already carved

def average(lst): return sum(lst)/len(lst)

def path_out(x, y, maxX, maxY, low=2, high=10):
    pathed = []
    for i in range(r.randint(low, high)):
        tx, ty = (r.randint(0, maxX-1), r.randint(0, maxY-2))

        # create path to tx, ty
        while (x, y) != (tx, ty):
            pathed.append((x, y))
                                                                      # to jazz up
            if x>tx:
                x-=1
                continue
            if y>ty:
                y-=1
                continue
            elif y<ty:
                y+=1
                continue
            elif x<tx:
                x+=1
                continue
        
    return pathed
