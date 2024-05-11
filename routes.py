from flask import Flask,Blueprint, render_template,request,jsonify,flash,send_file, session,redirect,url_for

# from controllers import matiere
# from models.models import Pvc
# from models  import models

from models.models   import User,Client, Commande,Matiere,Role,BridgeLettres,get_epaisseurs,get_prix,get_prix_pmma_usil, get_clients_by_user,get_en_attentes, get_en_attente_by_id, get_confirmes,get_usinés,get_livré,get_confirmé_by_id,change_confirmer, change_usiner, change_livré,supprimer_commande_attente,supprimer_commande_confirmé,supprimer_commande_usiné,get_types_by_matiere,get_types_usinage,Matiere,Commande,get_all_attentes,get_all_confirmes,get_all_usinés,get_all_livré,get_types_lettre_by_matiere,get_epaisseurs_lettre,get_usinage_types_lettre,get_hauteurs_lettre,get_users_by_role,get_data_matieres,get_all_representants,get_cients_by_rep,edit_client_data,get_prix_lettre,change_matiere_prix,change_limeaire_prix,get_types_usinage_prix,get_pmma_usil_list,delete_commande_client,delete_bridge_form_row,get_liste_prix_lettre,delete_bridge_lettre_row,change_lettre_prix
from flask_login import login_user, login_required, logout_user, current_user
from controllers.functions import get_dimension , create_pdf
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
from ezdxf.addons.drawing import RenderContext, Frontend

from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.enums import TextEntityAlignment
from datetime import timedelta, datetime

import ezdxf
import math
import os

# main = Blueprint ('main' , __name__) #routename = main7


app = Flask(__name__)

# @login_manager.user_loader
# def load_user(user_id):
#   return User.get(user_id)



@app.route('/usinage' ,  methods=['GET', 'POST'])
@login_required
def Usinage(): 
    if(current_user.role_id == 2 or current_user.role_id==1 ):
                    # premiere entrer a la page
                    # Pvc
        matiere_id = 1 
    # Blanc
        type_id = 3
        # 2
        epaisseur_id = 1
        matieres= Matiere.get_all_matiere()
        types_matiers= get_types_by_matiere(matiere_id)
                   
        epaisseurs = get_epaisseurs(matiere_id,type_id)
        types_usinage= get_types_usinage(matiere_id,type_id,epaisseur_id)
                    
        clients = get_clients_by_user(current_user)
  
        return render_template('usinage.html',user=current_user, matieres = matieres, types_matiers= types_matiers, clients=clients, epaisseurs= epaisseurs, types_usinage=types_usinage)
    else:
        return redirect(url_for('en_attente'))
   

@app.route('/en_attente' ,  methods=['GET', 'POST'])
@login_required
def en_attente(): 
    if current_user.role_id == 2:
        data = get_en_attentes(current_user)
    else:
       data = get_all_attentes()
    return render_template('en_attente.html', user = current_user,data=data)

@app.route('/confirmé' ,  methods=['GET', 'POST'])
@login_required
def confirmé(): 
    if current_user.role_id == 2:
        data = get_confirmes(current_user)
    else:
        data = get_all_confirmes()
    
    return render_template('confirmé.html', user = current_user,data=data)
@app.route('/usiné' ,  methods=['GET', 'POST'])
@login_required
def usiné(): 
    if current_user.role_id == 2:
        data = get_usinés(current_user)
    else:
       data = get_all_usinés()
    
    return render_template('usiné.html', user = current_user,data=data)

@app.route('/livré' ,  methods=['GET', 'POST'])
@login_required
def livré(): 
    if current_user.role_id == 2:
        data = get_livré(current_user)
    else:
       data = get_all_livré()
    
    return render_template('livré.html', user = current_user,data=data)


@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=30)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.filter_by_email(email)
        if user:
            if User.is_password_correct(user, password):
                flash('Connecté avec succès!', category='success')
                login_user(user, remember=True)
                if(current_user.role_id == 2 or current_user.role_id==1 ):
                    # premiere entrer a la page
                    # Pvc
                  
                    return redirect(url_for('Usinage'))
                else:
                    return redirect(url_for('en_attente'))
                    # return render_template("en_attente.html",user=current_user)
            else:
                flash('Email ou mot de passe incorrect, réessayez.', category='error')
        else:
            flash('Email ou mot de passe incorrect, réessayez.', category='error')
    # try:
    #     matiere = 'Pvc'
    #     name = 'Mat'
    #     data = get_data(matiere,name)
    #     clients = get_clients(current_user)
    #     return render_template('usinage.html',user=current_user, matiere = matiere, name = name , data = data, clients=clients)
    # except:
    #     return render_template("index.html")
    return render_template("index.html")
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

# @app.route('/en_attente/support' ,  methods=['GET', 'POST'])
# @login_required
# def en_attente_support(): 
#     print("111111111111111111111111111111")
   
#     return jsonify({'redirect_url': 'en_attente/detailles'})
@app.route('/en_attente/detailles' ,  methods=['GET', 'POST'])
@login_required
def en_attente_detailles(): 
    id = request.args.get('id')
    data = get_en_attente_by_id(id)
    prix_total_ht = f"{(((data[2]+data[3])/1.2)*data[13]):.2f}"
    prix_total_ttc = f"{((data[2]+data[3])*data[13]):.2f}"
    print(data)
    return render_template("en_attente_detailles.html",user=current_user,data=data,prix_total_ht=prix_total_ht, prix_total_ttc =prix_total_ttc)

@app.route('/confirmé/detailles' ,  methods=['GET', 'POST'])
@login_required
def confirmé_detailles(): 
    id = request.args.get('id')
    data = get_confirmé_by_id(id)
    prix_total_ht = f"{(((data[2]+data[3])/1.2)*data[13]):.2f}"
    prix_total_ttc = f"{((data[2]+data[3])*data[13]):.2f}"
    print(data)
    return render_template("confirmé_detailles.html",user=current_user,data=data,prix_total_ht=prix_total_ht, prix_total_ttc =prix_total_ttc)    
# @main.route('/login' ,  methods=['GET', 'POST'])
# def login():   
#     if request.method == 'POST':
#         email = request.form.get('email')
#         first_name = request.form.get('firstName')
#         password1 = request.form.get('password1')
#         password2 = request.form.get('password2')
#         role = request.form.get('role')

#         # user = User.query.filter_by(email=email).first()
#         # user = db.session.query(User).filter_by(email=email).first()
#         user = User.filter_by_email(email)
#         print("ùùùùùùù**********************")
#         print(user)
#         if user:
#             flash('Email already exists.', category='error')
#         elif len(email) < 4:
#             flash('Email must be greater than 3 characters.', category='error')
#         elif len(first_name) < 2:
#             flash('First name must be greater than 1 character.', category='error')
#         elif password1 != password2:
#             flash('Passwords don\'t match.', category='error')
#         elif len(password1) < 7:
#             flash('Password must be at least 7 characters.', category='error')
#         else:
        
            
#             new_user = User(email=email, username=first_name, password=password1, role= role )
#             User.set_password(new_user, password1)
#             # db.session.add(new_user)
#             # db.session.commit()
#             User.save(new_user)
#             # login_user(new_user, remember=True)
#             # flash('Account created!', category='success')
#     #         return redirect(url_for('views.home'))
#     # return render_template("sign_up.html", user=current_user)
  
