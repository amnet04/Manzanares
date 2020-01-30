"""Summary

Attributes:
    cretable_base (str): Query to create Thing table
    cretable_cpat (str): Query to create clean patterns table
    cretable_lang (str): Query to create lang table
    cretable_thcp (str): Query to create ThingsCleanPatterns table
    cretable_thil (str): Query to create ThingsCleanPatterns table 
    cretable_thty (str): Query to create TypThingtable
    table_dic (dict of str: tuple(int, str, str, ..)): Dict to check tables
    token_catalog (str): Query to create TokenCatalog table
    type_cataloge (str): Query to create TypeCatalog table
"""

table_dic = {"Things": [(0, 'ThigId', 'INTEGER', 1, None, 1),
                       (1, 'Name', 'TEXT', 1, None, 0),
                       (2, 'Description', 'TEXT', 1, None, 0),
                       (3, 'TFolder', 'TEXT', 1, None, 0), 
                       (4, 'TFile', 'TEXT', 1, None, 0), 
                       (5, 'Encoding', 'TEXT', 1, None, 0), 
                       (6, 'SBreak', 'TEXT', 0, None, 0), 
                       (7, 'LBreak', 'TEXT', 0, None, 0), 
                       (8, 'TokenCount', 'INTEGER', 0, None, 0), 
                       (9, 'TypeCount', 'INTEGER', 0, None, 0), 
                       (10, 'LastProcecedToken', 'INTEGER', 0, None, 0), 
                       (11, 'LastProcecedSentence', 'INTEGER', 0, None, 0), 
                       (12, 'LastProcecedLine', 'INTEGER', 0, None, 0), 
                       (13, 'TokensAre', 'TEXT', 1, None, 0), 
                       (14, 'Gap', 'TEXT', 1, None, 0),
                       (15, 'Finished', 'BOOL', 1, 'False', 0)],
             "Garbage": [(0, 'GarbageId', 'INTEGER', 1, None, 0), 
                         (1, 'Garbage', 'TEXT', 1, None, 0), 
                         (2, 'Replace', 'TEXT', 1, None, 0)],
             "GarbageTh": [(0, 'GarbageId', 'INTEGER', 1, None, 0), 
                          (1, 'ThingId', 'INTEGER', 1, None, 0), 
                          (2, 'Line', 'INTEGER', 1, None, 0), 
                          (3, 'Position', 'INTEGER', 1, None, 0)],
             "Langs": [(0, 'LId', 'INTEGER', 1, None, 1),
                       (1, 'Lang', 'TEXT', 1, None, 0)], 
             "ThingsLangs":[(0, 'ThingId', 'INTEGER', 1, None, 0), 
                            (1, 'LId', 'INTEGER', 1, None, 0)],
             "CleanPatterns":[(0, 'CPId', 'INTEGER', 1, None, 1), 
                              (1, 'Target', 'TEXT', 1, None, 0), 
                              (2, 'Replace', 'TEXT', 1, None, 0)],
             "ThingsCleanPatterns":[(0, 'ThingId', 'INTEGER', 1, None, 0),
                                    (1, 'CPId', 'INTEGER', 1, None, 0)],                 
             "TypeCatalogue":[(0, 'TypeId', 'INTEGER', 1, None, 1), 
                              (1, 'Type', 'TEXT', 1, None, 0)], 
             "TokenCatalog":[(0, 'TokThingId', 'INTEGER', 1, None, 1), 
                             (1, 'ThingId', 'INTEGER', 1, None, 0), 
                             (2, 'TypeId', 'INTEGER', 1, None, 0), 
                             (3, 'Form', 'TEXT', 0, None, 0), 
                             (4, 'Line', 'INTEGER', 1, None, 0), 
                             (5, 'Sentence', 'INTEGER', 1, None, 0), 
                             (6, 'SentenceEND', 'INTEGER', 1, None, 0), 
                             (7, 'InitialP', 'INTEGER', 1, None, 0), 
                             (8, 'FinalP', 'INTEGER', 1, None, 0)]
    }


