#coding=utf-8
import sys
import os
import json
import jieba

from collections import defaultdict
from pprint import pprint
import gensim
from gensim import corpora, models, similarities

fdocs = []
def seg_datafile(leading, fnitem):
    fn = '%s%s' %(leading, fnitem)
    fd = open(fn)
    content = ''
    while 1:
        line = fd.readline()
        if not line:
            break
        content += line.strip()
    fd.close()

    seg_list = jieba.cut(content, cut_all = True)

    txt = u' '.join(seg_list).encode('utf-8')

    print ' the text is:'
    print txt

    return txt

def loading_data_file():
    for it in os.walk('mldata/'):
        for filename in it[2]:
            fdocs.append(filename)

    print 'Totally %d data files' %(len(fdocs))

    docs = [] 
    for it in fdocs:
        docs.append(seg_datafile('mldata/', it))

    # Now, docs are the all document file?
    print 'the full len of docs = %d' %(len(docs))
    print str(docs).decode('string_escape') # This is how output China txt in list

    print ' '

    stoplist = set('的 是 在 了'.split())
    texts = [[word for word in doc.split() if word not in stoplist]for doc in docs]

    print str(texts).decode('string_escape')
    print ' \n'
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    texts = [[token for token in text if frequency[token] > 1]for text in texts]
    print str(texts).decode('string_escape')


    mydict = corpora.Dictionary(texts)
    mydict.save('./deerwester.dict')
    print mydict
    print ' \n'
    print json.dumps(mydict.token2id, ensure_ascii=False)

    print '=====VECTOR====\n'
    myvec = [mydict.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('./deerwester.mm', myvec)
    print myvec
    return 0

####################################################
def start_ml():
    if not os.path.exists('./deerwester.dict'):
        loading_data_file()
    else:
        for it in os.walk('mldata/'):
            for filename in it[2]:
                fdocs.append(filename)

    print '==== Try modeling the data ====\n'
    mydict = corpora.Dictionary.load('./deerwester.dict')
    myvec = corpora.MmCorpus('./deerwester.mm')
    print myvec

#    mytfidf = gensim.models.TfidfModel(myvec)


#    tfidf_vec = mytfidf[myvec]
#    print tfidf_vec
#    for vec in tfidf_vec:
#        print vec


# Creating a LSI model....
    mylsi = gensim.models.LsiModel(corpus = myvec, id2word = mydict)
    print '====================='
    mylsi.print_topics(100)
    print '====================='
    test_texts = ['电影', '专家', '骗子']
    test_vec = mydict.doc2bow(test_texts)
    print 'the test vector:'
    print test_vec
    test_vec_lsi = mylsi[test_vec]
    print test_vec_lsi
    print 'mark----'

    index = similarities.MatrixSimilarity(mylsi[myvec])
    print index

    sims = index[test_vec_lsi]
    print list(enumerate(sims))

    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    print '==== sorted result:'
    print sims

    print '\n\n'
    most_similar = sims[0][0]
    print '\n\n'


    print fdocs[most_similar]

#print json.dumps(mydict.token2id).decode("utf-8")
#print json.dumps(mydict.token2id, ensure_ascii=False)


    return 0

######################MAIN#########################

if __name__ == '__main__':
    start_ml()
