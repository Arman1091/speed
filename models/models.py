from extensions import db
from sqlalchemy import create_engine, ForeignKey,select, text,Date
from sqlalchemy.orm import relationship ,sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask,redirect,url_for
from sqlalchemy.types import Boolean, String
import sqlalchemy

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    rel_role_user = relationship("User", backref = "role") 

    def get_all_roles():
        return Role.query.all()
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
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    tel = db.Column(db.String(20), nullable=False) 
    role_id = db.Column(db.Integer , ForeignKey('role.id'),nullable=False)
    rel_user_client = relationship("Client", backref = "user")
    

     #property
    def _data (self):
        return{
            'id':self.id,
            'username':self.username,
            'email':self.email,
            'password':self.password,
            'tel':self.tel,
            'role_id':self.role_id,
        }
    def save (self):
        db.session.add (self)
        db.session.commit()
    
    def save_change (self):
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
    name = db.Column(db.String(80), nullable=False)
    ville = db.Column(db.String(80), nullable=False)
    cp = db.Column(db.Integer(), nullable=False)
    numero = db.Column(db.Integer(), nullable=True)
    addresse = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(255), unique=True)
    tel = db.Column(db.String(20), nullable=False) 
    rel_client_commande = relationship("Commande", backref = "client") 

    
      #property
    
    def _data (self):
        return{
            'id':self.id,
            'user_id':self.user_id,
            'name':self.name,
            'ville':self.ville,
            'cp':self.cp,
            'numero':self.numero,
            'addresse':self.addresse,
            'email':self.email,
            'tel':self.tel
           
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
    count_persage = db.Column(db.Integer ,default=0)
    prix_matiere = db.Column(db.Float , nullable=False)
    prix_limeaire = db.Column(db.Float, nullable=False)
    name_dxf = db.Column(db.String(256), nullable=True )
    name_bl = db.Column(db.String(256), nullable=True )
    text = db.Column(db.String(256), nullable=True )
    hauteur_text = db.Column(db.Float , nullable=True)
    description_commercial_responsable = db.Column(db.String(1000), nullable=True)
    description_responsable_comercial = db.Column(db.String(1000), nullable=True)
    date_envoi = db.Column(Date, nullable=False)
    date_confirmation = db.Column(Date, nullable=True)
    date_usinage = db.Column(Date, nullable=True)
    date_fin = db.Column(Date, nullable=False)
    responsable = db.Column(db.String(100),nullable=True )
    assistante = db.Column(db.String(100),nullable=True )
    is_livr = db.Column(db.Boolean(), server_default=sqlalchemy.sql.expression.true())
    ville_livr = db.Column(db.String(80), nullable=True)
    cp_livr = db.Column(db.Integer(), nullable=True)
    numero_livr = db.Column(db.Integer(), nullable=True)
    addresse_livr = db.Column(db.String(256), nullable=True)
    is_vu_attente = db.Column(db.Boolean(),server_default=sqlalchemy.sql.expression.false())
    is_vu_confirmé = db.Column(db.Boolean(),server_default=sqlalchemy.sql.expression.false())
    is_vu_usiné = db.Column(db.Boolean(),server_default=sqlalchemy.sql.expression.false())
    is_form = db.Column(db.Boolean(), server_default=sqlalchemy.sql.expression.true())


    
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
            'name_bl':self.name_bl,
            'text':self.text,
            'hauteur_text':self.hauteur_text,
            'description_commercial_responsable':description_commercial_responsable,
            'description_responsable_comercial': description_responsable_comercial,
            'date_envoi':self.date_envoi,
            'date_confirmation':self.date_confirmation, 
            'date_usinage':self.date_usinage,
            'date_fin':self.date_fin,
            'responsable':self.responsable,
            'assistante':self.assistante,
            'is_livr':self.is_livr,
            'ville_livr':self.ville_livr,
            'cp_livr':self.cp_livr,
            'numero_livr':self.numero_livr,
            'addresse_livr':self.addresse_livr,
            'is_vu_attente':self.is_vu_attente,
            'is_vu_confirmé': self.is_vu_confirmé,
            'is_vu_usiné':self.is_vu_usiné,
            'is_form':self.is_form,
            'count_persage':self.count_persage 
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
    rel_matiere_lettre = relationship("BridgeLettres", backref = "matiere")

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
    rel_type_lettre = relationship("BridgeLettres", backref = "type")

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
    rel_essaisseur_lettre = relationship("BridgeLettres", backref = "epaisseur")

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
    rel_usinage_lettre = relationship("BridgeLettres", backref = "type_usinage")
    #property
    def _data (self):
        return{
            'id':self.id,
            'name':self.name
        }
    def save (self):
        db.session.add (self)
        db.session.commit()

class Hauteur(db.Model):
    __tablename__ = "hauteur"
    id = db.Column(db.Integer, primary_key=True , autoincrement=True)
    value = db.Column(db.Integer, nullable=False)
    rel_hauteur_lettre = relationship("BridgeLettres", backref = "hauteur")

    #property
    def _data (self):
        return{
            'id':self.id,
            'value':self.value
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
    prix_matiere = db.Column(db.Float , nullable=True)
    prix_limeaire = db.Column(db.Float, nullable=True)
    prix_pmma_first = db.Column(db.Float, nullable=True)
    prix_pmma_second = db.Column(db.Float, nullable=True)
    prix_pmma_third = db.Column(db.Float, nullable=True)
      

     #property
    def _data (self):
        return{
            'matiere_id':self.matiere_id,
            'type_id':self.type_id,
            'epaisseur_id':self.epaisseur_id,
            'uginage_id':self.uginage_id,
            'prix_matiere':self.prix_matiere,
            'prix_limeaire':self. prix_limeaire,
            'prix_pmma_first':self.prix_pmma_first,
            'prix_pmma_second':self.prix_pmma_second,
            'prix_pmma_third':selfprix_pmma_third
        }
    def save (self):
        db.session.add (self)
        db.session.commit()

class BridgeLettres(db.Model):
    __tablename__ = 'bridge_lettres'
     
    matiere_id = db.Column(db.Integer,ForeignKey('matiere.id'),primary_key=True )
    type_id = db.Column(db.Integer,ForeignKey('type.id') ,primary_key=True)
    usinage_id = db.Column(db.Integer , ForeignKey('type_usinage.id') ,primary_key=True)
    epaisseur_id = db.Column(db.Integer , ForeignKey('epaisseur.id'),primary_key=True )
    hauteur_id = db.Column(db.Integer,ForeignKey('hauteur.id'),primary_key=True)
    prix = db.Column(db.Float , nullable=False)

    

    def get_all_matieres_lettre():
        return db.session.query(Matiere).join(BridgeLettres,BridgeLettres.matiere_id== Matiere.id ).all() 
     #property
    def _data (self):
        return{
            'matiere_id':self.matiere_id,
            'type_id':self.type_id,
            'usinage_id':self.usinage_id,
            'epaisseur_id':self.epaisseur_id,
            'hauteur_id':self.hauteur_id,
            'prix':self.prix
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

def get_prix_pmma_usil(mt,mt_name, epaisseur,type_usinage):
    print(type_usinage)
    result =[]
    
    # filtered = db.session.query(Pvc_bridge.prix_limeaire,Pvc_bridge.prix_matiere  ).join(Epaisseur,Epaisseur.id==Pvc_bridge.epaisseur_id).filter_by(value = epaisseur).join(Pvc, Pvc.id == Pvc_bridge.pvc_id ).filter_by(name = mt_name).first()
    filtered = db.session.query(Bridge.prix_pmma_first,Bridge.prix_pmma_second ,Bridge.prix_pmma_third).join(Matiere, Matiere.id == Bridge.matiere_id ).filter_by(id = mt).join(Type, Type.id == Bridge.type_id ).filter_by(id = mt_name).join(Epaisseur,Epaisseur.id==Bridge.epaisseur_id).filter_by(id = epaisseur).join(Type_usinage, Type_usinage.id == Bridge.usinage_id ).filter_by(id = type_usinage).first() 
    print(filtered)
    # r= Pvc.query.all()
    # bridge_name = matiere+'_briddge'
    # print(bridge_name)
    # filtered = db.session.query(Pvc,Epaisseur, Pvc_bridge).join(Epaisseur,Epaisseur.id==Pvc_bridge.epaisseur_id).join(Pvc, Pvc.id == Pvc_bridge.pvc_id ).filter_by(name = mt_name).all()
    # # orders = Pvc.query.join(Pvc_bridge).filter(Pvc.id == Pvc_bridge.pvc_id).all()
    # # mary = Pvc.query.filter_by(id=2).all()
   
    result.append(filtered._data)
    return result

def get_clients_by_user(current_user):
        clients = db.session.query(Client).join(User, Client.user_id == User.id  ).filter(User.id == current_user.id).all() 
        # print( clients)
        # result = []
        # for row in  clients : 
        #     result.append(row._data) 

        return clients

def get_en_attentes(current_user):
    data = db.session.query(Commande.name_matiere, Commande.type_matiere,Commande.prix_matiere,Commande.prix_limeaire,Commande.date_envoi,Commande.date_fin,Client.name,Statut.name,Type_usinage.name,Epaisseur.value,Commande.count,Commande.name_dxf,Commande.id,User.username).join(Client,Commande.client_id== Client.id ).filter(Client.user_id == current_user.id).join(User,Client.user_id== User.id ).join(Statut,Commande.statut_id== Statut.id ).filter(Statut.name =="en_attente").join(Type_usinage,Commande.usinage_id== Type_usinage.id ).join(Epaisseur,Commande.epaisseur_id== Epaisseur.id ).all() 
    
    result = []
    for row in  data : 
        result.append(row._data) 
    return result
def get_all_attentes():
    data = db.session.query(Commande.name_matiere, Commande.type_matiere,Commande.prix_matiere,Commande.prix_limeaire,Commande.date_envoi,Commande.date_fin,Client.name,Statut.name,Type_usinage.name,Epaisseur.value,Commande.count,Commande.name_dxf,Commande.id,User.username).join(Client,Commande.client_id== Client.id ).join(User,Client.user_id== User.id ).join(Statut,Commande.statut_id== Statut.id ).filter(Statut.name =="en_attente").join(Type_usinage,Commande.usinage_id== Type_usinage.id ).join(Epaisseur,Commande.epaisseur_id== Epaisseur.id ).all() 
    
    result = []
    for row in  data : 
        result.append(row._data) 
    return result
    
def get_en_attente_by_id(id):
    data = db.session.query(Commande.name_matiere, Commande.type_matiere,Commande.prix_matiere,Commande.prix_limeaire,Commande.date_envoi,Commande.date_fin,Client.name,Client.ville,Client.cp,Client.addresse,Statut.name,Type_usinage.name,Epaisseur.value,Commande.count,Commande.name_dxf,Commande.id,User.username).join(Client,Commande.client_id== Client.id ).join(User,Client.user_id== User.id ).join(Statut,Commande.statut_id== Statut.id ).join(Type_usinage,Commande.usinage_id== Type_usinage.id ).join(Epaisseur,Commande.epaisseur_id== Epaisseur.id ).filter(Commande.id ==id).first() 
    
    result = []
   
    result.append(data._data) 
    return data
def change_confirmer(changed_id, name):
    current_commande = Commande.query.filter_by(id= changed_id).first()
    current_commande.statut_id=2
    current_commande.name_dxf=name
    db.session.commit()
def change_livré(changed_id):
    current_commande = Commande.query.filter_by(id= changed_id).first()
    current_commande.statut_id=4
    db.session.commit()

def get_confirmes(current_user):
    data = db.session.query(Commande.name_matiere, Commande.type_matiere,Commande.prix_matiere,Commande.prix_limeaire,Commande.date_envoi,Commande.date_fin,Client.name,Statut.name,Type_usinage.name,Epaisseur.value,Commande.count,Commande.name_dxf,Commande.id,Commande.date_confirmation,User.username).join(Client,Commande.client_id== Client.id ).join(User,Client.user_id== User.id ).join(Statut,Commande.statut_id== Statut.id ).filter(Statut.name =="confirmé").join(Type_usinage,Commande.usinage_id== Type_usinage.id ).join(Epaisseur,Commande.epaisseur_id== Epaisseur.id ).all() 
    result = []
    for row in  data : 
        result.append(row._data) 
    return result
def get_all_confirmes():
    data = db.session.query(Commande.name_matiere, Commande.type_matiere,Commande.prix_matiere,Commande.prix_limeaire,Commande.date_envoi,Commande.date_fin,Client.name,Statut.name,Type_usinage.name,Epaisseur.value,Commande.count,Commande.name_dxf,Commande.id,Commande.date_confirmation,User.username).join(Client,Commande.client_id== Client.id ).join(User,Client.user_id== User.id ).join(Statut,Commande.statut_id== Statut.id ).filter(Statut.name =="confirmé").join(Type_usinage,Commande.usinage_id== Type_usinage.id ).join(Epaisseur,Commande.epaisseur_id== Epaisseur.id ).all() 
    result = []
    for row in  data : 
        result.append(row._data) 
    return result

def get_usinés(current_user):
    data = db.session.query(Commande.name_matiere, Commande.type_matiere,Commande.prix_matiere,Commande.prix_limeaire,Commande.date_envoi,Commande.date_fin,Client.name,Statut.name,Type_usinage.name,Epaisseur.value,Commande.count,Commande.name_dxf,Commande.id,Commande.date_confirmation,User.username,User.username).join(Client,Commande.client_id== Client.id ).filter(Client.user_id == current_user.id).join(User,Client.user_id== User.id ).join(Statut,Commande.statut_id== Statut.id ).filter(Statut.name =="usiné").join(Type_usinage,Commande.usinage_id== Type_usinage.id ).join(Epaisseur,Commande.epaisseur_id== Epaisseur.id ).all() 
    result = []
    for row in  data : 
        result.append(row._data) 
    return result
def get_all_usinés():
    data = db.session.query(Commande.name_matiere, Commande.type_matiere,Commande.prix_matiere,Commande.prix_limeaire,Commande.date_envoi,Commande.date_fin,Client.name,Statut.name,Type_usinage.name,Epaisseur.value,Commande.count,Commande.name_dxf,Commande.id,Commande.date_confirmation,User.username,User.username).join(Client,Commande.client_id== Client.id ).join(User,Client.user_id== User.id ).join(Statut,Commande.statut_id== Statut.id ).filter(Statut.name =="usiné").join(Type_usinage,Commande.usinage_id== Type_usinage.id ).join(Epaisseur,Commande.epaisseur_id== Epaisseur.id ).all() 
    result = []
    for row in  data : 
        result.append(row._data) 
    return result

def get_livré(current_user):
    data = db.session.query(Commande.name_matiere, Commande.type_matiere,Commande.prix_matiere,Commande.prix_limeaire,Commande.date_envoi,Commande.date_fin,Client.name,Statut.name,Type_usinage.name,Epaisseur.value,Commande.count,Commande.name_dxf,Commande.id,Commande.date_confirmation,User.username).join(Client,Commande.client_id== Client.id ).filter(Client.user_id == current_user.id).join(User,Client.user_id== User.id ).join(Statut,Commande.statut_id== Statut.id ).filter(Statut.name =="livré").join(Type_usinage,Commande.usinage_id== Type_usinage.id ).join(Epaisseur,Commande.epaisseur_id== Epaisseur.id ).all() 
    result = []
    for row in  data : 
        result.append(row._data) 
    return result
def get_all_livré():
    data = db.session.query(Commande.name_matiere, Commande.type_matiere,Commande.prix_matiere,Commande.prix_limeaire,Commande.date_envoi,Commande.date_fin,Client.name,Statut.name,Type_usinage.name,Epaisseur.value,Commande.count,Commande.name_dxf,Commande.id,Commande.date_confirmation,User.username).join(Client,Commande.client_id== Client.id ).join(User,Client.user_id== User.id ).join(Statut,Commande.statut_id== Statut.id ).filter(Statut.name =="livré").join(Type_usinage,Commande.usinage_id== Type_usinage.id ).join(Epaisseur,Commande.epaisseur_id== Epaisseur.id ).all() 
    result = []
    for row in  data : 
        result.append(row._data) 
    return result

def get_confirmé_by_id(id):
    data = db.session.query(Commande.name_matiere, Commande.type_matiere,Commande.prix_matiere,Commande.prix_limeaire,Commande.date_envoi,Commande.date_fin,Client.name,Client.ville,Client.cp,Client.addresse,Statut.name,Type_usinage.name,Epaisseur.value,Commande.count,Commande.name_dxf,Commande.id,User.username).join(Client,Commande.client_id== Client.id ).join(User,Client.user_id== User.id ).join(Statut,Commande.statut_id== Statut.id ).join(Type_usinage,Commande.usinage_id== Type_usinage.id ).join(Epaisseur,Commande.epaisseur_id== Epaisseur.id ).filter(Commande.id ==id).first() 
    
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

def get_types_usinage_prix(mat_id, type_id ):
    return db.session.query(Type_usinage).join(Bridge,Bridge.usinage_id== Type_usinage.id ).filter(Bridge.matiere_id == mat_id, Bridge.type_id == type_id).all()
def get_types_usinage(mat_id, type_id, epp_id):
    return db.session.query(Type_usinage).join(Bridge,Bridge.usinage_id== Type_usinage.id ).filter(Bridge.matiere_id == mat_id, Bridge.type_id == type_id,Bridge.epaisseur_id== epp_id).all()

def get_client_detailles_by_id(client_id):
    return  Client.query.filter(Client.id == client_id).first()

def get_types_lettre_by_matiere(mat_id):
    return db.session.query(Type).join(BridgeLettres,BridgeLettres.type_id== Type.id ).filter(BridgeLettres.matiere_id == mat_id).all() 

def get_epaisseurs_lettre(matiere_id,type_id):
    return db.session.query(Epaisseur).join(BridgeLettres,BridgeLettres.epaisseur_id== Epaisseur.id ).filter(BridgeLettres.matiere_id == matiere_id, BridgeLettres.type_id == type_id).all() 

def get_usinage_types_lettre(mat_id, type_id, epp_id):
    return db.session.query(Type_usinage).join(BridgeLettres,BridgeLettres.usinage_id== Type_usinage.id ).filter(BridgeLettres.matiere_id == mat_id, BridgeLettres.type_id == type_id,BridgeLettres.epaisseur_id== epp_id).all()

def get_hauteurs_lettre(mat_id, type_id, epp_id, usinage_id):
    return db.session.query(Hauteur).join(BridgeLettres,BridgeLettres.hauteur_id== Hauteur.id ).filter(BridgeLettres.matiere_id == mat_id, BridgeLettres.type_id == type_id,BridgeLettres.epaisseur_id== epp_id,BridgeLettres.usinage_id== usinage_id).all()

def get_users_by_role(roleId):
    return db.session.query(User).join(Role, Role.id==User.role_id ).filter(User.role_id == roleId).all()
def get_data_matieres (mt_id,type_id, usinage_id):
    return db.session.query(Matiere.name,Type.name, Type_usinage.name,Epaisseur.value, Bridge.prix_matiere, Bridge.prix_limeaire).join(Matiere, Bridge.matiere_id == Matiere.id).join(Type, Bridge.type_id==Type.id).join(Type_usinage, Bridge.usinage_id==Type_usinage.id).join(Epaisseur, Bridge.epaisseur_id==Epaisseur.id).filter(Bridge.matiere_id==mt_id,Bridge.type_id == type_id,Bridge.usinage_id == usinage_id ).all()

def get_all_representants():
    return User.query.filter_by(role_id=2).all()

def get_cients_by_rep(first_rep_id):
    clients=db.session.query(Client.name,Client.ville,Client.cp,Client.numero,Client.addresse,User.username,Client.email,Client.tel,User.id,Client.id).join(User,Client.user_id== User.id ).filter(Client.user_id == first_rep_id ).all()
    result = []
    for row in  clients : 
        result.append(row._data) 

    return result

def edit_client_data(Edit_data):
    print("test")
    print(Edit_data[0]['user_id'])
    print(Edit_data[0]['id'])
    client_id = Edit_data[0]['id']
    current_client = Client.query.filter(Client.id == client_id).first()

    
    current_client.user_id=Edit_data[0]['user_id']
    current_client.cp=Edit_data[0]['cp']
    current_client.numero=Edit_data[0]['numero']
    current_client.addresse=Edit_data[0]['addresse']
    current_client.email=Edit_data[0]['email']
    current_client.tel=Edit_data[0]['tel']

    db.session.commit()

    def edit_user_data(Edit_data):
        print("test")
    # print(Edit_data[0]['user_id'])
    # print(Edit_data[0]['id'])
    # client_id = Edit_data[0]['id']
    # current_client = Client.query.filter(Client.id == client_id).first()

    
    # current_client.user_id=Edit_data[0]['user_id']
    # current_client.cp=Edit_data[0]['cp']
    # current_client.numero=Edit_data[0]['numero']
    # current_client.addresse=Edit_data[0]['addresse']
    # current_client.email=Edit_data[0]['email']
    # current_client.tel=Edit_data[0]['tel']

    # db.session.commit()

def get_prix_lettre(matiere_id,type_id,type_usinage_id ,epaisseur_id,hauteur_id):
    prix = db.session.query(BridgeLettres.prix ).filter(BridgeLettres.matiere_id == matiere_id,BridgeLettres.type_id == type_id,BridgeLettres.epaisseur_id == epaisseur_id,BridgeLettres.usinage_id == type_usinage_id,BridgeLettres.hauteur_id == hauteur_id).first() 
    return prix

def get_liste_prix_lettre(matiere_id,type_id,epaisseur_id):

    prix = db.session.query(Matiere.name,Type.name,Type_usinage.name,Epaisseur.value,BridgeLettres.prix,Hauteur.value).join(Matiere,  BridgeLettres.matiere_id== Matiere.id ).filter(Matiere.id == matiere_id).join(Type,BridgeLettres.type_id == Type.id  ).filter(BridgeLettres.type_id == type_id).join(Epaisseur,BridgeLettres.epaisseur_id == Epaisseur.id).filter(Epaisseur.id == epaisseur_id).join(Type_usinage, BridgeLettres.usinage_id ==Type_usinage.id  ).join(Hauteur, BridgeLettres.hauteur_id ==Hauteur.id ).all() 
    return prix

def change_matiere_prix(matiere,type_matiere,type_usinage,epaisseur,prix_matiere):
    print(matiere)
    print(type_matiere)
    print(type_usinage)
    print(epaisseur)
    filtered_row = db.session.query(Bridge).join(Matiere,  Bridge.matiere_id== Matiere.id ).filter(Matiere.name == matiere.strip()).join(Type,Bridge.type_id == Type.id  ).filter(Type.name == type_matiere.strip()).join(Epaisseur,Bridge.epaisseur_id == Epaisseur.id).filter(Epaisseur.value == epaisseur).join(Type_usinage, Bridge.usinage_id ==Type_usinage.id  ).filter(Type_usinage.name == type_usinage.strip()).first() 
    filtered_row.prix_matiere=prix_matiere
    db.session.commit()
    # return filtered_row


def change_limeaire_prix(matiere,type_matiere,type_usinage,epaisseur,new_prix_limeaire):
    filtered_row = db.session.query(Bridge).join(Matiere,  Bridge.matiere_id== Matiere.id ).filter(Matiere.name == matiere.strip()).join(Type,Bridge.type_id == Type.id  ).filter(Type.name == type_matiere.strip()).join(Epaisseur,Bridge.epaisseur_id == Epaisseur.id).filter(Epaisseur.value == epaisseur).join(Type_usinage, Bridge.usinage_id ==Type_usinage.id  ).filter(Type_usinage.name == type_usinage.strip()).first() 
    filtered_row.prix_limeaire=new_prix_limeaire
    db.session.commit()

def get_pmma_usil_list(mt_id,type_id,type_usinage_id):
    return db.session.query(Matiere.name,Type.name, Type_usinage.name,Epaisseur.value, Bridge.prix_pmma_first, Bridge.prix_pmma_second , Bridge.prix_pmma_third).join(Matiere, Bridge.matiere_id == Matiere.id).join(Type, Bridge.type_id==Type.id).join(Type_usinage, Bridge.usinage_id==Type_usinage.id).join(Epaisseur, Bridge.epaisseur_id==Epaisseur.id).filter(Bridge.matiere_id==mt_id,Bridge.type_id == type_id,Bridge.usinage_id == type_usinage_id).all()

def delete_commande_client(id):
    try:
        db.session.begin()
        Commande.query.filter_by(client_id=id).delete()
        Client.query.filter_by(id=id).delete()
        db.session.commit()
        print("sddxxxxxxxxxxxxxxxxxxxxxx")
        
    except Exception as e:
        print(e)
    finally:
        # Close the session
        db.session.close()

def delete_bridge_form_row(matiere,type_mt ,usinage ,epaisseur):
    try:
        db.session.begin()
        delete_row = db.session.query(Bridge).join(Matiere,  Bridge.matiere_id== Matiere.id ).filter(Matiere.name == matiere.strip()).join(Type,Bridge.type_id == Type.id  ).filter(Type.name == type_mt.strip()).join(Epaisseur,Bridge.epaisseur_id == Epaisseur.id).filter(Epaisseur.value == epaisseur).join(Type_usinage, Bridge.usinage_id ==Type_usinage.id  ).filter(Type_usinage.name == usinage).first()
        db.session.delete(delete_row)
        db.session.commit()
        print("sddxxxxxxxxxxxxxxxxxxxxxx")
        
    except Exception as e:
        print(e)
    finally:
        # Close the session
        db.session.close()

def delete_bridge_lettre_row(matiere,type_mt ,usinage ,epaisseur):
    try:
        db.session.begin()
        delete_row = db.session.query(BridgeLettres).join(Matiere,  BridgeLettres.matiere_id== Matiere.id ).filter(Matiere.name == matiere.strip()).join(Type,BridgeLettres.type_id == Type.id  ).filter(Type.name == type_mt.strip()).join(Epaisseur,BridgeLettres.epaisseur_id == Epaisseur.id).filter(Epaisseur.value == epaisseur).join(Type_usinage, BridgeLettres.usinage_id ==Type_usinage.id  ).filter(Type_usinage.name == usinage).first()
        db.session.delete(delete_row)
        db.session.commit()
        print("sddxxxxxxxxxxxxxxxxxxxxxx")
        
    except Exception as e:
        print(e)
    finally:
        # Close the session
        db.session.close()
def  change_lettre_prix(matiere,type_matiere,type_usinage,epaisseur,new_prix,hauteur ):
    print(matiere)
    print(type_matiere)
    print(type_usinage)
    print(epaisseur)
    print(hauteur)
    filtered_row = db.session.query(BridgeLettres).join(Matiere,  BridgeLettres.matiere_id== Matiere.id ).filter(Matiere.name == matiere.strip()).join(Type,BridgeLettres.type_id == Type.id  ).filter(Type.name == type_matiere.strip()).join(Epaisseur,BridgeLettres.epaisseur_id == Epaisseur.id).filter(Epaisseur.value == epaisseur).join(Type_usinage, BridgeLettres.usinage_id ==Type_usinage.id  ).filter(Type_usinage.name == type_usinage.strip()).join(Hauteur, BridgeLettres.hauteur_id ==Hauteur.id  ).filter(Hauteur.value == hauteur).first() 
    filtered_row.prix=new_prix
    db.session.commit()