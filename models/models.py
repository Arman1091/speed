from extensions import db
from sqlalchemy import create_engine, ForeignKey,select, text,Date, desc,or_
from sqlalchemy.orm import relationship ,sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask,redirect,url_for
from sqlalchemy.types import Boolean, String
import sqlalchemy
import os

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

    def get_user_by_id(id):
        return User.query.filter_by(id=id).first()
    
    def delete_user(self):
        try:
            db.session.delete(self)
            db.session.commit()
            print("sddxxxxxxxxxxxxxxxxxxxxxx")
            
        except Exception as e:
            print(e)

    
    def filter_by_email(mail):
        return User.query.filter_by(email=mail).first()
    
    def is_password_correct(self, password_plaintext:str):
        if self.password is None:
            return False
        
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
    prix_livr = db.Column(db.Float , nullable=False)
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
            'tel':self.tel,
            'prix_livr':self.prix_livr
           
        }
    def save (self):
        db.session.add (self)
        db.session.commit()
    def get_clients_by_user_id(id):
        return Client.query.filter_by(user_id=id).all()

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


class Plaque(db.Model):
    __tablename__ = 'plaque'
    id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    value = db.Column(db.String(32), nullable=False)
    surface= db.Column(db.Float, nullable=False)
    rel_plaque_bridge = relationship("BridgePlaques", backref = "plaque") 
    rel_commande_plaques_bridge = relationship("BridgeCommandePlaques", backref = "plaque") 
    

    def _data (self):
        return{
            'id':self.id,
            'value':self.value,
            'surface':self.surface
        }
    def save (self):
        db.session.add (self)
        db.session.commit()


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
    prix_ht= db.Column(db.Float, nullable=False)
    name_dxf = db.Column(db.String(256), nullable=True )
    name_bl = db.Column(db.String(256), nullable=True )
    name_police = db.Column(db.String(50), nullable=True )
    text = db.Column(db.String(256), nullable=True )
    hauteur_text = db.Column(db.Float , nullable=True)
    description_commercial_responsable = db.Column(db.String(1000), nullable=True)
    date_envoi = db.Column(db.String(256), nullable=False)
    date_confirmation = db.Column(db.String(32), nullable=True)
    date_usinage = db.Column(db.String(32), nullable=True)
    date_fin = db.Column(db.String(32), nullable=False)
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
    prix_livr_ht= db.Column(db.Float, nullable=True)
    is_chute = db.Column(db.Boolean(), server_default=sqlalchemy.sql.expression.true())
    is_plaque = db.Column(db.Boolean(), server_default=sqlalchemy.sql.expression.false())
    rel_commande_commande_plaques_bridge = relationship("BridgeCommandePlaques", backref = "commande") 

    
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
            'name_dxf':self.name_dxf,
            'name_bl':self.name_bl,
            'text':self.text,
            'hauteur_text':self.hauteur_text,
            'description_commercial_responsable':description_commercial_responsable,
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
            'count_persage':self.count_persage,
            'name_police':self.name_police,
            'prix_ht':self.prix_ht,
            'prix_livr_ht':self.prix_livr_ht,
            'is_chute':self.is_chute,
            'is_plaque':self.is_plaque
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
    rel_matiere_plaque = relationship("BridgePlaques", backref = "matiere")
    #property
    def get_all_matiere():
        try:
            return Matiere.query.all()
        except Exception as e:
            print(f"Error fetching all matieres: {str(e)}")
            return None
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
    rel_type_plaque = relationship("BridgePlaques", backref = "type")
    

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
    rel_essaisseur_plaque= relationship("BridgePlaques", backref = "epaisseur")
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

