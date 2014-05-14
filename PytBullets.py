__author__ = 'Phi'
import pygame, math, sys,  random, math,  getopt

from pygame.locals import *

import BulletSprite
import World

# **********************************************************
class Game:

    def usage(self):
        print "Pytbullet 2014 (ppoupon@free.fr)"
        print " [-h/help] "
        print " [x/hex]                       use hex map        : default"
        print " [o/oct]                       use octogonal map"
        print " [w:size/width=size]           columns number     : default = 17" 
        print " [l:size/lines=size]          lines number       : default = 15" 
        print " [s:size/bullet_size=size]     bullets size       : default = 40"
        print " [f:size/frame=size]           frame rate         : default = 50"
        print " [i:size/init_fill_lines=size] initial fill lines : default =  9"
        
        
# ===========================================

    def __init__(self, pArgv ):
            
            
        try:
            lOpts, lArgs = getopt.getopt( pArgv, "hd:sxow:l:b:f:c:i:m:", 
                                          ["help","debug:=","sound","hex","oct","width=","lines=","bullet_size=","frame=", "colors=", "init_fill_lines=", "max_shot="])
            
        except getopt.GetoptError: 
            self.usage()
            sys.exit(2)   

        lDebug =False
        self.cSoundUse = False
        lModeHex = True;
        lColumns = 17
        lLines   = 15
        lBulletSize = 40
        self.cFrame = 50
        lInitFillLines=9
        lColors=6
        lMaxShot=8
                                          
        for lOpt, lArg in lOpts: 
      #      print "Op:", lOpt , " Arg=", lArg
            if lOpt in ("-h", "--help"):
                self.usage()                     
                sys.exit()  
            elif lOpt in ("-x", "--hex"):
                lModeHex = True                
            elif lOpt in ("-s", "--sound"):
                self.cSoundUse= True                
            elif lOpt in ("-o", "--oct"):
                lModeHex = False
            elif lOpt in ("-d", "--debug"):
                lDebug = int(lArg)
            elif lOpt in ("-w", "--width"):
                lColumns = int(lArg)
                if lColumns < 5 or lColumns > 100 :
                    print "Bad lColumn number ", lColumns
                    sys.exit(2)

            elif lOpt in ("-l", "--lines"):
                lLines = int(lArg)
                if  lLines < 5 or lLines > 100 :
                    print "Bad line number ", lLines
                    sys.exit(2)
            elif lOpt in ("-b", "--bullet_size"):
                lBulletSize = int(lArg)
                if lBulletSize < 3 or lBulletSize > 100:
                    print "Bad bullet size ", lBulletSize
                    sys.exit(2)
            elif lOpt in ("-f", "--frame"):
                lFrame  = int(lArg)
                if lFrame >= 20 and lFrame <= 100 :
                    self.cFrame = lFrame
                else:
                    print "Bad Frame rate ", lFrame
                    sys.exit(2)        
            elif lOpt in ("-c", "--colors"):
                lColors  = int(lArg)
                if lColors< 2 or lColors > 12 :
                    print "Bad colors number ", lColors
                    sys.exit(2)        
            elif lOpt in ("-i", "--init_fill_lines"):
                lInitFillLines  = int(lArg)
                if lInitFillLines< 2 or lInitFillLines > lLines-2 :
                    print "Bad init fill lines number ", lInitFillLines
                    sys.exit(2)        
      
            elif lOpt in ("-m", "--max_shot"):
                lMaxShot  = int(lArg)
                if lMaxShot < 2 or  lMaxShot> 12 :
                    print "Bad Max Shot ", lMaxShot
                    sys.exit(2)        
      

                


        self.initSound()


        self.cScreen = pygame.display.set_mode((1024, 768))
        self.cClock  = pygame.time.Clock()


        self.cWorld = World.World( self, lDebug, lModeHex, lColumns, lLines, lBulletSize, lColors, lInitFillLines, lMaxShot);
        
        self.cRect  =  self.cScreen.get_rect()
        self.cBullet = BulletSprite.BulletSprite( random.randint( 1, self.cWorld.MAX_BULLET_TYPE ), self.cWorld )
        
        self.cNextBullet = BulletSprite.BulletSprite( random.randint( 1, self.cWorld.MAX_BULLET_TYPE ), self.cWorld )
              
      
        self.cBulletGroup = pygame.sprite.RenderPlain(self.cBullet)

        self.cMemMousePos = (0.0,0.0);

        self.resetGame()

        #====================================

        
    def initSound( self ):

        if self.cSoundUse :
            self.cSoundOn = True
        else:
            self.cSoundOn = False


        if self.cSoundUse :

    #        self.cMixer     = pygame.mixer.init(44100, -16, 2, 4096)
            self.cMixer     = pygame.mixer.init()

            if self.cMixer == None:
                self.cSoundUse = self.cSoundOn = False
                print "Sound initialization failed ! ", pygame.get_error()

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
                if lEvent.key == K_UP and lEvent.type == pygame.KEYDOWN:
                    self.cWorld.cState = self.cWorld.STATE_TARGET
                    self.cBulletGroup.empty()
                    self.cBullet = BulletSprite.BulletSprite( self.cWorld.getRandomBullet(), self.cWorld )
                    self.cBulletGroup.add(self.cBullet)

                elif lEvent.key == K_r:
                    self.cWorld.flipMemTabBullet()

                elif lEvent.key == K_h and lEvent.type == pygame.KEYDOWN:
                        self.cWorld.cModeHex = not self.cWorld.cModeHex

                elif lEvent.key == K_ESCAPE:
                    sys.exit(0)
            elif lEvent.type == pygame.QUIT:
                sys.exit(0)


    
        #====================================

                    
    def run(self):

            # USER INPUT

            self.cDeltaTime = self.cClock.tick( self.cFrame )


            # ====================
            if self.cWorld.cState == self.cWorld.STATE_GAME_STOP:
                sys.exit()

            # ====================
            
            else :  



                # ============== Winner ? ==============
                if self.cWorld.countAllBullet() == 0:
                
             #       print "GameWin Game" 
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
             #           print "GameOver" 
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

pygame.init()

lGame = Game( sys.argv[1:] )

while 1 :
    while lGame.restart == False:           
        if lGame.run() == True :
            if lGame.render() == True :
                pygame.display.flip()

    lGame.restart = False
    lGame.resetGame()

    if lGame.cSoundUse:
        pygame.mixer.quit()
