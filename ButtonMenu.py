# __author__ = 'Phi'
import pygame, math, sys,  random, math
from pygame.locals import *



# ******************************************

class ButtonMenu:


    def __init__( self, pFont, pStr, pPos, pColor, pAction  ):

        
        self.cTextImg = pFont.render( pStr, 1, pColor)
        self.cPos = pPos
        self.cRect = pygame.Rect( pPos, self.cTextImg.get_size())

        self.cRect = self.cRect.inflate( 5, 5 )
        self.cColor = pColor
        self.cAction = pAction

        
    def draw( self, pSurfDest ) :
        pSurfDest.blit( self.cTextImg, ( self.cPos ) )

        pygame.draw.rect( pSurfDest, self.cColor, self.cRect, 1 )
     


    def into( self, pPoint  ) :
       return  self.cRect.collidepoint( pPoint )

    def testExec( self,  pPoint  ) :
       if self.into( pPoint):
           self.cAction()
           return True

       return False

  
class ButtonList:

    def __init__( self):
        
        self.cList = [];
        

    def append( self, pButtonMenu ):
        self.cList.append( pButtonMenu )
        
    def append( self, pButtonMenu ):        
        self.cList.append( pButtonMenu )
        

    def draw( self,  pSurfDest ) :
        for lButton in self.cList:
            lButton.draw( pSurfDest )

    def testExec( self,  pPoint  ) :
        for lButton in self.cList:
            if lButton.testExec(  pPoint ) :
                return True
        return False