"""
Base table
"""
cretable_base =  "CREATE TABLE IF NOT EXISTS Things ("
cretable_base += "ThigId INTEGER NOT NULL PRIMARY KEY, "
cretable_base += "Name TEXT NOT NULL, "
cretable_base += "Description TEXT NOT NULL, "
cretable_base += "TFolder TEXT NOT NULL, "
cretable_base += "TFile TEXT NOT NULL, "
cretable_base += "Encoding TEXT NOT NULL CHECK(Encoding IN ('ASCII', 'UTF-8')), "
cretable_base += "SBreak TEXT, "
cretable_base += "LBreak TEXT, "
cretable_base += "TokenCount INTEGER, "
cretable_base += "TypeCount INTEGER, "
cretable_base += "LastProcecedToken INTEGER, "
cretable_base += "LastProcecedSentence INTEGER, "
cretable_base += "LastProcecedLine INTEGER, "
cretable_base += "TokensAre TEXT NOT NULL CHECK(TokensAre IN ('symbols', 'words')), "
cretable_base += "Gap TEXT NOT NULL, "
cretable_base += "Finished BOOL NOT NULL DEFAULT False, " 
cretable_base += "CONSTRAINT unq UNIQUE (Name, TFolder, TFile, TokensAre, Gap))"

"""
Garbage table
"""
cretable_garb =  "CREATE TABLE IF NOT EXISTS Garbage("
cretable_garb += "GarbageId INTEGER NOT NULL, "
cretable_garb += "Garbage TEXT NOT NULL, "
cretable_garb += "Replace TEXT NOT NULL, "
cretable_garb += "CONSTRAINT unq UNIQUE (Garbage, Replace))"

"""
Garbage/thing table
"""
cretable_gart =  "CREATE TABLE IF NOT EXISTS GarbageTh("
cretable_gart += "GarbageId INTEGER NOT NULL, "
cretable_gart += "ThingId INTEGER NOT NULL, "
cretable_gart += "Line INTEGER NOT NULL, "
cretable_gart += "Position INTEGER NOT NULL, "
cretable_gart += "FOREIGN KEY(ThingId)  REFERENCES Things(ThingId), "
cretable_gart += "FOREIGN KEY(GarbageId)  REFERENCES Garbage(GarbageId), "
cretable_gart += "CONSTRAINT unq UNIQUE (ThingId, Line, Position))"

"""
Lang tables
"""
cretable_lang =  "CREATE TABLE IF NOT EXISTS Langs ("
cretable_lang += "LId INTEGER NOT NULL PRIMARY KEY, "
cretable_lang += "Lang TEXT NOT NULL UNIQUE)" 

cretable_thil =  "CREATE TABLE IF NOT EXISTS ThingsLangs ("
cretable_thil += "ThingId INTEGER NOT NULL, "
cretable_thil += "LId INTEGER NOT NULL, "
cretable_thil += "FOREIGN KEY(LId)  REFERENCES Langs(LId), "
cretable_thil += "FOREIGN KEY(ThingId)  REFERENCES Things(ThingId), "
cretable_thil += "CONSTRAINT unq UNIQUE (ThingId, LId))"

"""
Clean patterns
"""
cretable_cpat =  "CREATE TABLE IF NOT EXISTS CleanPatterns ("
cretable_cpat += "CPId INTEGER NOT NULL PRIMARY KEY, "
cretable_cpat += "Target TEXT NOT NULL, "
cretable_cpat += "Replace TEXT NOT NULL, "
cretable_cpat += "CONSTRAINT unq UNIQUE (Target, Replace))"

cretable_thcp =  "CREATE TABLE IF NOT EXISTS ThingsCleanPatterns ("
cretable_thcp += "ThingId INTEGER NOT NULL, "
cretable_thcp += "CPId INTEGER NOT NULL, "
cretable_thcp += "FOREIGN KEY(CPId)  REFERENCES ClearPatterns(CPId), "
cretable_thcp += "FOREIGN KEY(ThingId)  REFERENCES Things(ThingId), "
cretable_thcp += "CONSTRAINT unq UNIQUE (ThingId, CPId))"

