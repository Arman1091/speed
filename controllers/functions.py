from flask import Flask,request,send_file
from models import models
from models.models import get_client_detailles_by_id

import dxfgrabber
import ezdxf
import math

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
# from PyPDF2 import PdfReader, PdfWriter
# from io import BytesIO
from datetime import datetime
from io import BytesIO
import io

import os


def get_dimension( path_folder):
# Ouvrir le fichier DXF
    dxf = dxfgrabber.readfile(path_folder+"/current.dxf")
    larg = 0
    long = 0
    max_x=-math.inf
    min_x=math.inf
    max_y = -math.inf
    min_y = math.inf

    # Parcourir les entités du fichier
    for entity in dxf.entities:
        # Obtenir le type de l'entité (CIRCLE, LINE, LWPOLYLINE, etc.)
        entity_type = entity.dxftype

        print(entity_type)
        # Obtenir les coordonnées de l'entité
        if entity_type == "CIRCLE":
            # Pour un cercle, les coordonnées sont le centre et le rayon
            center = entity.center
            radius = entity.radius
            # Calculer les points minimaux et maximaux
            min_point = (center[0] - radius, center[1] - radius, center[2])
            max_point = (center[0] + radius, center[1] + radius, center[2])
        if entity_type == "LINE":
    # Pour une ligne, les coordonnées sont les points de départ et de fin
            start = entity.start
            end = entity.end
        
            # Vérifier si les points ont une troisième coordonnée (z), sinon définir z=0
            start_z = start[2] if len(start) > 2 else 0
            end_z = end[2] if len(end) > 2 else 0
        
            # Calculer les points minimaux et maximaux en tenant compte des coordonnées 2D et 3D
            min_point = (min(start[0], end[0]), min(start[1], end[1]), min(start_z, end_z))
            max_point = (max(start[0], end[0]), max(start[1], end[1]), max(start_z, end_z))
        elif entity_type == "LWPOLYLINE" or entity_type == "POLYLINE":
            # Pour une polyligne, les coordonnées sont une liste de points
            points = entity.points

            # Calculer les points minimaux et maximaux
            min_point = (min(p[0] for p in points), min(p[1] for p in points), min(p[2] if len(p) > 2 else 0 for p in points))
            max_point = (max(p[0] for p in points), max(p[1] for p in points), max(p[2] if len(p) > 2 else 0 for p in points))
        elif entity_type == "INSERT":
            # Pour une INSERT, les coordonnées sont le point d'insertion et les dimensions du bloc
            insert_point = entity.insert
            block_name = entity.name
            block = dxf.blocks.get(block_name)
            print("test_insert")
            if block:
                print("test_insert_block")
                block_min_x = min(ent.start[0] if hasattr(ent, 'start') else ent.center[0] - ent.radius for ent in block if hasattr(ent, 'start') or hasattr(ent, 'center'))
                block_max_x = max(ent.end[0] if hasattr(ent, 'end') else ent.center[0] + ent.radius for ent in block if hasattr(ent, 'end') or hasattr(ent, 'center'))
                block_min_y = min(ent.start[1] if hasattr(ent, 'start') else ent.center[1] - ent.radius for ent in block if hasattr(ent, 'start') or hasattr(ent, 'center'))
                block_max_y = max(ent.end[1] if hasattr(ent, 'end') else ent.center[1] + ent.radius for ent in block if hasattr(ent, 'end') or hasattr(ent, 'center'))

                min_point = (insert_point[0] + block_min_x, insert_point[1] + block_min_y, insert_point[2])
                max_point = (insert_point[0] + block_max_x, insert_point[1] + block_max_y, insert_point[2])
            else:
                continue
        # Calculer la distance entre les points minimaux et maximaux
        print(max_point[0])
        if max_point[0] > max_x:
            max_x = max_point[0]
        if min_point[0] < min_x:
            min_x = min_point[0]
        if max_point[1] > max_y:
            max_y = max_point[1]
        if min_point[1] < min_y:
            min_y = min_point[1]
    

    long = math.hypot(max_x - min_x)
    larg = math.hypot(max_y - min_y)



    dimension = {'larg': larg, 'long': long}
    return dimension



