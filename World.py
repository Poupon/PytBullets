
# __author__ = 'Phi'
import pygame, math, sys,  random, math
from pygame.locals import *


import ButtonMenu

gScreen = pygame.display.set_mode((1024, 768))



# ******************************************

class World:
    BULLET_W = 40
    BULLET_H = 40

    HEIGHT =  14
    WIDTH  = 17
    INIT_HEIGHT = 9

    MAX_BULLET_COLOR = 6
    
    INIT_FIRE_POSW = WIDTH/2

    INIT_FIRE_POSH = HEIGHT-1
    INIT_FIRE_POS  = ( INIT_FIRE_POSW, INIT_FIRE_POSH)

    MAX_SHOT =  6

    pygame.font.init()

    StrMyFont = pygame.font.get_default_font()
    myFont =pygame.font.SysFont(StrMyFont,32)
#       myFont = pygame.font.Font(None, 30)


    STATE_GAME_STOP = 0
    STATE_FIRE=4
    STATE_TARGET = 10
    
    


    cState=STATE_TARGET
    

    cDialogOk = False

        #-----------------------------------------
    def __init__(self, pGame ):

        World.sTheWorld = self

        self.cGame = pGame


        self.cDestroyedBulletSurf =   pygame.transform.scale( pygame.image.load( 'Iridescent.png'),(self.BULLET_W, self.BULLET_H))
        self.cVoidBulletSurf =   pygame.transform.scale( pygame.image.load( 'Ice.png'),(self.BULLET_W, self.BULLET_H))
        self.cBullet =[ 0, # pygame.image.load( 'Ice.png'),
                        pygame.transform.scale( pygame.image.load( 'Green.png'), (self.BULLET_W, self.BULLET_H)),
                        pygame.transform.scale( pygame.image.load( 'Indigo.png'),(self.BULLET_W, self.BULLET_H)),
                        pygame.transform.scale( pygame.image.load( 'Magenta.png'),(self.BULLET_W, self.BULLET_H)),
                        pygame.transform.scale( pygame.image.load( 'Red.png'),(self.BULLET_W, self.BULLET_H)),
                        pygame.transform.scale( pygame.image.load( 'Teal.png'),(self.BULLET_W, self.BULLET_H)),
                        pygame.transform.scale( pygame.image.load( 'Yellow.png'),(self.BULLET_W, self.BULLET_H)),

                        pygame.transform.scale( pygame.image.load( 'Silver.png'),(self.BULLET_W, self.BULLET_H)),
                        pygame.transform.scale( pygame.image.load( 'Crimson.png'),(self.BULLET_W, self.BULLET_H)),
                        pygame.transform.scale( pygame.image.load( 'Moss.png'),(self.BULLET_W, self.BULLET_H)),
                        pygame.transform.scale( pygame.image.load( 'Clouds.png'),(self.BULLET_W, self.BULLET_H)),
                        pygame.transform.scale( pygame.image.load( 'Amber.png'),(self.BULLET_W, self.BULLET_H)),
                        pygame.transform.scale( pygame.image.load( 'Embriotic.png'),(self.BULLET_W, self.BULLET_H)),


                        self.cDestroyedBulletSurf,
                        self.cVoidBulletSurf
                        ]


        self.cGameOver =   pygame.image.load( 'game_over.gif')
        self.cYouWin =   pygame.image.load( 'you_win.gif')

        
        self.cDestroyedBullet = self.cBullet.index( self.cDestroyedBulletSurf )
    
        self.MAX_BULLET_TYPE= len( self.cBullet)-3
        if self.MAX_BULLET_TYPE > self.MAX_BULLET_COLOR:
            self.MAX_BULLET_TYPE = self.MAX_BULLET_COLOR
        
        
        self.cBullW = self.cBullet[1].get_width()
        self.cBullH = self.cBullet[1].get_height()
        

        
        gScreen = pygame.display.set_mode( (self.cBullW*self.WIDTH, 
                                           ( self.cBullH+4)*self.HEIGHT) )

        gScreen.fill( (100,100,100) )

        self.yLinePrint = (self.cBullH+2)*self.HEIGHT
        self.yLineBullet = (int)(self.cBullH+1)*self.HEIGHT

        
        self.cDebug = False

        self.cDebugTabBullet = False

        self.cMemTabBullet = None

        self.resetWorld()



        self.cListButton = ButtonMenu.ButtonList();

        self.cButtonReset = ButtonMenu.ButtonMenu( self.myFont, "Reset", (gScreen.get_width()-200, self.yLinePrint),  (255,255,255), CallbackReset) 

        self.cListButton.append( self.cButtonReset );

        self.cButtonStop = ButtonMenu.ButtonMenu( self.myFont, "Stop", (gScreen.get_width()-100, self.yLinePrint),  (255,255,255),  CallbackStop) 

        self.cListButton.append( self.cButtonStop );

       #-----------------------------------------
       # make a copy of the TabBullet and return it
        
    def copyTabBullet( self ):

        lTmpTab = [[0] *self.WIDTH  for _ in range(self.HEIGHT)]
      
        for h in range(self.HEIGHT):
            for w in range(self.WIDTH):
               lTmpTab[h][w] = self.cTab[h][w] 
      
        return lTmpTab
       #-----------------------------------------
       # Reset game from the begining
    def resetWorld( self ):

        self.cScore = 0;
        self.cShotRemain = self.MAX_SHOT

        self.cState=self.STATE_TARGET

        self.cTurn = 0
        self.cMemTabBullet = None

        self.cTab = [[0] *self.WIDTH  for _ in range(self.HEIGHT)]
 
        self.cLifeType = [];

        for i in range( 1, self.MAX_BULLET_TYPE+1):
            self.cLifeType.append( i )


  
        for h in range(self.INIT_HEIGHT):
            self.randomRow( h );


    #    Game()

        self.cListButton = ButtonMenu.ButtonList();

        self.cButtonReset = ButtonMenu.ButtonMenu( self.myFont, "Reset", (gScreen.get_width()-200, self.yLinePrint),  (255,255,255), CallbackReset) 

        self.cListButton.append( self.cButtonReset );

        self.cButtonStop = ButtonMenu.ButtonMenu( self.myFont, "Stop", (gScreen.get_width()-100, self.yLinePrint),  (255,255,255),  CallbackStop) 

        self.cListButton.append( self.cButtonStop );

       #-----------------------------------------
       # make a copy of the TabBullet and return it
        
    def copyTabBullet( self ):

        lTmpTab = [[0] *self.WIDTH  for _ in range(self.HEIGHT)]
      
        for h in range(self.HEIGHT):
            for w in range(self.WIDTH):
               lTmpTab[h][w] = self.cTab[h][w] 
      
        return lTmpTab

        #-----------------------------------------
        #-----------------------------------------
        #-----------------------------------------

       #-----------------------------------------
       # Test if bullet is void bullet

    def isVoidBullet( self,  pBullet ):
        if pBullet == 0 or pBullet == self.cDestroyedBullet :
            return True
        return False

    def isFullBullet(self, pBullet ):
        return not isVoidBullet()

       #-----------------------------------------
    def getRandomBullet( self ):
        return self.cLifeType[ random.randint( 0, len( self.cLifeType)-1) ] 
       #-----------------------------------------
   
       # set random row 
    def randomRow( self, pRow ):
        for w in range(self.WIDTH):
     #       self.cTab[pRow][w] = random.randint( 1, self.MAX_BULLET_TYPE )
            self.cTab[pRow][w] = self.getRandomBullet() #  self.cLifeType[ random.randint( 0, len( self.cLifeType)-1) ] 

        #-----------------------------------------
    def randomFirstRow( self ):
        self.randomRow( 0 )
        #-----------------------------------------
                
    def get( self, pCoordWorld ) :
        return self.cTab[ pCoordWorld[1] ][ pCoordWorld[0]]
        
         #-----------------------------------------
    def set( self, pCoordWorld, pVal ) :
        self.cTab[ pCoordWorld[1] ][ pCoordWorld[0]] = pVal

    def setMem( self, pCoordWorld, pVal ) :
        if self.cMemTabBullet != None:
            self.cMemTabBullet[ pCoordWorld[1] ][ pCoordWorld[0]] = pVal
            
         #-----------------------------------------
    def safeGet( self, pCoordWorld ) :
        if self.outOfWorld( pCoordWorld ) :
            return 0

        return self.cTab[ pCoordWorld[1] ][ pCoordWorld[0]]
         #-----------------------------------------
    def getImage( self, pTypeColor ):
        return self.cBullet[pTypeColor];
      

         #-----------------------------------------
         # Translete Screen coordinate to World coordinate
    def screen2World( self, pCoordScreen ):        

  #      return ( ((int)((pCoordScreen[0]+self.cBullW/2)/self.cBullW)),
   #              ((int)((pCoordScreen[1]+self.cBullH/2)/self.cBullH))  )
        return ( ((int)((pCoordScreen[0])/self.cBullW)),
                 ((int)((pCoordScreen[1])/self.cBullH))  )

         #-----------------------------------------
         # Translete World  coordinate to Screencoordinate
    def world2Screen( self, pCoordWorld ):
