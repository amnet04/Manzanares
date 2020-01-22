from os import path, mkdir
import shutil
import sys
import pytest

sys.path.append(path.join(path.dirname(__file__), '../..'))
from manzanares.thing.thing_corp import thing_corp



def test_thing_corp_db(tmpdir_factory):
    tmp_folder = tmpdir_factory.mktemp("data")
    dbfile = "{}/{}.sqlite".format(tmp_folder,"prv")
    print(dbfile)
    tc1 = thing_corp(name="prv", db_folder=tmp_folder)
    assert path.isfile(dbfile), "Test passed, database file created"
    tc1.CheckDbStruc()
    tc1.AddThing( "name", 
                 "description", 
                 "./", 
                 "quevedoprv.txt",
                 "utf-8",
                 r"[\.\n]",
                 "\n",
                 "tokensare",
                 "gap",
                 [("\n{1,}","\n"),(r"[\!\¡\,]","")])
    tc1.Disconnect()
    tc2 = thing_corp(name="prv", db_folder=tmp_folder)
    tc2.AddThing( "name", 
                 "description", 
                 "./", 
                 "quevedoprv.txt",
                 "utf-8",
                 r"[\.\n]",
                 "\n",
                 "tokensare",
                 "gap",
                 [("\n{1,}","\n"),(r"[\!\¡\,]","")])
    tc2.Disconnect()