def create_pdf( data , path, dir_name):
    name_matiere = data ['name_matiere']
    type_matiere= data['type_matiere']

    type_usinage = data ['type_usinage']
    qte= int(data['qte'])
    prix_ht = float(data ['prix_ht'])
    epaisseur = data['epaisseur']
    user = data["user"]
    montant_total_ht = prix_ht
    montant_ht = prix_ht
    montant_tva = round(0.2*montant_total_ht, 2)

    if 'prix_livr_ht' in data:

        prix_livr_ht= data["prix_livr_ht"]
        montant_ht =float(f"{(float(montant_ht) -float(prix_livr_ht)):.2f}")



    montant_totat_ttc = round(1.2*montant_total_ht,2)

    current_date = str(datetime.now().date())

    devisVide_path = dir_name+"/static/img/devis_vide.png"
    output_filename = path+"/output.pdf"
    buffer = BytesIO()
    c = canvas.Canvas(output_filename, pagesize=letter)

    if devisVide_path:
        c.drawInlineImage(devisVide_path, 0, 0, c._pagesize[0], height=c._pagesize[1])
    
    if 'plaques' in data:
        arr_plaques = plaques = request.form.get('plaques', '')
        qtePlaques = request.form.get('qte_plaques', '') 
        if isinstance(arr_plaques, str):
            # Split the comma-separated string into a list
            plaques = arr_plaques.split(',')
        if isinstance(qtePlaques, str):
            # Split the comma-separated string into a list
            arr_qtePlaques  = qtePlaques.split(',')
        c.setFont("Helvetica", 9)
        c.drawString(130, 480, name_matiere+" "+ type_matiere+" "+ str(epaisseur)+" mm")
        vertical_space = 15
        for index, element in enumerate(plaques):
            c.setFont("Helvetica-Bold", 9)
            c.drawString(150, 460-index*vertical_space , element+"x"+ arr_qtePlaques[index])
    # Ajouter le titre

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
        name_client=detailles.name
        ville_client=detailles.ville
        cp_client=detailles.cp
        client_addresse=detailles.addresse
        c.setFont("Helvetica-Bold", 9)
        c.drawString(300, 662, name_client)

        c.setFont("Helvetica", 9)
        c.drawString(300, 645, client_addresse)

        c.setFont("Helvetica", 9)
        c.drawString(300, 630, str(cp_client)+" "+ville_client)

    if 'prix_livr_ht' in data:
        prix_livr_ht= data['prix_livr_ht']
        c.setFont("Helvetica", 9)
        c.drawString(175, 159, prix_livr_ht)
# USIM
    c.setFont("Helvetica", 9)
    c.drawString(30, 515, type_usinage)

    c.setFont("Helvetica", 9)
    c.drawString(90, 515, "USINAGE MECA:"+name_matiere+" "+ type_matiere+" "+ str(epaisseur)+" mm")

    if 'nbr_lettres' in data:
        c.setFont("Helvetica", 9)
        c.drawString(90, 495, "Text: "+data ['nbr_lettres']+" lettres  en "+ str(data ['hauteur'])+" mm")
# qte
    c.setFont("Helvetica", 9)
    c.drawString(315, 515, str(qte))

    # P.U
    c.setFont("Helvetica", 9)
    c.drawString(458, 515, str(montant_ht/qte))
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
    c.drawString(522, 188, str(montant_total_ht))

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

def create_bl(data):
    path = data['path']
    name = data['name']

    input_pdf_path = "static"+path + "/BL/"+name+".pdf"  # Replace with the actual path to the input PDF file
    output_pdf_path = "static/"+path + "/BL/"+name+".pdf"  # Replace with the desired output PDF file path
     # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)

    # Add content to the PDF
    add_content_to_pdf(input_pdf_path, output_pdf_path,data)

    # Send the modified PDF as a response
    return send_file(output_pdf_path, as_attachment=True, download_name='modified_output.pdf', mimetype='application/pdf')