class BridgePlaques(db.Model):
    __tablename__ = 'bridge_plaques'

    matiere_id = db.Column(db.Integer,ForeignKey('matiere.id') ,primary_key=True)
    type_id = db.Column(db.Integer,ForeignKey('type.id') ,primary_key=True)
    epaisseur_id = db.Column(db.Integer , ForeignKey('epaisseur.id') ,primary_key=True)
    plaque_id = db.Column(db.Integer , ForeignKey('plaque.id') ,primary_key=True)
    prix_plaque = db.Column(db.Float, nullable=False)
      

     #property
    def _data (self):
        return{
            'matiere_id':self.matiere_id,
            'type_id':self.type_id,
            'epaisseur_id':self.epaisseur_id,
            'prix_plaque':self.prix_plaque,
            'plaque_id':plaque_id
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


class BridgeCommandePlaques(db.Model):
    __tablename__ = 'bridge_commande_plaques'
  
    id = db.Column(db.Integer, autoincrement=True,primary_key=True )
    commande_id = db.Column(db.Integer,ForeignKey('commande.id') ,nullable=False)
    plaque_id = db.Column(db.Integer,ForeignKey('plaque.id') ,nullable=False)
    nbr_plaque = db.Column(db.Integer ,nullable=False)

      

     #property
    def _data (self):
        return{
            'id':self.id,
            'commande_id':self.commande_id,
            'plaque_id':self.plaque_id,
            'nbr_plaque':self.nbr_plaque
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

    
    result =[]
    
    # filtered = db.session.query(Pvc_bridge.prix_limeaire,Pvc_bridge.prix_matiere  ).join(Epaisseur,Epaisseur.id==Pvc_bridge.epaisseur_id).filter_by(value = epaisseur).join(Pvc, Pvc.id == Pvc_bridge.pvc_id ).filter_by(name = mt_name).first()
    filtered = db.session.query(Bridge.prix_limeaire,Bridge.prix_matiere ).join(Matiere, Matiere.id == Bridge.matiere_id ).filter_by(id = mt).join(Type, Type.id == Bridge.type_id ).filter_by(id = mt_name).join(Epaisseur,Bridge.epaisseur_id == Epaisseur.id).filter_by(id = epaisseur).join(Type_usinage, Type_usinage.id == Bridge.usinage_id ).filter_by(id = type_usinage).first() 
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
    try:
        clients = (
            db.session.query(Client)
            .join(User, Client.user_id == User.id)
            .filter(User.id == current_user.id)
            .all()
        )
        return clients
    
    except Exception as e:
        # Log the error message if you have a logging system in place
        # For now, just print the error message
        print(f"An error occurred: {e}")
        return []

def get_en_attentes(current_user):
    try:
        data = (
            db.session.query(
                Commande.name_matiere,
                Commande.type_matiere,
                Commande.prix_ht,
                Commande.date_envoi,
                Client.name,
                Statut.name,
                Type_usinage.name,
                Epaisseur.value,
                Commande.count,
                Commande.name_dxf,
                Commande.id,
                User.username
            )
            .join(Client, Commande.client_id == Client.id)
            .filter(Client.user_id == current_user.id)
            .join(User, Client.user_id == User.id)
            .join(Statut, Commande.statut_id == Statut.id)
            .filter(Statut.name == "en_attente")
            .join(Type_usinage, Commande.usinage_id == Type_usinage.id)
            .join(Epaisseur, Commande.epaisseur_id == Epaisseur.id)
            .order_by(desc(Commande.date_envoi))
            .all()
        )
        
        result = []
        for row in data:
            result.append(row._data)
            
        return result
    
    except Exception as e:
        # Log the error message if  a logging system in place
        # For now, just print the error message
        print(f"An error occurred: {e}")
        return []
def get_all_attentes():
    try:
        data = (
            db.session.query(
                Commande.name_matiere,
                Commande.type_matiere,
                Commande.prix_ht,
                Commande.date_envoi,
                Client.name,
                Statut.name,
                Type_usinage.name,
                Epaisseur.value,
                Commande.count,
                Commande.name_dxf,
                Commande.id,
                User.username
            )
            .join(Client, Commande.client_id == Client.id)
            .join(User, Client.user_id == User.id)
            .join(Statut, Commande.statut_id == Statut.id)
            .filter(Statut.name == "en_attente")
            .join(Type_usinage, Commande.usinage_id == Type_usinage.id)
            .join(Epaisseur, Commande.epaisseur_id == Epaisseur.id)
            .all()
        )
        
        result = []
        for row in data:
            result.append(row._data)
            
        return result
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
def get_en_attente_by_id(id):
    try:
        data = (
            db.session.query(
                Commande.name_matiere,
                Commande.type_matiere,
                Commande.prix_ht,
                Commande.date_envoi,
                Commande.date_fin,
                Client.name,
                Commande.ville_livr,
                Commande.cp_livr,
                Commande.addresse_livr,
                Statut.name,
                Type_usinage.name,
                Epaisseur.value,
                Commande.count,
                Commande.name_dxf,
                Commande.id,
                User.username,
                Commande.numero_livr,
                Commande.is_livr,
                Commande.is_form,
                Commande.name_police,
                Commande.text,
                Commande.prix_livr_ht,
                Commande.description_commercial_responsable,
                Commande.count_persage,
                Role.name
            )
            .join(Client, Commande.client_id == Client.id)
            .join(User, Client.user_id == User.id)
            .join(Role, User.role_id == Role.id)
            .join(Statut, Commande.statut_id == Statut.id)
            .join(Type_usinage, Commande.usinage_id == Type_usinage.id)
            .join(Epaisseur, Commande.epaisseur_id == Epaisseur.id)
            .filter(Commande.id == id)
            .first()
        )
        
        if data:
            return data._data
        else:
            return None
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
def change_confirmer(changed_id, name,current_date ):
    current_commande = Commande.query.filter_by(id= changed_id).first()
    current_commande.statut_id=2
    current_commande.name_bl=name
    current_commande.date_confirmation = current_date
    db.session.commit()


def change_livré(changed_id):
    try:
        # Fetch the current commande
        current_commande = Commande.query.filter_by(id=changed_id).first()
        
        # Check if the commande exists
        if current_commande is None:
            raise ValueError(f"No Commande found with id {changed_id}")
        
        # Change the status to "livré"
        current_commande.statut_id = 4
        
        # Commit the changes to the database
        db.session.commit()
    
    except ValueError as ve:
        # Log the specific error if you have a logging system in place
        # For now, just print the error message
        print(f"ValueError: {ve}")
        raise
    
    except Exception as e:
        # Log the general error if you have a logging system in place
        # For now, just print the error message
        print(f"An error occurred: {e}")
        
        # Rollback the session to avoid partial commits
        db.session.rollback()
        
        # Raise the exception again to propagate the error
        raise

def get_confirmes(current_user):
    try:
        data = (
            db.session.query(
                Commande.name_matiere,
                Commande.type_matiere,
                Commande.prix_ht,
                Commande.date_envoi,
                Commande.date_fin,
                Client.name,
                Statut.name,
                Type_usinage.name,
                Epaisseur.value,
                Commande.count,
                Commande.name_dxf,
                Commande.id,
                Commande.date_confirmation,
                User.username
            )
            .join(Client, Commande.client_id == Client.id)
            .join(User, Client.user_id == User.id)
            .filter(User.id == current_user.id)
            .join(Statut, Commande.statut_id == Statut.id)
            .filter(Statut.name == "confirmé")
            .join(Type_usinage, Commande.usinage_id == Type_usinage.id)
            .join(Epaisseur, Commande.epaisseur_id == Epaisseur.id)
            .order_by(desc(Commande.date_envoi))
            .all()
        )
        
        result = []
        for row in data:
            result.append(row._data)
            
        return result
    
    except Exception as e:
        # Log the error message if you have a logging system in place
        # For now, just print the error message
        print(f"An error occurred: {e}")
        return []

def get_all_confirmes():
    try:
        data = (
            db.session.query(
                Commande.name_matiere,
                Commande.type_matiere,
                Commande.prix_ht,
                Commande.date_envoi,
                Commande.date_fin,
                Client.name,
                Statut.name,
                Type_usinage.name,
                Epaisseur.value,
                Commande.count,
                Commande.name_dxf,
                Commande.id,
                Commande.date_confirmation,
                User.username
            )
            .join(Client, Commande.client_id == Client.id)
            .join(User, Client.user_id == User.id)
            .join(Statut, Commande.statut_id == Statut.id)
            .filter(Statut.name == "confirmé")
            .join(Type_usinage, Commande.usinage_id == Type_usinage.id)
            .join(Epaisseur, Commande.epaisseur_id == Epaisseur.id)
            .all()
        )
        
        result = []
        for row in data:
            result.append(row._data)
            
        return result
    
    except Exception as e:
        # Log the error message if you have a logging system in place
        # For now, just print the error message
        print(f"An error occurred: {e}")
        return []

def get_usinés(current_user):
    try:
        data = (
            db.session.query(
                Commande.name_matiere,
                Commande.type_matiere,
                Commande.prix_ht,
                Commande.date_usinage,
                Commande.date_fin,
                Client.name,
                Statut.name,
                Type_usinage.name,
                Epaisseur.value,
                Commande.count,
                Commande.name_dxf,
                Commande.id,
                Commande.date_confirmation,
                User.username,
                Commande.name_bl,
                Role.name
            )
            .join(Client, Commande.client_id == Client.id)
            .filter(Client.user_id == current_user.id)
            .join(User, Client.user_id == User.id)
            .join(Role, User.role_id == Role.id)
            .join(Statut, Commande.statut_id == Statut.id)
            .filter(Statut.name == "usiné")
            .join(Type_usinage, Commande.usinage_id == Type_usinage.id)
            .join(Epaisseur, Commande.epaisseur_id == Epaisseur.id)
            .all()
        )
        
        result = []
        for row in data:
            result.append(row._data)
            
        return result
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
def get_all_usinés():
    try:
        data = (
            db.session.query(
                Commande.name_matiere,
                Commande.type_matiere,
                Commande.prix_ht,
                Commande.date_usinage,
                Commande.date_fin,
                Client.name,
                Statut.name,
                Type_usinage.name,
                Epaisseur.value,
                Commande.count,
                Commande.name_dxf,
                Commande.id,
                Commande.date_confirmation,
                User.username,
                Role.name
            )
            .join(Client, Commande.client_id == Client.id)
            .join(User, Client.user_id == User.id)
            .join(Role, User.role_id == Role.id)
            .join(Statut, Commande.statut_id == Statut.id)
            .filter(Statut.name == "usiné")
            .join(Type_usinage, Commande.usinage_id == Type_usinage.id)
            .join(Epaisseur, Commande.epaisseur_id == Epaisseur.id)
            .all()
        )
        
        result = []
        for row in data:
            result.append(row._data)
            
        return result
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def get_livré(current_user):
    try:
        data = (
            db.session.query(
                Commande.name_matiere,
                Commande.type_matiere,
                Commande.prix_ht,
                Commande.date_envoi,
                Commande.date_fin,
                Client.name,
                Statut.name,
                Type_usinage.name,
                Epaisseur.value,
                Commande.count,
                Commande.name_bl,
                Commande.id,
                Commande.date_confirmation,
                User.username,
                Commande.name_bl,
                Role.name
            )
            .join(Client, Commande.client_id == Client.id)
            .filter(Client.user_id == current_user.id)
            .join(User, Client.user_id == User.id)
            .join(Role, User.role_id == Role.id)
            .join(Statut, Commande.statut_id == Statut.id)
            .filter(Statut.name == "livré")
            .join(Type_usinage, Commande.usinage_id == Type_usinage.id)
            .join(Epaisseur, Commande.epaisseur_id == Epaisseur.id)
            .order_by(desc(Commande.date_envoi))
            .all()
        )
        
        result = []
        for row in data:
            result.append(row._data)
        
        return result
    
    except Exception as e:
        # Log the error message if you have a logging system in place
        # For now, just print the error message
        print(f"An error occurred: {e}")
        return []
def get_all_livré():
    try:
        data = (
            db.session.query(
                Commande.name_matiere,
                Commande.type_matiere,
                Commande.prix_ht,
                Commande.date_envoi,
                Commande.date_fin,
                Client.name,
                Statut.name,
                Type_usinage.name,
                Epaisseur.value,
                Commande.count,
                Commande.name_bl,
                Commande.id,
                Commande.date_confirmation,
                User.username,
                Role.name
            )
            .join(Client, Commande.client_id == Client.id)
            .join(User, Client.user_id == User.id)
            .join(Role, User.role_id == Role.id)
            .join(Statut, Commande.statut_id == Statut.id)
            .filter(Statut.name == "livré")
            .join(Type_usinage, Commande.usinage_id == Type_usinage.id)
            .join(Epaisseur, Commande.epaisseur_id == Epaisseur.id)
            .all()
        )
        
        result = []
        for row in data:
            result.append(row._data)
        
        return result
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def get_confirmé_by_id(id):
    try:
        data = (
            db.session.query(
                Commande.name_matiere,
                Commande.type_matiere,
                Commande.prix_ht,
                Commande.date_envoi,
                Commande.date_fin,
                Client.name,
                Commande.numero_livr,
                Commande.addresse_livr,
                Commande.cp_livr,
                Commande.ville_livr,
                Statut.name,
                Type_usinage.name,
                Epaisseur.value,
                Commande.count,
                Commande.name_dxf,
                Commande.id,
                User.username,
                Commande.name_bl,
                Role.name
            )
            .join(Client, Commande.client_id == Client.id)
            .join(User, Client.user_id == User.id)
            .join(Role, User.role_id == Role.id)
            .join(Statut, Commande.statut_id == Statut.id)
            .join(Type_usinage, Commande.usinage_id == Type_usinage.id)
            .join(Epaisseur, Commande.epaisseur_id == Epaisseur.id)
            .filter(Commande.id == id)
            .first()
        )
        
        if data:
            return data._data
        else:
            return None
    
    except Exception as e:
        # Log the error message if you have a logging system in place
        # For now, just print the error message
        print(f"An error occurred: {e}")
        return None

def change_usiner(changed_id, current_date):
    current_commande = Commande.query.filter_by(id= changed_id).first()
    current_commande.statut_id=3
    current_commande.date_usinage=current_date
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
    return db.session.query(User).filter(or_(User.role_id == 1, User.role_id == 2)).all()

def get_cients_by_rep(first_rep_id):
    clients=db.session.query(Client.name,Client.ville,Client.cp,Client.numero,Client.addresse,User.username,Client.email,Client.tel,User.id,Client.id,Client.prix_livr).join(User,Client.user_id== User.id ).filter(Client.user_id == first_rep_id ).all()
    result = []
    for row in  clients : 
        result.append(row._data) 

    return result
def get_plaques(mat_id, type_id, epp_id):
    return db.session.query(Plaque.value, Plaque.surface,BridgePlaques.prix_plaque).join(BridgePlaques,BridgePlaques.plaque_id== Plaque.id ).filter(BridgePlaques.matiere_id == mat_id, BridgePlaques.type_id == type_id,BridgePlaques.epaisseur_id== epp_id).all()

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
    current_client.prix_livr=Edit_data[0]['prix_livr']

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
        user_data  = db.session.query(User.username,Role.name).join(Client,  User.id== Client.user_id ).join(Role,  User.role_id== Role.id ).first()
        main_path = os.path.dirname(os.path.dirname(__file__))
        commands = Commande.query.filter_by(client_id=id).all()
        print(commands)
        for row in commands:
            print(row.name_dxf)
            path_dxf = 'static/members/'+user_data[1] +'/'+user_data[0]+'/DXF/'+row.name_dxf+'.dxf'
            path_bl = 'static/members/'+user_data[1] +'/'+user_data[0]+'/BL/'+row.name_dxf+'.pdf'
            path_img = 'static/members/'+user_data[1] +'/'+user_data[0]+'/IMG/'+row.name_dxf+'.png'
            print(path_img)
            if os.path.exists(path_dxf):
                os.remove(path_dxf)
            
            if os.path.exists(path_bl):
                os.remove(path_bl)
            
            if os.path.exists(path_img):
                os.remove(path_img)
        Commande.query.filter_by(client_id=id).delete()
        Client.query.filter_by(id=id).delete()
        db.session.commit()
        print("sddxxxxxxxxxxxxxxxxxxxxxx")
        
    except Exception as e:
        print(e)


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


def get_plaque_id(text_plaque):

    try:
        plaque = (
            db.session.query(
                Plaque.id
            )
            .join(BridgePlaques, BridgePlaques.plaque_id==  Plaque.id)
            .filter(Plaque.value == text_plaque)
            .first()
        )

        return plaque[0]
    
    except Exception as e:
        # Log the error message if you have a logging system in place
        # For now, just print the error message
        print(f"An error occurred: {e}")
        return None