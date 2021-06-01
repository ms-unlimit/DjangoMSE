from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

def wordslist2String(wordsList):
    str = " "
    return (str.join(wordsList))

def normalization(txt):
    words = []
    for w in word_tokenize(txt):
        if not w in stop_words:
            words.append(ps.stem(w))
        #filtered_sentence = [w for w in temp_list if not w in stop_words]
    return (wordslist2String(words))

def tokenize(txt):
    term = ''
    txt=txt+' '
    termsList = []
    for t in txt:
        if t ==' ' or t ==',':
            termsList.append(term.lower())
            term = ''
        else:
            term += t
    return termsList

def Convert_tuple_to_dict(tup, di):
    for a, b in tup:
        di[a] = b
    return di

def sort_dict(dict):
    tupleRes = sorted(dict.items(), key= lambda kv: kv[1]["Weight"], reverse=True)
    res = {}
    res = Convert_tuple_to_dict(tupleRes,res)
    return res

def sort_link(dict):
    tupleRes = sorted(dict.items(), key= lambda kv: kv[1]["sim"], reverse=True)
    res = {}
    res = Convert_tuple_to_dict(tupleRes,res)
    return res