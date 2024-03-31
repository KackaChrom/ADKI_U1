from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from shapely.geometry import shape
from fiona import *
from statistics import *

class IO:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # potřeba vytvořit qt dialog (execute?)
        self.dia = QFileDialog()
        self.dia.setNameFilter("Shapefile (*.shp)")
        
        
    def loadData(self, w, h):
        #Load data
        if self.dia.exec():
            fileNames = self.dia.selectedFiles()
            geometries = []
            
            #Set data
            
            with open(fileNames[0]) as shapefile:
                for record in shapefile:
                    
                    geom = shape(record['geometry'])
                    
                    geometries.append(geom)
        
            polygons = []
            for pol in geometries:
                qpolygon = QPolygonF()
                for point in pol.exterior.coords:
                    qpolygon.append(QPointF(point[0], point[1]*(-1)))
                polygons.append(qpolygon)
        
            #Conversion
            all_points_x = []
            all_points_y = []
            min_x_pols = float('inf')
            min_y_pols = float('inf')
            max_x_pols = float('-inf')
            max_y_pols = float('-inf') 
            for pol in polygons:
                min_x = float('inf')
                min_y = float('inf')
                max_x = float('-inf')
                max_y = float('-inf')

                # Procházení všech bodů polygonu a aktualizace minimálních a maximálních hodnot
                for point in pol:
                    x = point.x()
                    y = point.y()
                    all_points_x.append(x)
                    all_points_y.append(y)
                    min_x = min(min_x, x)
                    min_y = min(min_y, y)
                    max_x = max(max_x, x)
                    max_y = max(max_y, y)
                
                min_x_pols = min(min_x_pols, min_x)
                min_y_pols = min(min_y_pols, min_y)
                max_x_pols = max(max_x_pols, max_x)
                max_y_pols = max(max_y_pols, max_y)
            
            
            W = max_x_pols - min_x_pols
            H = max_y_pols - min_y_pols
            
            pomerw = w/W
            pomerh = h/H
            
            s = min(pomerw, pomerh)
            
            center_X = mean(all_points_x)
            center_Y = mean(all_points_y)
            
            center_X = center_X*s
            center_Y = center_Y*s        
            
            center_x = w/2
            center_y = h/2
            
            
            posun_x = center_X - center_x
            posun_y = center_Y - center_y
            
            
            polygons_finale = []
            for pol in polygons:
                polygon = QPolygonF()
                points = []
                for point in pol:
                    x = point.x()*s - posun_x
                    y = point.y()*s - posun_y   
                    
                    if x not in points:
                        points.append(x) 
      
                        point2 = QPointF(x,y)

                        polygon.append(point2)

                polygons_finale.append(polygon)


            #Return list of polygon
            return polygons_finale