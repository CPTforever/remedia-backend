from flask import Flask, request, jsonify, json
from flask_cors import CORS
import io
import os
import requests
from bs4 import BeautifulSoup
import re
import json
from requests.api import head


import requests

CLEANR = re.compile('<.*?>') 

def cleanhtml(raw_html):
    cleantext = re.sub(CLEANR, "", str(raw_html))  
    return cleantext



# Takes in a name
# Returns a URL
def drugSearch(drugName):
    drugURL = "https://vsearch.nlm.nih.gov/vivisimo/cgi-bin/query-meta?v%3Aproject=medlineplus&v%3Asources=medlineplus-bundle&query={}&binning-state=group%3d%3dDrugs%20and%20Supplements&".format(drugName)
    nlmsearch =  "https://vsearch.nlm.nih.gov"

    # Searching for the drug
    page = requests.get(drugURL)
    soup = BeautifulSoup(page.content, "html.parser")

    # Finding the results
    document = soup.find(id="document-list")
    results = document.find("ol", class_="results")
    drugURL = nlmsearch + results.div.a.get('href')

    # Getting the page with drug info
    
    return drugURL

# Takes in a URL, extracts useful data
# Returns a json
def drugProcess(drugURL):
    # Requests the URL
    drugPage = requests.get(drugURL)
    # Loading the page into the extracting thingy
    soup = BeautifulSoup(drugPage.content, "html.parser")

    # This chunk is all the info you'll need
    title = cleanhtml(soup.article.find("h1", class_="with-also"))
    prouncation = cleanhtml(soup.article.find("span", id="d-pronunciation"))
    why = soup.article.find("div", id="why").find("div", id="section-1").p
    #how = soup.article.find("div", id="how").find("div", id="section-2").p
    #other = soup.article.find("div", id="other-uses")
    #care = soup.article.find("div", id="precautions")
    diet = soup.article.find("div", id="special-dietary")
    #forget = soup.article.find("div", id="if-i-forget")
    store = soup.article.find("div", id="storage-conditions")

    side = soup.article.find("div", id="side-effects").find("div", id="section-side-effects")

    over = soup.article.find("div", id="overdose")
    #other = soup.article.find("div", id="other-information")
    brandSolo = soup.article.find("div", id="brand-name-1")
    brandCombo = soup.article.find("div", id="brand-name-2")

    try:
        # Gets one sentence on why you should take this drug
        cleanWhy = cleanhtml(why.p)
    except:
        cleanWhy = ""

    # Gets a list of side effects and serious side effects
    sideEffects = []
    doctorEffects = []
    try:
        for x in side.find_all("h3"):
            tag = cleanhtml(x).find("serious")
            for y in x.find_next_sibling('ul'):
                if tag != -1:
                    doctorEffects.append(cleanhtml(y))
                else:
                    sideEffects.append(cleanhtml(y))
    except:
        pass


    # Tells you to eat healthy 
    try:
        cleanDiet = cleanhtml(diet.p)
    except:
        cleanDiet = ""
    # Lists how to store it
    try:
        cleanStore = cleanhtml(store.p)
    except:
        cleanStore = ""

    try:
        # Lists what you should do when overdosing
        cleanOverdose = cleanhtml(over.p)
    except:
        pass
    
    # Lists overdose symptoms
    overdoseSymptoms = []
    try:
        for x in over.ul:
            overdoseSymptoms.append(cleanhtml(x))
    except:
        pass
    # Lists brand names that use this product
    brandNames = []
    try:
        try:
            for x in brandSolo.ul:
                brandNames.append(cleanhtml(x))
        except:
            pass
        try:
            for y in brandCombo.ul:
                brandNames.append(cleanhtml(y))
        except:
            pass
    except:
        pass

    return { 
        "Name": title,
        "Pronunciation": prouncation.replace('\n', "").replace('\r', ''),
        "Why": cleanWhy,
        "Diet": cleanDiet,
        "Store": cleanStore,
        "Overdose": cleanOverdose,
        "OverdoseSymptoms" : overdoseSymptoms,
        "BrandNames" : brandNames,
        "regEffects" : sideEffects,
        "severeEffects" : doctorEffects,
        "CombinedEffects" : overdoseSymptoms + doctorEffects + sideEffects,
    }



app = Flask(__name__)
CORS(app)

@app.route('/')
def this_works():
    print('this works')
    
    return "This works..."

@app.route("/multi", methods=["POST"])
def multi():
    if request.method == "POST":
        try:
            text = request.form.get('brand')
            return drugProcess(drugSearch(text))
        except:
            return "No drug"
        
""" 
with open('data.json', 'w') as f:
    json.dump(drugProcess(drugSearch("advil")), f, indent=4)

"""
url = drugSearch("APPG")
print(url)
drugProcess(url)
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8081)))

