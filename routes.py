from flask import Flask,Blueprint, render_template,request,jsonify,flash,send_file, session,redirect,url_for


from models.models   import User,Client, Commande,Matiere,Role,BridgeLettres,get_epaisseurs,get_prix,get_prix_pmma_usil, get_clients_by_user,get_en_attentes, get_en_attente_by_id, get_confirmes,get_usinés,get_livré ,get_confirmé_by_id,change_confirmer, change_usiner, change_livré,supprimer_commande_attente,supprimer_commande_confirmé,supprimer_commande_usiné,get_types_by_matiere,get_types_usinage,Matiere,Commande,get_all_attentes,get_all_confirmes,get_all_usinés,get_all_livré,get_types_lettre_by_matiere,get_epaisseurs_lettre,get_usinage_types_lettre,get_hauteurs_lettre,get_users_by_role,get_data_matieres,get_all_representants,get_cients_by_rep,edit_client_data,get_prix_lettre,change_matiere_prix,change_limeaire_prix,get_types_usinage_prix,get_pmma_usil_list,delete_commande_client,delete_bridge_form_row,get_liste_prix_lettre,delete_bridge_lettre_row,change_lettre_prix
from flask_login import login_user, login_required, logout_user, current_user
from controllers.functions import get_dimension , create_pdf, create_bl
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import matplotlib.pyplot as plt
from ezdxf.addons.drawing import RenderContext, Frontend
from sqlalchemy.orm.exc import NoResultFound

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


# ****simulation****
@app.route('/simulation' ,  methods=['GET', 'POST'])
@login_required
def Simulation():
    try:
        current_user_role = (Role.query.filter(Role.id == current_user.role_id).first()).name
    except Exception as e:
        return f"Error fetching current user role: {str(e)}"

    if current_user_role=="comercial":
        try:
            matieres = Matiere.get_all_matiere()
            result_matieres = [row_mt._data() for row_mt in matieres]
            first_matiere = result_matieres[0]['id']
        except Exception as e:
            return f"Error fetching matieres: {str(e)}"

        try:
            types_matiers = get_types_by_matiere(first_matiere)
            result_type_matieres = [row_tp._data() for row_tp in types_matiers]
            first_type_matieres = result_type_matieres[0]['id']
        except Exception as e:
            return f"Error fetching types matieres: {str(e)}"

        try:
            epaisseurs = get_epaisseurs(first_matiere, first_type_matieres)
            result_epaisseurs = [row_epp._data() for row_epp in epaisseurs]
            first_epaisseur = result_epaisseurs[0]['id']
        except Exception as e:
            return f"Error fetching epaisseurs: {str(e)}"

        try:
            usinage_type = get_types_usinage(first_matiere, first_type_matieres, first_epaisseur)
            result_usinage = [row_usinage._data() for row_usinage in usinage_type]
        except Exception as e:
            return f"Error fetching usinage types: {str(e)}"

        try:
            clients = get_clients_by_user(current_user)
        except Exception as e:
            return f"Error fetching clients: {str(e)}"
        return render_template('simulation.html', user=current_user,current_user_role = current_user_role, matieres=matieres, types_matiers=types_matiers, clients=clients, epaisseurs=epaisseurs, types_usinage=usinage_type, page="Simulation")
    else:
        return redirect(url_for('en_attente'))


@app.route('/en_attente' ,  methods=['GET', 'POST'])
@login_required
def en_attente():

    try:
        data = []


        try:
            current_user_role = (Role.query.filter(Role.id == current_user.role_id).first()).name
        except Exception as e:
            return f"Error fetching current user role: {str(e)}"
        if current_user_role == "comercial":
            data = get_en_attentes(current_user)
        else:
            data = get_all_attentes()
        for i in range(len(data)):
            row_list = list(data[i])
            datetime_obj = datetime.strptime(row_list[3], "%Y-%m-%d %H:%M:%S.%f")
            date_DMY = datetime_obj.strftime("%d-%m-%Y")
            date_HMS = datetime_obj.strftime("%H:%M:%S")

            today_date =  datetime.now().strftime("%d-%m-%Y")
            if date_DMY == today_date:
                row_list[3]  = date_HMS
            else:
                row_list[3]  = date_DMY

            data[i] = tuple(row_list)

        return render_template('en_attente.html', user = current_user,current_user_role = current_user_role, data=data, page ="attents")
    except ValueError as e:
        flash(str(e), 'error')