#     return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
   

# Replace the following with your ESP file parsing logic
# Example data (x, y coordinates)

    if request.method == 'POST':
        
        file = request.files['file']
        if file:
            # Get other data from the request
            data = request.form.to_dict()
            mt= data['mt']
            mt_name = data ['mt_name']
            epp = data['selectedValue']
            type_usinage = data['selectedTypeValue']
            mt_text = data['mt_text']
            usinage_text = data['usinage_text']
# ************
            filename = secure_filename(file.filename)
            preferred_name = "current" + os.path.splitext(filename)[1]
            # file_path =file.save(os.path.join('./upload_folder', preferred_name))
            # result = "comercial"
            match current_user.role_id:
                case 1:
                    result =  'admin'
                case 2:
                    result = 'comercial'
                case 3:
                    result = 'responsable'
                case 4:
                    result = 'usinier'
                case 5:
                    result = 'assiatante'
            path_folder = "static/members/"+result+'/'+current_user.username
            file_path = os.path.join('./'+path_folder, preferred_name)
            file.save(file_path)
            dimension = get_dimension(path_folder)
            plt.rcParams["savefig.facecolor"] = 'black'
            plt.rcParams['axes.facecolor'] = 'black'
            dwg = ezdxf.readfile("./"+path_folder+"/current.dxf")
            msp = dwg.modelspace()
            # *******************c********************
            dwg.layers.new(name='MyLines', dxfattribs={'linetype': 'DASHED', 'color': 8})

            ezdxf.addons.drawing.properties.MODEL_SPACE_BG_COLOR = "#FFFFFF"
            auditor = dwg.audit()


            if len(auditor.errors) == 0:
               fig = plt.figure()
               ax = fig.add_axes([0, 0, 1, 1])
               ctx = RenderContext(dwg)
               out = MatplotlibBackend(ax)
               Frontend(ctx, out).draw_layout(msp, finalize=True)
               fig.savefig('./'+path_folder+'/current.png', dpi=300, facecolor = 'black', edgecolor = 'black')
        
            if mt_text == "Pmma" and usinage_text =="USIL":
                prix_pmma_usil = get_prix_pmma_usil(mt,mt_name,epp,type_usinage) 
                result = {'dimension': dimension, 'prix': prix_pmma_usil, 'path_folder':path_folder}
                return jsonify(result)
            else:
                print("auders")
            
                prix = get_prix(mt,mt_name,epp,type_usinage) 
                # os.remove('static/img/upload/current.png')
               
                # os.remove(file_path)
                perimetre = 0
                nbr_percage = 0
                # Parcourir toutes les entités dans l'espace modèle
                for e in msp:
                    # Si l'entité est une LWPOLYLINE (polygone)
                 # Si l'entité est une LWPOLYLINE (polygone)
                    if e.dxftype() == 'CIRCLE':
                        dc = 2*math.pi*e.dxf.radius
                        if dc < 30:
                            nbr_percage+=1
                        else:
                            perimetre += perimetre_entity 
                        perimetre +=dc
                    if e.dxftype() == 'LINE':
                                    # Extract start and end points
                        length = e.dxf.start.distance(e.dxf.end)
                                    # Calculate distance and add to total length
                        perimetre +=length
                    if e.dxftype() == 'LWPOLYLINE':
                        points = e.get_points()
                        points = list(points)
                        perimetre_entity = 0
                        for i in range(x- 1):
                            dx = points[i+1][0] - points[i][0]
                            dy = points[i+1][1] - points[i][1]
                            perimetre_entity+=math.sqrt(dx**2 + dy**2)
                        if perimetre_entity < 30:
                            nbr_percage+=1
                        else:
                            perimetre += perimetre_entity
                    
                    # Si l'entité est une POLYLINE
                    elif e.dxftype() == 'POLYLINE':
    
                        points = e.points()
                        points = list(points)
                        perimetre_entity = 0
                        for i in range(len(points) - 1):
                            dx = points[i+1][0] - points[i][0]
                            dy = points[i+1][1] - points[i][1]
                            perimetre_entity+=math.sqrt(dx**2 + dy**2)
                        if perimetre_entity < 30:
                            nbr_percage+=1
                        else:
                            perimetre += perimetre_entity
                # return str(perimetre)
                result = {'perimetre': perimetre,'dimension': dimension, 'prix': prix, 'path_folder':path_folder,'nbr_percage':nbr_percage}
                return jsonify(result)


@app.route('/new_command', methods=['POST'])
def new_command():
   

# Replace the following with your ESP file parsing logic
# Example data (x, y coordinates)

    if request.method == 'POST':   
        # Get other data from the request
        # current_date = datetime.now().date()
        current_date = datetime.now()
        
        data = request.form.to_dict()
        client_id= data['client_id']
        name_matiere = data ['name_matiere']
        type_matiere= data['type_matiere']
        type_usinage = data ['type_usinage']
        count= data['count']
        prix_matiere = data ['prix_matiere']
        statut_id = data ['statut']
        prix_limeaire = data ['prix_limeaire']
        name_dxf= data['name_dxf']
        description = data ['description']
        date_fin = data ['date_fin']
        epaisseur_id = data['epaisseur_id']


        # user_id = current_user.id

        new_commande = Commande(client_id=client_id, statut_id=1, name_matiere=name_matiere, type_matiere= type_matiere ,usinage_id = type_usinage,count=count,epaisseur_id = epaisseur_id, prix_matiere=prix_matiere, prix_limeaire=prix_limeaire, name_dxf= name_dxf,description_commercial_responsable=description, date_envoi=current_date, date_fin = current_date)
#             User.set_password(new_user, password1)
        # db.session.add(new_commande)
        # db.session.commit()
        Commande.save(new_commande)

        return "d"
    return "c"
@app.route('/change_statut_confirmer', methods=['POST'])
def change_statut_confirmer():
   

# Replace the following with your ESP file parsing logic
# Example data (x, y coordinates)

    if request.method == 'POST':
        file = request.files['file']
        dt = request.form.to_dict()
        id=dt["id"]
        filename = secure_filename(file.filename)
        print(filename)
        preferred_name = filename 
        # file_path =file.save(os.path.join('./upload_folder', preferred_name))
        # result = "comercial"
        match current_user.role_id:
            case 1:
                result =  'admin'
            case 2:
                result = 'comercial'
            case 3:
                result = 'responsable'
            case 4:
                result = 'usinier'
            case 5:
                result = 'assiatante'
        path_folder = "static/members/"+result+'/'+current_user.username
        file_path = os.path.join('./'+path_folder, preferred_name)
        file.save(file_path)
        change_confirmer(id, filename)
    return "its ok"
