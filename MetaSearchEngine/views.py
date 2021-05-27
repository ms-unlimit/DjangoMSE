from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import threading
import html2text
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import math


# n_html = requests.get('https://90tv.ir/news')
# n_soup = BeautifulSoup(n_html.content, 'html.parser')
# n_heading = n_soup.find_all('h2')
n_news = []
# for n_header in n_heading:
#     n_news.append(n_header.get_text())
# #python manage.py runserver
#
# v_html = requests.get('https://www.varzesh3.com/')
# v_soup = BeautifulSoup(v_html.content, 'html.parser')
# v_heading = v_soup.find_all('li', {'data-filter':{'1', '3'}})
v_news = []
# for v_header in v_heading[0:10]:
#     v_news.append(v_header.get_text())
query='car'
def getQuery():

    global query
    query=input.get()
    print("query : " ,input.get())

h2t =html2text.HTML2Text()

headers = {'accept-language': 'en-US,en;q=0.9', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate',
     'sec-fetch-site': 'same-origin', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1',
     'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
     'x-client-data': 'CKu1yQEIjrbJAQijtskBCMS2yQEIqZ3KAQjQr8oBCLywygEIl7XKAQjttcoBCI66ygEYvbrKAQ=='}

searchResults = {}
searchEngResults = {}
linksSim = {}
resultCount = 0

#--------------------------------porter-------------------------
ps = PorterStemmer()

stop_words = set(stopwords.words('english'))

def listToString(s):
    str1 = " "
    return (str1.join(s))

def normalization(s):
    temp_list = []
    for j in word_tokenize(s):
        temp_list.append(ps.stem(j))
        filtered_sentence = [w for w in temp_list if not w in stop_words]
    return (listToString(filtered_sentence))

#----------------------------------------------------------------------------------------------------------

class myThread (threading.Thread):
   def __init__(self, threadID, name, counter, url, select,  start_result, search_text, header, title, dec, link):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.url = url
      self.select = select
      self.start_result = start_result
      self.search_text = search_text
      self.search_text_steam = normalization(search_text)
      self.header = header
      self.counter = counter
      self.title = title
      self.dec = dec
      self.link = link

   def run(self):
      print(self.name+' start')
      url=self.url+self.search_text
      r = requests.get(url, headers=self.header)
      print(r.status_code)
      soup = BeautifulSoup(r.text, 'html.parser')
      # search_result_titles = soup.select(self.title)
      # search_result_decs = soup.select(self.dec)
      search_result_links = soup.select(self.select)
      searchEngResults[self.name] = []

      for i in search_result_links:
          steam_title = normalization(h2t.handle(i.select(self.title)[0].text))
          steam_dec = normalization(h2t.handle(i.select(self.dec)[0].text))
          if i.a['href'] not in searchResults.keys():
              sim = mergSim(steam_title, steam_dec, self.search_text_steam)
              #sim = mergSim(h2t.handle(i.select(self.title)[0].text),h2t.handle(i.select(self.dec)[0].text),self.search_text)
              searchResults[i.a['href']] = {"Weight":0, "steam_title":steam_title,"Title":h2t.handle(i.select(self.title)[0].text),"steam_dec":steam_dec, "Description":h2t.handle(i.select(self.dec)[0].text), "Sim":sim, "simLink":simLink(i.a['href'],self.search_text)}
              linksSim[i.a['href']] ={"sim":simLink(i.a['href'],self.search_text)}
          else:
              sim = mergSim(steam_title, steam_dec, self.search_text_steam)
              #sim = mergSim(h2t.handle(i.select(self.title)[0].text),h2t.handle(i.select(self.dec)[0].text),self.search_text)
              if(sim>searchResults[i.a['href']]["Sim"]):
                  searchResults[i.a['href']] = {"Weight": 0, "steam_title":steam_title, "Title": h2t.handle(i.select(self.title)[0].text),
                                                "steam_dec": steam_dec, "Description": h2t.handle(i.select(self.dec)[0].text), "Sim": sim, "simLink":simLink(i.a['href'],self.search_text)}

          searchEngResults[self.name].append(i.a['href'])

          # print(h2t.handle(i.select(self.title)[0].text))
          print(self.name+" : "+i.a['href'])
          # print(h2t.handle(i.select(self.dec)[0].text))
      print(len(search_result_links))

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

def simLink(link, query):
    c = 0
    queryTerms = tokenize(query)
    for q in queryTerms:
        if q in link:
            c += 1
    sim=c/len(link)
    return sim

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

def sim(txt, query):

    termIndex = []
    NDT = 0
    ADJ= True

#------------tokenize query & text terms---------

    txtTerms=tokenize(normalization(txt))
    queryTerms=tokenize(query)

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


#if __name__=="__main__":

