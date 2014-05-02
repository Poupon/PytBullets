__author__ = 'Phi'
import pygame, math, sys,  random, math
from pygame.locals import *


gScreen = pygame.display.set_mode((1024, 768))
gClock = pygame.time.Clock()


# =============== WORLD ===============

class World:
    BULLET_W = 40
    BULLET_H = 40

    HEIGHT = 18
    WIDTH  = 24
    INIT_HEIGHT = 9
    
    INIT_FIRE_POSW = WIDTH/2

    INIT_FIRE_POSH = HEIGHT-1
    INIT_FIRE_POS  = ( INIT_FIRE_POSW, INIT_FIRE_POSH)

    pygame.font.init()

        #-----------------------------------------
    def __init__(self ):

        self.cDestroyAnimation = 0

        self.cDestroyedBulletSurf =   pygame.transform.scale( pygame.image.load( 'Iridescent.png'),(self.BULLET_W, self.BULLET_H))
        self.cVoidBulletSurf =   pygame.transform.scale( pygame.image.load( 'Ice.png.png'),(self.BULLET_W, self.BULLET_H))
        self.cBullet =[ 0, # pygame.image.load( 'Ice.png'),
                        pygame.transform.scale( pygame.image.load( 'Green.png'), (self.BULLET_W, self.BULLET_H)),
                        pygame.transform.scale( pygame.image.load( 'Indigo.png'),(self.BULLET_W, self.BULLET_H)),
                        pygame.transform.scale( pygame.image.load( 'Magenta.png'),(self.BULLET_W, self.BULLET_H)),
                        pygame.transform.scale( pygame.image.load( 'Red.png'),(self.BULLET_W, self.BULLET_H)),
                        pygame.transform.scale(  pygame.image.load( 'Teal.png'),(self.BULLET_W, self.BULLET_H)),
                        pygame.transform.scale( pygame.image.load( 'Yellow.png'),(self.BULLET_W, self.BULLET_H)),
                        self.cDestroyedBulletSurf,
                        self.cVoidBulletSurf
                        ]


        
        self.cDestroyedBullet = self.cBullet.index( self.cDestroyedBulletSurf )
    
        self.MAX_BULLET_TYPE= len( self.cBullet)-3
        
        
        self.cBullW = self.cBullet[1].get_width()
        self.cBullH = self.cBullet[1].get_height()
        

        
        gScreen = pygame.display.set_mode( (self.cBullW*self.WIDTH, 
                                           ( self.cBullH+4)*self.HEIGHT) )

        self.yLinePrint = (self.cBullH+2)*self.HEIGHT
        self.yLineBullet = (int)(self.cBullH+1)*self.HEIGHT

        
        self.cDebug = False

        self.cDebugTabBullet = False

        self.cMemTabBullet = None

        self.resetGame()
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
    def resetGame( self ):

        self.cAddOneTurn = False;

        self.cScore = 0;

        self.cTurn = 0
        self.cMemTabBullet = None

        self.cTab = [[0] *self.WIDTH  for _ in range(self.HEIGHT)]
  
        for h in range(self.INIT_HEIGHT):
            print "h:" , h
            self.randomRow( h );

       #-----------------------------------------
       # Test if bullet is void bullet

    def isVoidBullet( self,  pBullet ):
        if pBullet == 0 or pBullet == self.cDestroyedBullet :
            return True
        return False

    def isFullBullet(self, pBullet ):
        return not isVoidBullet()

       #-----------------------------------------
       # set random row 
    def randomRow( self, pRow ):
        for w in range(self.WIDTH):
            self.cTab[pRow][w] = random.randint( 1, self.MAX_BULLET_TYPE )
     
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
            print 'outOfWorld ' ,  pCoordWorld
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
        #-----------------------------------------
    def drawNext(self, pSurfDest, pNextBullet):
        
        pSurfDest.blit( self.cBullet[pNextBullet.cTypeColor], (350, self.yLineBullet))

        pSurfDest.blit( self.cVoidBulletSurf, (350+BULLET_W, self.yLineBullet))

        #-----------------------------------------
    def __init__(self ):

        self.cDestroyAnimation = 0

        self.cDestroyedBulletSurf =   pygame.transform.scale( pygame.image.load( 'Iridescent.png'),(self.BULLET_W, self.BULLET_H))
        self.cVoidBulletSurf =   pygame.transform.scale( pygame.image.load( 'Ice.png'),(self.BULLET_W, self.BULLET_H))
        self.cBullet =[ 0, # pygame.image.load( 'Ice.png'),
                        pygame.transform.scale( pygame.image.load( 'Green.png'), (self.BULLET_W, self.BULLET_H)),
                        pygame.transform.scale( pygame.image.load( 'Indigo.png'),(self.BULLET_W, self.BULLET_H)),
                        pygame.transform.scale( pygame.image.load( 'Magenta.png'),(self.BULLET_W, self.BULLET_H)),
                        pygame.transform.scale( pygame.image.load( 'Red.png'),(self.BULLET_W, self.BULLET_H)),
                        pygame.transform.scale(  pygame.image.load( 'Teal.png'),(self.BULLET_W, self.BULLET_H)),
                        pygame.transform.scale( pygame.image.load( 'Yellow.png'),(self.BULLET_W, self.BULLET_H)),
                        self.cDestroyedBulletSurf,
                        self.cVoidBulletSurf
                        ]


        
        self.cDestroyedBullet = self.cBullet.index( self.cDestroyedBulletSurf )
    
        self.MAX_BULLET_TYPE= len( self.cBullet)-3
        
        
        self.cBullW = self.cBullet[1].get_width()
        self.cBullH = self.cBullet[1].get_height()
        

        
        gScreen = pygame.display.set_mode( (self.cBullW*self.WIDTH, 
                                           ( self.cBullH+4)*self.HEIGHT) )

        self.yLinePrint = (self.cBullH+2)*self.HEIGHT
        self.yLineBullet = (int)(self.cBullH+1)*self.HEIGHT

        
        self.cDebug = False

        self.cDebugTabBullet = False

        self.cMemTabBullet = None

        self.resetGame()
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
    def resetGame( self ):

        self.cAddOneTurn = False;

        self.cScore = 0;

        self.cTurn = 0
        self.cMemTabBullet = None

        self.cTab = [[0] *self.WIDTH  for _ in range(self.HEIGHT)]
  
        for h in range(self.INIT_HEIGHT):
            print "h:" , h
            self.randomRow( h );

       #-----------------------------------------
       # Test if bullet is void bullet

    def isVoidBullet( self,  pBullet ):
        if pBullet == 0 or pBullet == self.cDestroyedBullet :
            return True
        return False

    def isFullBullet(self, pBullet ):
        return not isVoidBullet()

       #-----------------------------------------
       # set random row 
    def randomRow( self, pRow ):
        for w in range(self.WIDTH):
            self.cTab[pRow][w] = random.randint( 1, self.MAX_BULLET_TYPE )
     
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
            print 'outOfWorld ' ,  pCoordWorld
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
        #-----------------------------------------
    def drawNext(self, pSurfDest, pNextBullet):
        
        pSurfDest.blit( self.cBullet[pNextBullet.cTypeColor], (350, self.yLineBullet))

        pSurfDest.blit(  self.cVoidBulletSurf, (350+self.BULLET_W*2, self.yLineBullet))

    def draw(self, pSurfDest):
                    
        for h in range(self.HEIGHT):
            for w in range(self.WIDTH):
                lBullet = self.get( (w, h) )
                if lBullet !=  0 :
                    pSurfDest.blit( self.cBullet[lBullet], (w*self.cBullW, h*self.cBullH))

                # dessin des lignes pour le debuggage
            pygame.draw.line( pSurfDest, ( 200, 200, 200), (0, h*self.cBullH), (self.cBullW*self.WIDTH, h*self.cBullH))

        pygame.draw.line( pSurfDest, ( 200, 200, 200), (0, self.HEIGHT*self.cBullH), (self.cBullW*self.WIDTH, self.HEIGHT*self.cBullH))
          
        for w in range(self.WIDTH):
            pygame.draw.line( pSurfDest, ( 200, 200, 200), (w*self.cBullW, 0), (w*self.cBullW, self.cBullH*self.HEIGHT))

        StrMyFont = pygame.font.get_default_font()
        myFont =pygame.font.SysFont(StrMyFont,32)
 #       myFont = pygame.font.Font(None, 30)

        str = "Score: %d  Turn: %d" % (self.cScore,  self.cTurn)
        textImg = myFont.render( str, 1, (255,0,0))
        pSurfDest.blit( textImg, (50, self.yLinePrint) )
  
        

        #-----------------------------------------
    def drawVector(self, pSurfDest, pMousePos):

        lDestWorldCoord  = self.screen2World( pMousePos );
        lDestScreenCoord = self.world2Screen( lDestWorldCoord );
        
        lInitScreenCoord = self.world2Screen( self.INIT_FIRE_POS);

        pygame.draw.line( pSurfDest, ( 200, 200, 200),  
                          lInitScreenCoord, lDestScreenCoord, 4)
            
         #-----------------------------------------
    def remplaceAll(self, pTarget, pNew):
        
        print "************* remplaceAll **********************"
        for h in range(self.HEIGHT):
            for w in range(self.WIDTH):
                if self.get( (w, h) ) == pTarget:
                    print "**********************"
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

                print "len:", len(NeightorPosList), " Count:", lCount, " Pos:", lPos

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
                
                print "len:", len(NeightorPosList), " Pos:", lPos

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

    def shiftDown( self ):

        # detect if there are an bullet at the last line -> lose 
        for w in range(self.WIDTH):
            lBullet = self.get( (w, self.HEIGHT-1) )
            if lBullet != 0 :
                return False
            
            
        
        for h in xrange(self.HEIGHT-2, -1, -1):
            for w in range( self.WIDTH ):
                self.set( (w, h+1), self.get( (w, h) ))                          
        return True


        #-----------------------------------------
    def resolve( self, pBullet ):

        
        lWorldPos = self.screen2World( pBullet.cNewPosition )
        
        
        if  lWorldPos[1] < 0 :
            lWorldPos  = (lWorldPos[0], 0 )
            return False;
        
        
        if self.isWorldVoid( lWorldPos ):
            return True
        

        lWorldPos = self.screen2World( pBullet.position ) # la derniere position        

        if  lWorldPos[1] < 0 :
            lWorldPos[1]  = 0
            return False;
   

        lCount = self.countNeighbor( lWorldPos, pBullet.cTypeColor )        

        if lCount >= 3 :
            self.cMemTabBullet = self.copyTabBullet()
            self.setMem( lWorldPos, pBullet.cTypeColor )

            self.cScore += self.destroyNeighbor(  lWorldPos, pBullet.cTypeColor, self.cDestroyedBullet)     
            self.set( lWorldPos, self.cDestroyedBullet )
            self.cScore += self.resolveHole(  self.cDestroyedBullet )
            self.cDestroyAnimation = 30
            self.cAddOneTurn = False;
        else: 
            self.cAddOneTurn = True;
            self.set( lWorldPos, pBullet.cTypeColor )

        return False
        #-----------------------------------------
    def flipMemTabBullet( self ):
        lMem = self.cTab
        self.cTab = self.cMemTabBullet
        self.cMemTabBullet = lMem
    
        #-----------------------------------------
    def destroyAnimation( self ):

        self.flipMemTabBullet()

        print "======== destroyAnimation:" , self.cDestroyAnimation 
        self.cDestroyAnimation -= 1

        if self.cDestroyAnimation <= 0 :
            self.cDestroyAnimation = 0
            self.remplaceAll( self.cDestroyedBullet, 0 )
  

        