@app.route('/change_statut_livré', methods=['POST'])
def change_statut_livré():
   

# Replace the following with your ESP file parsing logic
# Example data (x, y coordinates)

    if request.method == 'POST':
        dt = request.form.to_dict()
        id=dt["id"]
        change_livré(id)
    return "its ok"

# @app.route('/change_statut_usiner', methods=['POST'])
# def change_statut_usiner():
   

# # Replace the following with your ESP file parsing logic
# # Example data (x, y coordinates)

#     if request.method == 'POST':
#         dt = request.form.to_dict()
#         id=dt["id"]
#         change_usiner(id)
#     return "its ok"


@app.route('/change_statut_usiner', methods=['POST'])
def change_statut_usiner():
   
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxx")
# Replace the following with your ESP file parsing logic
# Example data (x, y coordinates)

    if request.method == 'POST':
        dt = request.form.to_dict()
        id=dt["id"]
        change_usiner(id)
    return "ok"

@app.route('/supprimer_attente', methods=['POST'])
def supprimer_attente():
   

# Replace the following with your ESP file parsing logic
# Example data (x, y coordinates)

    if request.method == 'POST':
        dt = request.form.to_dict()
        id=dt["id"]
        supprimer_commande_attente(id)
    return "its ok"

@app.route('/supprimer_confirmé', methods=['POST'])
def supprimer_confirmé():
   

# Replace the following with your ESP file parsing logic
# Example data (x, y coordinates)

    if request.method == 'POST':
        dt = request.form.to_dict()
        id=dt["id"]
        supprimer_commande_confirmé(id)
    return "its ok"
@app.route('/supprimer_usiné', methods=['POST'])
def supprimer_usiné():
   

# Replace the following with your ESP file parsing logic
# Example data (x, y coordinates)

    if request.method == 'POST':
        dt = request.form.to_dict()
        id=dt["id"]
        supprimer_commande_usiné(id)
    return "its ok"

@app.route('/telecharger_pdf', methods=['POST'])
def telecharger_pdf():
   

# Replace the following with your ESP file parsing logic
# Example data (x, y coordinates)

    if request.method == 'POST':   
        # Get other data from the request
        
        data = request.form.to_dict()
        create_pdf(data)
        
    return "c"


# **************************

@app.route('/generate_dxf', methods=['POST'])
def generate_dxf():
    text = request.form['text']
    font = request.form['font']
    width = float(request.form['width'])
    height = float(request.form['height'])

    # Create a DXF document
    doc = ezdxf.new()


    # Add TEXT entity to the DXF document
    msp = doc.modelspace()

    msp.add_text(
    text,
    height=100,
    dxfattribs={"style": "MV Boli"}
).set_placement((0, 0))
    # Get the bounding box of the text
  


    # print(x.font_name)
    # Save the DXF document to a file
    file_path = 'static/output.dxf'
    doc.saveas(file_path)
    dwg = ezdxf.readfile("static/output.dxf")
    min_left = float('inf')
    max_right = float('-inf')
    text_entities=dwg.modelspace().query('TEXT')
    leftmost_point = float('inf')
    rightmost_point = float('-inf')
    for text in text_entities:
        x, y, _ = text.dxf.insert
        text_width = len(text.dxf.text)  # Adjust for text width as needed
        leftmost_point = min(leftmost_point, x)
        right_point = x + text_width
        rightmost_point = max(rightmost_point, x)
        print(text.dxf.text)
        print("############")
        print(leftmost_point )
        print(rightmost_point )
    
    msp = dwg.modelspace()
    dwg.layers.new(name='MyLines', dxfattribs={'linetype': 'DASHED', 'color': 8})

    ezdxf.addons.drawing.properties.MODEL_SPACE_BG_COLOR = "#FFFFFF"
    auditor = dwg.audit()


    if len(auditor.errors) == 0:
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ctx = RenderContext(dwg)
        out = MatplotlibBackend(ax)
        Frontend(ctx, out).draw_layout(msp, finalize=True)
        fig.savefig('static/current.png', dpi=300)
        #  facecolor = 'black', edgecolor = 'black'
    return send_file(file_path, as_attachment=True)

@app.route('/change_type', methods=['POST'])
def change_type():
    data = request.form.to_dict()
    matiere_id = data ['matiere_id']
    type_id = data ['type_id']
    selectedMatiereText = data['selectedMatiereText']
    epaisseurs = get_epaisseurs(matiere_id,type_id)
    result_epp = []
    for row_epp in  epaisseurs : 
        result_epp.append(row_epp._data()) 
    epaisseur_id = result_epp[0]['id']

  
    types_usinage= get_types_usinage(matiere_id,type_id,epaisseur_id)
    # print("****<<<<<<*******")
    # print(types_usinage)
    result_type = []
    for row_type in  types_usinage : 
        result_type.append(row_type._data()) 
    first_tpye_usinage = result_type[0]['id']
    first_tpye_text = result_type[0]['name']

    if 'file' in request.files:
        if selectedMatiereText == "Pmma" and first_tpye_text =="USIL":
            prix = get_prix_pmma_usil(matiere_id,type_id,epaisseur_id,first_tpye_usinage) 
        else:
            prix = get_prix(matiere_id,type_id,epaisseur_id,first_tpye_usinage ) 
        prix = get_prix(matiere_id,type_id,epaisseur_id,first_tpye_usinage ) 
        result_envoi = {'epaisseurs': result_epp, "types_usinage":result_type, 'prix':prix}
    else:
        result_envoi = {'epaisseurs': result_epp, "types_usinage":result_type}
    return jsonify(result_envoi)

@app.route('/change_matiere', methods=['POST'])
def change_matiere():
    data = request.form.to_dict()
    matiere_id = data ['matiere_id']
    matiereText = data['matiereText']
    types_matiers= get_types_by_matiere(matiere_id)
    result_matiere_types = []
    for row_type in  types_matiers : 
        result_matiere_types.append(row_type._data()) 
    first_type = result_matiere_types[0]['id']
    # first_type = types_matiers[0].id
    epaisseurs = get_epaisseurs(matiere_id,first_type)
    result_epp = []
    for row_epp in  epaisseurs : 
        result_epp.append(row_epp._data()) 
    epaisseur_id = result_epp[0]['value']
    
    # print(epaisseur_id)
  
    types_usinage= get_types_usinage(matiere_id,first_type,epaisseur_id)
    # # print("****<<<<<<*******")
    result_type = []
    for row_type in  types_usinage : 
        result_type.append(row_type._data()) 
    first_tpye_usinage = result_type[0]['id']
    first_type_usinage_name = result_type[0]['name']
    
    if 'file' in request.files:
        if matiereText == "Pmma" and first_type_usinage_name  =="USIL":
            prix = get_prix_pmma_usil(matiere_id,first_type,epaisseur_id,first_tpye_usinage) 
        else:
            prix = get_prix(matiere_id,first_type,epaisseur_id,first_tpye_usinage ) 
        result_envoi = {"matieres_types":result_matiere_types,'epaisseurs': result_epp, "types_usinage":result_type, 'prix':prix}
    else:
        result_envoi = {"matieres_types":result_matiere_types,'epaisseurs': result_epp, "types_usinage":result_type}
    
    return jsonify(result_envoi)


