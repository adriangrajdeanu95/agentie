from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# coding: utf-8
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Admin(Base):
    __tablename__ = 'Admin'

    ID_Admin = Column(Integer, primary_key=True, server_default=text("nextval('Admin_ID_Admin_seq'::regclass)"))
    username = Column(String(30), nullable=False)
    password = Column(String(100), nullable=False)

class Cazare(Base):
    __tablename__ = 'Cazare'

    ID_Cazare = Column(Integer, primary_key=True, server_default=text("nextval('Cazare_ID_Cazare_seq'::regclass)"))
    Tip = Column(Integer, nullable=False)
    Nume = Column(String, nullable=False)
    Nr_Stele = Column(Integer, nullable=False)
    Rating = Column(Integer, nullable=False)
    Descriere = Column(String, nullable=False)
    All_inclusive = Column(Boolean, nullable=False)
    Baie_camera = Column(Boolean, nullable=False)
    Uscator_par = Column(Boolean, nullable=False)
    Incalzire_centrala = Column(Boolean, nullable=False)
    Aer_Conditionat = Column(Boolean, nullable=False)
    Baie_cu_cada = Column(Boolean, nullable=False)
    Internet_in_camera = Column(Boolean, nullable=False)
    Wi_fi = Column('Wi-fi', Boolean, nullable=False)
    Gratar = Column(Boolean, nullable=False)
    Mic_dejun_inclus = Column(Boolean, nullable=False)
    Nr_camere_duble_m = Column(Integer, nullable=False)
    Nr_camere_triple = Column(Integer, nullable=False)
    Nr_apartamente = Column(Integer, nullable=False)
    ID_Oras = Column(ForeignKey(u'Orase.ID_Oras'), nullable=False)

    Orase = relationship(u'Orase')

class Client(Base):
    __tablename__ = 'Client'

    ID_Client = Column(Integer, primary_key=True, server_default=text("nextval('Client_ID_Client_seq'::regclass)"))
    Nume = Column(String, nullable=False)
    Oras_Domiciliu = Column(ForeignKey(u'Orase.ID_Oras'), nullable=False)
    CNP = Column(String(13), nullable=False, unique=True)
    Observatii = Column(String, nullable=False)
    Asig_Sanatate = Column(String(20), nullable=False, unique=True)
    Nr_Telefon = Column(String(10), nullable=False, unique=True)
    Email = Column(String, nullable=False, unique=True)

    Orase = relationship(u'Orase')

class ClientExcursie(Base):
    __tablename__ = 'Client_Excursie'

    ID_Client_Excursie = Column(Integer, primary_key=True, server_default=text("nextval('Client_Excursie_ID_Client_Excursie_seq'::regclass)"))
    ID_Client = Column(ForeignKey(u'Client.ID_Client'), nullable=False, server_default=text("nextval('Client_Excursie_ID_Client_seq'::regclass)"))
    ID_Excursie = Column(ForeignKey(u'Excursie.ID_Excursie'), nullable=False, server_default=text("nextval('Client_Excursie_ID_Excursie_seq'::regclass)"))
    Nr_Adulti = Column(Integer, nullable=False)
    Nr_Copii = Column(Integer, nullable=False)
    Data_Plecare = Column(Date, nullable=False)

    Client = relationship(u'Client')
    Excursie = relationship(u'Excursie')

class CompTransport(Base):
    __tablename__ = 'Comp_Transport'

    ID_Comp_Transport = Column(Integer, primary_key=True, server_default=text("nextval('Comp_Transport_ID_Comp_Transport_seq'::regclass)"))
    Nume = Column(String, nullable=False)
    Rating = Column(Integer, nullable=False)

class Excursie(Base):
    __tablename__ = 'Excursie'

    ID_Excursie = Column(Integer, primary_key=True, server_default=text("nextval('Excursie_ID_Excursie_seq'::regclass)"))
    Data_Inceput_Perioada = Column(Date, nullable=False)
    Data_Sfarsit_Perioada = Column(Date, nullable=False)
    Pret = Column(Integer, nullable=False)
    Nr_zile = Column(Integer, nullable=False)
    Nr_mese_zi = Column(Integer, nullable=False)

class ExcursieCazare(Base):
    __tablename__ = 'Excursie_Cazare'

    Excursie_Cazare = Column(Integer, primary_key=True, server_default=text("nextval('Excursie_Cazare_Excursie_Cazare_seq'::regclass)"))
    ID_Excursie = Column(ForeignKey(u'Excursie.ID_Excursie'), nullable=False)
    ID_Cazare = Column(ForeignKey(u'Cazare.ID_Cazare'), nullable=False)

    Cazare = relationship(u'Cazare')
    Excursie = relationship(u'Excursie')

class ExcursieTransport(Base):
    __tablename__ = 'Excursie_Transport'

    ID_Excursie_Transport = Column(Integer, primary_key=True, server_default=text("nextval('Excursie_Transport_ID_Excursie_Transport_seq'::regclass)"))
    ID_Excursie = Column(ForeignKey(u'Excursie.ID_Excursie'), nullable=False)
    ID_Transport = Column(ForeignKey(u'Transport.ID_Transport'), nullable=False)

    Excursie = relationship(u'Excursie')
    Transport = relationship(u'Transport')

class Orase(Base):
    __tablename__ = 'Orase'

    ID_Oras = Column(Integer, primary_key=True, server_default=text("nextval('Orase_ID_Oras_seq'::regclass)"))
    Nume = Column(String(20), nullable=False)
    Tara = Column(String(20), nullable=False)
    Rating = Column(Integer, nullable=False)

class Transport(Base):
    __tablename__ = 'Transport'

    ID_Transport = Column(Integer, primary_key=True, server_default=text("nextval('Transport_ID_Transport_seq'::regclass)"))
    ID_Comp_transport = Column(ForeignKey(u'Comp_Transport.ID_Comp_Transport'), nullable=False)
    ID_Oras_Plecare = Column(ForeignKey(u'Orase.ID_Oras'), nullable=False)
    ID_Oras_Sosire = Column(ForeignKey(u'Orase.ID_Oras'), nullable=False)
    Distanta = Column(Integer, nullable=False)
    Durata = Column(Integer, nullable=False)
    Tip_Transport = Column(Integer, nullable=False)
    Incarcator = Column(Boolean, nullable=False)
    Wifi = Column(Boolean, nullable=False)

    Comp_Transport = relationship(u'CompTransport')
    Orase = relationship(u'Orase', primaryjoin='Transport.ID_Oras_Plecare == Orase.ID_Oras')
    Orase1 = relationship(u'Orase', primaryjoin='Transport.ID_Oras_Sosire == Orase.ID_Oras')
