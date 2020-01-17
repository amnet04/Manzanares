# thing.py

import sqlite3
import re
import logging
from datetime import datetime


class thing():
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










