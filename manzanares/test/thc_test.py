from os import path, mkdir
import shutil
import sys
import pytest
import timeit

sys.path.append(path.join(path.dirname(__file__), '../..'))
from manzanares.thing.thing import thing

def test_master_block(tmpdir_factory):
    print("\n\n")
    tmp_folder = tmpdir_factory.mktemp("data")

    starttime = timeit.default_timer()

    thing1 = thing('Name', 'Description', 'manzanares/test', 'lorem.txt', 'UTF-8', r'(?:[.¿?¿!\"]+)(?=(?:\s*[A-Z])|$|(?:"\.)|(?:\s+\n+))', '[\n+]',
                    r'[\s+]', ['L1','L2'], [(r"[\!\¡\¿\?\,]","")],
                   db_folder=tmp_folder)
    print("*** ---> Object creation:\t{}".format(timeit.default_timer() - starttime))

    starttime = timeit.default_timer()
    thing1.process_text()
    print("*** ---> Processing_text:\t{}".format(timeit.default_timer() - starttime))
    
    thing1.Disconnect()

    """starttime = timeit.default_timer()
    thing2 = thing('Name', 'Description', 'manzanares/test', 'lorem.txt', 'UTF-8', r'([\.])', '[\n+]',
                    r'[\s+]', ['L2','L1'], [(r"[\!\¡\¿\?\,]","")],
                   db_folder=tmp_folder)
    print("*** ---> Reopen Objetc 1 time :\t{}".format(timeit.default_timer() - starttime))

    thing2.Disconnect()"""

    starttime = timeit.default_timer()
    thing3 = thing('Name', db_folder="/tmp/pytest-of-carlos/stable/data0")
    print("*** ---> Reopen Objetc 2 time :\t{}".format(timeit.default_timer() - starttime))

    starttime = timeit.default_timer()
    thing3.reconstruction_check(1)
    print("*** ---> Reconstruction by symbols :\t{}".format(timeit.default_timer() - starttime))

    starttime = timeit.default_timer()
    thing3.reconstruction_check(1, by="Word")
    print("*** ---> Reconstruction by words :\t{}".format(timeit.default_timer() - starttime))
    #thing3.reconstruction_check(1, by="Words")
    thing3.Disconnect()