#        return ((int)(pCoordWorld[0]*self.cBullW-self.cBullW/2),
#                (int)(pCoordWorld[1]*self.cBullH-self.cBullH/2))
        return ((int)(pCoordWorld[0]*self.cBullW+self.cBullW/2),
                (int)(pCoordWorld[1]*self.cBullH+self.cBullH/2))

        #-----------------------------------------
    def outOfWorld(  self, pCoordWorld ):

        if pCoordWorld[0] < 0 or pCoordWorld[0] >= self.WIDTH or  pCoordWorld[1] < 0 or pCoordWorld[1] >=  self.HEIGHT :
#            print 'outOfWorld ' ,  pCoordWorld
            return True
        return False
    
        #-----------------------------------------
    def outOfScreen(  self, pCoordScreen ):

        if pCoordScreen[0]-self.WIDTH/2 < 0 :
            return True

        lCoord = self.screen2World(pCoordScreen)
        return self.outOfWorld(lCoord ); 
    
        #-----------------------------------------
    def inScreen(  self, pCoordScreen ):
        return not self.outOfScreen( pCoordScreen );
    
        #-----------------------------------------
        # Detect if there is a bullet at World coordonate

    def isWorldVoid(  self, pCoordWorld ) :
        if self.outOfWorld( pCoordWorld ) :
            return True

        return  self.isVoidBullet( (self.cTab[ pCoordWorld[1] ][ pCoordWorld[0]]) )

    def isWorldFull(  self, pCoordWorld ) :
        return not self.isWorldVoid(pCoordWorld )
        #-----------------------------------------
        # Detect if there is a bullet at Screen coordonate
   
    def isScreenVoid(  self, pCoordWorld ) :

        lCoord = self.screen2World(pCoordScreen)
        return self.isWorldVoid( lCoord );

    def isScreendFull(  self, pCoordWorld ) :
        return not self.isScreenVoid(pCoordWorld )
 
        #-----------------------------------------
        #-----------------------------------------
        #------------------------------------
    def countAllBullet(self):

       lTotalCount =0
              
       for h in range(self.HEIGHT):
           for w in range(self.WIDTH):                
               if  self.get( (w, h) ) !=  0 :
                   lTotalCount += 1

       print "countAllBullet :", lTotalCount

       return lTotalCount

   #------------------------------------
 
    def countBulletType(self):


       lCountBullet = []
       for i in range(0,self.MAX_BULLET_TYPE+1):
           lCountBullet.append( 0 )
           
       for h in range(self.HEIGHT):
           for w in range(self.WIDTH):                
               lBulletType = self.get( (w, h) )
               if lBulletType !=  0 :
          #         print "lBulletType:",lBulletType
                   lCountBullet[ lBulletType ] += 1

       self.cLifeType = [];

       for i in range( self.MAX_BULLET_TYPE):
           if lCountBullet[i ] > 0:
               self.cLifeType.append( i )
       