@app.route('/change_lettre_matiere', methods=['POST'])
def change_lettre_matiere():
    data = request.form.to_dict()
    matiere_id = data ['matiere_id']
    types_matiers = get_types_lettre_by_matiere(matiere_id)
    result_type_matieres_lettre = []
    for row_tp in  types_matiers: 
        result_type_matieres_lettre.append(row_tp._data()) 
    first_type_matieres_lettre = result_type_matieres_lettre[0]['id']

    epaisseurs_lettre= get_epaisseurs_lettre(matiere_id,first_type_matieres_lettre)
    result_epaisseurs_lettre = []
    for row_epp in  epaisseurs_lettre: 
        result_epaisseurs_lettre.append(row_epp._data()) 
    first_epaisseur_lettre = result_epaisseurs_lettre[0]['id']   

    usinage_type_lettre = get_usinage_types_lettre(matiere_id,first_type_matieres_lettre,first_epaisseur_lettre)
    result_usinage_lettre = []
    for row_usinage in  usinage_type_lettre: 
        result_usinage_lettre.append(row_usinage._data()) 
    first_usinage_lettre = result_usinage_lettre[0]['id'] 

    hauteurs_lettre = get_hauteurs_lettre(matiere_id,first_type_matieres_lettre,first_epaisseur_lettre,first_usinage_lettre)
    result_hauteurs_lettre = []
    for row_hauteur in  hauteurs_lettre: 
        result_hauteurs_lettre.append(row_hauteur._data())
    hauteur_id  = result_hauteurs_lettre[0]["id"]
    if 'nbr_lettres' in data:
        prix_lettre = get_prix_lettre(matiere_id,first_type_matieres_lettre,first_usinage_lettre ,first_epaisseur_lettre,hauteur_id )
        result_prix = []
        result_prix.append(prix_lettre._data)
        result_envoi = {"matieres_types":result_type_matieres_lettre,'epaisseurs': result_epaisseurs_lettre, "types_usinage":result_usinage_lettre,"hauteurs":result_hauteurs_lettre, "prix":result_prix}
    else:
        result_envoi = {"matieres_types":result_type_matieres_lettre,'epaisseurs': result_epaisseurs_lettre, "types_usinage":result_usinage_lettre,"hauteurs":result_hauteurs_lettre}
    
    return jsonify(result_envoi)
    

@app.route('/change_epaisseur', methods=['POST'])
def change_epaisseur():
    data = request.form.to_dict()
    matiere_id = data ['matiere_id']
    type_id = data ['type_id']
    epaisseur_id = data ['epaisseur_id']
    matiereText = data['matiereText']


  
    types_usinage= get_types_usinage(matiere_id,type_id,epaisseur_id)
    # print("****<<<<<<*******")
    # print(types_usinage)
    result_type = []
    for row_type in  types_usinage : 
        result_type.append(row_type._data()) 
    first_tpye_usinage = result_type[0]['id']
    first_type_usinage_name = result_type[0]['name']
    # file = request.files['file']

    if 'file' in request.files:

        if matiereText == "Pmma" and first_type_usinage_name  =="USIL":
            prix = get_prix_pmma_usil(matiere_id,first_type,epaisseur_id,first_tpye_usinage) 
        else:
            prix = get_prix(matiere_id,first_type,epaisseur_id,first_tpye_usinage ) 
        result_envoi = {"types_usinage":result_type, 'prix':prix}
    else:
        result_envoi = {"types_usinage":result_type}
    return jsonify(result_envoi)
# change type usinage
@app.route('/change_type_usinage', methods=['POST'])
def change_type_usinage():
    data = request.form.to_dict()
    matiere_id = data ['matiere_id']
    type_id = data ['type_id']
    epaisseur_id = data ['epaisseur_id']
    type_usinage_id = data ['type_usinage_id']
    matiereText = data['matiereText']
    print(matiereText)
    selectedUsinageTypeText = data['selectedUsinageTypeText']
    if matiereText == "Pmma" and selectedUsinageTypeText  =="USIL":
        print("testttt")
        prix = get_prix_pmma_usil(matiere_id,type_id,epaisseur_id,type_usinage_id) 
    else:
        prix = get_prix(matiere_id,type_id,epaisseur_id,type_usinage_id ) 
    result_envoi = { 'prix':prix}
    return jsonify(result_envoi)

@app.route('/change_lettre_type', methods=['POST'])
def change_lettre_type():
    data = request.form.to_dict()
    matiere_id = data ['matiere_id']
    type_id= data ['type_id']


    epaisseurs_lettre= get_epaisseurs_lettre(matiere_id,type_id)
    result_epaisseurs_lettre = []
    for row_epp in  epaisseurs_lettre: 
        result_epaisseurs_lettre.append(row_epp._data()) 
    first_epaisseur_lettre = result_epaisseurs_lettre[0]['id']   

    usinage_type_lettre = get_usinage_types_lettre(matiere_id,type_id,first_epaisseur_lettre)
    result_usinage_lettre = []
    for row_usinage in  usinage_type_lettre: 
        result_usinage_lettre.append(row_usinage._data()) 
    first_usinage_lettre = result_usinage_lettre[0]['id'] 

    hauteurs_lettre = get_hauteurs_lettre(matiere_id,type_id,first_epaisseur_lettre,first_usinage_lettre)
    result_hauteurs_lettre = []
    for row_hauteur in  hauteurs_lettre: 
        result_hauteurs_lettre.append(row_hauteur._data())
    hauteur_id  = result_hauteurs_lettre[0]["id"]
    if 'nbr_lettres' in data:
        prix_lettre = get_prix_lettre(matiere_id,type_id,first_usinage_lettre ,first_epaisseur_lettre,hauteur_id )
        result_prix = []
        result_prix.append(prix_lettre._data)
        result_envoi = {'epaisseurs': result_epaisseurs_lettre, "types_usinage":result_usinage_lettre,"hauteurs":result_hauteurs_lettre, "prix":result_prix}
    else:
        result_envoi = {'epaisseurs': result_epaisseurs_lettre, "types_usinage":result_usinage_lettre,"hauteurs":result_hauteurs_lettre}
    
    return jsonify(result_envoi)

