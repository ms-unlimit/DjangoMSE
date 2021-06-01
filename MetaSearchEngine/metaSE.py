import requests
from bs4 import BeautifulSoup
import threading
import html2text
import MetaSearchEngine.similarity as similarity
import MetaSearchEngine.textProcessor as textProcessor
h2t =html2text.HTML2Text()

class searchEngine (threading.Thread):

    results = {}
    enginesResults = {}
    linksSim = {}
    resultsCount = 0


    def __init__(self, threadID, name, url, selectItems, startResult, query, header, selectTitle, selectDecription, selectLink):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.url = url
        self.selectItems = selectItems
        self.start_result = startResult
        self.query = query
        self.queryNormalize= textProcessor.normalization(query)
        self.selectTitle = selectTitle
        self.selectDecription = selectDecription
        self.selectLink = selectLink
        self.header = header

    def run(self):
        print(self.name + ' start')
        url = self.url + self.query
        r = requests.get(url, headers=self.header)
        print(r.status_code)
        soup = BeautifulSoup(r.text, 'html.parser')
        selectResult = soup.select(self.selectItems)
        searchEngine.enginesResults[self.name] = []

        for i in selectResult:
            titleNormalize = textProcessor.normalization(h2t.handle(i.select(self.selectTitle)[0].text))
            decNormalize = textProcessor.normalization(h2t.handle(i.select(self.selectDecription)[0].text))
            sim = similarity.mergSim(titleNormalize, decNormalize, self.queryNormalize)
            if i.a['href'] not in searchEngine.results.keys():
                searchEngine.results[i.a['href']] = {"Weight": 0, "steam_title": titleNormalize,
                                                     "Title": h2t.handle(i.select(self.selectTitle)[0].text), "steam_dec": decNormalize,
                                                     "Description": h2t.handle(i.select(self.selectDecription)[0].text), "Sim": sim,
                                                     "simLink": similarity.simLink(i.a['href'], self.query)}
                searchEngine.linksSim[i.a['href']] = {"sim": similarity.simLink(i.a['href'], self.query)}
            else:
                if (sim > searchEngine.results[i.a['href']]["Sim"]):
                    searchEngine.results[i.a['href']] = {"Weight": 0, "steam_title": titleNormalize,
                                                  "Title": h2t.handle(i.select(self.selectTitle)[0].text),
                                                  "steam_dec": decNormalize,
                                                  "Description": h2t.handle(i.select(self.selectDecription)[0].text), "Sim": sim,
                                                  "simLink": similarity.simLink(i.a['href'], self.query)}

            searchEngine.enginesResults[self.name].append(i.a['href'])

            print(self.name + " : " + i.a['href'])
        print(len(selectResult))