#       for i in range(0,self.MAX_BULLET_TYPE+1):
#           print "countBulletType:", i , "=", lCountBullet[i ]
     
        #-----------------------------------------


    def draw(self, pSurfDest):
                    
        for h in range(self.HEIGHT):
            for w in range(self.WIDTH):
                lBullet = self.get( (w, h) )
                if lBullet !=  0 :
                    pSurfDest.blit( self.cBullet[lBullet], (w*self.cBullW, h*self.cBullH))

                # dessin des lignes pour le debuggage
#            pygame.draw.line( pSurfDest, ( 200, 200, 200), (0, h*self.cBullH), (self.cBullW*self.WIDTH, h*self.cBullH))

 #       pygame.draw.line( pSurfDest, ( 200, 200, 200), (0, self.HEIGHT*self.cBullH), (self.cBullW*self.WIDTH, self.HEIGHT*self.cBullH))
          
  #      for w in range(self.WIDTH):
#            pygame.draw.line( pSurfDest, ( 200, 200, 200), (w*self.cBullW, 0), (w*self.cBullW, self.cBullH*self.HEIGHT))


        #-----------------------------------------
  
    def drawScoreNextMenu( self, pSurfDest, pNextBullet):

        lX = 5
        str = "Score: %d  Turn: %d" % (self.cScore,  self.cTurn)
        textImg = self.myFont.render( str, 1, (255,0,0))

        pSurfDest.blit( textImg, (lX, self.yLinePrint) )

        lX += 250 

        lTypeBullet = self.cVoidBulletSurf
        for i in range( self.cShotRemain ):            
            if i==0:
                lTypeBullet = self.cBullet[pNextBullet.cTypeColor]
            else:
                lTypeBullet = self.cVoidBulletSurf

            pSurfDest.blit( lTypeBullet , (lX, self.yLineBullet))

            lX += self.BULLET_W

        self.cListButton.draw( pSurfDest )

        #-----------------------------------------
    def drawVector(self, pSurfDest, pMousePos):

        lDestWorldCoord  = self.screen2World( pMousePos );
        lDestScreenCoord = self.world2Screen( lDestWorldCoord );
        
        lInitScreenCoord = self.world2Screen( self.INIT_FIRE_POS);

        pygame.draw.line( pSurfDest, ( 200, 200, 200),  
                          lInitScreenCoord, lDestScreenCoord, 4)
            
         #-----------------------------------------
    def remplaceAll(self, pTarget, pNew):
        
        for h in range(self.HEIGHT):
            for w in range(self.WIDTH):
                if self.get( (w, h) ) == pTarget:
                    self.set( (w, h), pNew )
                

        #-------------------------------------------------------
        #-------------------- NEIGBOR --------------------------
        #-------------------------------------------------------

        # detecte s'il y a un groupe de plus de 2 boules de meme type

    def countNeighbor( self, lPos, pTypeColor ):
        lCount = 1
        
        NeightorPosList = [ (lPos[0]-1, lPos[1]-1 ), (lPos[0]+0, lPos[1]-1 ),(lPos[0]+1, lPos[1]-1 ),
                                     (lPos[0]-1, lPos[1] ),(lPos[0]+1, lPos[1] ),
                                     (lPos[0]-1, lPos[1]+1 ), (lPos[0]+0, lPos[1]+1 ), (lPos[0]+1, lPos[1]+1 )]

        AlreadyDo = [lPos]

        while len(NeightorPosList) > 0 and lCount< 3:

            lPos = NeightorPosList.pop() 
            
            try :
                index = AlreadyDo.index( lPos )
                continue
            except:
                AlreadyDo += lPos

            #    print "len:", len(NeightorPosList), " Count:", lCount, " Pos:", lPos

                if self.safeGet( lPos ) == pTypeColor:
                    lCount+=1
                    NeightorPosList += ( (lPos[0]-1, lPos[1]-1 ), (lPos[0]+0, lPos[1]-1 ),(lPos[0]+1, lPos[1]-1 ),
                                         (lPos[0]-1, lPos[1] ),(lPos[0]+1, lPos[1] ),
                                         (lPos[0]-1, lPos[1]+1 ), (lPos[0]+0, lPos[1]+1 ), (lPos[0]+1, lPos[1]+1 ))

        return lCount
        #-----------------------------------------
        # detruit toutes les boules contigue a la position et de meme type

    def destroyNeighbor( self, lPos, pTypeColor, pDestroyedBullet ):

        lScore = 0


        NeightorPosList = [ (lPos[0]-1, lPos[1]-1 ), (lPos[0]+0, lPos[1]-1 ),(lPos[0]+1, lPos[1]-1 ),
                                     (lPos[0]-1, lPos[1] ),(lPos[0]+1, lPos[1] ),
                                     (lPos[0]-1, lPos[1]+1 ), (lPos[0]+0, lPos[1]+1 ), (lPos[0]+1, lPos[1]+1 )]

        AlreadyDo = [lPos]

        while len(NeightorPosList) > 0:
            lPos = NeightorPosList.pop() 

            try :
                index = AlreadyDo.index( lPos )
                continue
            except:   # on ne l'a pas trouve !
                AlreadyDo += lPos
                
