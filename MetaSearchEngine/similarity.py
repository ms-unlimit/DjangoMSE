import MetaSearchEngine.textProcessor as textProcessor

def simLink(link, query):
    c = 0
    queryTerms = textProcessor.tokenize(query)
    for q in queryTerms:
        if q in link:
            c += 1
    sim=c/len(link)
    return sim

def sim(txt, query):

    termIndex = []
    NDT = 0
    ADJ= True

#------------tokenize query & text terms---------
    txtTerms=textProcessor.tokenize(textProcessor.normalization(txt))
    queryTerms=textProcessor.tokenize(query)

#------------------NDT--------------------------
    for l in queryTerms:
        if l in txtTerms:
          NDT+=1
# ----------------TNT & WS-----------------------
    index = 0
    for t in txtTerms:
        if t in queryTerms:
            termIndex.append(index)
        index+=1
    TNT= len(termIndex)

    termIndex_len=len(termIndex)
    if termIndex_len < 2:
        WS= 1
    else:
        WS = termIndex[termIndex_len-1]-termIndex[0]+1
#---------------ADJ & WS -------------------------
    if len(queryTerms) == NDT:
         q=0
         for a in range(termIndex_len-1):
             if queryTerms[q]==txtTerms[a]:
                 q+=1
                 if len(queryTerms)==q:
                    ADJ = True
                    break
    else:
        WS= 999999
        ADJ= False
#-------------------sim--------------------------
    qlen=len(queryTerms)
    tlen=len(txtTerms)
    Sws=0
    SADJ=0
    if WS != 999999:
        Sws=(tlen-WS+qlen)/tlen
    if ADJ :
        SADJ=1
    sim=(1.5*(NDT/qlen)+2*(SADJ)+1.2*(Sws)+(TNT/tlen))/5.7

    # print("sim : ",sim)
    # print("NDT : ",NDT)
    # print("TNT : ",TNT)
    # print("WS : ",WS)
    # print("Sws : ",Sws)
    # print("ADJ : ",ADJ)
    # print("SADJ : ",SADJ)
    # print("tlen : ",tlen)
    # print("qlen : ",qlen)
    # print(termIndex)
    # print(txtTerms)
    # print(queryTerms)
    return sim

def mergSim(title , des , query):
    titleSim=sim(title,query)
    desSim=sim(des,query)
    s=(1.5*titleSim + desSim)/2.5
    return s