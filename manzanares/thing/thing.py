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
                 wordbreak = False,
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
                "sentencebreak":sentencebreak,
                "linebreak":linebreak,
                "wordbreak":wordbreak,
                "language":languages,
                "cleanpatt":cleanpatt}

        if  description == tfolder == tfile == encoding == sentencebreak == linebreak  == wordbreak == languages == cleanpatt == False:
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
                self.wordbreak = wordbreak
                self.tokencount = 0
                self.typecount = 0
                self.lastprocecedtoken = 0
                self.lastprocecedsentence = 0
                self.lastprocecedline = 0
                self.languages = languages
                self.cleanpatt = cleanpatt
                self.finished = 0

                self.text_file = "{}/{}".format(self.tfolder,self.tfile)
                self.chunk_reader = ChunkReader(self.text_file,end=self.linebreak)

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
            print("@@@@@@@ ", self.db_file)
            raise IOError("El archivo {} no existe".format(self.db_file))
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
                                         self.wordbreak,
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

        #todo verificar chunks


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
                      wordbreak = master[8],
                      languages = langs,
                      cleanpatt= cpatt,
                      db_folder=self.db_folder)


    def create_struct(self):
        self.db_cur.execute(CRE_MASTER)
        self.db_cur.execute(CRE_LANGU)
        self.db_cur.execute(CRE_CLEPT)
        self.db_cur.execute(CRE_SYMBOL)
        self.db_cur.execute(CRE_SYMTOK)
        self.db_cur.execute(CRE_WORDS)
        self.db_cur.execute(CRE_WORTOK)
        self.db_cur.execute(CRE_GARBAGE)
        self.db_cur.execute(CRE_GARBTOK)
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
                                        (8, 'WordBreak', 'TEXT', 0, None, 0),
                                        (9, 'TokenCount', 'INTEGER', 1, None, 0),
                                        (10, 'TypeCount', 'INTEGER', 1, None, 0),
                                        (11, 'LastProcecedToken', 'INTEGER', 1, None, 0),
                                        (12, 'LastProcecedSentence', 'INTEGER', 1, None, 0),
                                        (13, 'LastProcecedLine', 'INTEGER', 1, None, 0),
                                        (14, 'Finished', 'INTEGER', 1, '0', 0)],


                            "Langs": [(0, 'Lang', 'TEXT', 1, None, 1)],

                            "CleanPatterns": [(0, 'Target', 'TEXT', 1, None, 1),
                                              (1, 'Replace', 'TEXT', 1, None, 0)],

                            "Symbols": [(0, 'Id', 'INTEGER', 1, None, 1),
                                        (1, 'Symbol', 'TEXT', 1, None, 0)],

                            "SymbolTokens":  [(0, 'SymId', 'INTEGER', 1, None, 0),
                                             (1, 'Form', 'TEXT', 1, None, 0),
                                             (2, 'Chunk', 'INTEGER', 1, None, 0),
                                             (3, 'Sentence', 'INTEGER', 1, None, 0),
                                             (4, 'SentencePos', 'INTEGER', 1, None, 0)],

                            "Words": [(0, 'Id', 'INTEGER', 1, None, 1),
                                      (1, 'Word', 'TEXT', 1, None, 0)],

                            "WordTokens": [(0, 'WordId', 'INTEGER', 1, None, 0), 
                                           (1, 'Form', 'TEXT', 1, None, 0), 
                                           (2, 'Chunk', 'INTEGER', 1, None, 0), 
                                           (3, 'Sentence', 'INTEGER', 1, None, 0), 
                                           (4, 'SentenceposStart', 'INTEGER', 1, None, 0), 
                                           (5, 'SentenceposEnd', 'INTEGER', 1, None, 0)],

                            "Cleaned": [(0, 'Id', 'INTEGER', 0, None, 1),
                                        (1, 'Garbage', 'TEXT', 1, None, 0),
                                        (2, 'Replace', 'TEXT', 1, None, 0)],

                            "CleanTokens":[(0, 'GarId', 'INTEGER', 1, None, 0),
                                           (1, 'Chunk', 'INTEGER', 1, None, 0),
                                           (2, 'Sentence', 'INTEGER', 1, None, 0),
                                           (3, 'Start', 'INTEGER', 1, None, 0),
                                           (4, 'End', 'INTEGER', 1, None, 0)]
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
        self.db_cur.row_factory = None
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
                               self.linebreak,
                               self.wordbreak]
                master_data = list(self.db_cur.fetchone())
                if check_tuple == master_data[1:9]:
                    return True
                else:
                    diference = list(set(check_tuple) - set(master_data[1:9]))
                    raise AssertionError(check_tuple, "\n", master_data[1:9])
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



    def add_symbol(self, symbol):
        try:
            self.db_cur.execute(ADD_SYMBOL, symbol.lower())
            self.db_con.commit()
        except sqlite3.IntegrityError as e:
            if not "UNIQUE constraint failed: Symbols.Symbol" in "{}".format(e):
                 raise e

        self.db_cur.row_factory = lambda cursor, row: (row[0])
        self.db_cur.execute(GET_SYM_ID, symbol.lower())
        symbol_id = self.db_cur.fetchone()
        return symbol_id

    def add_symbol_token(self, symbol_id, symbol,  chunk, sentence, pos_in_sen):
        try:
            if symbol == symbol.lower():
                symbol = ""    
            self.db_cur.execute(ADD_SYMTOK, [symbol_id, symbol, chunk, sentence, pos_in_sen])
            self.db_con.commit()
        except sqlite3.IntegrityError as e:
            if not "UNIQUE constraint failed: Symbols.Symbol" in "{}".format(e):
                 print("***********************************************************************")
                 print(symbol_id, symbol, chunk, sentence, pos_in_sen)  
                 print("***********************************************************************")
                 raise e  
                 

        self.db_cur.row_factory = None
        self.db_cur.execute(GET_STO_ID, [chunk, sentence, pos_in_sen])
        symbol_tok = self.db_cur.fetchone()
        return symbol_tok

    def add_word(self, word):
        #print("word ------------------------------####", word)
        try:
            self.db_cur.execute(ADD_WORD, [word.lower()])
            self.db_con.commit()
        except sqlite3.IntegrityError as e:
            if not "UNIQUE constraint failed: Words.Word" in "{}".format(e):
                raise e

        self.db_cur.row_factory = lambda cursor, row: (row[0])
        self.db_cur.execute(GET_WORD_ID, [word.lower()])
        word_id = self.db_cur.fetchone()
        word = ""
        return word_id

    def add_word_token(self, word_id, word,  chunk, sentence, pos_start, pos_end):
        #print("pre: ",word)
        try:
            #print("try: ", word)
            if word == word.lower():
                word = ""
            self.db_cur.execute(ADD_WORTOK, [word_id, word,  chunk, sentence, pos_start, pos_end])
            self.db_con.commit()
        except sqlite3.IntegrityError as e:
            if not "UNIQUE constraint failed: Symbols.Symbol" in "{}".format(e):
                 raise e

        self.db_cur.row_factory = None
        self.db_cur.execute(GET_WTO_ID, [chunk, sentence, pos_start])
        symbol_tok = self.db_cur.fetchone()
        return symbol_tok


    def add_garbage(self, garbage, replace):
        try:
            self.db_cur.execute(ADD_GARBAGE, [garbage, replace])
            self.db_con.commit()
        except sqlite3.IntegrityError as e:
            if not "UNIQUE constraint failed: Cleaned.Garbage, Cleaned.Replace" in "{}".format(e):
                 raise e

        self.db_cur.row_factory = lambda cursor, row: (row[0])
        self.db_cur.execute(GET_GAR_ID, [garbage, replace] )
        garbage_id = self.db_cur.fetchone()
        return garbage_id

    def add_garbage_token(self, garbage_id, chunk, sentence, start, end):
        try:
            self.db_cur.execute(ADD_GARBTOK, [garbage_id, chunk, sentence, start, end])
            self.db_con.commit()
        except sqlite3.IntegrityError as e:
            if not "UNIQUE constraint failed: Symbols.Symbol" in "{}".format(e):
                 raise e

        self.db_cur.row_factory = None
        self.db_cur.execute(GET_GARBTOK, [chunk, sentence, start, end])
        garbage_tok = self.db_cur.fetchone()

        return garbage_tok

    def process_text(self):
        for chunk in self.chunk_reader:
            if chunk !="":      
                sentences, splitters = split_sentence(self.sentencebreak,chunk[1])
                if sentences:
                    sentences_lens = [len(x) for x in sentences]
                    normals = [normalize_txt(x, self.cleanpatt) for x in sentences]

                if splitters:
                    splitters_lens = [len(x) for x in splitters]
                

                for enum, sentence in enumerate(normals, start=0):
                    #print("sentence:::   ",sentence)
                    if enum < len(splitters):
                        gar_id = self.add_garbage(splitters[enum], "<IsSentenceBreak>")
                        gartok_id = self.add_garbage_token(gar_id, chunk[0], enum, sentences_lens[enum], splitters_lens[enum])
                    
                    word=""
                    
                    for symb_enum, symbol in enumerate(sentence[0]):
                        simbol = str(symbol)

                        if re.match(self.linebreak, symbol):
                            #print("linebreak",  "word = ", word)
                            gar_id = self.add_garbage(symbol, "<IsLineBreak>")
                            gartok_id = self.add_garbage_token(gar_id, chunk[0], enum, symb_enum, symb_enum+1)
                            if word != "":
                                word_id = self.add_word(word)
                                word_token = self.add_word_token(word_id, word, chunk[0], enum, symb_enum-len(word), symb_enum )
                            word = ""

                        #elif re.match(self.sentencebreak, symbol):
                        #    gar_id = self.add_garbage(symbol, "<IsSentenceBreak>")
                            #print("sentencebreak", "word = ", word)
                        #    gartok_id = self.add_garbage_token(gar_id, chunk[0], enum, symb_enum, symb_enum+1)
                        #    if word != "":
                        #        word_id = self.add_word(word)
                        #        word_token = self.add_word_token(word_id, word, chunk[0], enum, symb_enum-len(word), symb_enum )
                        #    word = "" 


                        elif re.match(self.wordbreak, symbol):
                            #print("wordbreak: ",  "word = ", word)
                            gar_id = self.add_garbage(symbol, "<IsWordBreak>")
                            gartok_id = self.add_garbage_token(gar_id, chunk[0], enum, symb_enum, symb_enum+1)
                            if word != "":
                                word_id = self.add_word(word)
                                word_token = self.add_word_token(word_id, word, chunk[0], enum, symb_enum-len(word), symb_enum )
                            word = ""

                        else:
                            #print("wordgrow ",  "word = ", word)
                            symbol_id = self.add_symbol(symbol)
                            symbol_tok = self.add_symbol_token(symbol_id,
                                                                  symbol,
                                                                  chunk[0],
                                                                  enum,
                                                                  symb_enum)
                            word += symbol

                            
                    if word != "":
                        #print("worddddd",  "word = ", word)
                        word_id = self.add_word(word)
                        word_token = self.add_word_token(word_id, word, chunk[0], enum, symb_enum-len(word), symb_enum )

                    for gar in sentence[1]:
                        gar_id = self.add_garbage(gar[1], gar[2])
                        gartok_id = self.add_garbage_token(gar_id, chunk[0], enum, gar[0][0], gar[0][1])

            self.db_cur.execute(UPD_FINIS)
            self.db_con.commit()


    def reconstruction_check(self, chunk_number, by="Symbols"):
        if by == "Symbols":
            self.db_cur.execute(GET_ALLSTO, [chunk_number])
            self.db_cur.row_factory = None
        else:
            self.db_cur.execute(GET_ALLWTO, [chunk_number])
            self.db_cur.row_factory = None
        chunk_elements= self.db_cur.fetchmany(1)
        #position_count = [chunk[2],chunk[3],chunk[4]]
        #pre_position_count = [chunk[2],chunk[3],chunk[4]]
        sentence = chunk_elements[0][3]
        old_sentence =  chunk_elements[0][3]
        reconstructed = [[]]*(sentence+1)
        
        while  chunk_elements:
            element = chunk_elements[0][0]
            if element == "":
                    element = chunk_elements[0][1]

            if old_sentence == sentence:
                if by == "Symbols":
                    reconstructed[sentence].append(element)
                else:
                    reconstructed[sentence] += list(element)
            else:
                reconstructed = reconstructed + ([[]] * (sentence+1-len(reconstructed)))
                if by == "Symbols":
                    reconstructed[sentence].append(element)
                else:
                    reconstructed[sentence] += list(element)

            old_sentence = chunk_elements[0][3]
            chunk_elements = self.db_cur.fetchmany(1)
            if chunk_elements:
                sentence = chunk_elements[0][3]
        print("Sin basura: ","".join([y for x in reconstructed for y in x]))
        #print(reconstructed[0])


        self.db_cur.execute(GET_ALLGAR, [chunk_number])
        self.db_cur.row_factory = None
        gar_sec = self.db_cur.fetchmany(1)
        sentence = gar_sec[0][2] 
        begin = gar_sec[0][3]  
        final = gar_sec[0][4]
        garbage = gar_sec[0][0]
        while gar_sec:
            sentence = gar_sec[0][2] 
            begin = gar_sec[0][3]  
            final = gar_sec[0][4]
            garbage = gar_sec[0][0]
            """if sentence == 0:
                print(sentence, garbage, begin, final)"""
            print("".join([y for x in reconstructed for y in x]))
            if sentence < len(reconstructed):
                for counter, g in enumerate(garbage, start=0):
                    reconstructed[sentence].insert(begin+counter, g)
            else:
                reconstructed = reconstructed + ([[]] * (sentence+1-len(reconstructed)))
                for counter, g in enumerate(garbage, start=0):
                    reconstructed[sentence].insert(begin+counter, g)
            gar_sec = self.db_cur.fetchmany(1)
        print("Con basura: ", "".join([y for x in reconstructed for y in x]))
        #print(reconstructed[0])
                
    def Disconnect(self):
        self.db_con.close()
