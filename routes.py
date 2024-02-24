from flask import Flask,Blueprint, render_template,request,jsonify,flash
from datetime import datetime
# from controllers import matiere
# from models.models import Pvc
from models  import models

from models.models   import User, Matiere,get_data,get_prix, get_clients,get_en_attentes, get_confirmes,change_confirmer, change_usiner,Commande
from flask_login import login_user, login_required, logout_user, current_user
from controllers.functions import get_dimension
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
import ezdxf
import math
import os

main = Blueprint ('main' , __name__) #routename = main7




# @login_manager.user_loader
# def load_user(user_id):
#   return User.get(user_id)

@main.route('/usinage' ,  methods=['GET', 'POST'])
@login_required
def Usinage(): 
    if request.method == 'POST':
        matiere = request.args.get('matiere')
        name = request.args.get('type')
        data = get_data(matiere,name)
        return render_template('usinage.html',user=current_user, matiere = matiere, name = name , data = data)
    if(current_user.role_id == 2):
        matiere = 'Pvc'
        name = 'Mat'
        data = get_data(matiere,name)
        clients = get_clients(current_user)
        return render_template('usinage.html',user=current_user, matiere = matiere, name = name , data = data, clients=clients)
    return render_template('home.html')

@main.route('/en_attente' ,  methods=['GET', 'POST'])
@login_required
def en_attente(): 
    data = get_en_attentes(current_user)
    print(data)

    return render_template('en_attente.html', user = current_user,data=data)

@main.route('/confirmé' ,  methods=['GET', 'POST'])
@login_required
def confirmé(): 
    data = get_confirmes(current_user)
    return render_template('confirmé.html', user = current_user,data=data)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.filter_by_email(email)
        if user:
            if User.is_password_correct(user, password):
                flash('Connecté avec succès!', category='success')
                login_user(user, remember=True)
                if(current_user.role_id == 2):
                    matiere = 'Pvc'
                    name = 'Mat'
                    data = get_data(matiere,name)
                    clients = get_clients(current_user)
                    return render_template('usinage.html',user=current_user, matiere = matiere, name = name , data = data, clients=clients)
                else:
                    return render_template("en_attente.html",user=current_user)
            else:
                flash('Email ou mot de passe incorrect, réessayez.', category='error')
        else:
            flash('Email ou mot de passe incorrect, réessayez.', category='error')
    return render_template("index.html")

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template("index.html")

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

@main.route('/upload', methods=['POST'])
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
                    print("dsssssssssssssss")
                    print(result)
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
                    print(length)
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
                    print("e")
                    points = e.points()
                    points = list(points)
                    for i in range(len(points) - 1):
                        dx = points[i+1][0] - points[i][0]
                        dy = points[i+1][1] - points[i][1]
                        perimetre += math.sqrt(dx**2 + dy**2)
            # return str(perimetre)
        result = {'perimetre': perimetre,'dimension': dimension, 'prix': prix, 'path_folder':path_folder}
        return jsonify(result)


@main.route('/new_command', methods=['POST'])
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
@main.route('/change_statut_confirmer', methods=['POST'])
def change_statut_confirmer():
   

# Replace the following with your ESP file parsing logic
# Example data (x, y coordinates)

    if request.method == 'POST':
        dt = request.form.to_dict()
        id=dt["id"]
        print(id)
        change_confirmer(id)
    return "ds"

@main.route('/change_statut_usiner', methods=['POST'])
def change_statut_usiner():
   
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxx")
# Replace the following with your ESP file parsing logic
# Example data (x, y coordinates)

    if request.method == 'POST':
        dt = request.form.to_dict()
        id=dt["id"]
        print(id)
        change_usiner(id)
    return "ds"
 