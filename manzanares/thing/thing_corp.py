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
        
        if path.isfile(self.db_folder+self.name):
            logging.info('Database {} already exists, checking and loading it.'.format(self.name))
            db_uri = "file:{}?mode=rw".format(pathname2url(self.db_folder+self.name+".sqlite"))
            self.db_con = sqlite3.connect(db_uri, uri=True)
            self.db_cur = self.con.cursor()
            self.CheckDbStruck()
            

        else:
            logging.info('Creating database {} in {}'.format(self.name, self.db_folder))
            self.db_con = sqlite3.connect('{}/{}.sqlite'.format(self.db_folder,self.name))
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


    def CheckStruc(self):
        for key in table_dic:
            check="PRAGMA table_info({})".format(key)
            self.db_cur.execute(check)
            table_str = self.db_cur.fetchall()
            if table_str != table_dic[key]:
                raise AssertionError("Table {} doesnt fit:\n {}".format(key, table_str))
        return True


    def Disconnect(self):
        self.db_con.commit()
        self.db_con.close()




    