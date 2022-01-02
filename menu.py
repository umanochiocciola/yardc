import pygame as g

screen = g.display.set_mode((700, 700))
clock = g.time.Clock()

def menu():
        
        screen.fill((0,0,0))
        screen.blit(g.image.load('assets/Background.png'), (0,0))
        g.display.flip()
    
        while 1:
            for ev in g.event.get():
                if ev.type == g.QUIT:
                    g.quit()
                    quit()
                
                if ev.type == g.KEYDOWN:
                    if ev.key == g.K_m:
                        g.mixer.pause()
                    elif ev.key == g.K_u:
                        g.mixer.unpause()
                    else:
                        return
        
        
        clock.tick(60)


menu()