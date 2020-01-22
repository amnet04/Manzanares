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

table_dic = {"Thing": [(0, 'ThigId', 'INTEGER', 1, None, 1),
                       (1, 'Name', 'TEXT', 1, None, 0),
                       (2, 'Description', 'TEXT', 1, None, 0),
                       (3, 'TFolder', 'TEXT', 1, None, 0), 
                       (4, 'TFile', 'TEXT', 1, None, 0), 
                       (5, 'Encoding', 'TEXT', 1, "'UTF-8'", 0), 
                       (6, 'SBreak', 'TEXT', 0, None, 0), 
                       (7, 'LBreak', 'TEXT', 0, None, 0), 
                       (8, 'TokenCount', 'INTEGER', 0, None, 0), 
                       (9, 'TypeCount', 'INTEGER', 0, None, 0), 
                       (10, 'LastProcecedToken', 'INTEGER', 0, None, 0), 
                       (11, 'LastProcecedSentence', 'INTEGER', 0, None, 0), 
                       (12, 'LastProcecedLine', 'INTEGER', 0, None, 0), 
                       (13, 'TokensAre', 'TEXT', 0, None, 0), 
                       (14, 'Gap', 'TEXT', 1, None, 0),
                       (15, 'Finished', 'BOOL', 1, 'False', 0)],
             "Langs": [(0, 'LId', 'INTEGER', 1, None, 1),
                       (1, 'Lang', 'TEXT', 1, None, 0)], 
             "ThingsLangs":[(0, 'TLId', 'INTEGER', 1, None, 1), 
                            (1, 'ThingId', 'INTEGER', 1, None, 0), 
                            (2, 'LId', 'INTEGER', 1, None, 0)],
             "CleanPatterns":[(0, 'CPId', 'INTEGER', 1, None, 1), 
                              (1, 'Target', 'TEXT', 1, None, 0), 
                              (2, 'Replace', 'TEXT', 1, None, 0)],
             "ThingsCleanPatterns":[(0, 'CPId', 'INTEGER', 1, None, 1), 
                                    (1, 'ThingId', 'INTEGER', 1, None, 0)],                 
             "TypeCatalogue":[(0, 'TypeID', 'INTEGER', 1, None, 1), 
                              (1, 'Type', 'TEXT', 1, None, 0), 
                              (2, 'Length', 'INTEGER', 1, None, 0)],
             "TypThing": [(0, 'TypThingId', 'INTEGER', 1, None, 1), 
                          (1, 'ThingId', 'INTEGER', 1, None, 0), 
                          (2, 'TypeId', 'INTEGER', 1, None, 0), 
                          (3, 'Count', 'INTEGER', 1, None, 0)],
             "TokenCatalog":[(0, 'TokThingId', 'INTEGER', 1, None, 1), 
                             (1, 'TypThingId', 'INTEGER', 1, None, 0), 
                             (2, 'Sentence', 'INTEGER', 1, None, 0), 
                             (3, 'PositionInSentence', 'INTEGER', 1, None, 0), 
                             (4, 'SymbolBefore', 'TEXT', 0, None, 0), 
                             (5, 'SymbolAfter', 'TEXT', 0, None, 0), 
                             (6, 'Position', 'INTEGER', 1, None, 0)]
    }


"""
Base table
"""
cretable_base =  "CREATE TABLE IF NOT EXISTS Thing ("
cretable_base += "ThigId INTEGER NOT NULL PRIMARY KEY, "
cretable_base += "Name TEXT NOT NULL, "
cretable_base += "Description TEXT NOT NULL, "
cretable_base += "TFolder TEXT NOT NULL, "
cretable_base += "TFile TEXT NOT NULL, "
cretable_base += "Encoding TEXT NOT NULL DEFAULT 'UTF-8', "
cretable_base += "SBreak TEXT, "
cretable_base += "LBreak TEXT, "
cretable_base += "TokenCount INTEGER, "
cretable_base += "TypeCount INTEGER, "
cretable_base += "LastProcecedToken INTEGER, "
cretable_base += "LastProcecedSentence INTEGER, "
cretable_base += "LastProcecedLine INTEGER, "
cretable_base += "TokensAre TEXT, "
cretable_base += "Gap TEXT NOT NULL, "
cretable_base += "Finished BOOL NOT NULL DEFAULT False, " 
cretable_base += "CONSTRAINT unq UNIQUE (Name, TFolder, TFile, TokensAre, Gap))"

