__author__ = 'Phi'
import pygame, math, sys,  random, math
from pygame.locals import *

import BulletSprite
import World
import ButtonMenu

gScreen = pygame.display.set_mode((1024, 768))
gClock = pygame.time.Clock()



# =============  MAIN ==============

gWorld = World.World();
gRect = gScreen.get_rect()
gBullet = BulletSprite.BulletSprite( random.randint( 1, gWorld.MAX_BULLET_TYPE ), gWorld )

gNextBullet = BulletSprite.BulletSprite( random.randint( 1, gWorld.MAX_BULLET_TYPE ), gWorld )
              
      
gBulletGroup = pygame.sprite.RenderPlain(gBullet)

gStateFire   = False;
gMemMousePos = (0.0,0.0);


lGameFinish = False

gWorld.cGameFinish = 20
while 1:
    # USER INPUT

    lDeltaTime = gClock.tick(50)

    
    if gWorld.cGameFinish != 0 :
        gWorld.gameOverAnimation(gScreen);
        if gWorld.cGameFinish  == 1:
            gWorld.resetGame()
        continue
    
    if gWorld.cDestroyAnimation != 0 :
        gWorld.destroyAnimation();
    else :        
        if gWorld.cShotRemain <= 0 :
            gWorld.countBulletType()

            gWorld.cShotRemain = gWorld.MAX_SHOT
            lResult = gWorld.shiftDownRange();
            if lResult == False :
                gWorld.cGameFinish = 200
                continue
            else:
                a = 0

                    
        for lEvent in pygame.event.get():
            if lEvent.type == pygame.MOUSEMOTION:
                print "mouse" 
                if gStateFire == False:
                    # on est en mode vieur, on fait bouger le vecteur
                    gMemMousePos = lEvent.pos
                    
                    
                    print "gMemMousePos", gMemMousePos
                    
                    
            elif lEvent.type == pygame.MOUSEBUTTONDOWN and gStateFire == False:


                if gWorld.cListButton.testExec( lEvent.pos ) == True :
                    continue



                gStateFire = True

                gWorld.cTurn += 1

                lDiffX = lEvent.pos[0]-gBullet.cNewPosition[0]
                lDiffY = lEvent.pos[1]-gBullet.cNewPosition[1]

                print ">>>>>>>>>>>Bullet fire " , lDiffY , " eventy:" , lEvent.pos[1] ," Pos:" , gBullet.cNewPosition[1]

                if lDiffY > -gWorld.BULLET_H :
                    print ">>>>>>>>>>>Bullet fire " , gWorld.BULLET_H 
                    lDiffY =  -gWorld.BULLET_H 

                
                gMemMousePos = (lDiffX, lDiffY)
                lNorm = math.sqrt( gMemMousePos[0]*gMemMousePos[0]+gMemMousePos[1]*gMemMousePos[1]);
                
                print "lNorm ", gMemMousePos
                
                gBullet.cSpeedX = gMemMousePos[0] / (lNorm)  
                gBullet.cSpeedY = gMemMousePos[1] / (lNorm)
                
                print "cSpeedX ", gBullet.cSpeedX, " cSpeedY ", gBullet.cSpeedY
                    
                    
                    
            elif hasattr( lEvent, 'key'):                            
                if lEvent.key == K_UP:
                    gStateFire = False
                    gBulletGroup.empty()
                    gBullet = BulletSprite.BulletSprite( gWorld.getRandomBullet(), gWorld )
# random.randint( 1, gWorld.MAX_BULLET_TYPE ), gWorld )
                    gBulletGroup.add(gBullet)
                    #    gBullet.init(  random.randint( 1, gWorld.MAX_BULLET_TYPE), gWorld )

                elif lEvent.key == K_r:
                    gWorld.flipMemTabBullet()

                elif lEvent.key == K_ESCAPE:
                    sys.exit(0)
                        
# RENDERING
                        
    gScreen.fill((150, 150, 150))
    gBulletGroup.update( lDeltaTime, gRect )

    if gStateFire == True and gBullet.cInternalState == False:
        gStateFire = False

        
     #   gBullet.init(  random.randint( 1, gWorld.MAX_BULLET_TYPE), gWorld )

    
        # new bullet
        gBulletGroup.empty()
        gBullet = gNextBullet;
        gBulletGroup.add(gBullet)
        gNextBullet = BulletSprite.BulletSprite( gWorld.getRandomBullet(), gWorld ) # random.randint( 1, gWorld.MAX_BULLET_TYPE ), gWorld )
        continue

    if gStateFire == False:
        gWorld.drawVector( gScreen, gMemMousePos);                            

    gWorld.draw( gScreen )
    gWorld.drawScoreNextMenu( gScreen, gNextBullet )
    gBulletGroup.draw( gScreen )
    pygame.display.flip()

    

    
