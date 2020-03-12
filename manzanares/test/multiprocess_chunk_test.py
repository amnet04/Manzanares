import multiprocessing as mp
import pytest

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from manzanares.text_preproc.chunkreader import ChunkReader

def test_chunkreader():
    CPUS = len(os.sched_getaffinity(0))
    chunk_gen = ChunkReader('manzanares/test/chinese.txt', end=r"[\n]{1,}")
    are_next = True
    while are_next:
        are_next = get_chunks_list(chunk_gen,CPUS)
        if are_next:
            process_count = len(are_next)
            process = mp.Pool(process_count)
            print(process.map(str.strip, [x[1] for x in are_next]))
    


def get_chunks_list(chunk_generator,size):
    chunks_list = []
    print("\n\n")
    for n in range(0, size):
        try:
            chunk = next(chunk_generator)
            if chunk !="":
                chunks_list.append(chunk)
        except StopIteration:
           return False
    return chunks_list