@app.route('/confirme' ,  methods=['GET', 'POST'])
@login_required
def confirme():
    try:
        current_user_role = (Role.query.filter(Role.id == current_user.role_id).first()).name

        if current_user_role == "comercial":
            data = get_confirmes(current_user)
        else:
            data = get_all_confirmes()

        for i in range(len(data)):
            # Convert the tuple to a list
            row_list = list(data[i])
            datetime_obj = datetime.strptime(row_list[12], "%Y-%m-%d %H:%M:%S.%f")
            date_DMY = datetime_obj.strftime("%d-%m-%Y")
            date_HMS = datetime_obj.strftime("%H:%M:%S")

            today_date = datetime.now().strftime("%d-%m-%Y")
            if date_DMY == today_date:
                row_list[12] = date_HMS
            else:
                row_list[12] = date_DMY

            data[i] = tuple(row_list)

        return render_template('confirme.html', user=current_user, current_user_role= current_user_role,data=data, page="Confirmés")

    except Exception as e:
        print(f"An error occurred: {e}")
        return render_template('error.html', message="An unexpected error occurred"), 500
@app.route('/usiner' ,  methods=['GET', 'POST'])
@login_required
def usiner():
    try:
            current_user_role = (Role.query.filter(Role.id == current_user.role_id).first()).name
    except Exception as e:
            return f"Error fetching current user role: {str(e)}"
    if current_user_role == "comercial":
        data = get_usinés(current_user)
    else:
        data = get_all_usinés()
    path_folder = "/members/"+ current_user_role+'/'+current_user.username
    return render_template('usiner.html', user = current_user, current_user_role= current_user_role, data=data, page ="Usinés", path_folder = path_folder)

@app.route('/livrer' ,  methods=['GET', 'POST'])
@login_required
def livrer():
    if current_user.role_id == 2:
        data = get_livré(current_user)
    else:
       data = get_all_livré()
    current_user_role = (Role.query.filter(Role.id == current_user.role_id).first()).name
    path_folder = "/members/"+ current_user_role+'/'+current_user.username
    return render_template('livrer.html', user = current_user,current_user_role= current_user_role,data=data, page = "Livrés", path_folder = path_folder)


@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=30)

# connexion
@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('en_attente'))

        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            if not email or not password:
                flash('Tous les champs sont obligatoires.', category='error')
                return render_template("index.html")

            user = User.filter_by_email(email)
            if user:
                if User.is_password_correct(user, password):
                    flash('Connecté avec succès!', category='success')
                    login_user(user, remember=True)
                    current_user_role = (Role.query.filter(Role.id == current_user.role_id).first()).name
                    if current_user_role == "comercial":
                        return redirect(url_for('Simulation'))
                    else:
                        return redirect(url_for('en_attente'))
                else:
                    flash('Email ou mot de passe incorrect, réessayez.', category='error')
            else:
                flash('Email ou mot de passe incorrect, réessayez.', category='error')

        return render_template("index.html")
    except Exception as e:
        flash(f'Une erreur s\'est produite: {str(e)}', category='error')
        return render_template("index.html")
@app.route('/logout', methods=['GET', 'POST'])

def logout():
	logout_user()
	return redirect(url_for('index'))


#     return jsonify({'redirect_url': 'en_attente/detailles'})
@app.route('/en_attente/detailles' ,  methods=['GET', 'POST'])
@login_required
def en_attente_detailles():
    try:
        id = request.args.get('id')

        # Check if id is provided
        if id is None:
            raise ValueError("ID is required")

        # Fetch the data using the provided ID
        data = get_en_attente_by_id(id)

        if data is None:
            raise NoResultFound(f"No data found for ID: {id}")

        # Fetch the current user's role
        current_client_role = data[24]
        current_client_username = data[15]
        # Construct the path folder
        path_folder = "/members/" + current_client_role + '/' + current_client_username
        try:
            current_user_role = (Role.query.filter(Role.id == current_user.role_id).first()).name
        except Exception as e:
            return f"Error fetching current user role: {str(e)}"
        # Render the template with the data
        return render_template("en_attente_detailles.html", user=current_user,current_user_role = current_user_role, data=data, path_folder=path_folder)

    except NoResultFound as e:
        # Log the error message if you have a logging system in place
        # For now, just print the error message
        print(f"An error occurred: {e}")
        return render_template("error.html", message=str(e)), 404

    except ValueError as e:
        # Handle missing ID or other value errors
        print(f"An error occurred: {e}")
        return render_template("error.html", message=str(e)), 400

    except Exception as e:
        # Log the error message if you have a logging system in place
        # For now, just print the error message
        print(f"An unexpected error occurred: {e}")
        return render_template("error.html", message="An unexpected error occurred"), 500

