from os import path, mkdir
import shutil
import sys
import pytest

sys.path.append(path.join(path.dirname(__file__), '../..'))
from manzanares.text_preproc.chunkreader import ChunkReader
from manzanares.text_preproc.text_preprocess import normalize_txt, split_sentence

def test_chunk():
    for chunk in ChunkReader("manzanares/test/lorem.txt",end=r"[\n{1:}]"):
        clean_pttrs = [(r"[\,]",""), (r"[\t]{2:}","\t")]
        normal=normalize_txt(chunk, clean_pttrs)
        sentences = split_sentence(chunk,r"([\.\!\?])")
        print(sentences)
        clean_text=normal[0]
        garbage=normal[1]

        reconst = clean_text
        for element in garbage:
            if element[2] == "":
                reconst = reconst[:element[0][0]] + element[1] + reconst[element[0][0]:]
            else:
                reconst = reconst[:element[0][0]] + element[1] + reconst[element[0][0]+len(element[2])-1:]
        print("------------------------------")
        if reconst != chunk:
            raise ValueError("Mal reconstruido\n{}\n{}".format(reconst.encode("UTF-8"),chunk.encode("UTF-8")))
