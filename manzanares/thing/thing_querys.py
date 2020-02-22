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
CRE_MASTER += "WordBreak TEXT, "
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
ADD_MASTER += "WordBreak, TokenCount, TypeCount, LastProcecedToken, LastProcecedSentence, "
ADD_MASTER += "LastProcecedLine)"
ADD_MASTER += "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

"""
Test Insert into Master (Only for test)
"""
INS_MASTER =  "INSERT INTO MASTER("
INS_MASTER += "Name, Description, TFolder, TFile, Encoding, SentenceBreak, LineBreak, WordBreak,"
INS_MASTER += "TokenCount, TypeCount, LastProcecedToken, LastProcecedSentence, "
INS_MASTER += "LastProcecedLine,  Finished )"
INS_MASTER += "VALUES('Name', 'Description', 'TFolder', 'TFile', 'UTF-8', 'SentenceBreak', 'LineBreak',"
INS_MASTER += "'WordBreak', 'TokenCount', 'TypeCount', 'LastProcecedToken', 'LastProcecedSentence', "
INS_MASTER += "'LastProcecedLine', 0)"

"""
Master table Updates
"""
UPD_TOKCO = "UPDATE MASTER SET TokenCount = ? WHERE ID = 1"

UPD_TYPCO = "UPDATE MASTER SET TypeCount = ? WHERE ID = 1"

UPD_LPTOK = "UPDATE MASTER SET LastProcecedToken = ? WHERE ID = 1"

UPD_LPSEN = "UPDATE MASTER SET LastProcecedSentence  = ? WHERE ID = 1"

UPD_LPLIN = "UPDATE MASTER SET LastProcecedLine  = ? WHERE ID = 1"

UPD_FINIS = "UPDATE MASTER SET Finished = 1 WHERE ID = 1"




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
ADD_SYMBOL = "INSERT INTO Symbols(Symbol) VALUES(?)"


"""
******************************************* Symbols Token  Catalogue  *******************************
"""
CRE_SYMTOK =  "CREATE TABLE IF NOT EXISTS SymbolTokens("
CRE_SYMTOK += "SymId INTEGER NOT NULL, "
CRE_SYMTOK += "Form TEXT NOT NULL, "
CRE_SYMTOK += "Chunk INTEGER NOT NULL, "
CRE_SYMTOK += "Sentence INTEGER NOT NULL, "
CRE_SYMTOK += "SentencePos INTEGER NOT NULL, "
CRE_SYMTOK += "CONSTRAINT unq UNIQUE (Chunk, Sentence, SentencePos),"
CRE_SYMTOK += "FOREIGN KEY(SymId)  REFERENCES Symbols(Id))"

"""
Get content of  Symbol Table
"""
GET_ALLSTO = "SELECT * FROM SymbolTokens"

"""
Get symbol id
"""
GET_STO_ID =  "SELECT * FROM SymbolTokens WHERE "
GET_STO_ID += "Chunk=? AND Sentence=? AND SentencePos=?"

"""
Get all forms
"""
GET_ALL_SF =  "SELECT * FROM SymbolTokens WHERE "
GET_ALL_SF += "SymId = ?"

"""
Get all of one form
"""
GET_SF =  "SELECT * FROM SymbolTokens WHERE "
GET_SF += "Form = ?"


"""
ADD symbol
"""
ADD_SYMTOK = "INSERT INTO SymbolTokens(SymId, Form, Chunk, Sentence, SentencePos) VALUES(?,?,?,?,?)"



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
ADD_WORD = "INSERT INTO Words(Word) VALUES(?)"



"""
******************************************* Word Token  Catalogue  *******************************
"""
CRE_WORTOK =  "CREATE TABLE IF NOT EXISTS WordTokens("
CRE_WORTOK += "WordId INTEGER NOT NULL, "
CRE_WORTOK += "Form TEXT NOT NULL, "
CRE_WORTOK += "Chunk INTEGER NOT NULL, "
CRE_WORTOK += "Sentence INTEGER NOT NULL, "
CRE_WORTOK += "SentenceposStart INTEGER NOT NULL, "
CRE_WORTOK += "SentenceposEnd INTEGER NOT NULL, "
CRE_WORTOK += "CONSTRAINT unq UNIQUE (Chunk, Sentence, SentencePosStart, SentenceposEnd),"
CRE_WORTOK += "FOREIGN KEY(WordId)  REFERENCES Word(Id))"

"""
Get content of  Symbol Table
"""
GET_ALLWTO = "SELECT * FROM WordTokens"

"""
Get symbol id
"""
GET_WTO_ID =  "SELECT * FROM WordTokens WHERE "
GET_WTO_ID += "Chunk=? AND Sentence=? AND SentencePosStart=?"

"""
Get all forms
"""
GET_ALL_WF =  "SELECT * FROM WordTokens WHERE "
GET_ALL_WF += "SymId = ?"

"""
Get all of one form
"""
GET_WF =  "SELECT * FROM WordTokens WHERE "
GET_WF += "Form = ?"


"""
ADD symbol
"""
ADD_WORTOK = "INSERT INTO WordTokens(WordId, Form, Chunk, Sentence, SentencePosStart, SentenceposEnd) VALUES(?,?,?,?,?,?)"




"""
******************************************* Cleaned table  *******************************
"""
CRE_GARBAGE =  "CREATE TABLE IF NOT EXISTS Cleaned("
CRE_GARBAGE += "Id INTEGER PRIMARY KEY, "
CRE_GARBAGE += "Garbage TEXT NOT NULL, "
CRE_GARBAGE += "Replace TEXT NOT NULL, "
CRE_GARBAGE += "CONSTRAINT unq UNIQUE (Garbage, Replace))"

"""
Get content of  garbage Table
"""
GET_GARBAGE = "SELECT * FROM Cleaned"

"""
Get garbage id
"""
GET_GAR_ID = "SELECT Id FROM Cleaned WHERE Garbage=? AND Replace=?"

"""
ADD garbage
"""
ADD_GARBAGE = "INSERT INTO Cleaned(Garbage, Replace) VALUES(?,?)"


"""
******************************************* Cleaned Token table  *******************************
"""
CRE_GARBTOK =  "CREATE TABLE IF NOT EXISTS CleanTokens("
CRE_GARBTOK += "GarId INTEGER NOT NULL, "
CRE_GARBTOK += "Chunk INTEGER NOT NULL, "
CRE_GARBTOK += "Sentence INTEGER NOT NULL,"
CRE_GARBTOK += "Start INTEGER NOT NULL, "
CRE_GARBTOK += "End INTEGER NOT NULL, "
CRE_GARBTOK += "FOREIGN KEY(GarId)  REFERENCES Cleaned(Id),"
CRE_GARBTOK += "CONSTRAINT unq UNIQUE (GarId, Chunk,Sentence,Start,End))"


"""
Get content of garbage table
"""
GET_GARBTOK = "SELECT * FROM CleanTokens WHERE Chunk=? AND Sentence=? And Start=? And End=?"

"""
ADD garbage
"""
ADD_GARBTOK = "INSERT INTO  CleanTokens(GarId, Chunk, Sentence, Start, End) VALUES(?,?,?,?,?)"