@app.route('/confirme/detailles' ,  methods=['GET', 'POST'])
@login_required
def confirme_detailles():
    id = request.args.get('id')
    data = get_confirmé_by_id(id)
    if data is None:
        raise NoResultFound(f"No data found for ID: {id}")
    current_client_role = data[18]
    current_client_username=data[16]

    path_folder = "/members/"+ current_client_role+'/'+current_client_username
    try:
        current_user_role = (Role.query.filter(Role.id == current_user.role_id).first()).name
    except Exception as e:
        return f"Error fetching current user role: {str(e)}"
    return render_template("confirme_detailles.html",user=current_user,current_user_role = current_user_role,data=data,path_folder= path_folder)
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

    if request.method == 'POST':

        file = request.files['file']
        if file:
            data = request.form.to_dict()
            mt= data['mt']
            mt_name = data ['mt_name']
            epp = data['selectedValue']
            type_usinage = data['selectedTypeValue']
            mt_text = data['mt_text']
            usinage_text = data['usinage_text']


            filename = secure_filename(file.filename)
            preferred_name = "current" + os.path.splitext(filename)[1]
            current_user_role = (Role.query.filter(Role.id == current_user.role_id).first()).name
            path_folder = "static/members/"+ current_user_role+'/'+current_user.username
            fulle_path_folder = os.path.dirname(__file__)+"/"+ path_folder

            file_path = os.path.join(fulle_path_folder, preferred_name)


            # Check if the folder exists, if not, create it
            if not os.path.exists(fulle_path_folder):
                os.makedirs(fulle_path_folder)
            file.save(file_path)

            dimension = get_dimension(fulle_path_folder)


            plt.rcParams["savefig.facecolor"] = 'black'
            plt.rcParams['axes.facecolor'] = 'black'
            dwg = ezdxf.readfile(fulle_path_folder+"/current.dxf")
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
               fig.savefig(fulle_path_folder+'/current.png', dpi=300, facecolor = 'black', edgecolor = 'black')
            if mt_text == "Pmma" and usinage_text =="USIL":
                prix_pmma_usil = get_prix_pmma_usil(mt,mt_name,epp,type_usinage)
            else:
                prix = get_prix(mt,mt_name,epp,type_usinage)
                # os.remove('static/img/upload/current.png')

                # os.remove(file_path)
                perimetre = 0
                nbr_percage = 0
                # Parcourir toutes les entités dans l'espace modèle
                for e in msp:
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
                    elif e.dxftype() == 'LWPOLYLINE':
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
                    elif e.dxftype() == 'ARC':
                        radius = e.dxf.radius
                        start_angle = math.radians(e.dxf.start_angle)
                        end_angle = math.radians(e.dxf.end_angle)
                        arc_length = radius * abs(end_angle - start_angle)
                        perimetre += arc_length
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
        statut_id = data ['statut']
        description = data ['description']
        date_fin = data ['date_fin']
        epaisseur_id = data['epaisseur_id']

        is_livr = data ['is_livr']
        prix_ht = data ['prix_ht']
        if 'file' in request.files:
            file = request.files['file']
            filename = secure_filename(file.filename)
            preferred_name = os.path.splitext(filename)[0]
            last_row = Commande.query.order_by(Commande.id.desc()).first()
            if last_row is None:
                support_name = 1
            else:
                support_name = last_row.id+1

            current_user_role = (Role.query.filter(Role.id == current_user.role_id).first()).name


            path_folder = "static/members/"+current_user_role+'/'+current_user.username+'/DXF/'
            first_full_name = preferred_name+str(support_name)
            full_name = preferred_name+str(support_name)+'.dxf'
            is_form = True
            file_path = os.path.join(os.path.dirname(__file__)+'/'+path_folder, full_name)
            if not os.path.exists(os.path.dirname(__file__)+'/'+path_folder):
                os.makedirs(os.path.dirname(__file__)+'/'+path_folder)
            file.save(file_path)
            plt.rcParams["savefig.facecolor"] = 'black'
            plt.rcParams['axes.facecolor'] = 'black'
            dwg = ezdxf.readfile(file_path)
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


                path_img = os.path.join(os.path.dirname(__file__)+'/static', 'members', current_user_role, current_user.username, 'IMG')
                print("dsdjsdshds")
                print(path_img)