#                print "len:", len(NeightorPosList), " Pos:", lPos

                if self.safeGet( lPos ) == pTypeColor:
                    self.set(lPos,  pDestroyedBullet )
                    lScore += 1
                    NeightorPosList += ( (lPos[0]-1, lPos[1]-1 ), (lPos[0]+0, lPos[1]-1 ),(lPos[0]+1, lPos[1]-1 ),
                                         (lPos[0]-1, lPos[1] ),(lPos[0]+1, lPos[1] ),
                                         (lPos[0]-1, lPos[1]+1 ), (lPos[0]+0, lPos[1]+1 ), (lPos[0]+1, lPos[1]+1 ))


        return lScore
      
        #-------------------------------------------------------
        #---------------------- HOLE ---------------------------
        #-------------------------------------------------------
                    
    def getHole( self, pCoordWorld ) :
        if self.outOfWorld( pCoordWorld ) :
            return 0
        return self.cHoleTab[ pCoordWorld[1] ][ pCoordWorld[0]]
        
         #-----------------------------------------
    def setHole( self, pCoordWorld, pVal ) :
        self.cHoleTab[ pCoordWorld[1] ][ pCoordWorld[0]] = pVal
            
          #-----------------------------------------
    def resolveHole( self,  pDestroyedBullet):

        lScore = 0
        # initialization
        self.cHoleTab = [[0] *self.WIDTH  for _ in range(self.HEIGHT)]
        
        for h in range(self.HEIGHT):
            for w in range(self.WIDTH):
                self.setHole( (w,h), 0 )



        NeightorPosList = []        
        AlreadyDo = []


        # first line initialized like the bullet first line
        for w in range(self.WIDTH):
            lPos = (w,0)
            
            if self.isWorldFull( lPos ) :
                self.setHole( lPos, 1)
                NeightorPosList += ( (lPos[0]-1, lPos[1]+1 ), (lPos[0]+0, lPos[1]+1 ), (lPos[0]+1, lPos[1]+1 ))              


        while len(NeightorPosList) > 0 :

            lPos = NeightorPosList.pop() 

            try :
                index = AlreadyDo.index( lPos )

                continue
            except:  # on ne l'a pas trouve !
              AlreadyDo.append( lPos )
              
              if self.isWorldFull( lPos) :
                  NeightorPosList += ( (lPos[0]-1, lPos[1]-1 ), (lPos[0]+0, lPos[1]-1 ), (lPos[0]+1, lPos[1]-1 ),
                                       (lPos[0]-1, lPos[1] ),(lPos[0]+1, lPos[1] ),
                                       (lPos[0]-1, lPos[1]+1 ), (lPos[0]+0, lPos[1]+1 ), (lPos[0]+1, lPos[1]+1 ))      
                  self.setHole( lPos, 1)

        
        # repercute the result to the bullet tab
        for h in range(1,self.HEIGHT):
            for w in range(self.WIDTH):
                if self.getHole((w,h)) == 0 and self.isWorldFull( (w,h)):
                    self.set( (w,h),  pDestroyedBullet )
                    lScore +=1


        return lScore
         
        #-------------------------------------------------------
        #-------------------------------------------------------
        #-------------------------------------------------------

        # decale le tableau d'une ligne vers le bas et detecte s'il y a debordement:partie perdue

        # detect if there are an bullet at the last line -> lose 

    def scrollDownOneRow( self ):

        print "scrollDownOneRow"
        # detect if there are an bullet at the last line -> lose 
        for w in range(self.WIDTH):
            lBullet = self.get( (w, self.HEIGHT-1) )
            if lBullet != 0 :
                return False
                                    
        for h in range(self.HEIGHT-2, -1, -1):
            for w in range( self.WIDTH ):
                self.set( (w, h+1), self.get( (w, h) ))                          
        return True

     
         #-----------------------------------------
    def scrollDownRows( self, nb ):

        print "scrollDownRows " , nb
        for i in range( 0, nb):
            if self.scrollDownOneRow() == False:
                return False
            else:
                self.randomFirstRow()
  
        return True
       #-----------------------------------------
    
    def scrollDownRange( self ):

        print "scrollDownRange"

        self.cGame.playSound( self.cGame.cSoundScroll )

        lVal =  self.scrollDownRows( (self.MAX_BULLET_TYPE+1) - len( self.cLifeType ))
       
        self.cGame.fadeOutSound( self.cGame.cSoundScroll, 10 )
                                
        return lVal

        #-----------------------------------------
    def resolveMoving( self, pBullet ):

        
        lWorldPos = self.screen2World( pBullet.cNewPosition )

     #   print " 0 resolveMoving :", self.cShotRemain 

        
        if  lWorldPos[1] < 0 :
            lWorldPos = (lWorldPos[0] ,0)
            self.cShotRemain -= 1;
            self.set( lWorldPos, pBullet.cTypeColor )
            return False

        
        if self.isWorldVoid( lWorldPos ):
            return True # on continue de bouger
        

        lWorldPos = self.screen2World( pBullet.position ) # la derniere position        

        if  lWorldPos[1] < 0 :
            lWorldPos = (lWorldPos[0],0)
            self.cShotRemain -= 1;
            self.set( lWorldPos, pBullet.cTypeColor )
            return False
   

        lCount = self.countNeighbor( lWorldPos, pBullet.cTypeColor )        

        if lCount >= 3 :
            self.cMemTabBullet = self.copyTabBullet()
            self.setMem( lWorldPos, pBullet.cTypeColor )

            self.cScore += self.destroyNeighbor(  lWorldPos, pBullet.cTypeColor, self.cDestroyedBullet)     
            self.set( lWorldPos, self.cDestroyedBullet )
            self.cScore += self.resolveHole(  self.cDestroyedBullet )


            self.destroyAnimation(10  )

            self.remplaceAll( self.cDestroyedBullet, 0 )

        else: 
            self.cShotRemain -= 1;
            self.set( lWorldPos, pBullet.cTypeColor )

        return False

        #-----------------------------------------
    def flipMemTabBullet( self ):
        lMem = self.cTab
        self.cTab = self.cMemTabBullet
        self.cMemTabBullet = lMem
    
        #-----------------------------------------
    def destroyAnimation( self, pNb ):

        self.cGame.playSound( self.cGame.cSoundDestroy  )

        for i in range( pNb ):
            self.flipMemTabBullet()
            self.cGame.render()
            pygame.display.flip()

        self.cGame.fadeOutSound( self.cGame.cSoundDestroy, 10  )

        #-----------------------------------------
    def gameOverAnimation( self,  pNb ):

        self.cGame.playSound( self.cGame.cSoundGameOver, 4  )
 
        lSurf = self.cGameOver
        
        lPoint = ((gScreen.get_width()/2)-self.cGameOver.get_width()/2, 
                      (gScreen.get_height()/2-self.cGameOver.get_height()/2))

        lRect  = pygame.Rect( lPoint, self.cGameOver.get_size() )
        
        lListButton = ButtonMenu.ButtonList();
        lListButton.append(  ButtonMenu.ButtonMenu( self.myFont, "Ok", lPoint,  (255,255,255), CallbackOk) )

        self.cDialogOk = False


        while self.cDialogOk == False:
            self.cGame.render()

            pygame.draw.rect( self.cGame.cScreen, (50, 0, 0 ), lRect )

            self.cGame.cScreen.blit( lSurf, lPoint)
            lListButton.draw(  self.cGame.cScreen )

            pygame.display.flip()
            for lEvent in pygame.event.get():
                if lEvent.type == pygame.MOUSEBUTTONDOWN :
                    lListButton.testExec( lEvent.pos )

        self.cGame.fadeOutSound( self.cGame.cSoundGameOver, 100  )


         #-----------------------------------------
    def gameWinAnimation( self,  pNb ):
                          
        self.cGame.playSound( self.cGame.cSoundGameWin  )

        lSurf = self.cYouWin
       
        lPoint = ((gScreen.get_width()/2)-self.cGameOver.get_width()/2, 
                      (gScreen.get_height()/2-self.cGameOver.get_height()/2))

        lRect  = pygame.Rect( lPoint, self.cGameOver.get_size() )

        lListButton = ButtonMenu.ButtonList();
        lListButton.append(  ButtonMenu.ButtonMenu( self.myFont, "Ok", lPoint,  (255,255,255), CallbackOk) )

        self.cDialogOk = False


        while self.cDialogOk == False:

            self.cGame.render()

            pygame.draw.rect( self.cGame.cScreen, (0, 100, 100 ), lRect )

            self.cGame.cScreen.blit( lSurf, lPoint)

            lListButton.draw(  self.cGame.cScreen )
   
            pygame.display.flip()

            for lEvent in pygame.event.get():
                if lEvent.type == pygame.MOUSEBUTTONDOWN :
                    lListButton.testExec( lEvent.pos )

        self.cGame.fadeOutSound( self.cGame.cSoundGameWin, 100  )
         #-----------------------------------------

def CallbackReset():
  #  World.sTheWorld.cGame.resetGame()
    World.sTheWorld.cGame.restart = True


def CallbackStop():
    sys.exit(0)


def CallbackOk():
     World.sTheWorld.cDialogOk = True