"""
Type Catalogue
"""
type_cataloge =  "CREATE TABLE IF NOT EXISTS TypeCatalogue("
type_cataloge += "TypeId INTEGER NOT NULL PRIMARY KEY, "
type_cataloge += "Type TEXT NOT NULL UNIQUE )"

"""
Token Catalogue
"""
token_catalog =  "CREATE TABLE IF NOT EXISTS TokenCatalog("
token_catalog += "TokThingId  INTEGER NOT NULL PRIMARY KEY, "
token_catalog += "ThingId  INTEGER NOT NULL, "
token_catalog += "TypeId  INTEGER NOT NULL, "
token_catalog += "Form TEXT,"
token_catalog += "Line INTEGER NOT NULL, "
token_catalog += "Sentence INTEGER NOT NULL,"
token_catalog += "SentenceEND INTEGER NOT NULL CHECK(SentenceEND IN (0, 1)),"
token_catalog += "InitialP INTEGER NOT NULL, "
token_catalog += "FinalP INTEGER NOT NULL, "
token_catalog += "FOREIGN KEY(ThingId)  REFERENCES Thing(ThingId),"
token_catalog += "FOREIGN KEY(TypeId)  REFERENCES TypeCatalogue(TypeId), "
token_catalog += "CONSTRAINT unq UNIQUE (ThingId, Line, InitialP))"

"""
ADDTHINGS
"""
ADD_THING = ''' INSERT INTO Things(Name,
                Description,
                TFolder,
                TFile,
                Encoding,
                SBreak,
                LBreak,
                TokensAre,
                Gap
                )
                VALUES(?,?,?,?,?,?,?,?,?) '''

CHK_THING = ''' SELECT  *
                FROM Things
                WHERE Name=? 
                AND TFolder=? 
                AND TFile=?
                AND TokensAre=? 
                AND Gap =?
                '''

ADD_CPATR = ''' INSERT INTO CleanPatterns(Target, Replace)
                VALUES(?,?) '''

ADD_CPATT = ''' INSERT INTO ThingsCleanPatterns(ThingId, CPId)
                VALUES(?,?) '''

ADD_LANGU = ''' INSERT INTO Langs(Lang)
                VALUES(?) '''

ADD_LANGT = ''' INSERT INTO ThingsLangs(ThingId, LId)
                VALUES(?,?) '''                 

CHK_CPATR = ''' SELECT  * 
                FROM CleanPatterns
                WHERE Target=? AND Replace=? '''

CHK_CPATT = ''' SELECT  *
                FROM ThingsCleanPatterns
                WHERE  ThingId=? AND CPId=? '''

CHK_LANGU = ''' SELECT  *
                FROM Langs
                WHERE Lang=? '''

CHK_LANGT = ''' SELECT  *
                FROM ThingsLangs
                WHERE ThingId=? AND  LId=?'''  

"""
Garbage
"""
CHK_GARB = ''' SELECT *
               FROM Garbage
               WHERE Garbage=? AND Replace =?'''

ADD_GARB = ''' INSERT INTO Garbage(Garbage, Replace)
               VALUES(?,?) '''

"""
Gatbage/Thing
"""
CHK_GARB = ''' SELECT *
               FROM GarbageTh
               WHERE ThingId=? AND Line=?  AND Position=?'''

ADD_GARB = ''' INSERT INTO Garbage(GarbageId, ThingId, Line, Position)
               VALUES(?,?,?,?) '''



"""
TypeCatalogue
"""
CHK_TYPE = ''' SELECT *
               FROM TypeCatalogue
               WHERE Type=? '''

ADD_TYPE = ''' INSERT INTO TypeCatalogue(Type)
               VALUES(?) '''

"""
TokenCatalogue
"""
CHK_TOKE = ''' SELECT *
               FROM TokenCatalog
               WHERE ThingId=? AND Line=?  AND InitialP=?'''

ADD_TOKE = ''' INSERT INTO  TokenCatalog(ThingId, TypeId, Form, Line, InitialP, FinalP)
               VALUES(?,?,?,?,?) '''


"""
Get thing properties
"""
GET_CPATT = """ SELECT *
                FROM CleanPatterns
                INNER JOIN B on B.f = A.f;"""