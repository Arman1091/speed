from flask import Flask,request,send_file
from models import models
from models.models import get_client_detailles_by_id

import dxfgrabber
import math

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from PyPDF2 import PdfReader, PdfWriter
# from io import BytesIO
from datetime import datetime
import io
from io import BytesIO
import os


def get_dimension(path_folder):
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



def create_pdf( data ):
    name_matiere = data ['name_matiere']
    type_matiere= data['type_matiere']

    type_usinage = data ['type_usinage']
    qte= int(data['qte'])
    prix_ht = float(data ['prix_ht'])

    print(prix_ht )
    epaisseur = data['epaisseur']
    user = data["user"]
    montant_total_ht = prix_ht
    montant_ht = prix_ht
    montant_tva = round(0.2*montant_total_ht, 2)
    print("eee")
    print(montant_total_ht)
    print(montant_tva)
    if 'prix_livr_ht' in data:

        prix_livr_ht= data["prix_livr_ht"]
        montant_ht =round(float(montant_ht) -float(prix_livr_ht))



    montant_totat_ttc = round(1.2*montant_total_ht,2)

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