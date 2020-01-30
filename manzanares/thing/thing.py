# thing.py

import sqlite3
import re
import logging
from os import path
from urllib.request import pathname2url

import sys
sys.path.append(path.join(path.dirname(__file__), '../..'))
from manzanares.thing.thing_querys import * 
from manzanares.text_preproc.chunkreader import ChunkReader
from manzanares.text_preproc.text_preprocess import normalize_txt, split_sentence


logging.basicConfig(filename="/tmp/thing_corp.log",
                    level=logging.DEBUG,
                    format='%(asctime)s - %(message)s')


class thing():

    def __init__(self,
                 name,
                 description = False, 
                 tfolder = False, 
                 tfile = False,
                 encoding = False,
                 sentencebreak = False,
                 linebreak = False,  
                 languages = False,
                 cleanpatt= False, 
                 db_folder="../../dbases/"):

        self.name  = name
        self.db_folder = db_folder
        self.db_file = '{}/{}.sqlite'.format(self.db_folder,self.name)

        dict = {"description":description, 
                "tfolder":tfolder, 
                "tfile":tfile, 
                "encoding":encoding, 
                "sentensebreak":sentencebreak, 
                "linebreak":linebreak, 
                "language":languages, 
                "cleanpatt":cleanpatt}

        if  description == tfolder == tfile == encoding == sentencebreak == linebreak  == languages == cleanpatt == False:
            self.open_db(from_file=True)
            self.load_values()

        else:
            values_in_false = []
            setted_values = []
            for key, value in dict.items():
                if value == False:
                    values_in_false.append(key)
                else:
                    setted_values.append(key)
            if values_in_false == []:
                self.description = description
                self.tfolder = tfolder
                self.tfile = tfile
                self.encoding = encoding
                self.sentencebreak = sentencebreak
                self.linebreak = linebreak
                self.tokencount = 0 
                self.typecount = 0
                self.lastprocecedtoken = 0
                self.lastprocecedsentence = 0
                self.lastprocecedline = 0
                self.languages = languages
                self.cleanpatt = cleanpatt
                self.finished = 0

                self.load_db()

            else:
                raise ValueError("No  setees los parametros {}, o termina de setear {}".format(setted_values, values_in_false)) 

       


    def open_db(self, from_file=False):
        if path.isfile(self.db_file):
            logging.info('Database {} already exists, checking and loading it.'.format(self.name))
            db_uri = "file:{}?mode=rw".format(pathname2url(self.db_file))
            self.db_con = sqlite3.connect(db_uri, uri=True)
            self.db_cur = self.db_con.cursor()
            self.check_struct()
        elif from_file==True:
            raise IntegrityError("El archivo no existe")
        else:
            self.create_db()
        

    def create_db(self):
        logging.info('Creating database {} in {}'.format(self.name, self.db_folder))
        self.db_con = sqlite3.connect(self.db_file)
        self.db_cur = self.db_con.cursor()
        
        self.create_struct()
        
        self.db_cur.execute(ADD_MASTER, [self.name, 
                                         self.description, 
                                         self.tfolder, 
                                         self.tfile, 
                                         self.encoding,
                                         self.sentencebreak,
                                         self.linebreak,
                                         self.tokencount,
                                         self.typecount,
                                         self.lastprocecedtoken,
                                         self.lastprocecedsentence,
                                         self.lastprocecedline] )
        self.db_con.commit()

        for lang in self.languages:
            try:
                self.db_cur.execute(ADD_LANGU, [lang])
                self.db_con.commit()
            except sqlite3.IntegrityError as e:
                if "UNIQUE constraint failed: Langs.Lang" in "{}".format(e):
                    pass
                else:
                    raise AssertionError(e)

        for pattern in self.cleanpatt :
            try:
                self.db_cur.execute(ADD_CLEPT, [pattern[0],pattern[1]])
                self.db_con.commit()
            except sqlite3.IntegrityError as e:
                if "UNIQUE constraint failed:" in "{}".format(e):
                    raise AssertionError(e)
                else:
                    raise AssertionError(e)

        self.process_text()


    def load_db(self):
        self.open_db()        
        self.check_master()
        self.check_langs()
        self.check_cpattr()

    def load_values(self):
        self.db_cur.row_factory = None
        self.db_cur.execute(GET_MASTER)
        master = self.db_cur.fetchone()

        self.db_cur.row_factory = lambda cursor, row: row[0]
        self.db_cur.execute(GET_LANGS)
        langs = self.db_cur.fetchall()

        self.db_cur.row_factory = lambda cursor, row: (row[0],row[1])
        self.db_cur.execute(GET_CLEPT)
        cpatt = self.db_cur.fetchall()

        self.__init__(self.name,
                      description = master[2], 
                      tfolder = master[3], 
                      tfile = master[4],
                      encoding = master[5],
                      sentencebreak = master[6],
                      linebreak = master[7],  
                      languages = langs,
                      cleanpatt= cpatt, 
                      db_folder=self.db_folder)




    def create_struct(self):
        self.db_cur.execute(CRE_MASTER)
        self.db_cur.execute(CRE_LANGU)
        self.db_cur.execute(CRE_CLEPT)
        self.db_cur.execute(CRE_SYMBOL)
        self.db_cur.execute(CRE_WORDS)
        self.db_cur.execute(CRE_GARBAGE)
        self.db_con.commit()


    def check_struct(self):

        expected_struct = { "MASTER": [(0, 'Id', 'INTEGER', 0, None, 1), 
                                        (1, 'Name', 'TEXT', 1, None, 0), 
                                        (2, 'Description', 'TEXT', 1, None, 0), 
                                        (3, 'TFolder', 'TEXT', 1, None, 0), 
                                        (4, 'TFile', 'TEXT', 1, None, 0), 
                                        (5, 'Encoding', 'TEXT', 1, None, 0), 
                                        (6, 'SentenceBreak', 'TEXT', 0, None, 0), 
                                        (7, 'LineBreak', 'TEXT', 0, None, 0), 
                                        (8, 'TokenCount', 'INTEGER', 1, None, 0), 
                                        (9, 'TypeCount', 'INTEGER', 1, None, 0), 
                                        (10, 'LastProcecedToken', 'INTEGER', 1, None, 0), 
                                        (11, 'LastProcecedSentence', 'INTEGER', 1, None, 0), 
                                        (12, 'LastProcecedLine', 'INTEGER', 1, None, 0), 
                                        (13, 'Finished', 'INTEGER', 1, '0', 0)],


                            "Langs": [(0, 'Lang', 'TEXT', 1, None, 1)],

                            "CleanPatterns": [(0, 'Target', 'TEXT', 1, None, 1), 
                                              (1, 'Replace', 'TEXT', 1, None, 0)],

                            "Symbols": [(0, 'Id', 'INTEGER', 1, None, 1), 
                                        (1, 'Symbol', 'TEXT', 1, None, 0)],

                            "Words": [(0, 'Id', 'INTEGER', 1, None, 1), 
                                      (1, 'Word', 'TEXT', 1, None, 0)],

                            "Cleaned":[(0, 'Id', 'INTEGER', 1, None, 0), 
                                       (1, 'Garbage', 'TEXT', 1, None, 0), 
                                       (2, 'Replace', 'TEXT', 1, None, 0)]


        }
        self.db_cur.row_factory = lambda cursor, row: row[0]
        self.db_cur.execute(CHK_ALLTBL)
        db_tables = self.db_cur.fetchall()
        if sorted(list(expected_struct.keys())) == sorted(db_tables):
            for key in expected_struct:
                check="PRAGMA table_info({})".format(key)
                self.db_cur.row_factory = None
                self.db_cur.execute(check)
                table_str = self.db_cur.fetchall()
                #print(key)
                if table_str != expected_struct[key]:
                    diference = list(set(expected_struct[key]) - set(table_str))
                    raise AssertionError("Table {} doesnt fit:\n {}".format(key, table_str))
                
            logging.info("Database {} checked".format(self.name))
            return True
        else:
            raise ValueError("Tables name/number doestn match")


    def check_master(self):
        try:
            self.db_cur.execute(INS_MASTER)
            self.db_con.commit()
        except sqlite3.IntegrityError as e:
            if "CHECK constraint failed: MASTER" in "{}".format(e):
                self.db_cur.execute(GET_MASTER)
                check_tuple = [self.name, 
                               self.description, 
                               self.tfolder, 
                               self.tfile, 
                               self.encoding,
                               self.sentencebreak,
                               self.linebreak]
                master_data = list(self.db_cur.fetchone())
                if check_tuple == master_data[1:8]:
                    return True
                else:
                    diference = list(set(check_tuple) - set(master_data[1:8])) 
                    raise AssertionError(check_tuple, "\n", master_data[1:8])
            else:
                raise AssertionError(e)


    def check_langs(self):
        self.db_cur.row_factory = lambda cursor, row: row[0]
        self.db_cur.execute(GET_LANGS)
        langs = self.db_cur.fetchall()
        if sorted(langs) == sorted(self.languages):
            return True
        else:
            raise ValueError("Los lenguajes introducidos no son iguales a los registrados")


    def check_cpattr(self):
        self.db_cur.row_factory = lambda cursor, row: (row[0],row[1])
        self.db_cur.execute(GET_CLEPT)
        clept = self.db_cur.fetchall()
        if clept == self.cleanpatt:
            return True
        else:
            raise ValueError("Los patrones de limpieza introducidos no son iguales a los registrados o no tienen el mismo orden")


    def process_text(self):
        f = "{}/{}".format(self.tfolder,self.tfile)
        for chunk in ChunkReader(f,end=r"[\n{1:}]"):
            normal=normalize_txt(chunk, self.cleanpatt)
            print(normal)


    def Disconnect(self):
        self.db_con.close()










