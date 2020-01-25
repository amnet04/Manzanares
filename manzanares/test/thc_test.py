from os import path, mkdir
import shutil
import sys
import pytest

sys.path.append(path.join(path.dirname(__file__), '../..'))
from manzanares.thing.thing_corp import thing_corp



def test_thing_samething(tmpdir_factory):
    tmp_folder = tmpdir_factory.mktemp("data")
    dbfile = "{}/{}.sqlite".format(tmp_folder,"prv")
    tc1 = thing_corp(name="prv", db_folder=tmp_folder)
    assert path.isfile(dbfile), "Test passed, database file created"
    tc1.CheckDbStruc()
    tc1.AddThing( "name", 
                 "description", 
                 "./", 
                 "quevedoprv.txt",
                 "UTF-8",
                 r"[\.\n]",
                 r"\n",
                 "symbols",
                 "gap",
                 ["Lang1", "Lang2", "L3"],
                 [(r"\n{1,}",r"\n"),(r"[\!\¡\,]","")])
    tc1.Disconnect()
    tc2 = thing_corp(name="prv", db_folder=tmp_folder)
    tc2.AddThing( "name", 
                 "description", 
                 "./", 
                 "quevedoprv.txt",
                 "UTF-8",
                 r"[\.\n]",
                 r"\n",
                 "symbols",
                 "gap",
                 ["Lang1", "Lang2", "L3"],
                 [(r"\n{1,}",r"\n"),(r"[\!\¡\,]","")])
    tc2.Disconnect()


def test_otherthing(tmpdir_factory):
    tmp_folder = tmpdir_factory.mktemp("data")
    dbfile = "{}/{}.sqlite".format(tmp_folder,"prv")
    tc1 = thing_corp(name="prv", db_folder=tmp_folder)
    assert path.isfile(dbfile), "Test passed, database file created"
    tc1.CheckDbStruc()
    tc1.AddThing( "name", 
                 "description", 
                 "./", 
                 "quevedoprv.txt",
                 "UTF-8",
                 r"[\.\n]",
                 r"\n",
                 "symbols",
                 "gap",
                 ["Lang1", "Lang2", "L3"],
                 [(r"\n{1,}",r"\n"),(r"[\!\¡\,]","")])
    tc1.Disconnect()

    tc2 = thing_corp(name="prv", db_folder=tmp_folder)
    tc2.AddThing( "name2", 
                 "description", 
                 "./", 
                 "quevedoprv.txt",
                 "UTF-8",
                 r"[\.\n]",
                 r"\n",
                 "symbols",
                 "gap",
                 ["Lang1", "Lang2", "L3"],
                 [(r"\n{1,}",r"\n")])
    tc2.Disconnect()

    tc3 = thing_corp(name="prv", db_folder=tmp_folder)
    tc3.AddThing( "name3", 
                 "description", 
                 "./", 
                 "quevedoprvp.txt",
                 "UTF-8",
                 r"[\.\n]",
                 r"\n",
                 "symbols",
                 "gap",
                 ["L3", "L4"],
                 [(r"\n{2,}",r"\n{1}"),(r"[\!\¡\,]","\n")])
    tc3.Disconnect()