# Check if the path exists, if not, create it
                if not os.path.exists(path_img):
                    os.makedirs(path_img)

                # Define the complete file path
                file_path_img = os.path.join(path_img, f'{first_full_name}.png')
                # Save the figure
                fig.savefig(file_path_img, dpi=300, facecolor='black', edgecolor='black')
        # user_id = current_user.id
            if is_livr.lower() == 'true':
                is_livr = True
                numero_voie_livr = data ['numero_voie_livr']
                nom_voie_livr = data ['nom_voie_livr']
                cp_livr = data['cp_livr']
                ville_livr = data ['ville_livr']
                prix_livr_ht = data ['prix_livr_ht']
                new_commande = Commande(client_id=client_id, statut_id=1, name_matiere=name_matiere, type_matiere= type_matiere ,usinage_id = type_usinage,count=count,epaisseur_id = epaisseur_id, prix_ht=prix_ht, prix_livr_ht = prix_livr_ht, name_dxf = first_full_name  ,description_commercial_responsable=description, date_envoi=current_date, date_fin = date_fin, is_livr = is_livr,is_form = is_form,numero_livr= numero_voie_livr ,addresse_livr = nom_voie_livr, cp_livr = cp_livr,ville_livr = ville_livr )
            elif is_livr.lower() == 'false':
                is_livr = False
                new_commande = Commande(client_id=client_id, statut_id=1, name_matiere=name_matiere, type_matiere= type_matiere ,usinage_id = type_usinage,count=count,epaisseur_id = epaisseur_id, prix_ht=prix_ht, name_dxf= first_full_name  ,description_commercial_responsable=description, date_envoi=current_date, date_fin = date_fin, is_livr = is_livr,is_form = is_form)

        else:
            if 'text_input' in data:
                is_form = False
                text_input = data ['text_input']
                height = data ['height']
                name_police = data ['name_police']

                if is_livr.lower() == 'true':
                    is_livr = True
                    numero_voie_livr = data ['numero_voie_livr']
                    nom_voie_livr = data ['nom_voie_livr']
                    cp_livr = data['cp_livr']
                    ville_livr = data ['ville_livr']
                    prix_livr_ht = data ['prix_livr_ht']
                    new_commande = Commande(client_id=client_id, statut_id=1, name_matiere=name_matiere, type_matiere= type_matiere ,usinage_id = type_usinage,count=count,epaisseur_id = epaisseur_id,
                        description_commercial_responsable=description, date_envoi=current_date, date_fin = date_fin, is_livr = is_livr,is_form = is_form,numero_livr= numero_voie_livr ,addresse_livr = nom_voie_livr, cp_livr = cp_livr,ville_livr = ville_livr,
                        text = text_input,hauteur_text = height, name_police = name_police,prix_ht = prix_ht, prix_livr_ht=prix_livr_ht
                     )
                elif is_livr.lower() == 'false':
                    is_livr = False
                    new_commande = Commande(client_id=client_id, statut_id=1, name_matiere=name_matiere, type_matiere= type_matiere ,usinage_id = type_usinage,count=count,epaisseur_id = epaisseur_id  ,description_commercial_responsable=description, date_envoi=current_date, date_fin = date_fin, is_livr = is_livr,is_form = is_form, text = text_input,hauteur_text = height, name_police = name_police,prix_ht = prix_ht)
#
#  User.set_password(new_user, password1)
            # db.session.add(new_commande)
            # db.session.commit()
        Commande.save(new_commande)

        return "Super,La commande a été bien enregistrer!"

@app.route('/change_statut_confirmer', methods=['POST'])
def change_statut_confirmer():


# Replace the following with your ESP file parsing logic
# Example data (x, y coordinates)

    if request.method == 'POST':
        file = request.files['file']
        dt = request.form.to_dict()
        id=dt["id"]
        if id is None:
            raise ValueError("ID is required")

        # Fetch the data using the provided ID
        data = get_en_attente_by_id(id)

        if data is None:
            raise NoResultFound(f"No data found for ID: {id}")

        # Fetch the current user's role
        current_user_role = data[24]
        current_user_username = data[15]

        filename = secure_filename(file.filename)
        preferred_name = filename

        filename = secure_filename(file.filename)
        preferred_name = os.path.splitext(filename)[0]
        last_row = Commande.query.order_by(Commande.id.desc()).first()
        if last_row is None:
            support_name = 1
        else:
            support_name = last_row.id+1
        first_name = preferred_name+str(support_name)
        full_name = preferred_name+str(support_name)+'.pdf'

        path_folder = os.path.dirname(__file__)+ "/static/members/"+current_user_role+'/'+current_user_username+'/BL/'
        file_path = os.path.join(path_folder , full_name)
        if not os.path.exists(path_folder):
            os.makedirs(path_folder)
        file.save(file_path)
        current_date = datetime.now()
        change_confirmer(id, first_name,current_date )
    return "its ok"