"""
Lang tables
"""
cretable_lang =  "CREATE TABLE IF NOT EXISTS Langs ("
cretable_lang += "LId INTEGER NOT NULL PRIMARY KEY, "
cretable_lang += "Lang TEXT NOT NULL UNIQUE)" 

cretable_thil =  "CREATE TABLE IF NOT EXISTS ThingsLangs ("
cretable_thil += "TLId INTEGER NOT NULL PRIMARY KEY, "
cretable_thil += "ThingId INTEGER NOT NULL, "
cretable_thil += "LId INTEGER NOT NULL, "
cretable_thil += "FOREIGN KEY(LId)  REFERENCES Langs(LId), "
cretable_thil += "FOREIGN KEY(ThingId)  REFERENCES ThingId(ThingId), "
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
cretable_thcp += "CPId INTEGER NOT NULL PRIMARY KEY, "
cretable_thcp += "ThingId INTEGER NOT NULL, "
cretable_thcp += "FOREIGN KEY(CPId)  REFERENCES ClearPatterns(CPId), "
cretable_thcp += "FOREIGN KEY(ThingId)  REFERENCES ThingId(ThingId), "
cretable_thcp += "CONSTRAINT unq UNIQUE (ThingId, CPId))"

"""
Type Catalogue
"""
type_cataloge =  "CREATE TABLE IF NOT EXISTS TypeCatalogue("
type_cataloge += "TypeID INTEGER NOT NULL PRIMARY KEY, "
type_cataloge += "Type TEXT NOT NULL UNIQUE, "
type_cataloge += "Length INTEGER NOT NULL)"

cretable_thty =  "CREATE TABLE IF NOT EXISTS  TypThing("
cretable_thty += "TypThingId  INTEGER NOT NULL PRIMARY KEY, "
cretable_thty += "ThingId INTEGER NOT NULL, "
cretable_thty += "TypeId INTEGER NOT NULL, "
cretable_thty += "Count INTEGER NOT NULL, "
cretable_thty += "FOREIGN KEY(TypeId)  REFERENCES TypeCatalogue(TypeId), "
cretable_thty += "FOREIGN KEY(ThingId)  REFERENCES ThingId(ThingId), "
cretable_thty += "CONSTRAINT unq UNIQUE (ThingId, TypeId))"

"""
Token Catalogue
"""
token_catalog =  "CREATE TABLE IF NOT EXISTS TokenCatalog("
token_catalog += "TokThingId  INTEGER NOT NULL PRIMARY KEY, "
token_catalog += "TypThingId  INTEGER NOT NULL, "
token_catalog += "Sentence INTEGER NOT NULL, "
token_catalog += "PositionInSentence INTEGER NOT NULL,"
token_catalog += "SymbolBefore TEXT,  "
token_catalog += "SymbolAfter TEXT,  "
token_catalog += "Position  INTEGER NOT NULL, "
token_catalog += "FOREIGN KEY(TypThingId)  REFERENCES TypThing(TypThingId))"

"""
ADDTHIGS
"""
ADD_THING = ''' INSERT INTO Thing(Name,
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
                FROM Thing
                WHERE Name=? 
                AND TFolder=? 
                AND TFile=?
                AND TokensAre=? 
                AND Gap =?
                '''

ADD_CPATT = ''' INSERT INTO CleanPatterns(Target, Replace)
                VALUES(?,?) '''

ADD_CPATR = ''' INSERT INTO ThingsCleanPatterns(CPId, ThingId)
                VALUES(?,?) '''

CHK_CPATT = ''' SELECT  CPId, Target, Replace 
                FROM CleanPatterns
                WHERE Target=? AND Replace=? '''

CHK_CPATR = ''' SELECT  CPId, ThingId 
                FROM ThingsCleanPatterns
                WHERE CPId=? AND ThingId=? ''' 