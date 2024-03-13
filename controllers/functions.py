from flask import Flask,request,send_file
from models import models
from models.models import get_client_detailles_by_id

import dxfgrabber
import math

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime



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



def create_pdf( data ):
    name_matiere = data ['name_matiere']
    type_matiere= data['type_matiere']

    type_usinage = data ['type_usinage']
    qte= int(data['qte'])
    prix_ht = float(data ['prix_ht'])
    epaisseur = data['epaisseur']
    user = data["user"]
    montant_ht = qte*prix_ht

    montant_tva = round(0.2*montant_ht, 2)
    montant_totat_ttc = round(1.2*montant_ht)
    print(montant_totat_ttc)
    current_date = str(datetime.now().date())
        
    devisVide_path = "static/img/devis_vide.png"
    output_filename = "static/members/comercial/Eric/output.pdf"
    buffer = BytesIO()
    c = canvas.Canvas(output_filename, pagesize=letter)

    if devisVide_path:
        c.drawInlineImage(devisVide_path, 0, 0, c._pagesize[0], height=c._pagesize[1])
    # Ajouter le titre
    c.setFont("Helvetica", 8)
    c.drawString(350, 729, "9SDHS564SD")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(28, 580, "Devis N°")
    # Date value
    c.setFont("Helvetica", 9)
    c.drawString(114, 563, current_date)

    # Representante
    c.setFont("Helvetica", 9)
    c.drawString(193, 563, user)

    
    # Ajouter les informations de la société
    if 'client_id' in data:
        client_id= data['client_id']
        detailles = get_client_detailles_by_id(client_id)
        referance_client=detailles[0].reference
        name_client=detailles[1].name
        ville_client=detailles[1].ville
        cp_client=detailles[1].cp
        client_addresse=detailles[1].addresse
        c.setFont("Helvetica-Bold", 9)
        c.drawString(300, 662, name_client)
    
        c.setFont("Helvetica", 9)
        c.drawString(300, 645, client_addresse)

        c.setFont("Helvetica", 9)
        c.drawString(300, 630, str(cp_client)+" "+ville_client)
# USIM
    c.setFont("Helvetica", 9)
    c.drawString(30, 515, type_usinage)
   
    c.setFont("Helvetica", 9)
    c.drawString(90, 515, "USINAGE MECA:"+name_matiere+" "+ type_matiere+" "+ str(epaisseur)+" mm")
# qte
    c.setFont("Helvetica", 9)
    c.drawString(315, 515, str(qte))

    # P.U
    c.setFont("Helvetica", 9)
    c.drawString(458, 515, str(prix_ht))
    # MontantHT
    c.setFont("Helvetica", 9)
    c.drawString(522, 515, str(montant_ht) )

    # TauxTva
    c.setFont("Helvetica", 9)
    c.drawString(10, 159, "20.00")

    # MontantHT
    c.setFont("Helvetica", 9)
    c.drawString(57, 159, str(montant_ht))

    # MontantTVA
    c.setFont("Helvetica", 9)
    c.drawString(315, 159, str(montant_tva))
    
    # TotalHT
    c.setFont("Helvetica", 8)
    c.drawString(522, 188, str(montant_ht))

    # TotalTVA
    c.setFont("Helvetica", 8)
    c.drawString(522, 144, str(montant_tva))

    # TotalTTC
    c.setFont("Helvetica", 8)
    c.drawString(522, 134, str(montant_totat_ttc))

    # Net a payer
    c.setFont("Helvetica-Bold", 9)
    c.drawString(522, 106, str(montant_totat_ttc))


    c.save()