@app.route('/change_lettre_epaisseur', methods=['POST'])
def change_lettre_epaisseur():
    data = request.form.to_dict()
    matiere_id = data ['matiere_id']
    type_id= data ['type_id']
    epaisseur_id = data['epaisseur_id']
 

    usinage_type_lettre = get_usinage_types_lettre(matiere_id,type_id,epaisseur_id)
    result_usinage_lettre = []
    for row_usinage in  usinage_type_lettre: 
        result_usinage_lettre.append(row_usinage._data()) 
    first_usinage_lettre = result_usinage_lettre[0]['id'] 

    hauteurs_lettre = get_hauteurs_lettre(matiere_id,type_id,epaisseur_id,first_usinage_lettre)
    result_hauteurs_lettre = []
    for row_hauteur in  hauteurs_lettre: 
        result_hauteurs_lettre.append(row_hauteur._data())
    hauteur_id  = result_hauteurs_lettre[0]["id"]
    if 'nbr_lettres' in data:
        prix_lettre = get_prix_lettre(matiere_id,type_id,first_usinage_lettre ,epaisseur_id,hauteur_id )
        result_prix = []
        result_prix.append(prix_lettre._data)
        result_envoi = { "types_usinage":result_usinage_lettre,"hauteurs":result_hauteurs_lettre, "prix":result_prix}
    else:
        result_envoi = { "types_usinage":result_usinage_lettre,"hauteurs":result_hauteurs_lettre}
    
    return jsonify(result_envoi)


@app.route('/change_lettre_usinage', methods=['POST'])
def change_lettre_usinage():
    data = request.form.to_dict()
    matiere_id = data ['matiere_id']
    type_id= data ['type_id']
    epaisseur_id = data['epaisseur_id']
    usinage_id = data['usinage_id']


    hauteurs_lettre = get_hauteurs_lettre(matiere_id,type_id,epaisseur_id,usinage_id)
    result_hauteurs_lettre = []
    for row_hauteur in  hauteurs_lettre: 
        result_hauteurs_lettre.append(row_hauteur._data())
    hauteur_id  = result_hauteurs_lettre[0]["id"]
    if 'nbr_lettres' in data:
        prix_lettre = get_prix_lettre(matiere_id,type_id,usinage_id ,epaisseur_id,hauteur_id )
        result_prix = []
        result_prix.append(prix_lettre._data)
        result_envoi = { "hauteurs":result_hauteurs_lettre, "prix":result_prix}
    else:
        result_envoi = { "hauteurs":result_hauteurs_lettre}
    
    return jsonify(result_envoi)

@app.route('/change_lettre_hauteur', methods=['POST'])
def change_lettre_hauteur():
    data = request.form.to_dict()
    matiere_id = data ['matiere_id']
    type_id= data ['type_id']
    epaisseur_id = data['epaisseur_id']
    usinage_id = data['type_usinage']
    hauteur_id = data['hauteur']

    prix_lettre = get_prix_lettre(matiere_id,type_id,usinage_id ,epaisseur_id,hauteur_id )
    result_prix = []
    result_prix.append(prix_lettre[0])
    result_envoi = {"prix":result_prix}

    
    return jsonify(result_envoi)

@app.route('/charge_text_data', methods=['POST'])
def charge_text_data():
    matieres= BridgeLettres.get_all_matieres_lettre()
    result_matieres_lettre = []
    for row_mt in  matieres : 
        result_matieres_lettre.append(row_mt._data()) 


    first_matiere = result_matieres_lettre[0]['id']
    types_matiers = get_types_lettre_by_matiere(first_matiere)
    result_type_matieres_lettre = []
    for row_tp in  types_matiers: 
        result_type_matieres_lettre.append(row_tp._data()) 
    first_type_matieres_lettre = result_type_matieres_lettre[0]['id']

    epaisseurs_lettre= get_epaisseurs_lettre(first_matiere,first_type_matieres_lettre)
    result_epaisseurs_lettre = []
    for row_epp in  epaisseurs_lettre: 
        result_epaisseurs_lettre.append(row_epp._data()) 
    first_epaisseur_lettre = result_epaisseurs_lettre[0]['id']   

    usinage_type_lettre = get_usinage_types_lettre(first_matiere,first_type_matieres_lettre,first_epaisseur_lettre)
    result_usinage_lettre = []
    for row_usinage in  usinage_type_lettre: 
        result_usinage_lettre.append(row_usinage._data()) 
    first_usinage_lettre = result_usinage_lettre[0]['id'] 

    hauteurs_lettre = get_hauteurs_lettre(first_matiere,first_type_matieres_lettre,first_epaisseur_lettre,first_usinage_lettre)
    result_hauteurs_lettre = []
    for row_hauteur in  hauteurs_lettre: 
        result_hauteurs_lettre.append(row_hauteur._data())

    result_envoi = {"matieres":result_matieres_lettre,"types":result_type_matieres_lettre,'epaisseurs': result_epaisseurs_lettre, "types_usinage":result_usinage_lettre,"hauteurs":result_hauteurs_lettre}
    return jsonify(result_envoi)
@app.route('/charge_form_data', methods=['POST'])
def charge_form_data():

    matieres= Matiere.get_all_matiere()
    result_matieres = []
    for row_mt in  matieres : 
        result_matieres.append(row_mt._data()) 
    first_matiere = result_matieres[0]['id']

    types_matiers = get_types_by_matiere(first_matiere) 
    result_type_matieres = []
    for row_tp in  types_matiers: 
        result_type_matieres.append(row_tp._data()) 
    first_type_matieres = result_type_matieres[0]['id']

    epaisseurs= get_epaisseurs(first_matiere,first_type_matieres)
    result_epaisseurs = []
    for row_epp in  epaisseurs: 
        result_epaisseurs.append(row_epp._data()) 
    first_epaisseur = result_epaisseurs[0]['id']   

    usinage_type = get_types_usinage(first_matiere,first_type_matieres,first_epaisseur)
    result_usinage = []
    for row_usinage in  usinage_type: 
        result_usinage.append(row_usinage._data()) 

    result_envoi = {"matieres":result_matieres,"types":result_type_matieres,'epaisseurs': result_epaisseurs, "types_usinage":result_usinage}
    return jsonify(result_envoi)

@app.route('/membres')
@login_required
def membres():
    roles = Role.get_all_roles()
    # result_roles=[]
    # for row_role in  roles: 
    #     result_roles.append(row_role._data()) 
   
    first_role = roles[0].id
    users = get_users_by_role(first_role)
  
        
    return render_template('membres.html', roles=roles,select_users=users, user = current_user)

@app.route('/clients')
@login_required
def clients():
    representants = get_all_representants()
   
   
    first_rep = representants[0].id
    clients= get_cients_by_rep(first_rep)

    return render_template('clients.html', user = current_user,representants = representants, clients=clients)

