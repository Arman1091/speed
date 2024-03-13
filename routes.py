from flask import Flask,Blueprint, render_template,request,jsonify,flash,send_file, session,redirect,url_for

# from controllers import matiere
# from models.models import Pvc
from models  import models

from models.models   import User, Matiere,get_epaisseurs,get_prix, get_clients,get_en_attentes, get_en_attente_by_id, get_confirmes,get_usinés,get_livré,get_confirmé_by_id,change_confirmer, change_usiner, change_livré,supprimer_commande_attente,supprimer_commande_confirmé,supprimer_commande_usiné,get_types_by_matiere,get_types_usinage,Matiere,Commande,get_all_attentes,get_all_confirmes,get_all_usinés,get_all_livré
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
                    
        clients = get_clients(current_user)
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
            prix = get_prix(mt,mt_name,epp,type_usinage) 
            # os.remove('static/img/upload/current.png')
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


# *****************
           
         
# *****************************************
            # os.remove(file_path)
            perimetre = 0
            # Parcourir toutes les entités dans l'espace modèle
            for e in msp:
                # Si l'entité est une LWPOLYLINE (polygone)
             # Si l'entité est une LWPOLYLINE (polygone)
                if e.dxftype() == 'CIRCLE':
                    dc = 2*math.pi*e.dxf.radius
                    perimetre +=dc
                if e.dxftype() == 'LINE':
                                # Extract start and end points
                    length = e.dxf.start.distance(e.dxf.end)
                                # Calculate distance and add to total length
                    perimetre +=length
                if e.dxftype() == 'LWPOLYLINE':
                    points = e.get_points()
                    points = list(points)
                 
                    for i in range(x- 1):
                        dx = points[i+1][0] - points[i][0]
                        dy = points[i+1][1] - points[i][1]
                        perimetre += math.sqrt(dx**2 + dy**2)
                
                # Si l'entité est une POLYLINE
                elif e.dxftype() == 'POLYLINE':

                    points = e.points()
                    points = list(points)
                    for i in range(len(points) - 1):
                        dx = points[i+1][0] - points[i][0]
                        dy = points[i+1][1] - points[i][1]
                        perimetre += math.sqrt(dx**2 + dy**2)
            # return str(perimetre)
        result = {'perimetre': perimetre,'dimension': dimension, 'prix': prix, 'path_folder':path_folder}
        return jsonify(result)


@app.route('/new_command', methods=['POST'])
def new_command():
   

# Replace the following with your ESP file parsing logic
# Example data (x, y coordinates)

    if request.method == 'POST':   
        # Get other data from the request
        current_date = datetime.now().date()
        
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
        dt = request.form.to_dict()
        id=dt["id"]
        change_confirmer(id)
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

    if 'file' in request.files:
        prix = get_prix(matiere_id,type_id,epaisseur_id,first_tpye_usinage ) 
        result_envoi = {'epaisseurs': result_epp, "types_usinage":result_type, 'prix':prix}
    else:
        result_envoi = {'epaisseurs': result_epp, "types_usinage":result_type}
    return jsonify(result_envoi)

@app.route('/change_matiere', methods=['POST'])
def change_matiere():
    data = request.form.to_dict()
    matiere_id = data ['matiere_id']
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
    
    if 'file' in request.files:
        prix = get_prix(matiere_id,first_type,epaisseur_id,first_tpye_usinage ) 
        result_envoi = {"matieres_types":result_matiere_types,'epaisseurs': result_epp, "types_usinage":result_type, 'prix':prix}
    else:
        result_envoi = {"matieres_types":result_matiere_types,'epaisseurs': result_epp, "types_usinage":result_type}
    
    return jsonify(result_envoi)

@app.route('/change_epaisseur', methods=['POST'])
def change_epaisseur():
    data = request.form.to_dict()
    matiere_id = data ['matiere_id']
    type_id = data ['type_id']
    epaisseur_id = data ['epaisseur_id']


  
    types_usinage= get_types_usinage(matiere_id,type_id,epaisseur_id)
    # print("****<<<<<<*******")
    # print(types_usinage)
    result_type = []
    for row_type in  types_usinage : 
        result_type.append(row_type._data()) 
    first_tpye_usinage = result_type[0]['id']
    # file = request.files['file']

    if 'file' in request.files:
        prix = get_prix(matiere_id,type_id,epaisseur_id,first_tpye_usinage ) 
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

    prix = get_prix(matiere_id,type_id,epaisseur_id,type_usinage_id ) 
    result_envoi = { 'prix':prix}
    return jsonify(result_envoi)
