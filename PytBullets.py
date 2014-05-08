__author__ = 'Phi'
import pygame, math, sys,  random, math
from pygame.locals import *

import BulletSprite
import World
import ButtonMenu

# **********************************************************
class Game:

    def __init__(self ):

        self.cScreen = pygame.display.set_mode((1024, 768))
        self.cClock  = pygame.time.Clock()

        self.cSoundUse = True

        if self.cSoundUse :
            self.cSoundOn = True
        else:
            self.cSoundOn = False


        if self.cSoundUse :

            self.cMixer     = pygame.mixer.init(44100, -16, 2, 4096)

            if self.cMixer == None:
                self.cSoundUse = self.cSoundOn = False
            

        if self.cSoundUse == False:

            self.cSoundFire = None
            self.cSoundPut =None
            self.cSoundScroll = None
            
            self.cSoundDestroy = None
            self.cSoundGameWin = None
            self.cSoundGameOver = None
        else:
            print "MaxChannel:" , pygame.mixer.get_num_channels()


            self.cSoundFire = pygame.mixer.Sound( "Fire.wav" )
            self.cSoundPut = pygame.mixer.Sound( "Put.wav" )
            self.cSoundScroll = pygame.mixer.Sound( "Scroll.wav" )
            
            self.cSoundDestroy = pygame.mixer.Sound( "Destroy.wav" )
            self.cSoundGameWin = pygame.mixer.Sound( "GameWin.wav" )
            self.cSoundGameOver = pygame.mixer.Sound( "GameOver.wav" )
            



        self.cWorld = World.World(self);
        self.cRect  =  self.cScreen.get_rect()
        self.cBullet = BulletSprite.BulletSprite( random.randint( 1, self.cWorld.MAX_BULLET_TYPE ), self.cWorld )
        
        self.cNextBullet = BulletSprite.BulletSprite( random.randint( 1, self.cWorld.MAX_BULLET_TYPE ), self.cWorld )
              
      
        self.cBulletGroup = pygame.sprite.RenderPlain(self.cBullet)

        self.cMemMousePos = (0.0,0.0);

        self.resetGame()

        #====================================

    def resetGame( self ):

        self.cBullet = BulletSprite.BulletSprite( random.randint( 1, self.cWorld.MAX_BULLET_TYPE ), self.cWorld )
        
        self.cNextBullet = BulletSprite.BulletSprite( random.randint( 1, self.cWorld.MAX_BULLET_TYPE ), self.cWorld )
              
      
        self.cBulletGroup = pygame.sprite.RenderPlain(self.cBullet)

        self.cMemMousePos = (0.0,0.0);

        self.cWorld.resetWorld()

        self.restart = False
     
        #====================================
    def playSound( self, pSound, pLoops=0, pMaxtime=0, pFade=0 ):
        
        if self.cSoundOn and pSound != None:
            pSound.play( pLoops, pMaxTime, pFade )
            
        #====================================
    def stopSound( self, pSound ):
        a =0
     #   if self.cSoundOn and pSound != None:
      #      pSound.stop()
     
       #====================================
    def fadeOutSound( self, pSound, pFade ):
        a=0
    #    if self.cSoundOn and pSound != None:
     #y       pSound.stop()
     
        #====================================

    def execEvent( self ):
          
        for lEvent in pygame.event.get():
            if lEvent.type == pygame.MOUSEMOTION:
                if self.cWorld.cState == self.cWorld.STATE_TARGET:
                    # on est en mode viseur, on fait bouger le vecteur
                    self.cMemMousePos = lEvent.pos
                    continue