# window = Tk()
# window.geometry("420x100")
# window.title("Set the path")
# Label1 = Label(window, text="Query  :").grid(row=0, column=0)
# Label2 = Label(window, text="  ").grid(row=1, column=1)
# b1 = tk.Button(window, text='Search', command=window.destroy, height=2, width=10).grid(row=3, column=0,padx=10)
# b2 = tk.Button(window, text='SET', command=getQuery, height=2, width=10).grid(row=3, column=1)
# input = Entry(window, width="50")
# input.grid(row=0, column=1)
# window.mainloop()
# print(query)
query = 'nokia 3.1 plus'
thread1 = myThread(101, "google", 1, "https://www.google.com/search?q=", ".rc", "", query, headers, '.LC20lb', '.st', 'd')
thread2 = myThread(202, "bing", 2, "https://www.bing.com/search?q=", ".b_algo", "", query, headers, 'h2 a', '.b_caption p', 'd')
thread3 = myThread(202, "Ask", 2, 'https://www.ask.com/web?q=', ".PartialSearchResults-item", "", query, headers,'.result-link', '.PartialSearchResults-item-abstract', 'd')
thread4 = myThread(101, "egerin", 1, "https://egerin.com/user/searchresult?type=Web&query=", ".result", "", query, headers, '.result-title', '.result-snippet', 'd')
thread5 = myThread(101, "yippy", 1, "https://yippy.com/search?query=", ".source-bing-azure-2016", "", query, headers, '.title', '.field-snippet .value', 'd')

thread1.start()
thread2.start()
thread3.start()
#thread4.start() #need_VPN
thread5.start()

thread1.join()
thread2.join()
thread3.join()
#thread4.join() #need_VPN
thread5.join()

# print(searchResults)
print(len(searchResults.keys()))
# print(searchEngResults)

resultCount = len(searchResults.keys())
for i in searchEngResults:
    counter = resultCount
    for j in searchEngResults[i]:
        # searchResults[j]["Weight"] += counter
        if searchResults[j]["Weight"] == 0:
            searchResults[j]["Weight"] += counter
        else:
            searchResults[j]["Weight"] += counter / (resultCount - counter + 1)
        counter -= 1
    diffList = list(set(searchResults.keys()) - set(searchEngResults[i]))
    totalSim = 0
    remainWeight = counter * (counter + 1) / 2
    for j in diffList:
        totalSim += searchResults[j]["Sim"]
    if totalSim != 0:
        for j in diffList:
            sim_Weight = searchResults[j]["Sim"] * remainWeight / totalSim
            if sim_Weight > 0:
                searchResults[j]["Weight"] += math.log(sim_Weight)
            #      searchResults[j]["Weight"] += searchResults[j]["Sim"] * remainWeight / totalSim
    else:
        for j in diffList:
            searchResults[j]["Weight"] += remainWeight / len(diffList)
    # print(searchResults)
searchResults = sort_dict(searchResults)

for r in searchResults:
    print(r, " Weight: ", searchResults[r]["Weight"], "  Sim: ", searchResults[r]["Sim"], "simLink: ",
          searchResults[r]["simLink"], "steam_title : ", searchResults[r]["steam_title"], "Title:",
          searchResults[r]["Title"], "steam_dec:", searchResults[r]["steam_dec"], "Description:",
          searchResults[r]["Description"])

print("-----------------------------------------------------------------------------")

linksSim = sort_link(linksSim)
for ls in linksSim:
    max = linksSim[ls]["sim"]
    break

for w in searchResults:
    log_w = math.log(searchResults[w]["Weight"])
    if linksSim[w]["sim"] != 0:
        norm = linksSim[w]["sim"] / max
        f = log_w * norm
        searchResults[w]["Weight"] += f
        print("link ", w)
        print("final ", f)

searchResults = sort_dict(searchResults)
for r in searchResults:
    print(r, " Weight: ", searchResults[r]["Weight"], "  Sim: ", searchResults[r]["Sim"], "simLink: ",
          searchResults[r]["simLink"], "steam_title : ", searchResults[r]["steam_title"], "Title:",
          searchResults[r]["Title"])
print("-----------------------------------------------------------------------------")

# linksSim = sort_link(linksSim)
for l in linksSim:
    print(l, "link sim : ", linksSim[l]["sim"])

rc=0
for r in searchResults:
    rc+=1
    n_news.append(r)
    v_news.append( " result "+str(rc)+" - "+r+"  Title: "+searchResults[r]["Title"])
    #print(r," Weight: ",searchResults[r]["Weight"],"  Sim: ",searchResults[r]["Sim"],"simLink: ",searchResults[r]["simLink"])




#python manage.py runserver
def index(request):
    return render(request, 'index.html', {'n_news':n_news, 'v_news':v_news, 'query':query})