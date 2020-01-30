"""
******************************************* Database  check  *******************************
"""
CHK_ALLTBL = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"


"""
******************************************* Master table  *******************************
"""


"""
Create Master Table
"""
CRE_MASTER =  "CREATE TABLE IF NOT EXISTS MASTER("
CRE_MASTER += "Id INTEGER PRIMARY KEY CHECK (Id = 1),"
CRE_MASTER += "Name TEXT NOT NULL, "
CRE_MASTER += "Description TEXT NOT NULL, "
CRE_MASTER += "TFolder TEXT NOT NULL, "
CRE_MASTER += "TFile TEXT NOT NULL, "
CRE_MASTER += "Encoding TEXT NOT NULL CHECK(Encoding IN ('ASCII', 'UTF-8')), "
CRE_MASTER += "SentenceBreak TEXT, "
CRE_MASTER += "LineBreak TEXT, "
CRE_MASTER += "TokenCount INTEGER NOT NULL, "
CRE_MASTER += "TypeCount INTEGER NOT NULL,"
CRE_MASTER += "LastProcecedToken INTEGER NOT NULL, "
CRE_MASTER += "LastProcecedSentence INTEGER NOT NULL, "
CRE_MASTER += "LastProcecedLine INTEGER NOT NULL, "
CRE_MASTER += "Finished INTEGER NOT NULL DEFAULT 0 CHECK(Finished IN (1, 0)) )"


"""
Get content of Master Table
"""
GET_MASTER = "SELECT * FROM MASTER"


"""
Add Master Row
"""
ADD_MASTER =  "INSERT INTO MASTER("
ADD_MASTER += "Name, Description, TFolder, TFile, Encoding, SentenceBreak, LineBreak,"
ADD_MASTER += "TokenCount, TypeCount, LastProcecedToken, LastProcecedSentence, "
ADD_MASTER += "LastProcecedLine)"
ADD_MASTER += "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

"""
Test Insert into Master (Only for test)
"""
INS_MASTER =  "INSERT INTO MASTER("
INS_MASTER += "Name, Description, TFolder, TFile, Encoding, SentenceBreak, LineBreak,"
INS_MASTER += "TokenCount, TypeCount, LastProcecedToken, LastProcecedSentence, "
INS_MASTER += "LastProcecedLine,  Finished )"
INS_MASTER += "VALUES('Name', 'Description', 'TFolder', 'TFile', 'UTF-8', 'SentenceBreak', 'LineBreak',"
INS_MASTER += "'TokenCount', 'TypeCount', 'LastProcecedToken', 'LastProcecedSentence', "
INS_MASTER += "'LastProcecedLine', 'True')"

"""
Master table Updates 
"""
UPD_TOKCO = "UPDATE MASTER SET TokenCount = ? WHERE ID = 1"

UPD_TYPCO = "UPDATE MASTER SET TypeCount = ? WHERE ID = 1"

UPD_LPTOK = "UPDATE MASTER SET LastProcecedToken = ? WHERE ID = 1"

UPD_LPSEN = "UPDATE MASTER SET LastProcecedSentence  = ? WHERE ID = 1"

UPD_LPLIN = "UPDATE MASTER SET LastProcecedLine  = ? WHERE ID = 1"

UPD_FINIS = "UPDATE MASTER SET Finished = True WHERE ID = 1"




"""
******************************************* Lang Table  *******************************
"""
CRE_LANGU =  "CREATE TABLE IF NOT EXISTS Langs ("
CRE_LANGU += "Lang TEXT NOT NULL PRIMARY KEY)" 

"""
Get content of Lang Table
"""
GET_LANGS = "SELECT * FROM Langs"

"""
ADD Language
"""
ADD_LANGU = "INSERT INTO Langs(Lang) VALUES(?)"




"""
******************************************* Clean Patterns Table  *******************************
"""
CRE_CLEPT =  "CREATE TABLE IF NOT EXISTS CleanPatterns ("
CRE_CLEPT += "Target TEXT NOT NULL PRIMARY KEY,"
CRE_CLEPT += "Replace TEXT NOT NULL) "

"""
Get content of  CleanPatterns Table
"""
GET_CLEPT = "SELECT * FROM CleanPatterns"

"""
ADD CleanPatterns
"""
ADD_CLEPT = "INSERT INTO CleanPatterns(Target,Replace) VALUES(?, ?)"



"""
******************************************* Symbols Catalogue  *******************************
"""
CRE_SYMBOL =  "CREATE TABLE IF NOT EXISTS Symbols("
CRE_SYMBOL += "Id INTEGER NOT NULL PRIMARY KEY, "
CRE_SYMBOL += "Symbol TEXT NOT NULL UNIQUE )"

"""
Get content of  Symbol Table
"""
GET_ALLSYM = "SELECT * FROM Symbols"

"""
Get symbol id
"""
GET_SYM_ID = "SELECT * FROM Symbols WHERE Symbol=?"

"""
ADD symbol
"""
ADD_SYMBOL = "INSERT INTO Symbols(Symbols) VALUES(?)"



"""
******************************************* Words Catalogue  *******************************
"""
CRE_WORDS =  "CREATE TABLE IF NOT EXISTS Words("
CRE_WORDS += "Id INTEGER NOT NULL PRIMARY KEY, "
CRE_WORDS += "Word TEXT NOT NULL UNIQUE )"

"""
Get content of  Words Table
"""
GET_WORDS = "SELECT * FROM Words"

"""
Get symbol id
"""
GET_WORD_ID = "SELECT Id FROM Words WHERE Word=?"

"""
ADD symbol
"""
ADD_WORD = "INSERT INTO Words(Words) VALUES(?)"



"""
******************************************* Cleaned table  *******************************
"""
CRE_GARBAGE =  "CREATE TABLE IF NOT EXISTS Cleaned("
CRE_GARBAGE += "Id INTEGER NOT NULL, "
CRE_GARBAGE += "Garbage TEXT NOT NULL, "
CRE_GARBAGE += "Replace TEXT NOT NULL, "
CRE_GARBAGE += "CONSTRAINT unq UNIQUE (Garbage, Replace))"

"""
Get content of  Words Table
"""
GET_GARBAGE = "SELECT * FROM Cleaned"

"""
Get symbol id
"""
GET_GAR_ID = "SELECT Id FROM Cleaned WHERE Garbage=? AND Replace=?"

"""
ADD symbol
"""
ADD_GARBAGE = "INSERT INTO Cleaned(Garbage, Replace) VALUES(?, ?)"