@app.route('/prix')
@login_required
def prix():
    matieres= Matiere.get_all_matiere()
   
    result_matieres = []
    for row_mt in  matieres : 
        result_matieres.append(row_mt._data()) 
    first_matiere = result_matieres[0]['id']

    types_matieres = get_types_by_matiere(first_matiere) 
    result_type_matieres = []
    for row_tp in  types_matieres: 
        result_type_matieres.append(row_tp._data())
    first_type = result_type_matieres[0]['id']
     
    result_types_usinage = []
    types_usinage = get_types_usinage_prix(first_matiere,first_type )
    for row_usinage  in  types_usinage: 
        result_types_usinage.append(row_usinage ._data())
    first_type_usinage = result_types_usinage[0]['id']

    data_matieres = get_data_matieres(first_matiere,first_type,first_type_usinage)
    print(data_matieres)

    return render_template('prix.html', matieres = matieres,types_matieres=types_matieres , types_usinage = types_usinage,data_matieres= data_matieres, user = current_user)


@app.route('/users_by_role_selected', methods=['POST'])
def users_by_role_selected():
    data = request.form.to_dict()
    role = data ['role_value']

    users_by_role= get_users_by_role(role )
    # print("****<<<<<<*******")
    # print(types_usinage)
    result_users = []
    for row_user in  users_by_role : 
        result_users.append(row_user._data()) 
 
    # file = request.files['file']
    result_envoi = {"users_by_role":result_users}
    return jsonify(result_envoi)

@app.route('/matieres_liste', methods=['POST'])
def matieres_liste():
    data = request.form.to_dict()
    mt_id = data ['matiere_id']
    types_matieres = get_types_by_matiere(mt_id) 
    result_type_matieres = []
    for row_tp in  types_matieres: 
        result_type_matieres.append(row_tp._data())
    first_type = result_type_matieres[0]['id']

    result_types_usinage = []
    types_usinage = get_types_usinage_prix(mt_id,first_type )
    for row_usinage  in  types_usinage: 
        result_types_usinage.append(row_usinage ._data())
    first_type_usinage = result_types_usinage[0]['id']

    data_matieres = get_data_matieres(mt_id,first_type,first_type_usinage)
    res_data = []
        

    for row_data in data_matieres: 
        res_data.append({
            "matiere_name": row_data[0],
            "type_name": row_data[1],
            "usinage_name": row_data[2],
            "epaisseur_value": row_data[3],
            "prix_matiere": row_data[4],
            "prix_limeaire": row_data[5]
        })
 
    # file = request.files['file']
    result_envoi = {"liste_data":res_data, "types_matieres":result_type_matieres,"types_usinage":result_types_usinage}
    return jsonify(result_envoi)

@app.route('/type_liste', methods=['POST'])
def type_liste():
    data = request.form.to_dict()
    mt_id = data ['matiere_id']
    type_id = data ['type_id']

    result_types_usinage = []
    types_usinage = get_types_usinage_prix(mt_id,type_id )
    for row_usinage  in  types_usinage: 
        result_types_usinage.append(row_usinage ._data())
    first_type_usinage = result_types_usinage[0]['id']

    data_matieres = get_data_matieres(mt_id,type_id,first_type_usinage)
    
    res_data = []
        

    for row_data in data_matieres: 
        res_data.append({
            "matiere_name": row_data[0],
            "type_name": row_data[1],
            "usinage_name": row_data[2],
            "epaisseur_value": row_data[3],
            "prix_matiere": row_data[4],
            "prix_limeaire": row_data[5]
        })
 
    # file = request.files['file']
    result_envoi = {"liste_data":res_data, "types_usinage":result_types_usinage}
    return jsonify(result_envoi)
        

@app.route('/type_usinage_liste', methods=['POST'])
def type_usinage_liste():
    data = request.form.to_dict()
    mt_id = data ['matiere_id']
    type_id = data ['type_id']
    usinage_id = data['type_usinage_id']
    res_data = []

    if 'matiere_name' in data:
        matiere_name = data ['matiere_name']
        usinage_name = data ['usinage_name']
        pmma_usil_list = get_pmma_usil_list(mt_id ,type_id ,usinage_id)
        
        for row_data in pmma_usil_list: 
            res_data.append({
                "matiere_name": row_data[0],
                "type_name": row_data[1],
                "usinage_name": row_data[2],
                "epaisseur_value": row_data[3],
                "prix_1": row_data[4],
                "prix_2": row_data[5],
                "prix_3": row_data[6],
            })
        result_envoi = {"data_usil":res_data}
    else:
        data_matieres = get_data_matieres(mt_id,type_id,usinage_id)
        
        
        for row_data in data_matieres: 
            res_data.append({
                "matiere_name": row_data[0],
                "type_name": row_data[1],
                "usinage_name": row_data[2],
                "epaisseur_value": row_data[3],
                "prix_matiere": row_data[4],
                "prix_limeaire": row_data[5]
            })
 
    # file = request.files['file']
        result_envoi = {"liste_data":res_data}

    
    return jsonify(result_envoi)
@app.route('/change_representant', methods=['POST'])
def change_representant():

    data = request.form.to_dict()
    rep_id = data ['representant']
    print ("sqsqsqs")
    print(rep_id)
    clients= get_cients_by_rep(rep_id)
    # result_clients = []
    # for item in  clients : 
    #     client_data = item._data()
    #     result_clients.append(client_data) 
 
    # file = request.files['file']
    result_envoi = {"clients":clients}
    return jsonify(result_envoi)

@app.route('/new_client', methods=['POST'])
def new_client():
   

# Replace the following with your ESP file parsing logic
# Example data (x, y coordinates)
    print("xxxxxxxxx*****11111111")
    if request.method == 'POST':   
        print("99999999999999999999999")
        # Get other data from the request
        # current_date = datetime.now().date()
        
        data = request.form.to_dict()
        representant= data['representant']
        print ("eeee")
        print(data)
        name = data ['name']
        numeroVoie= data['numeroVoie']
        nameVoie= data ['nameVoie']
        cp= data['cp']
        ville = data ['ville']
        email = data ['email']
        tel = data ['tel']
        new_client = Client(user_id=representant, name=name, ville=ville, cp= cp ,numero = numeroVoie,addresse=nameVoie,email = email,tel=tel)
#             User.set_password(new_user, password1)
        # db.session.add(new_commande)
        # db.session.commit()
        print(new_client)
        Client.save(new_client)


        # user_id = current_user.id

        # new_commande = Commande(client_id=client_id, statut_id=1, name_matiere=name_matiere, type_matiere= type_matiere ,usinage_id = type_usinage,count=count,epaisseur_id = epaisseur_id, prix_matiere=prix_matiere, prix_limeaire=prix_limeaire, name_dxf= name_dxf,description_commercial_responsable=description, date_envoi=current_date, date_fin = current_date)
#             User.set_password(new_user, password1)
        # db.session.add(new_commande)
        # db.session.commit()
        # Commande.save(new_commande)

        return "d"
    return "c"


