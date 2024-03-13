from extensions import db
from sqlalchemy import create_engine, ForeignKey,select, text,Date
from sqlalchemy.orm import relationship ,sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask,redirect,url_for

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    rel_role_user = relationship("User", backref = "role") 
      #property
    def _data (self):
        return{
            'id':self.id,
            'name':self.name
        }
    def save (self):
        db.session.add (self)
        db.session.commit()
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username=db.Column(db.String(255), nullable=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    role_id = db.Column(db.Integer , ForeignKey('role.id'),nullable=False)
    rel_user_client = relationship("Client", backref = "user")
    

     #property
    def _data (self):
        return{
            'id':self.id,
            'username':self.username,
            'email':self.email,
            'password':self.password,
            'role_id':self.role_id,
        }
    def save (self):
        db.session.add (self)
        db.session.commit()
    
    def filter_by_email(mail):
        return User.query.filter_by(email=mail).first()

    
    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.password, password_plaintext)

    def set_password(self, password_plaintext: str):
        self.password = generate_password_hash(password_plaintext)
    
class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer(),autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer , ForeignKey('user.id'),nullable=False)
    reference = db.Column(db.Integer ,nullable=False)
    rel_users_client_data = relationship("Client_data", backref = "client") 
    rel_client_commande = relationship("Commande", backref = "client") 
      #property
    def _data (self):
        return{
            'id':self.id,
            'user_id':self.user_id,
            'reference':self.reference,
        }
    def save (self):
        db.session.add (self)
        db.session.commit()

