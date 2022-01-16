from flask import Flask, request, jsonify, json
from flask_cors import CORS
import os
import requests
from bs4 import BeautifulSoup
import re



import requests

app = Flask(__name__)
CORS(app)

CLEANR = re.compile('<.*?>') 

def cleanhtml(raw_html):
    cleantext = re.sub(CLEANR, "", str(raw_html))  
    return cleantext

shapeList = {
    "any": 0,
    "round":24,
    "capsule":5,
    "oval":11,
    "egg":9,
    "barrel":1,
    "rectangle":23,
    "3 side": 32,
    "4 side": 14,
    "5 side": 13,
    "6 side": 27,
    "7 side": 25,
    "8 side": 10,
    "U shape": 33,
    "8 shape": 12,
    "heart": 16,
    "kidney": 18,
    "gear": 15,
    "character": 6
    }

colorList = {
    "any": "",
    "white": 12,
    "beige": 14,
    "black": 73,
    "blue": 1,
    "brown": 2,
    "clear": 3,
    "gold": 4,
    "gray": 5,
    "green": 6,
    "maroon": 44,
    "orange": 7,
    "peach": 74,
    "pink": 8,
    "purple": 9,
    "red": 10,
    "tan": 11,
}

def uncombine(string):
    a = cleanhtml(string)
    if "," in a:
        a = a.split(",")
        for z in range(len(a)):
            a[z] = a[z].replace("or ", "").replace("and ", "").strip()
        return a
    else:
        return [a]


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
    how = soup.article.find("div", id="how").find("div", id="section-2").p
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
        cleanWhy = cleanhtml(why)
    except:
        cleanWhy = ""

    try:
        # Gets one sentence on why you should take this drug
        cleanHow = cleanhtml(how)
    except:
        cleanHow = ""

    # Gets a list of side effects and serious side effects
    sideEffects = []
    doctorEffects = []
    try:
        for x in side.find_all("h3"):
            tag = cleanhtml(x).find("serious")
            for y in x.find_next_sibling('ul'):
                if tag != -1:
                    doctorEffects+=uncombine(y)
                else:
                    sideEffects+=uncombine(y)
    except:
        pass


    # Tells you to eat healthy 
    try:
        cleanDiet = cleanhtml(diet.p)
    except:
        cleanDiet = "Unless your doctor tells you otherwise, continue your normal diet."
        
    # Lists how to store it
    try:
        cleanStore = cleanhtml(store.p)
    except:
        cleanStore = "Keep this medication in the container it came in, tightly closed, and out of reach of children. Store it at room temperature and away from excess heat and moisture (not in the bathroom)."

    try:
        # Lists what you should do when overdosing
        cleanOverdose = cleanhtml(over.p)
    except:
        cleanOverdose = ""

    # Lists overdose symptoms
    overdoseSymptoms = []
    try:
        for x in over.ul:
            overdoseSymptoms+=uncombine(x)
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
        "How": cleanHow,
        "Diet": cleanDiet,
        "Store": cleanStore,
        "Overdose": cleanOverdose,
        "OverdoseSymptoms" : overdoseSymptoms,
        "BrandNames" : brandNames,
        "regEffects" : sideEffects,
        "severeEffects" : doctorEffects,
        "CombinedEffects" : overdoseSymptoms + doctorEffects + sideEffects,
    }

def pillImage(imprint, color, shape):
    pillURL = "https://www.drugs.com/imprints.php?imprint={}&color={}&shape={}".format(imprint.lower(), colorList[color], shapeList[shape])

    image = []
    name = []

    # Searching for the drug
    page = requests.get(pillURL)
    soup = BeautifulSoup(page.content, "html.parser")

    
    for x in soup.find_all('img'):
        a = x.get("src")
        if a[:5] == "https":
            image.append(a)

    for x in soup.find('div', 'contentBox').findAll('div', class_="pid-details"):
        name.append(cleanhtml(x.li.a))

    pills = dict()
    for x in range(len(name)):
        pills[name[x]] = image[x]
    
    return pills

@app.route('/')
def this_works():
    print('this works')
    
    return jsonify({"Success", "This works..."})

@app.route("/multi", methods=["POST"])
def multi():
    if request.method == "POST":
        try:
            text = request.form.get('brand')
            return jsonify({"success": drugProcess(drugSearch(text))})
        except:
            return jsonify({"failure": "No drug"})

    
@app.route("/pill", methods=["POST"])
def pill():
    if request.method == "POST":
        imprint = request.form.get('imprint')
        shape = request.form.get('shape')
        color = request.form.get('color')
        try:
            return jsonify({"success": pillImage(imprint, shape, color)})
        except:
            return jsonify({"failure": "No pill"})

""" 
with open('data.json', 'w') as f:
    json.dump(drugProcess(drugSearch("advil")), f, indent=4)

"""


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8081)))

