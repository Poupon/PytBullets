
# __author__ = 'Phi'
import pygame, math, sys,  random, math
from pygame.locals import *



# ******************************************

class BulletSprite( pygame.sprite.Sprite):
    
        #-----------------------------------------

    def __init__( self, pTypeColor, pWorld ):
        pygame.sprite.Sprite.__init__(self)
        self.init( pTypeColor, pWorld )
        
        #-----------------------------------------

    def init( self, pTypeColor, pWorld ):
        self.cTypeColor = pTypeColor
        self.cMyWorld   = pWorld

        self.src_image = pWorld.getImage( self.cTypeColor )
        self.cMoving= False;


        self.position= pWorld.world2Screen( pWorld.INIT_FIRE_POS );

        self.cNewPosition = self.position;

#        self.cX = (pWorld.INIT_FIRE_POSW*pWorld.cBullW-pWorld.cBullW/2.0)
#        self.cY = (pWorld.INIT_FIRE_POSH*pWorld.cBullH-pWorld.cBullH/2.0)

        
#        self.position = (self.cX, self.cY )
        
        self.speed = self.direction = 0
        
        self.cSpeedX = self.cSpeedY = 0.0;

        
        #-----------------------------------------

    def update( self, pDeltaT, pRectLimit ):


        # SIMULATION
        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        


        self.cNewPosition = ( self.cNewPosition[0]+self.cSpeedX*pDeltaT, self.cNewPosition[1]+self.cSpeedY*pDeltaT)


            # rebond si on quitte par les bords

        if self.cMyWorld.outOfScreen( self.cNewPosition ) :
           # print "OutOfScreen " , self.cNewPosition
            self.cSpeedX = -self.cSpeedX
            self.cNewPosition = (self.cNewPosition[0] + self.cSpeedX*pDeltaT, self.cNewPosition[1] )
          #  print " ---> " , self.cNewPosition


        if self.cMoving  == True:

        # A t on touche ?
                self.cMoving = self.cMyWorld.resolveMoving( self )
                if  self.cMoving == False :
                    # oui 
                    return self.cMoving;


        self.position = self.cNewPosition

   #     print "cX:", self.cX , "  cY:", self.cY , " position:" , self.position

        self.rect.center = self.position


        return self.cMoving;
        
# ******************************************
