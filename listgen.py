import requests
from bs4 import BeautifulSoup
import json
import re

CLEANR = re.compile('<.*?>') 
CLEANS = re.compile(r"\([^()]*\)") 
def cleanhtml(raw_html):
    cleantext = re.sub(CLEANR, "", str(raw_html))  
    return cleantext

def cleanParan(text):
    cleantext = re.sub(CLEANS, "", str(text))  
    return cleantext

alphabet = sorted("QWERTYUIOPASDFGHJKLZXCVBNM")

urlList = ["https://medlineplus.gov/druginfo/drug_{}a.html".format(x) for x in alphabet] + ["https://medlineplus.gov/druginfo/drug_00.html"]
thebigone = dict()
searchURL = "https://medlineplus.gov/druginfo"
drugSet = set()

for url in urlList:
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    for x in soup.article.find('ul', id='index').find_all("li"):
        if (cleanParan(cleanhtml(x.span).replace("see", "")) == "None"):
            #thebigone[cleanhtml(x.a).strip().replace("\u00ae", "")] = searchURL + x.a.get("href")[1:]
            drugSet.add(cleanhtml(x.a).strip().replace("\u00ae", ""))

        else:
            #thebigone[cleanParan(cleanhtml(x.span).replace("see", "")).strip().replace("\u00ae", "")] = searchURL + x.a.get("href")[1:]
            drugSet.add(cleanParan(cleanhtml(x.span).replace("see", "")).strip().replace("\u00ae", ""))


with open('data.json', 'w') as f:
    json.dump(list(drugSet), f, sort_keys=True,indent=4)