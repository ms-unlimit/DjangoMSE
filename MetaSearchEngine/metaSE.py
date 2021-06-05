import requests
from bs4 import BeautifulSoup
import math
import threading
import html2text
import MetaSearchEngine.similarity as similarity
import MetaSearchEngine.textProcessor as textProcessor
h2t =html2text.HTML2Text()
from time import sleep

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

class MSE():

    running=False

    def __init__(self, query):
        self.query=query
        print(self.query)

    def __del__(self):
        searchEngine.results.clear()
        searchEngine.enginesResults.clear()
        searchEngine.linksSim.clear()
        searchEngine.resultsCount = 0
        MSE.running=False
        print("del obj MSE")

    def runMSE(self):
        print("start runMSE")
        headers = {'accept-language': 'en-US,en;q=0.9', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate',
                   'sec-fetch-site': 'same-origin', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1',
                   'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
                   'x-client-data': 'CKu1yQEIjrbJAQijtskBCMS2yQEIqZ3KAQjQr8oBCLywygEIl7XKAQjttcoBCI66ygEYvbrKAQ=='}

        # while(MSE.running):
        #     sleep(1)
        # MSE.running=True

        engine1 = searchEngine(101, "google", "https://www.google.com/search?q=", ".rc", "", self.query, headers, '.LC20lb', '.st', 'd')
        engine2 = searchEngine(202, "bing", "https://www.bing.com/search?q=", ".b_algo", "", self.query, headers, 'h2 a', '.b_caption p', 'd')
        engine3 = searchEngine(202, "Ask", 'https://www.ask.com/web?q=', ".PartialSearchResults-item", "", self.query, headers,'.result-link', '.PartialSearchResults-item-abstract', 'd')
        #engine4 = searchEngine(101, "egerin", "https://egerin.com/user/searchresult?type=Web&query=", ".result", "", query, headers, '.result-title', '.result-snippet', 'd')
        engine5 = searchEngine(101, "yippy", "https://yippy.com/search?query=", ".source-bing-azure-2016", "", self.query, headers, '.title', '.field-snippet .value', 'd')

        engine1.start()
        engine2.start()
        engine3.start()
        #thread4.start() #need_VPN
        engine5.start()

        engine1.join()
        engine2.join()
        engine3.join()
        #thread4.join() #need_VPN
        engine5.join()

        print(" start MSE.searchResults")
        searchResults=searchEngine.results
        searchEngResults=searchEngine.enginesResults
        resultCount = len(searchResults.keys())


        # engine1.__del__()
        # engine2.__del__()
        # engine3.__del__()
        # #engine4.__del__()
        # engine5.__del__()

        #print(len(searchResults.keys()))

        for i in searchEngResults:
            counter = resultCount
            for j in searchEngResults[i]:
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
        searchResults = textProcessor.sort_dict(searchResults)

        # for r in searchResults:
        #     print(r, " Weight: ", searchResults[r]["Weight"], "  Sim: ", searchResults[r]["Sim"], "simLink: ",
        #           searchResults[r]["simLink"], "steam_title : ", searchResults[r]["steam_title"], "Title:",
        #           searchResults[r]["Title"], "steam_dec:", searchResults[r]["steam_dec"], "Description:",
        #           searchResults[r]["Description"])
        #
        # print("-----------------------------------------------------------------------------")

        linksSim = textProcessor.sort_link(searchEngine.linksSim)
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

        searchResults = textProcessor.sort_dict(searchResults)
        # for r in searchResults:
        #     print(r, " Weight: ", searchResults[r]["Weight"], "  Sim: ", searchResults[r]["Sim"], "simLink: ",
        #           searchResults[r]["simLink"], "steam_title : ", searchResults[r]["steam_title"], "Title:",
        #           searchResults[r]["Title"])
        # print("-----------------------------------------------------------------------------")

        #linksSim = textProcessor.sort_link(linksSim)
        # for l in linksSim:
        #     print(l, "link sim : ", linksSim[l]["sim"])

        rc=0
        for r in searchResults:
            rc+=1
            searchResults[r]["Link"],searchResults[r]["Rank"]=str(r),rc

        return searchResults