#                    return True
                    
            elif lEvent.type == pygame.MOUSEBUTTONDOWN and self.cWorld.cState == self.cWorld.STATE_TARGET:
                # -----------------------------
                # on teste si on a clique sur un boutons de commande
                if self. cWorld.cListButton.testExec( lEvent.pos ) == True :
                    # yes !
                    if self.restart == True :
                        return False
                    continue


                self.cWorld.cState = self.cWorld.STATE_FIRE
                self.cBullet.cMoving = True

                self.playSound( 0, 10, 3) 

                self.cWorld.cTurn += 1

                lDiffX = lEvent.pos[0]-self.cBullet.cNewPosition[0]
                lDiffY = lEvent.pos[1]-self.cBullet.cNewPosition[1]


                if lDiffY > -self.cWorld.BULLET_H :
                    lDiffY =  -self.cWorld.BULLET_H 

                
                self.cMemMousePos = (lDiffX, lDiffY)
                lNorm = math.sqrt( self.cMemMousePos[0]*self.cMemMousePos[0]+self.cMemMousePos[1]*self.cMemMousePos[1]);
                
                
                self.cBullet.cSpeedX = self.cMemMousePos[0] / (lNorm)  
                self.cBullet.cSpeedY = self.cMemMousePos[1] / (lNorm)
                
                    
                    
                # -----------------------------
                # on teste si on a appuyer sur une touche 
            elif hasattr( lEvent, 'key'):                            
                if lEvent.key == K_UP:
                    self.cWorld.cState = STATE_TARGET
                    self.cBulletGroup.empty()
                    self.cBullet = BulletSprite.BulletSprite( self.cWorld.getRandomBullet(), gWorld )
# random.randint( 1, gWorld.MAX_BULLET_TYPE ), gWorld )
                    self.cBulletGroup.add(self.cBullet)
                    #    pBullet.init(  random.randint( 1, gWorld.MAX_BULLET_TYPE), gWorld )

                elif lEvent.key == K_r:
                    self.cWorld.flipMemTabBullet()

                elif lEvent.key == K_ESCAPE:
                    sys.exit(0)


    
        #====================================

                    
    def run(self):

            # USER INPUT

            self.cDeltaTime = self.cClock.tick(50)


            # ====================
            if self.cWorld.cState == self.cWorld.STATE_GAME_STOP:
                sys.exit()

            # ====================
            
            else :  



                # ============== Winner ? ==============
                if self.cWorld.countAllBullet() == 0:
                
                    print "GameWin Game" 
                    self.cWorld.gameWinAnimation( 300 )
                    self.restart = True
                    return False


                # Scrolling ? 
                if self.cWorld.cShotRemain <= 0 :
                    

                    self.cWorld.countBulletType()

                    self.cWorld.cShotRemain = self.cWorld.MAX_SHOT


                    lResult = self.cWorld.scrollDownRange();

                    # ============= Game Over ? =============
                    if lResult == False :                        
                        print "GameOver" 
                        self.cWorld.gameOverAnimation( 200 )
                        self.restart = True
                        return False



                lMemMovingState =  self.cBullet.cMoving 

                if  self.execEvent() == False:
                    return False
                


                # We return to target mode where bullet has finish to move
                if self.cWorld.cState == self.cWorld.STATE_FIRE and  self.cBullet.cMoving == False:
                    self.cWorld.cState = self.cWorld.STATE_TARGET
                    self.playSound( self.cSoundPut ) 

                    # new bullet
                    self.cBulletGroup.empty()
                    self.cBullet = self.cNextBullet;
                    self.cBulletGroup.add(self.cBullet)
                    self.cNextBullet = BulletSprite.BulletSprite( self.cWorld.getRandomBullet(), self.cWorld ) 
    

        

            if  self.cWorld.cState == self.cWorld.STATE_TARGET or self.cWorld.cState == self.cWorld.STATE_FIRE:
                self.cBulletGroup.update( self.cDeltaTime, self.cRect )  # call the resolution of world
                

            return True
 
        
# RENDERING
    def render( self ):         
               
        self.cScreen.fill((150, 150, 150))

        if self.cWorld.cState == self.cWorld.STATE_TARGET:
            self.cWorld.drawVector( self.cScreen, self.cMemMousePos);   
                         

        self.cWorld.draw( self.cScreen )
        self.cWorld.drawScoreNextMenu( self.cScreen, self.cNextBullet )
        self.cBulletGroup.draw( self.cScreen )

        return True

        #====================================

# **********************************************************

# MAIN

lGame = Game()

while 1 :
    while lGame.restart == False:           
        if lGame.run() == True :
            if lGame.render() == True :
                pygame.display.flip()

    lGame.restart = False
    lGame.resetGame()
