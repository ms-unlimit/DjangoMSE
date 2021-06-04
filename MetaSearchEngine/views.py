from django.shortcuts import render
import math
import MetaSearchEngine.metaSE as metaSE
from MetaSearchEngine import textProcessor
from django.http import HttpResponse
from .models import Query
from .forms import QueryForm

"""
print("im MetaSearchEngine")

headers = {'accept-language': 'en-US,en;q=0.9', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate',
     'sec-fetch-site': 'same-origin', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1',
     'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
     'x-client-data': 'CKu1yQEIjrbJAQijtskBCMS2yQEIqZ3KAQjQr8oBCLywygEIl7XKAQjttcoBCI66ygEYvbrKAQ=='}

#if __name__=="__main__":

query = 'car'

engine1 = metaSE.searchEngine(101, "google", "https://www.google.com/search?q=", ".rc", "", query, headers, '.LC20lb', '.st', 'd')
engine2 = metaSE.searchEngine(202, "bing", "https://www.bing.com/search?q=", ".b_algo", "", query, headers, 'h2 a', '.b_caption p', 'd')
engine3 = metaSE.searchEngine(202, "Ask", 'https://www.ask.com/web?q=', ".PartialSearchResults-item", "", query, headers,'.result-link', '.PartialSearchResults-item-abstract', 'd')
#engine4 = metaSE.searchEngine(101, "egerin", "https://egerin.com/user/searchresult?type=Web&query=", ".result", "", query, headers, '.result-title', '.result-snippet', 'd')
engine5 = metaSE.searchEngine(101, "yippy", "https://yippy.com/search?query=", ".source-bing-azure-2016", "", query, headers, '.title', '.field-snippet .value', 'd')

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

searchResults=metaSE.searchEngine.results
searchEngResults=metaSE.searchEngine.enginesResults
resultCount = len(searchResults.keys())

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

for r in searchResults:
    print(r, " Weight: ", searchResults[r]["Weight"], "  Sim: ", searchResults[r]["Sim"], "simLink: ",
          searchResults[r]["simLink"], "steam_title : ", searchResults[r]["steam_title"], "Title:",
          searchResults[r]["Title"], "steam_dec:", searchResults[r]["steam_dec"], "Description:",
          searchResults[r]["Description"])

print("-----------------------------------------------------------------------------")

linksSim = textProcessor.sort_link(metaSE.searchEngine.linksSim)
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
for r in searchResults:
    print(r, " Weight: ", searchResults[r]["Weight"], "  Sim: ", searchResults[r]["Sim"], "simLink: ",
          searchResults[r]["simLink"], "steam_title : ", searchResults[r]["steam_title"], "Title:",
          searchResults[r]["Title"])
print("-----------------------------------------------------------------------------")

linksSim = textProcessor.sort_link(linksSim)
for l in linksSim:
    print(l, "link sim : ", linksSim[l]["sim"])

rc=0
for r in searchResults:
    rc+=1
    searchResults[r]["Link"],searchResults[r]["Rank"]=str(r),rc
"""
def results_list(request):
    query="chelsea"
    ms=metaSE.MSE(query)
    ms.runMSE()
    return render(request, 'MSE.html', {'items':ms.searchResults, 'query':query})

def home(request):
    return HttpResponse("hi")