# ============== BULLET ================


class BulletSprite( pygame.sprite.Sprite):
    
    def __init__( self, pTypeColor, pWorld ):
        pygame.sprite.Sprite.__init__(self)
        self.init( pTypeColor, pWorld )
        

    def init( self, pTypeColor, pWorld ):
        self.cTypeColor = pTypeColor
        self.cMyWorld   = pWorld

        self.src_image = pWorld.getImage( self.cTypeColor )
        self.cInternalState = True;


        self.position= pWorld.world2Screen( pWorld.INIT_FIRE_POS );

        self.cNewPosition = self.position;

#        self.cX = (pWorld.INIT_FIRE_POSW*pWorld.cBullW-pWorld.cBullW/2.0)
#        self.cY = (pWorld.INIT_FIRE_POSH*pWorld.cBullH-pWorld.cBullH/2.0)

        
#        self.position = (self.cX, self.cY )
        
        self.speed = self.direction = 0
        
        self.cSpeedX = self.cSpeedY = 0.0;
        


    def update( self, pDeltaT, pRectLimit ):
        # SIMULATION
        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        
        self.cNewPosition = ( self.cNewPosition[0]+self.cSpeedX*pDeltaT, self.cNewPosition[1]+self.cSpeedY*pDeltaT)


        # rebond si on quitte par les bords

        if self.cMyWorld.outOfScreen( self.cNewPosition ) :
            print "OutOfScreen " , self.cNewPosition
            self.cSpeedX = -self.cSpeedX
            self.cNewPosition = (self.cNewPosition[0] + self.cSpeedX*pDeltaT, self.cNewPosition[1] )
            print " ---> " , self.cNewPosition


        
        # A t on touche ?
        self.cInternalState = self.cMyWorld.resolve( self )
        if  self.cInternalState == False :
            return ;


        self.position = self.cNewPosition

   #     print "cX:", self.cX , "  cY:", self.cY , " position:" , self.position

        self.rect.center = self.position


        return ;
        


