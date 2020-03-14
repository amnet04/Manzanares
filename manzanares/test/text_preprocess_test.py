from os import path, mkdir
import shutil
import sys
import pytest

sys.path.append(path.join(path.dirname(__file__), '../..'))
from manzanares.text_preproc.chunkreader import ChunkReader
from manzanares.text_preproc.text_preprocess import normalize_txt, split_sentence

def test_chunk():
    for chunk in ChunkReader("manzanares/test/lorem.txt",end=r"\n+"):

        if isinstance(chunk, tuple): 
            print()
            print("----->>> Chunk: {}:".format(chunk[0]), "{}".format(chunk[1]).encode("utf8")) 
            sentences, splits = split_sentence(r"(?:[.!?]+[\s]+)|(?:[ \t]*\n+)|$",chunk[1])
            #print("----->>> Sente: ", sentences)
            #print("----->>> Split: ", splits)
            clean_pttrs = [(r"[,]","")]
            normal = [normalize_txt(x, clean_pttrs) for x in sentences]
            #print("----->>> Norma:", normal)
            clean_text=normal[0]
            garbage=normal[1]

            """reconst = clean_text
            for element in garbage:
                if element[2] == "":
                    reconst = reconst[:element[0][0]] + element[1] + reconst[element[0][0]:]
                else:
                    reconst = reconst[:element[0][0]] + element[1] + reconst[element[0][0]+len(element[2])-1:]
            if reconst != chunk[1]:
                raise ValueError("Mal reconstruido\n{}\n{}".format(reconst.encode("UTF-8"),chunk[1].encode("UTF-8")))
            """