@app.route('/edit_client', methods=['POST'])
def edit_client():
   

    if request.method == 'POST':   
        
        data = request.form.to_dict()
        user_id= data['representant']
        name = data ['name']
        numeroVoie= data['numeroVoie']
        nameVoie= data ['nameVoie']
        cp= data['cp']
        ville = data ['ville']
        email = data ['email']
        tel = data ['tel']
        client_id = data['client_id']

       
        Edit_data=[
            {
                'id':client_id,
                'user_id':user_id, 
                'name':name, 
                'ville':ville,
                'cp': cp ,
                'numero': numeroVoie,
                'addresse':nameVoie,
                'email' : email,
                'tel':tel
            },
            ]
       

        edit_client_data(Edit_data)
        
    #    Client.save(edit_client)


        # user_id = current_user.id

        # new_commande = Commande(client_id=client_id, statut_id=1, name_matiere=name_matiere, type_matiere= type_matiere ,usinage_id = type_usinage,count=count,epaisseur_id = epaisseur_id, prix_matiere=prix_matiere, prix_limeaire=prix_limeaire, name_dxf= name_dxf,description_commercial_responsable=description, date_envoi=current_date, date_fin = current_date)
#             User.set_password(new_user, password1)
        # db.session.add(new_commande)
        # db.session.commit()
        # Commande.save(new_commande)

        return "d"
    return "c"


@app.route('/recevoir_prix_lettre', methods=['POST'])
def recevoir_prix_lettre():
    data = request.form.to_dict()
    matiere_id = data ['mt']
    type_id = data ['type']
    type_usinage_id = data['type_usinage']
    epaisseur_id = data['epaisseur']
    hauteur_id= data['hauteur']
    prix_lettre = get_prix_lettre(matiere_id,type_id,type_usinage_id ,epaisseur_id,hauteur_id )
    result_prix = []
    result_prix.append(prix_lettre._data)
 
    result_envoi = {'prix': result_prix }
    return jsonify(result_envoi)

@app.route('/edit_prix_matiere', methods=['POST'])
def edit_prix_matiere():
    data = request.form.to_dict()
    new_prix_matiere = data ['new_prix_matiere']
    matiere = data ['matiere']
    type_matiere= data['type_matiere']
    type_usinage = data['type_usinage']
    epaisseur= data['epaisseur']
    print(epaisseur)
    try:
    # Code that might raise an exception
        change_matiere_prix(matiere,type_matiere,type_usinage,epaisseur,new_prix_matiere )
        return ("it's ok")
    except ZeroDivisionError:
    # Handle the exception
        print("problem!")

@app.route('/edit_prix_limeaire', methods=['POST'])
def edit_prix_limeaire():
    data = request.form.to_dict()
    new_prix_limeaire = data ['new_prix_limeaire']
    matiere = data ['matiere']
    type_matiere= data['type_matiere']
    type_usinage = data['type_usinage']
    epaisseur= data['epaisseur']
    print(epaisseur)
    try:
    # Code that might raise an exception
        change_limeaire_prix(matiere,type_matiere,type_usinage,epaisseur,new_prix_limeaire )
        return ("it's ok")
    except ZeroDivisionError:
    # Handle the exception
        print("problem!")

@app.route('/delete_client', methods=['POST'])
def delete_client():
    data = request.form.to_dict()
    delete_client_id = data ['id_client']
    try:
        delete_commande_client(delete_client_id)
        return "it's ok" 
    except Exception as e:
        # Rollback the transaction in case of error
        return (e)

@app.route('/delete_bridge_row', methods=['POST'])
def delete_bridge_row():
    data = request.form.to_dict()
    matiere = data ['matiere']
    type_mt = data ['type']
    usinage = data ['usinage']
    epaisseur = data ['epaisseur']

    try:
        delete_bridge_form_row(matiere,type_mt ,usinage ,epaisseur)
        return "it's ok" 
    except Exception as e:
        # Rollback the transaction in case of error
        return (e)

# @app.route('/delete_bridge_usil_row', methods=['POST'])
# def delete_bridge_usil_row():
#     data = request.form.to_dict()
#     matiere = data ['matiere']
#     type_mt = data ['type']
#     usinage = data ['usinage']
#     epaisseur = data ['epaisseur']
#     print(matiere)
#     print(type_mt)
#     print(usinage)
#     print(epaisseur)
#     try:
#         delete_bridge_form_usil_row(matiere,type_mt ,usinage ,epaisseur)
#         return "it's ok" 
#     except Exception as e:
#         # Rollback the transaction in case of error
#         return (e)


@app.route('/charge_text_prix_data', methods=['POST'])
def charge_text_prix_data():
    matieres= BridgeLettres.get_all_matieres_lettre()
    result_matieres_lettre = []
    for row_mt in  matieres : 
        result_matieres_lettre.append(row_mt._data()) 


    first_matiere = result_matieres_lettre[0]['id']
    types_matiers = get_types_lettre_by_matiere(first_matiere)
    result_type_matieres_lettre = []
    for row_tp in  types_matiers: 
        result_type_matieres_lettre.append(row_tp._data()) 
    first_type_matieres_lettre = result_type_matieres_lettre[0]['id']

    epaisseurs_lettre= get_epaisseurs_lettre(first_matiere,first_type_matieres_lettre)
    result_epaisseurs_lettre = []
    for row_epp in  epaisseurs_lettre: 
        result_epaisseurs_lettre.append(row_epp._data()) 
    first_epaisseur_lettre = result_epaisseurs_lettre[0]['id']   

    # usinage_type_lettre = get_usinage_types_lettre(first_matiere,first_type_matieres_lettre,first_epaisseur_lettre)
    # result_usinage_lettre = []
    # for row_usinage in  usinage_type_lettre: 
    #     result_usinage_lettre.append(row_usinage._data()) 
    # first_usinage_lettre = result_usinage_lettre[0]['id'] 

    # hauteurs_lettre = get_hauteurs_lettre(first_matiere,first_type_matieres_lettre,first_epaisseur_lettre,first_usinage_lettre)
    # result_hauteurs_lettre = []
    # for row_hauteur in  hauteurs_lettre: 
    #     result_hauteurs_lettre.append(row_hauteur._data())
    prix_lettre_liste = get_liste_prix_lettre(first_matiere,first_type_matieres_lettre,first_epaisseur_lettre )
    result_prix_liste = []
    for row_data in prix_lettre_liste: 
        result_prix_liste.append({
            "matiere_name": row_data[0],
            "type_name": row_data[1],
            "usinage_name": row_data[2],
            "epaisseur_value": row_data[3],
            "hauteur_value": row_data[5],
            "prix": row_data[4],
        })

   
  
    result_envoi = {"matieres":result_matieres_lettre,"types":result_type_matieres_lettre,'epaisseurs': result_epaisseurs_lettre, "prix_lettre_list":result_prix_liste}
    return jsonify(result_envoi)