def add_content_to_pdf(input_pdf_path, output_pdf_path,data):
    # Read the existing PDF
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    plaque = data['plaque']
    qte_plaque = data['qte_plaque']
    selectedValues = data['selectedValues']
    selectedValuesEmplacement = data['selectedValuesEmplacement']

    # Create a new PDF to add additional content
    packet = io.BytesIO()

    can = canvas.Canvas(packet, pagesize=letter)

    can.setFont("Helvetica-Bold", 12)
    can.drawString(110, 430, "S:"+plaque+"(x"+qte_plaque +")")

    val = 105
    inc = 15
    can.drawString(val, 400, "(")
    for item in selectedValuesEmplacement:
        print(item)
        val += inc
        can.setFont("Helvetica-Bold", 12)
        can.drawString(val, 400, item)
    can.drawString(val+inc, 400, ")")

    val_realis = 40
    inc_realis = 10
    can.drawString(val_realis, 615, "(")
    for item in selectedValues:
        val_realis += inc_realis
        can.setFont("Helvetica-Bold", 12)
        can.drawString(val_realis, 615, item)
    can.drawString(val_realis+inc_realis, 615, ")")







    can.save()

    # Move to the beginning of the StringIO buffer
    packet.seek(0)

    # Read the new PDF
    new_pdf = PdfReader(packet)
    new_page = new_pdf.pages[0]

    # Iterate through all pages of the existing PDF and merge the new content
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        if i == 0:  # Only add to the first page
            page.merge_page(new_page)
        writer.add_page(page)

    # Write the modified content to a new PDF
    with open(output_pdf_path, 'wb') as f:
        writer.write(f)

def calculate_perimeter_and_drilling_count(path_folder):
    # Ouvrir le fichier DXF
    doc = ezdxf.readfile(path_folder + "/current.dxf")
    msp = doc.modelspace()
    perimetre = 0
    nbr_percage = 0

    def calculate_perimeter_for_entity(entity):
        nonlocal perimetre, nbr_percage

        if entity.dxftype() == 'CIRCLE':
            dc = 2 * math.pi * entity.dxf.radius
            if dc < 30:
                nbr_percage += 1
            else:
                perimetre += dc
        elif entity.dxftype() == 'LINE':
            start = entity.dxf.start
            end = entity.dxf.end
            length = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2 + (end[2] - start[2]) ** 2)
            perimetre += length
        elif entity.dxftype() == 'LWPOLYLINE':
            points = entity.get_points('xyb')
            perimetre_entity = 0
            for i in range(len(points) - 1):
                dx = points[i + 1][0] - points[i][0]
                dy = points[i + 1][1] - points[i][1]
                perimetre_entity += math.sqrt(dx ** 2 + dy ** 2)
            if perimetre_entity < 30:
                nbr_percage += 1
            else:
                perimetre += perimetre_entity
        elif entity.dxftype() == 'POLYLINE':
            points = list(entity.points())
            perimetre_entity = 0
            for i in range(len(points) - 1):
                dx = points[i + 1][0] - points[i][0]
                dy = points[i + 1][1] - points[i][1]
                perimetre_entity += math.sqrt(dx ** 2 + dy ** 2)
            if perimetre_entity < 30:
                nbr_percage += 1
            else:
                perimetre += perimetre_entity
        elif entity.dxftype() == 'ARC':
            radius = entity.dxf.radius
            start_angle = math.radians(entity.dxf.start_angle)
            end_angle = math.radians(entity.dxf.end_angle)
            arc_length = radius * abs(end_angle - start_angle)
            perimetre += arc_length
        elif entity.dxftype() == 'INSERT':
            block_name = entity.dxf.name
            insert_point = entity.dxf.insert
            block = doc.blocks.get(block_name)

            if block:
                for block_entity in block:
                    if hasattr(block_entity, 'dxf'):
                        original_insert = block_entity.dxf.insert if block_entity.dxftype() == 'INSERT' else None
                        if original_insert:
                            block_entity.dxf.insert = [insert_point[0] + original_insert[0], insert_point[1] + original_insert[1], insert_point[2] + original_insert[2]]
                        calculate_perimeter_for_entity(block_entity)
                        if original_insert:
                            block_entity.dxf.insert = original_insert

    # Parcourir toutes les entités dans l'espace modèle
    for e in msp:
        calculate_perimeter_for_entity(e)

    return {'perimetre': perimetre, 'nbr_percage': nbr_percage}