# =============  MAIN ==============

gWorld = World();
gRect = gScreen.get_rect()
gBullet = BulletSprite( random.randint( 1, gWorld.MAX_BULLET_TYPE ), gWorld )

gNextBullet = BulletSprite( random.randint( 1, gWorld.MAX_BULLET_TYPE ), gWorld )
              
      
gBulletGroup = pygame.sprite.RenderPlain(gBullet)

gStateFire = False;
gMemMousePos = (0.0,0.0);


while 1:
    # USER INPUT

    lDeltaTime = gClock.tick(50)

    if gWorld.cDestroyAnimation != 0 :
        gWorld.destroyAnimation();
    else :

        
        if gWorld.cAddOneTurn:
            print "*********** cAddOneTurn:" ,  gWorld.cAddOneTurn
            gWorld.cAddOneTurn = False;
            gWorld.cTurn += 1
            if (gWorld.cTurn % 8) == 0 :
                lResult = gWorld.shiftDown();
                if lResult == False :
                    lGameFinish = True
                    print "You lose !!!"                
                else:
                    gWorld.randomFirstRow()

                    
        for lEvent in pygame.event.get():
            if lEvent.type == pygame.MOUSEMOTION:
                print "mouse" 
                if gStateFire == False:
                    # on est en mode vieur, on fait bouger le vecteur
                    gMemMousePos = lEvent.pos
                    
                    
                    print "gMemMousePos", gMemMousePos
                    
                    
            elif lEvent.type == pygame.MOUSEBUTTONDOWN and gStateFire == False:
                gStateFire = True

                lDiffX = lEvent.pos[0]-gBullet.cNewPosition[0]
                lDiffY = lEvent.pos[1]-gBullet.cNewPosition[1]

                print ">>>>>>>>>>>Bullet fire " , lDiffY , " eventy:" , lEvent.pos[1] ," Pos:" , gBullet.cNewPosition[1]

                if lDiffY > -gWorld.BULLET_H :
                    print ">>>>>>>>>>>Bullet fire " , gWorld.BULLET_H 
                    lDiffY =  -gWorld.BULLET_H 

                
                gMemMousePos = (lDiffX, lDiffY)
                lNorm = math.sqrt( gMemMousePos[0]*gMemMousePos[0]+gMemMousePos[1]*gMemMousePos[1]);
                
                print "lNorm ", gMemMousePos
                
                gBullet.cSpeedX = gMemMousePos[0] / (lNorm*2)  
                gBullet.cSpeedY = gMemMousePos[1] / (lNorm*2)
                
                print "cSpeedX ", gBullet.cSpeedX, " cSpeedY ", gBullet.cSpeedY
                    
                    
                    
            elif hasattr( lEvent, 'key'):                            
                if lEvent.key == K_UP:
                    gStateFire = False
                    gBulletGroup.empty()
                    gBullet = BulletSprite( random.randint( 1, gWorld.MAX_BULLET_TYPE ), gWorld )
                    gBulletGroup.add(gBullet)
                    #    gBullet.init(  random.randint( 1, gWorld.MAX_BULLET_TYPE), gWorld )

                elif lEvent.key == K_r:
                    gWorld.flipMemTabBullet()

                elif lEvent.key == K_ESCAPE:
                    sys.exit(0)
                        
# RENDERING
                        
    gScreen.fill((0, 0, 0))
    gBulletGroup.update( lDeltaTime, gRect )

    if gStateFire == True and gBullet.cInternalState == False:
        gStateFire = False

        
     #   gBullet.init(  random.randint( 1, gWorld.MAX_BULLET_TYPE), gWorld )

     

        # new bullet
        gBulletGroup.empty()
        gBullet = gNextBullet;
        gBulletGroup.add(gBullet)
        gNextBullet = BulletSprite( random.randint( 1, gWorld.MAX_BULLET_TYPE ), gWorld )
        continue

    if gStateFire == False:
        gWorld.drawVector( gScreen, gMemMousePos);                            

    gWorld.draw( gScreen )
    gWorld.drawNext( gScreen, gNextBullet )
    gBulletGroup.draw( gScreen )
    pygame.display.flip()

    
