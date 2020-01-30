import sqlite3
import re
import logging
from os import path
from urllib.request import pathname2url

import sys
sys.path.append(path.join(path.dirname(__file__), '../..'))
from manzanares.thing.db_querys import * 
from manzanares.text_preproc.chunkreader import ChunkReader
from manzanares.text_preproc.text_preprocess import normalize_txt, split_sentence


logging.basicConfig(filename="/tmp/thing_corp.log",
                    level=logging.DEBUG,
                    format='%(asctime)s - %(message)s')

class thing_corp():

    """Summary
    
    Attributes:
        db_con (TYPE): Description
        db_cur (TYPE): Description
        db_folder (str): Description
        name (str): Description
    
    """

    def __init__(self, name="", db_folder="../../dbases/"):
        """Summary
        
        Args:
            name (str, optional): Description
            db_folder (str, optional): Description
        """
        self.name = name
        self.db_folder = db_folder
        self.file = '{}/{}.sqlite'.format(self.db_folder,self.name)



        
        if path.isfile(self.file):
            logging.info('Database {} already exists, checking and loading it.'.format(self.name))
            db_uri = "file:{}?mode=rw".format(pathname2url(self.file))
            self.db_con = sqlite3.connect(db_uri, uri=True)
            self.db_cur = self.db_con.cursor()
            self.CheckDbStruc()
            

        else:
            logging.info('Creating database {} in {}'.format(self.name, self.db_folder))
            self.db_con = sqlite3.connect(self.file)
            self.db_cur = self.db_con.cursor()
            self.CreateDbStruc()
            


    def CreateDbStruc(self):
        self.db_cur.execute(cretable_base)
        self.db_cur.execute(cretable_garb)
        self.db_cur.execute(cretable_gart)
        self.db_cur.execute(cretable_lang)
        self.db_cur.execute(cretable_thil)
        self.db_cur.execute(cretable_cpat)
        self.db_cur.execute(cretable_thcp)
        self.db_cur.execute(cretable_thcp)
        self.db_cur.execute(type_cataloge)
        self.db_cur.execute(token_catalog)
        self.db_con.commit()


    def CheckDbStruc(self):
        for key in table_dic:
            check="PRAGMA table_info({})".format(key)
            self.db_cur.execute(check)
            table_str = self.db_cur.fetchall()
            if table_str != table_dic[key]:
                raise AssertionError("Table {} doesnt fit:\n {}".format(key, table_str))
        logging.info("Database {} checked".format(self.name))
        return True


    def Disconnect(self):
        self.db_con.commit()
        self.db_con.close()

    def AddThing(self, 
                 name, 
                 description, 
                 tfolder, 
                 tfile,
                 encoding,
                 sbreak,
                 lbreak,
                 tokensare,
                 gap,
                 languages,
                 cleanpatt):


        ThingValues = (name, 
                 description, 
                 tfolder, 
                 tfile,
                 encoding,
                 sbreak,
                 lbreak,
                 tokensare,
                 gap)
        try:
            self.db_cur.execute(ADD_THING, ThingValues)
            self.db_con.commit()
            ThingId = self.db_cur.lastrowid
            logging.info("Thing {} created".format(self.name))
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in "{}".format(e):
                logging.info("{} Thing whit the same file, tokens and gaps already exists, checking status".format(name))
                self.db_cur.execute(CHK_THING, [ThingValues[val] for val in [0,2,3,7,8]])
                resultt  = self.db_cur.fetchone()
                if  resultt: 
                    ThingId = resultt[0]
                    Finished = resultt[15]
                    if Finished == True:
                        raise "{} Thing already exists and the process was finished".format(name)
            else:
                logging.info(e)
                raise e

                       

        for pattern in cleanpatt:
                self.db_cur.execute(CHK_CPATR, pattern)
                resulta = self.db_cur.fetchone()
                if resulta:
                    cpattid = resulta[0]
                    self.db_cur.execute(CHK_CPATT, (ThingId, cpattid))
                    resultb = self.db_cur.fetchone()
                    if resultb == None:
                        self.db_cur.execute(ADD_CPATT, (ThingId, cpattid))
                        self.db_con.commit()
                else:               
                    self.db_cur.execute(ADD_CPATR, pattern)
                    self.db_con.commit()
                    cpattid = self.db_cur.lastrowid
                    self.db_cur.execute(ADD_CPATT, (ThingId,cpattid))
                    self.db_con.commit()




        for language in languages:
                self.db_cur.execute(CHK_LANGU, [language])
                resulta = self.db_cur.fetchone()
                if resulta:
                    LId = resulta[0]
                    self.db_cur.execute(CHK_LANGT, (ThingId, LId))
                    resultb = self.db_cur.fetchone()
                    if not resultb:
                        self.db_cur.execute(ADD_LANGT, (ThingId, LId))
                        self.db_con.commit()
                else:               
                    self.db_cur.execute(ADD_LANGU, [language])
                    self.db_con.commit()
                    LId = self.db_cur.lastrowid
                    self.db_cur.execute(ADD_LANGT, (ThingId, LId))
                    self.db_con.commit()



        Check =  "SELECT * FROM sqlite_master WHERE type ='Propiedad'"
        self.db_cur.execute(Check)
        result = self.db_cur.fetchall()
        print(">>>>>>>-------\n{}\n------<<<<<<".format(result))


    """def GetThing(self, ThingID)
        self.db_cur.execute(CHK_THING, [ThingValues[val] for val in [0,2,3,7,8]])
        resultt  = self.db_cur.fetchone()
        

        ThigId = resultt[0]
        Name = resultt[1]
        Description = resultt[2]
        TFolder = resultt[3]
        TFile = resultt[4]
        Encoding  = resultt[5]
        SBreak = resultt[6]
        LBreak = resultt[7]
        TokenCount = resultt[8] 
        TypeCount = resultt[9]
        LastProcecedToken = resultt[10]
        LastProcecedSentence = resultt[11]
        LastProcecedLine = resultt[12]
        TokensAre = resultt[13]
        Gap = resultt[14]
        Finished = resultt[15]


    def ProcessTextThing(self, name):
        self.db_cur.execute(CHK_THING, [ThingValues[val] for val in [0,2,3,7,8]])"""


    