"""
Stuff
Major league hacking


"""


import requests
from bs4 import BeautifulSoup

drug = "advil"
URL = "https://vsearch.nlm.nih.gov/vivisimo/cgi-bin/query-meta?v%3Aproject=medlineplus&v%3Asources=medlineplus-bundle&query={}&binning-state=group%3d%3dDrugs%20and%20Supplements&".format(drug)
#URL)
nlmsearch =  "https://vsearch.nlm.nih.gov"
drugplus = URL + drug

page = requests.get(drugplus)

soup = BeautifulSoup(page.content, "html.parser")
document = soup.find(id="document-list")
results = document.find("ol", class_="results")
drugURL = nlmsearch + results.div.a.get('href')


drugPage = requests.get(drugURL)
soup = BeautifulSoup(drugPage.content, "html.parser")

why = soup.article.find("div", id="why")
how = soup.article.find("div", id="how")
other = soup.article.find("div", id="other-uses")
care = soup.article.find("div", id="precautions")
diet = soup.article.find("div", id="special-dietary")
forget = soup.article.find("div", id="if-i-forget")
store = soup.article.find("div", id="storage-conditions")
side = soup.article.find("div", id="side-effects")
over = soup.article.find("div", id="overdose")
other = soup.article.find("div", id="other-information")


    #x.prettify())
#job_elements)