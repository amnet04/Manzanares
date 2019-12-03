# TheThing.py

import sqlite3
import re
import logging
from datetime import datetime


class thingClass():
	""" The primary class for text analysis whit the Manzanares package:  Stores the txt/csv/tsv/sqlite file location and some other data and methods to process it. Also, create and connect with sqlite databases  to handle token/types.
    
    ...

    Attributes
    ----------

    name: str
    	The name of the Document/Thing

    t_folder: str
    	Location of the thing file

    t_file: str
    	Name of the thing file

    db_folder: str = '../dbases/'+name/
    	Location of the database file

    db_file: str = db_folder+name+".sqlite"
    	Name of the database file

    lang: List[str] = []
    	List of ISO 639-2 Code for the language/languages in the file

    encoding: str = 'UTF-8'
    	Encoding of the Document/Thing file

    s_break: _sre.SRE_Pattern = re.compile("\.")
		Regex expression to split sentences

    l_break: _sre.SRE_Pattern = re.compile("\.")
		Regex expression to split lines

    w_break: _sre.SRE_Pattern = re.compile(" ")
    	Regex expresion to split words

    c_patt: List(Tuple(_sre.SRE_Pattern,_sre.SRE_Pattern))
		List of regular expression tuples to replace in thing: 
		Tuple [0] regular expression to be replaced, Tuple [1] 
		regular replacement expression.

    db_con: sqlite3.Connection
		Database conection 
 
    db_cur: sqlite3.Cursor
		Database cursor

    Methods
    -------
    Create table

	"""

	LOG_FILENAME = 'info.log'

	def __init__(self,
				 name,
				 t_folder,
				 t_file,
				 s_level = True,
				 w_level = True,
				 gaps = [[0]],
				 db_folder = "../../dbases/",
				 db_name = "colection",
				 lang = ["und"],
				 encoding = "UTF-8",
				 s_break = r"\.",
				 l_break = r"\n+",
				 w_break = r"\s+",
				 c_patt = [("","")])


	
		try:
			self.db_con = sqlite3.connect("{}/{}.sqlite?mode=rw".format(db_folder,db_name), 
										  uri=True)
			now = datetime.now()
			logging.info('{}: Info: Database already exists, checking and loading it.')
			
		
		except:
			self.name = name,
			self.t_folder = t_folder
			self.t_file = t_file
			self.db_folder = db_folder
			self.db_name = db_name
			self.lang = lang
			"""
			ISO 639-3 especial  codes :

			mis 	Uncoded languages
			mul 	Multiple languages
			und 	Undetermined
			zxx 	No linguistic content / Not applicable 
			"""
			self.encoding = encodingode=rw".format(db_folder,db_name), 
			self.s_break = s_break
			self.l_break = l_break
			self.w_break = w_break
			self.s_level = s_level
			self.w_level = w_level
			self.db_con = sqlite3.connect('{}/{}.sqlite'.format(db_folder,db_name))


		def create_structure(self)

			cretable_base =  "CREATE TABLE IF NOT EXISTS Thing ("
			creteble_base += "ThigId INTEGER NOT NULL PRIMARY KEY, "
			cretable_base += "Name TEXT NOT NULL UNIQUE, "
			cretable_base += "TFolder TEXT NOT NULL UNIQUE, "
			cretable_base += "TFile TEXT NOT NULL UNIQUE, "
			cretable_base += "Encoding TEXT NOT NULL DEFAULT 'UTF-8', "
			cretable_base += "SBreak TEXT, "
			cretable_base += "LBreak TEXT, " 
         	cretable_base += "CONSTRAINT unq UNIQUE (Name, TFolder, TFile))"

         	cretable_lang =  "CREATE TABLE IF NOT EXISTS Langs ("
         	cretable_lang += "LId INTEGER NOT NULL PRIMARY KEY, "
         	cretable_lang += "Lang TEXT NOT NULL UNIQUE)" 

         	cretable_thil =  "CREATE TABLE IF NOT EXISTS ThingsLangs ("
         	cretable_thil += "TLId INTEGER NOT NULL PRIMARY KEY, "
         	cretable_thil += "ThingId INTEGER NOT NULL, "
         	cretable_thil += "LId INTEGER NOT NULL, "
         	cretable_thil += "FOREING KEY(LId)  REFERENCES Langs(LId), "
         	cretable_thil += "FOREING KEY(ThingId)  REFERENCES ThingId(ThingId)), "
         	cretable_thil += "CONSTRAINT unq UNIQUE (ThingId, LId))"

         	cretable_gaps += "CREATE TABLE IF NOT EXISTS GAPS ("
         	cretable_gaps += "GapsId INTEGER NOT NULL PRIMARY KEY, "
         	cretable_gaps += "Gaps TEXT NOT NULL UNIQUE)"

         	cretable_thga =  "CREATE TABLE IF NOT EXISTS ThingsGaps ("
         	cretable_thga += "TGId INTEGER NOT NULL PRIMARY KEY, "
         	cretable_thga += "ThingId INTEGER NOT NULL, "
         	cretable_thga += "GapsId INTEGER NOT NULL, "
         	cretable_thga += "FOREING KEY(GapsId)  REFERENCES Gaps(GapsId), "
         	cretable_thga += "FOREING KEY(ThingId)  REFERENCES ThingId(ThingId)), "
         	cretable_thga += "CONSTRAINT unq UNIQUE (ThingId, GapsId))" 

         	
         	cretable_cpat =  "CREATE TABLE IF NOT EXISTS ClearPatterns ("
         	cretable_cpat += "CPId INTEGER NOT NULL PRIMARY KEY, "
         	cretable_cpat += "Target TEXT NOT NULL"
         	cretable_cpat += "Replace TEXT NOT NULL"
         	cretable_cpat += "CONSTRAINT unq UNIQUE (Target Replace))"

         	cretable_thcp =  "CREATE TABLE IF NOT EXISTS ThingsCleanPatterns ("
         	cretable_thcp += "CPId INTEGER NOT NULL PRIMARY KEY, "
         	cretable_thcp += "ThingId INTEGER NOT NULL, "
         	cretable_thcp += "GapsId INTEGER NOT NULL, "
         	cretable_thcp += "FOREING KEY(CPId)  REFERENCES Gaps(CPId), "
         	cretable_thcp += "FOREING KEY(ThingId)  REFERENCES ThingId(ThingId)), "
         	cretable_thcp += "CONSTRAINT unq UNIQUE (ThingId, CPId))"

         	token_catalog =  "CREATE TABLE IF NOT EXIST TypeCatalogue("
         	token_catalog += "TypeID INTEGER NOT NULL PRIMARY KEY, "
         	token_catalog += "Type TEXT NOT NULL UNIQUE, "
         	token_catalog += "Length INTEGER NOT NULL)"

         	token_thing_c =  "REATE TABLE IF NOT EXIST  TokThing("
         	token_thing_c =  "TokThingId  INTEGER NOT NULL PRIMARY KEY, "
         	token_thing_c =  