@app.route('/matieres_text_liste', methods=['POST'])
def matieres_text_liste():
    data = request.form.to_dict()
    mt_id = data ['matiere_id']
    types_matiers = get_types_lettre_by_matiere(mt_id)
    result_type_matieres_lettre = []
    for row_tp in  types_matiers: 
        result_type_matieres_lettre.append(row_tp._data()) 
    first_type_matieres_lettre = result_type_matieres_lettre[0]['id']

    epaisseurs_lettre= get_epaisseurs_lettre(mt_id,first_type_matieres_lettre)
    result_epaisseurs_lettre = []
    for row_epp in  epaisseurs_lettre: 
        result_epaisseurs_lettre.append(row_epp._data()) 
    first_epaisseur_lettre = result_epaisseurs_lettre[0]['id'] 
    prix_lettre_liste = get_liste_prix_lettre(mt_id,first_type_matieres_lettre,first_epaisseur_lettre )
    result_prix_liste = []
    for row_data in prix_lettre_liste: 
        result_prix_liste.append({
            "matiere_name": row_data[0],
            "type_name": row_data[1],
            "usinage_name": row_data[2],
            "epaisseur_value": row_data[3],
            "hauteur_value": row_data[5],
            "prix": row_data[4],
        })

   
  
    result_envoi = {"types":result_type_matieres_lettre,'epaisseurs': result_epaisseurs_lettre, "prix_lettre_list":result_prix_liste}
    return jsonify(result_envoi)


@app.route('/change_type_text_liste', methods=['POST'])
def change_type_text_liste():
    data = request.form.to_dict()
    mt_id = data ['matiere_id']
    type_id = data ['type_id']

    epaisseurs_lettre= get_epaisseurs_lettre(mt_id,type_id)
    result_epaisseurs_lettre = []
    for row_epp in  epaisseurs_lettre: 
        result_epaisseurs_lettre.append(row_epp._data()) 
    first_epaisseur_lettre = result_epaisseurs_lettre[0]['id'] 
    prix_lettre_liste = get_liste_prix_lettre(mt_id,type_id,first_epaisseur_lettre )
    result_prix_liste = []
    for row_data in prix_lettre_liste: 
        result_prix_liste.append({
            "matiere_name": row_data[0],
            "type_name": row_data[1],
            "usinage_name": row_data[2],
            "epaisseur_value": row_data[3],
            "hauteur_value": row_data[5],
            "prix": row_data[4],
        })

   
  
    result_envoi = {'epaisseurs': result_epaisseurs_lettre, "prix_lettre_list":result_prix_liste}
    return jsonify(result_envoi)


@app.route('/change_eppaisseur_text_liste', methods=['POST'])
def change_eppaisseur_text_liste():
    data = request.form.to_dict()
    mt_id = data ['matiere_id']
    type_id = data ['type_id']
    epaisseur_id = data['epaisseur_id']
   
    prix_lettre_liste = get_liste_prix_lettre(mt_id,type_id,epaisseur_id)
    result_prix_liste = []
    for row_data in prix_lettre_liste: 
        result_prix_liste.append({
            "matiere_name": row_data[0],
            "type_name": row_data[1],
            "usinage_name": row_data[2],
            "epaisseur_value": row_data[3],
            "hauteur_value": row_data[5],
            "prix": row_data[4],
        })

   
  
    result_envoi = {"prix_lettre_list":result_prix_liste}
    return jsonify(result_envoi)


@app.route('/delete_Lettrebridge_row', methods=['POST'])
def delete_Lettrebridge_row():
    data = request.form.to_dict()
    matiere = data ['matiere']
    type_mt = data ['type']
    usinage = data ['usinage']
    epaisseur = data ['epaisseur']

    try:
        delete_bridge_lettre_row(matiere,type_mt ,usinage ,epaisseur)
        return "it's ok" 
    except Exception as e:
        # Rollback the transaction in case of error
        return (e)


@app.route('/edit_prix_lettre', methods=['POST'])
def edit_prix_lettre():
    data = request.form.to_dict()
    new_prix_matiere = data ['new_prix']
    matiere = data ['matiere']
    type_matiere= data['type_matiere']
    type_usinage = data['type_usinage']
    epaisseur= data['epaisseur']
    hauteur= data['hauteur']
    print(epaisseur)
    try:
    # Code that might raise an exception
        change_lettre_prix(matiere,type_matiere,type_usinage,epaisseur,new_prix_matiere,hauteur )
        return ("it's ok")
    except ZeroDivisionError:
    # Handle the exception
        print("problem!")

@app.route('/new_user', methods=['POST'])
def new_user():
   

# Replace the following with your ESP file parsing logic
# Example data (x, y coordinates)
    print("xxxxxxxxx*****11111111")
    if request.method == 'POST':   
        print("99999999999999999999999")
        # Get other data from the request
        # current_date = datetime.now().date()
        
        data = request.form.to_dict()
        role= data['role']
        print ("eeee")
        print(data)
        email = data ['email']
        username = data ['username']
        password= data['password']
        
        tel = data ['tel']
        new_user = User(username=username, email=email, password=password, tel=tel,role_id = role)
        User.set_password(new_user, password)  
#  User.set_password(new_user, password1)
        # db.session.add(new_commande)
        # db.session.commit()
       
        User.save(new_user)


        # user_id = current_user.id

        # new_commande = Commande(client_id=client_id, statut_id=1, name_matiere=name_matiere, type_matiere= type_matiere ,usinage_id = type_usinage,count=count,epaisseur_id = epaisseur_id, prix_matiere=prix_matiere, prix_limeaire=prix_limeaire, name_dxf= name_dxf,description_commercial_responsable=description, date_envoi=current_date, date_fin = current_date)
#             User.set_password(new_user, password1)
        # db.session.add(new_commande)
        # db.session.commit()
        # Commande.save(new_commande)

        return "d"
    return "c"

@app.route('/edit_user', methods=['POST'])
def edit_user():
   

    if request.method == 'POST':   
        
        data = request.form.to_dict()
        user_id= data['user_id']
        role= data ['role']
        username= data['username']
        email= data ['email']
        password= data['password']
        tel = data ['tel']
        
        current_user = User.query.filter(User.id == user_id).first()
        print("xxxxxxxxxxxx")
        print(current_user.username)
        current_user.email = email
        current_user.role_id = role
        current_user.tel = tel
        current_user.username = username

        User.save(current_user)
        
    #    Client.save(edit_client)


        # user_id = current_user.id

        # new_commande = Commande(client_id=client_id, statut_id=1, name_matiere=name_matiere, type_matiere= type_matiere ,usinage_id = type_usinage,count=count,epaisseur_id = epaisseur_id, prix_matiere=prix_matiere, prix_limeaire=prix_limeaire, name_dxf= name_dxf,description_commercial_responsable=description, date_envoi=current_date, date_fin = current_date)
#             User.set_password(new_user, password1)
        # db.session.add(new_commande)
        # db.session.commit()
        # Commande.save(new_commande)

        return "d"
    return "c"


    

