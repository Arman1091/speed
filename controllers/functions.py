from flask import request
from models import models

import dxfgrabber
import math

def get_dimension(ssd):
# Ouvrir le fichier DXF
    dxf = dxfgrabber.readfile("./"+ssd+"/current.dxf")
    larg = 0
    long = 0
    
    # Parcourir les entités du fichier
    for entity in dxf.entities:
        # Obtenir le type de l'entité (CIRCLE, LINE, LWPOLYLINE, etc.)
        entity_type = entity.dxftype
        # Obtenir les coordonnées de l'entité
        if entity_type == "CIRCLE":
            # Pour un cercle, les coordonnées sont le centre et le rayon
            center = entity.center
            radius = entity.radius
            # Calculer les points minimaux et maximaux
            min_point = (center[0] - radius, center[1] - radius, center[2])
            max_point = (center[0] + radius, center[1] + radius, center[2])
        elif entity_type == "LINE":
            # Pour une ligne, les coordonnées sont les points de départ et de fin
            start = entity.start
            end = entity.end
            # Calculer les points minimaux et maximaux
            min_point = (min(start[0], end[0]), min(start[1], end[1]), min(start[2], end[2]))
            max_point = (max(start[0], end[0]), max(start[1], end[1]), max(start[2], end[2]))
        elif entity_type == "LWPOLYLINE" or entity_type == "POLYLINE":
            # Pour une polyligne, les coordonnées sont une liste de points
            points = entity.points
    
            # Calculer les points minimaux et maximaux
            min_point = (min(p[0] for p in points), min(p[1] for p in points), min(p[2] if len(p) > 2 else 0 for p in points))
            max_point = (max(p[0] for p in points), max(p[1] for p in points), max(p[2] if len(p) > 2 else 0 for p in points))
        # Calculer la distance entre les points minimaux et maximaux
        entity_long = math.hypot(max_point[0] - min_point[0])
        entity_larg = math.hypot(max_point[1] - min_point[1])
        if larg < entity_larg:
            larg = entity_larg
        if long < entity_long:
            long = entity_long
            
  
    dimension = {'larg': larg, 'long': long}
    return dimension
