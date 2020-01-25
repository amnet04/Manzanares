import pandas as pd
from itertools import groupby
import pycld2 as cld2
import random
import re
from multiprocessing import cpu_count, Pool, Manager
from functools import partial
import numpy as np
import csv


def normalize_txt(text,patterns): 
    """ Apply a list of subtring replaces over the text. Usefull for normalize
    some text (number of linebreaks between parragraphs, case of the first letter, split or
    join punctuation marks, etc)

    Parameters
    ----------
    doc : str
        Text string to be cleaned.

    patterns : List[Tuple[Pattern[str],Pattern[str]]]
        A list of tuples of regex patterns to be replaced, the first member is 
        the pattern to find and the second the replace pattern.
        
        Note: Take care with the orden of the list of patterns!!!!.
        
        Example of patterns: 
            
            1) Replace <<number:number>> to nothing:
            
            ori_pat1 = (r"\d+\:\d+\ ")
            rep_to_pat1 =  (r"")
            
            2) Replace more than 2 linebreaks with only 2 linebreaks:
            
            ori_pat2 = (r"\n{2,}")
            rep_to_pat2 =  ("\n\n")         
            
            
    Returns
    -------
    string
       New string without the text that matches whit patterns.

    """
    for pattern in patterns:
        text = re.sub(pattern[0], pattern[1], text)
    return text



def process_sentence(sentence, clean_p, alpha, token_base, gs):
    if clean_p:
        sentence = normalize_txt(sentence,clean_p)
        
    if alpha:
        sentence = " ".join(x for x in sentence if x.isalpha())

    sentence_tokens = []

    if token_base == "symbols":
        lambda_finish = lambda x, y : sentence[x+y] if x+y < len(sentence) else("$" if x+y==len(sentence) else "#")
        if len(gs) > 1:
            sentence = "^"+sentence
        for i in range (0, len(sentence)):
            sentence_tokens.append("".join([lambda_finish(gap,i) for gap in gs]))

                

    if token_base == "words":
        sentence = sentence.split()
        lambda_finish = lambda x, y : sentence[x+y] if x+y < len(sentence) else("<-sentence_end!->" if x+y==len(sentence) else "<-beyond_limits!->")
        if len(gs) > 1:
            sentence.insert(0, "<-sentence_begin!->")    
        for i in range (0, len(sentence)):
            sentence_tokens.append(" ".join([lambda_finish(gap,i) for gap in gs]))

    return sentence_tokens
  




def randtext(tokens, path, max_len=1000):
    simbols = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u", "v","w","x","y","z"," "]
    text = []
    while len(text) < tokens:
        word = ""
        simbol = ""
        while simbol != " ":
            if len(word) < max_len:
                simbol = random.choice(simbols)
                if simbol != " ":
                    word += simbol
                else:
                    word = word.strip()
            else:
                simbol = " "
        text.append(word)
        
    text = " ".join(text)
    f = open(path, 'w')
    f.write(text)
    f.close

def randomtxt():
    randtext(len(Ulisses.onlyalpha_words_low), "./src/data/random_no_limits.txt")
    randtext(len(Ulisses.onlyalpha_words_low), "./src/data/random_30.txt", max_len=30)







