from os import path, mkdir
import shutil
import sys
import pytest

sys.path.append(path.join(path.dirname(__file__), '../..'))
from manzanares.thing.thing import thing

def test_master_block(tmpdir_factory):
    print("\n\n")
    tmp_folder = tmpdir_factory.mktemp("data")
    thing1 = thing('Name', 'Description', 'manzanares/test', 'chinese.txt', 'UTF-8', r'([\.])', '[\n+]',
                    r'[\s+]', ['L1','L2'], [(r"[\!\¡\¿\?\,]","")],
                   db_folder=tmp_folder)
    thing1.Disconnect()
    thing2 = thing('Name', 'Description', 'manzanares/test', 'chinese.txt', 'UTF-8', r'([\.])', '[\n+]',
                    r'[\s+]', ['L2','L1'], [(r"[\!\¡\¿\?\,]","")],
                   db_folder=tmp_folder)
    thing2.Disconnect()
    thing3 = thing('Name', db_folder=tmp_folder)
    thing3.Disconnect()
