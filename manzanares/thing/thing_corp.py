import sqlite3
import re
import logging
from os import path
from urllib.request import pathname2url

import sys
sys.path.append(path.join(path.dirname(__file__), '../..'))
from manzanares.thing.db_querys import * 

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
        self.db_cur.execute(cretable_lang)
        self.db_cur.execute(cretable_thil)
        self.db_cur.execute(cretable_cpat)
        self.db_cur.execute(cretable_thcp)
        self.db_cur.execute(cretable_thcp)
        self.db_cur.execute(type_cataloge)
        self.db_cur.execute(cretable_thty)
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
                 cleanpatt):

        
        CleanPatt = ''' INSERT INTO 
                    '''
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
        except:
            logging.info("{} Thing whit the same file, tokens and gaps already exists".format(name))
            self.db_cur.execute(CHK_THING, [ThingValues[val] for val in [0,2,3,7,8]])
            ThingId = self.db_cur.fetchone()[0]

        for pattern in cleanpatt:
                self.db_cur.execute(CHK_CPATT, pattern)
                resulta = self.db_cur.fetchone()
                if resulta:
                    cpattid = resulta[0]
                    self.db_cur.execute(CHK_CPATR, (cpattid, ThingId))
                    resultb = self.db_cur.fetchone()
                    if not resultb:
                        self.db_cur.execute(ADD_CPATR, (cpattid, ThingId))
                        self.db_con.commit()
                else:               
                    self.db_cur.execute(ADD_CPATT, pattern)
                    self.db_con.commit()
                    cpattid = self.db_cur.lastrowid
                    self.db_cur.execute(ADD_CPATR, (cpattid, ThingId))
                    self.db_con.commit()

                

                


    def RecoverThing(self):
        pass

    def ProcessTextThing(self):
        pass


    