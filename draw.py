from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.polygons = []
        self.pol = QPolygonF()
        self.polygons.append(self.pol)
        self.q = QPointF(-100,-100)
        self.add_vertex = True
        self.hpol = QPolygonF()
        
    def mousePressEvent(self, e:QMouseEvent):   
        
        self.hpol = QPolygonF()
        #Get cursor position
        x = e.position().x()
        y = e.position().y()

        #Draw polygon
        if self.add_vertex:
            #Create new point
            p = QPointF(x,y)
        
            #Add point to polygon
            self.pol.append(p)
            self.polygons[0] = self.pol
            
            
        #Draw point
        else:
            self.q.setX(x)
            self.q.setY(y)

        #Repaint screen
        self.repaint()
        

    def paintEvent(self,  e:QPaintEvent):
        #Draw situation
        
        #Create new object
        qp = QPainter(self)

        #Start drawing
        qp.begin(self)
        
        #Set atributes
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.yellow)

        #Draw polygon
        for i in self.polygons:
            qp.drawPolygon(i)
        
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.green)
        
        qp.drawPolygon(self.hpol)
        
        #Set atributes
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.red)
        
        #Draw point
        r = 5
        qp.drawEllipse(int(self.q.x() - r), int(self.q.y() - r), int(2*r), int(2*r))

        #End drawing
        qp.end()
        
    def switchDraw(self):
        self.add_vertex = not(self.add_vertex)
        
    def switchToPoint(self):
        self.add_vertex = False
        
    def switchToPols(self):
        self.add_vertex = True
    
    #return point    
    def getPoint(self):
        return self.q
    
    #Return polygon
    def getPolygon(self):
        return self.polygons
    
    def clearData(self):
        #Clear point
        self.q.setX(-100)
        self.q.setY(-100)
        
        #Clear polygon
        
        self.pol.clear()
        self.hpol.clear()
        self.polygons = []
        self.polygons.append(self.pol)
        
        #Repaint screen
        self.repaint()
    
    def setData(self, pols):
        self.clearData()
        
        self.polygons = pols
        
        self.repaint()
    
    def highlightPolygon(self, pol):
        self.hpol = pol
        self.repaint()
        
                
                
    