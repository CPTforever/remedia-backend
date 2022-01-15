"""
Stuff
Major league hacking


"""


import requests
from bs4 import BeautifulSoup

drug = "Acarbose"
URL = "https://vsearch.nlm.nih.gov/vivisimo/cgi-bin/query-meta?v%3Aproject=medlineplus&v%3Asources=medlineplus-bundle&query={}&binning-state=group%3d%3dDrugs%20and%20Supplements&".format(drug)
#print(URL)
nlmsearch =  "https://vsearch.nlm.nih.gov"
drugplus = URL + drug

page = requests.get(drugplus)

soup = BeautifulSoup(page.content, "html.parser")
document = soup.find(id="document-list")
results = document.find("ol", class_="results")
drugURL = nlmsearch + results.div.a.get('href')
print(drugURL)

drugPage = requests.get(drugURL)
soup = BeautifulSoup(drugPage.content, "html.parser")
print(soup)
#print(job_elements)