@app.route('/change_statut_livré', methods=['POST'])
def change_statut_livré():
    try:
        if request.method == 'POST':
            dt = request.form.to_dict()

            # Check if 'id' is in the form data
            if 'id' not in dt:
                raise ValueError("ID is required in the form data")

            id = dt["id"]

            # Call the function to change the status to "livré"
            change_livré(id)

        return "it's ok"

    except ValueError as ve:
  
        print(f"ValueError: {ve}")
        return f"Error: {ve}", 400

    except Exception as e:

        print(f"An error occurred: {e}")
        return "An unexpected error occurred", 500

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

    if request.method == 'POST':
        data = request.form.to_dict()
        id=data["id"]
        create_bl(data)
        current_date = datetime.now()
        change_usiner(id ,current_date)
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
    try:
        current_user_role = (Role.query.filter(Role.id == current_user.role_id).first()).name
    except Exception as e:
        return f"Error fetching current user role: {str(e)}"
    if current_user_role != "admin" and current_user_role != "responsable":
        return render_template("error.html", message="probleme d'autorisation d'accès"), 500
    try:
        roles = Role.get_all_roles()
        if not roles:
            raise ValueError("Aucun rôle trouvé.")
        first_role = roles[0].id
        users = get_users_by_role(first_role)
        if not roles:
            raise ValueError("Aucun user trouvé.")
        return render_template('membres.html', roles=roles,select_users=users, user = current_user,current_user_role = current_user_role, page ="Membres")
    except ValueError as e:
        flash(str(e), 'error')
        return render_template('membres.html', roles=[], select_users=[], user=current_user,current_user_role = current_user_role, page="Membres")
@app.route('/clients')
@login_required
def clients():
    try:
        current_user_role = (Role.query.filter(Role.id == current_user.role_id).first()).name
    except Exception as e:
        return f"Error fetching current user role: {str(e)}"
    if current_user_role != "admin" and current_user_role != "responsable":
        return render_template("error.html", message="probleme d'autorisation d'accès"), 500
    representants = get_all_representants()

    first_rep = representants[0].id
    clients= get_cients_by_rep(first_rep)
    return render_template('clients.html', user = current_user,current_user_role = current_user_role,representants = representants, clients=clients, page ="Clients")

@app.route('/prix')
@login_required
def prix():
    try:
        current_user_role = (Role.query.filter(Role.id == current_user.role_id).first()).name
    except Exception as e:
        return f"Error fetching current user role: {str(e)}"
    if current_user_role != "admin" and current_user_role != "responsable":
        return render_template("error.html", message="probleme d'autorisation d'accès"), 500
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
  

    return render_template('prix.html', matieres = matieres,types_matieres=types_matieres , types_usinage = types_usinage,data_matieres= data_matieres, user = current_user, current_user_role = current_user_role,page = "Prix")


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

    if 'is_usil' in data:
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



    if request.method == 'POST':
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
        prix_clent_livr = data['prix_clent_livr']
        tel = data ['tel']
        new_client = Client(user_id=representant, name=name, ville=ville, cp= cp ,numero = numeroVoie,addresse=nameVoie,email = email,tel=tel, prix_livr = prix_clent_livr)
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
        prix_livr = data['prix_livr']


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
                'tel':tel,
                'prix_livr':prix_livr
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



@app.route('/get_client_data', methods=['POST'])
def get_client_data():
    data = request.form.to_dict()
    client_id = data ['client_id']
    client = Client.query.filter_by(id=client_id).first()
    result = []

    if client:
        result.append(client._data())  # Assuming _data() is a method that returns the desired data
    else:
    # Handle the case where no client is found
        result.append({'error': 'Aucun client trouvé avec lidentifiant donné'})
    # for row_data in prix_lettre_liste:
    #     result_prix_liste.append({
    #         "matiere_name": row_data[0],
    #         "type_name": row_data[1],
    #         "usinage_name": row_data[2],
    #         "epaisseur_value": row_data[3],
    #         "hauteur_value": row_data[5],
    #         "prix": row_data[4],
    #     })



    # result_envoi = {'epaisseurs': result_epaisseurs_lettre, "prix_lettre_list":result_prix_liste}
    return jsonify(result)