class Client_data(db.Model):
    __tablename__ = 'client_data'
    client_id = db.Column(db.Integer , ForeignKey('client.id'),primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    ville = db.Column(db.String(80), nullable=False)
    cp = db.Column(db.Integer(), nullable=False)
    addresse = db.Column(db.String(256), nullable=False)
    
      #property
    
    def _data (self):
        return{
            'client_id':self.id,
            'name':self.name,
            'ville':self.ville,
            'cp':self.cp,
            'addresse':self.adressse
        }
    def save (self):
        db.session.add (self)
        db.session.commit()

class Statut(db.Model):
    __tablename__ = "statut"
    id = db.Column(db.Integer, primary_key=True , autoincrement=True)
    name = db.Column(db.String(50), nullable=False )
    rel_statut_commande = relationship("Commande", backref = "statut")

    #property
    def _data (self):
        return{
            'id':self.id,
            'name':self.name
        }
    def save (self):
        db.session.add (self)
        db.session.commit()

# class Sectors(db.Model):
#     __tablename__ = "sectors"
#     id = db.Column(db.Integer, primary_key=True , autoincrement=True)
#     name = db.Column(db.String(50), nullable=False )
#     rel_matiere_bridge = relationship("Commande", backref = "sectors")

#     #property
#     def _data (self):
#         return{
#             'id':self.id,
#             'name':self.name
#         }
#     def save (self):
#         db.session.add (self)
#         db.session.commit()
class Commande(db.Model):
    __tablename__ = 'commande'
    id = db.Column(db.Integer, autoincrement=True,primary_key=True )
    client_id = db.Column(db.Integer , ForeignKey('client.id'),nullable=False)
    statut_id = db.Column(db.Integer, ForeignKey('statut.id'),nullable=False )
    usinage_id = db.Column(db.Integer, ForeignKey('type_usinage.id'), nullable=False )
    name_matiere = db.Column(db.String(50), nullable=False )
    type_matiere = db.Column(db.String(50), nullable=False )
    epaisseur_id = db.Column(db.Integer, ForeignKey('epaisseur.id'),nullable=False )
    count = db.Column(db.Integer ,default=1,nullable=False)
    prix_matiere = db.Column(db.Float , nullable=False)
    prix_limeaire = db.Column(db.Float, nullable=False)
    name_dxf = db.Column(db.String(256), nullable=False )
    description_commercial_responsable = db.Column(db.String(1000), nullable=True)
    description_responsable_comercial = db.Column(db.String(1000), nullable=True)
    description_responsable_usinage = db.Column(db.String(1000), nullable=True)
    date_envoi = db.Column(Date, nullable=False)
    date_confirmation = db.Column(Date, nullable=True)
    date_usinage = db.Column(Date, nullable=True)
    date_fin = db.Column(Date, nullable=False)
    responsable_user = db.Column(db.String(100),nullable=True )
    usinage_user = db.Column(db.String(100),nullable=True )
    assistante_user = db.Column(db.String(100),nullable=True )

    
      #property
    
    def _data (self):
        return{
            'id':self.id,
            'client_id':self.client_id,
            'statut_id':self.statut_id,
            'usinage_id':self.usinage_id,
            'name_matiere':self.name_matiere,
            'type_matiere':self.type_matiere,
            'epaisseur_id':epaisseur_id,
            'count':self.count,
            'prix_matiere':self.prix_matiere,
            'prix_limeaire':self.prix_limeaire,
            'name_dxf':self.name_dxf,
            'description_commercial_responsable':description_commercial_responsable,
            'description_responsable_comercial': description_responsable_comercial,
            'description_responsable_usinage':description_responsable_usinage,
            'date_envoi':self.date_envoi,
            'date_confirmation':self.date_confirmation, 
            'date_usinage':self.date_usinage,
            'date_fin':self.date_fin,
            'responsable_user':responsable_user,
            'usinage_user':usinage_user,
            'assistante_user':assistante_user
        }
    
    def save (self):
        db.session.add (self)
        db.session.commit()
# class Reference(db.Model):
#     __tablename__ = 'reference'
#     id = db.Column(db.Integer(),autoincrement=True,primary_key=True)
#     value = db.Column(db.String(80), nullable=False)
#       #property
#     def _data (self):
#         return{
#             'id':self.id,
#             'value':self.value
#         }
#     def save (self):
#         db.session.add (self)
#         db.session.commit()
     
# creates all database tables
# @main.before_first_request
# def create_tables():
#     db.create_all()
class Matiere(db.Model):
    __tablename__ = "matiere"
    id = db.Column(db.Integer, primary_key=True , autoincrement=True)
    name = db.Column(db.String(50), nullable=False )
    rel_matiere_bridge = relationship("Bridge", backref = "matiere")
   

    #property
    def get_all_matiere():
        return Matiere.query.all()
    def _data (self):
        return{
            'id':self.id,
            'name':self.name
        }
    def save (self):
        db.session.add (self)
        db.session.commit()

class Type(db.Model):
    __tablename__ = "type"
    id = db.Column(db.Integer, primary_key=True , autoincrement=True)
    name = db.Column(db.String(50), nullable=False )
    rel_type_bridge = relationship("Bridge", backref = "type")

    #property
    
    def _data (self):
        return{
            'id':self.id,
            'name':self.name
        }
    def save (self):
        db.session.add (self)
        db.session.commit()
    
    #classmethod
    # def get_data(mt_name):
    #     result =[]
       
    #     # r= Pvc.query.all()
    #     filtered = db.session.query(Pvc,Epaisseur, Pvc_bridge).join(Epaisseur,Epaisseur.id==Pvc_bridge.epaisseur_id).join(Pvc, Pvc.id == Pvc_bridge.pvc_id ).filter_by(name = mt_name).all()
    #     # orders = Pvc.query.join(Pvc_bridge).filter(Pvc.id == Pvc_bridge.pvc_id).all()
    #     # mary = Pvc.query.filter_by(id=2).all()
    #     for row in  filtered : 
    #         result.append(row._data)
        
    #     return result
class Epaisseur(db.Model):
    __tablename__ = "epaisseur"
    id = db.Column(db.Integer, primary_key=True , autoincrement=True)
    value = db.Column(db.Integer, nullable=False, unique=True)
    rel_essaisseur_bridge = relationship("Bridge", backref = "epaisseur")
    rel_essaisseur_commande = relationship("Commande", backref = "epaisseur")

    #property
    def _data (self):
        return{
            'id':self.id,
            'value':self.value
        }
    def save (self):
        db.session.add (self)
        db.session.commit()

class Type_usinage(db.Model):
    __tablename__ = "type_usinage"
    id = db.Column(db.Integer, primary_key=True , autoincrement=True)
    name = db.Column(db.String(50), nullable=False )
    rel_usinage_bridge = relationship("Bridge", backref = "type_usinage")
    rel_usinage_commande = relationship("Commande", backref = "type_usinage")
    #property
    def _data (self):
        return{
            'id':self.id,
            'name':self.name
        }
    def save (self):
        db.session.add (self)
        db.session.commit()


class Bridge(db.Model):
    __tablename__ = 'bridge'

    matiere_id = db.Column(db.Integer,ForeignKey('matiere.id') ,primary_key=True)
    type_id = db.Column(db.Integer,ForeignKey('type.id') ,primary_key=True)
    epaisseur_id = db.Column(db.Integer , ForeignKey('epaisseur.id') ,primary_key=True)
    usinage_id = db.Column(db.Integer , ForeignKey('type_usinage.id') ,primary_key=True)
    prix_matiere = db.Column(db.Float , nullable=False)
    prix_limeaire = db.Column(db.Float, nullable=False)

     #property
    def _data (self):
        return{
            'matiere_id':self.matiere_id,
            'type_id':self.type_id,
            'epaisseur_id':self.epaisseur_id,
            'uginage_id':self.uginage_id,
            'prix_matiere':self.prix_matiere,
            'prix_limeaire':self. prix_limeaire
        }
    def save (self):
        db.session.add (self)
        db.session.commit()



def get_epaisseurs(matiere_id,type_id):

    return db.session.query(Epaisseur).join(Bridge,Bridge.epaisseur_id== Epaisseur.id ).filter(Bridge.matiere_id == matiere_id, Bridge.type_id == type_id).all() 
    
    # if matiere == "Pvc":
    #     filtered = db.session.query(Matiere,Type,Epaisseur, Bridge,Type_usinage).join(Matiere, Matiere.id == Bridge.matiere_id ).filter_by(name = mt_name).join(Type, Type.id == Bridge.type_id ).filter_by(name = name).join(Epaisseur,Epaisseur.id==Bridge.epaisseur_id).join(Type_usinage, Type_usinage.id == Bridge.usinage_id ).all() 
    # elif matiere == "Newbond":
    #           filtered = db.session.query(Matiere,Type,Epaisseur, Bridge,Type_usinage).join(Matiere, Matiere.id == Bridge.matiere_id ).filter_by(name = mt_name).join(Type, Type.id == Bridge.type_id ).filter_by(name = name).join(Epaisseur,Epaisseur.id==Bridge.epaisseur_id).join(Type_usinage, Type_usinage.id == Bridge.usinage_id ).all() 
    # elif matiere == "Pmma":
    #            filtered = db.session.query(Matiere,Type,Epaisseur, Bridge,Type_usinage).join(Matiere, Matiere.id == Bridge.matiere_id ).filter_by(name = mt_name).join(Type, Type.id == Bridge.type_id ).filter_by(name = name).join(Epaisseur,Epaisseur.id==Bridge.epaisseur_id).join(Type_usinage, Type_usinage.id == Bridge.usinage_id ).all() 
    # elif matiere == "Polycarbonat":
    #            filtered = db.session.query(Matiere,Type,Epaisseur, Bridge,Type_usinage).join(Matiere, Matiere.id == Bridge.matiere_id ).filter_by(name = mt_name).join(Type, Type.id == Bridge.type_id ).filter_by(name = name).join(Epaisseur,Epaisseur.id==Bridge.epaisseur_id).join(Type_usinage, Type_usinage.id == Bridge.usinage_id ).all() 
    # for row in  filtered : 
    #         result.append(row._data) 

    return result



def get_prix(mt,mt_name, epaisseur,type_usinage):
    print(type_usinage)
    result =[]
    
    # filtered = db.session.query(Pvc_bridge.prix_limeaire,Pvc_bridge.prix_matiere  ).join(Epaisseur,Epaisseur.id==Pvc_bridge.epaisseur_id).filter_by(value = epaisseur).join(Pvc, Pvc.id == Pvc_bridge.pvc_id ).filter_by(name = mt_name).first()
    filtered = db.session.query(Bridge.prix_limeaire,Bridge.prix_matiere ).join(Matiere, Matiere.id == Bridge.matiere_id ).filter_by(id = mt).join(Type, Type.id == Bridge.type_id ).filter_by(id = mt_name).join(Epaisseur,Epaisseur.id==Bridge.epaisseur_id).filter_by(id = epaisseur).join(Type_usinage, Type_usinage.id == Bridge.usinage_id ).filter_by(id = type_usinage).first() 
    print(filtered)
    # r= Pvc.query.all()
    # bridge_name = matiere+'_briddge'
    # print(bridge_name)
    # filtered = db.session.query(Pvc,Epaisseur, Pvc_bridge).join(Epaisseur,Epaisseur.id==Pvc_bridge.epaisseur_id).join(Pvc, Pvc.id == Pvc_bridge.pvc_id ).filter_by(name = mt_name).all()
    # # orders = Pvc.query.join(Pvc_bridge).filter(Pvc.id == Pvc_bridge.pvc_id).all()
    # # mary = Pvc.query.filter_by(id=2).all()
   
    result.append(filtered._data)
    return result
def get_clients(current_user):
        clients = db.session.query(User,Client,Client_data).join(User, User.id == Client.user_id ).filter_by(id = current_user.id).join(Client_data, Client.id == Client_data.client_id ).all() 
        result = []
        for row in  clients : 
            result.append(row._data) 

        return result

def get_en_attentes(current_user):
    data = db.session.query(Commande.name_matiere, Commande.type_matiere,Commande.prix_matiere,Commande.prix_limeaire,Commande.date_envoi,Commande.date_fin,Client_data.name,Statut.name,Type_usinage.name,Epaisseur.value,Commande.count,Commande.name_dxf,Commande.id,User.username).join(Client,Commande.client_id== Client.id ).filter(Client.user_id == current_user.id).join(Client_data,Commande.client_id== Client_data.client_id ).join(User,Client.user_id== User.id ).join(Statut,Commande.statut_id== Statut.id ).filter(Statut.name =="en_attente").join(Type_usinage,Commande.usinage_id== Type_usinage.id ).join(Epaisseur,Commande.epaisseur_id== Epaisseur.id ).all() 
    
    result = []
    for row in  data : 
        result.append(row._data) 
    return result
def get_all_attentes():
    data = db.session.query(Commande.name_matiere, Commande.type_matiere,Commande.prix_matiere,Commande.prix_limeaire,Commande.date_envoi,Commande.date_fin,Client_data.name,Statut.name,Type_usinage.name,Epaisseur.value,Commande.count,Commande.name_dxf,Commande.id,User.username).join(Client,Commande.client_id== Client.id ).join(Client_data,Commande.client_id== Client_data.client_id ).join(User,Client.user_id== User.id ).join(Statut,Commande.statut_id== Statut.id ).filter(Statut.name =="en_attente").join(Type_usinage,Commande.usinage_id== Type_usinage.id ).join(Epaisseur,Commande.epaisseur_id== Epaisseur.id ).all() 
    
    result = []
    for row in  data : 
        result.append(row._data) 
    return result
    
def get_en_attente_by_id(id):
    data = db.session.query(Commande.name_matiere, Commande.type_matiere,Commande.prix_matiere,Commande.prix_limeaire,Commande.date_envoi,Commande.date_fin,Client_data.name,Client_data.ville,Client_data.cp,Client_data.addresse,Statut.name,Type_usinage.name,Epaisseur.value,Commande.count,Commande.name_dxf,Commande.id,User.username).join(Client,Commande.client_id== Client.id ).join(Client_data,Commande.client_id== Client_data.client_id ).join(User,Client.user_id== User.id ).join(Statut,Commande.statut_id== Statut.id ).join(Type_usinage,Commande.usinage_id== Type_usinage.id ).join(Epaisseur,Commande.epaisseur_id== Epaisseur.id ).filter(Commande.id ==id).first() 
    
    result = []
   
    result.append(data._data) 
    return data
def change_confirmer(changed_id):
    current_commande = Commande.query.filter_by(id= changed_id).first()
    current_commande.statut_id=2
    db.session.commit()
def change_livré(changed_id):
    current_commande = Commande.query.filter_by(id= changed_id).first()
    current_commande.statut_id=4
    db.session.commit()

def get_confirmes(current_user):
    data = db.session.query(Commande.name_matiere, Commande.type_matiere,Commande.prix_matiere,Commande.prix_limeaire,Commande.date_envoi,Commande.date_fin,Client_data.name,Statut.name,Type_usinage.name,Epaisseur.value,Commande.count,Commande.name_dxf,Commande.id,Commande.date_confirmation,User.username).join(Client,Commande.client_id== Client.id ).filter(Client.user_id == current_user.id).join(Client_data,Commande.client_id== Client_data.client_id ).join(User,Client.user_id== User.id ).join(Statut,Commande.statut_id== Statut.id ).filter(Statut.name =="confirmé").join(Type_usinage,Commande.usinage_id== Type_usinage.id ).join(Epaisseur,Commande.epaisseur_id== Epaisseur.id ).all() 
    result = []
    for row in  data : 
        result.append(row._data) 
    return result
def get_all_confirmes():
    data = db.session.query(Commande.name_matiere, Commande.type_matiere,Commande.prix_matiere,Commande.prix_limeaire,Commande.date_envoi,Commande.date_fin,Client_data.name,Statut.name,Type_usinage.name,Epaisseur.value,Commande.count,Commande.name_dxf,Commande.id,Commande.date_confirmation,User.username).join(Client,Commande.client_id== Client.id ).join(Client_data,Commande.client_id== Client_data.client_id ).join(User,Client.user_id== User.id ).join(Statut,Commande.statut_id== Statut.id ).filter(Statut.name =="confirmé").join(Type_usinage,Commande.usinage_id== Type_usinage.id ).join(Epaisseur,Commande.epaisseur_id== Epaisseur.id ).all() 
    result = []
    for row in  data : 
        result.append(row._data) 
    return result

def get_usinés(current_user):
    data = db.session.query(Commande.name_matiere, Commande.type_matiere,Commande.prix_matiere,Commande.prix_limeaire,Commande.date_envoi,Commande.date_fin,Client_data.name,Statut.name,Type_usinage.name,Epaisseur.value,Commande.count,Commande.name_dxf,Commande.id,Commande.date_confirmation,User.username,User.username).join(Client,Commande.client_id== Client.id ).filter(Client.user_id == current_user.id).join(Client_data,Commande.client_id== Client_data.client_id ).join(User,Client.user_id== User.id ).join(Statut,Commande.statut_id== Statut.id ).filter(Statut.name =="usiné").join(Type_usinage,Commande.usinage_id== Type_usinage.id ).join(Epaisseur,Commande.epaisseur_id== Epaisseur.id ).all() 
    result = []
    for row in  data : 
        result.append(row._data) 
    return result
def get_all_usinés():
    data = db.session.query(Commande.name_matiere, Commande.type_matiere,Commande.prix_matiere,Commande.prix_limeaire,Commande.date_envoi,Commande.date_fin,Client_data.name,Statut.name,Type_usinage.name,Epaisseur.value,Commande.count,Commande.name_dxf,Commande.id,Commande.date_confirmation,User.username,User.username).join(Client,Commande.client_id== Client.id ).join(Client_data,Commande.client_id== Client_data.client_id ).join(User,Client.user_id== User.id ).join(Statut,Commande.statut_id== Statut.id ).filter(Statut.name =="usiné").join(Type_usinage,Commande.usinage_id== Type_usinage.id ).join(Epaisseur,Commande.epaisseur_id== Epaisseur.id ).all() 
    result = []
    for row in  data : 
        result.append(row._data) 
    return result

def get_livré(current_user):
    data = db.session.query(Commande.name_matiere, Commande.type_matiere,Commande.prix_matiere,Commande.prix_limeaire,Commande.date_envoi,Commande.date_fin,Client_data.name,Statut.name,Type_usinage.name,Epaisseur.value,Commande.count,Commande.name_dxf,Commande.id,Commande.date_confirmation,User.username).join(Client,Commande.client_id== Client.id ).filter(Client.user_id == current_user.id).join(Client_data,Commande.client_id== Client_data.client_id ).join(User,Client.user_id== User.id ).join(Statut,Commande.statut_id== Statut.id ).filter(Statut.name =="livré").join(Type_usinage,Commande.usinage_id== Type_usinage.id ).join(Epaisseur,Commande.epaisseur_id== Epaisseur.id ).all() 
    result = []
    for row in  data : 
        result.append(row._data) 
    return result
def get_all_livré():
    data = db.session.query(Commande.name_matiere, Commande.type_matiere,Commande.prix_matiere,Commande.prix_limeaire,Commande.date_envoi,Commande.date_fin,Client_data.name,Statut.name,Type_usinage.name,Epaisseur.value,Commande.count,Commande.name_dxf,Commande.id,Commande.date_confirmation,User.username).join(Client,Commande.client_id== Client.id ).join(Client_data,Commande.client_id== Client_data.client_id ).join(User,Client.user_id== User.id ).join(Statut,Commande.statut_id== Statut.id ).filter(Statut.name =="livré").join(Type_usinage,Commande.usinage_id== Type_usinage.id ).join(Epaisseur,Commande.epaisseur_id== Epaisseur.id ).all() 
    result = []
    for row in  data : 
        result.append(row._data) 
    return result

def get_confirmé_by_id(id):
    data = db.session.query(Commande.name_matiere, Commande.type_matiere,Commande.prix_matiere,Commande.prix_limeaire,Commande.date_envoi,Commande.date_fin,Client_data.name,Client_data.ville,Client_data.cp,Client_data.addresse,Statut.name,Type_usinage.name,Epaisseur.value,Commande.count,Commande.name_dxf,Commande.id,User.username).join(Client,Commande.client_id== Client.id ).join(Client_data,Commande.client_id== Client_data.client_id ).join(User,Client.user_id== User.id ).join(Statut,Commande.statut_id== Statut.id ).join(Type_usinage,Commande.usinage_id== Type_usinage.id ).join(Epaisseur,Commande.epaisseur_id== Epaisseur.id ).filter(Commande.id ==id).first() 
    
    result = []
   
    result.append(data._data) 
    return data

def change_usiner(changed_id):
    current_commande = Commande.query.filter_by(id= changed_id).first()
    current_commande.statut_id=3
    db.session.commit()
def  supprimer_commande_attente(id):
    row_to_delete = Commande.query.get(id)
    if row_to_delete:
        # Delete the row
        db.session.delete(row_to_delete)
        db.session.commit()
         # Redirect to another route or page after deletion
    else:
        return "Row not found", 404
        

def  supprimer_commande_confirmé(id):
    row_to_delete = Commande.query.get(id)
    if row_to_delete:
        # Delete the row
        db.session.delete(row_to_delete)
        db.session.commit()
         # Redirect to another route or page after deletion
    else:
        return "Row not found", 404

def  supprimer_commande_usiné(id):
    row_to_delete = Commande.query.get(id)
    if row_to_delete:
        # Delete the row
        db.session.delete(row_to_delete)
        db.session.commit()
         # Redirect to another route or page after deletion
    else:
        return "Row not found", 404

         
def get_types_by_matiere(mat_id):
    return db.session.query(Type).join(Bridge,Bridge.type_id== Type.id ).filter(Bridge.matiere_id == mat_id).all() 

def get_types_usinage(mat_id, type_id, epp_id):
    return db.session.query(Type_usinage).join(Bridge,Bridge.usinage_id== Type_usinage.id ).filter(Bridge.matiere_id == mat_id, Bridge.type_id == type_id,Bridge.epaisseur_id== epp_id).all()

def get_client_detailles_by_id(client_id):
    return db.session.query(Client,Client_data).join(Client_data,Client_data.client_id == Client.id).filter(Client.id == client_id).first() 