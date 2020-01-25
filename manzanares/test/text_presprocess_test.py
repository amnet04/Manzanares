from os import path, mkdir
import shutil
import sys
import pytest

sys.path.append(path.join(path.dirname(__file__), '../..'))
from manzanares.text_preproc.chunkreader import ChunkReader

def test_chunk():
    for chunk in ChunkReader("manzanares/test/quevedoprv.txt",end="\s"):
        print("<-{}->".format(chunk))
    