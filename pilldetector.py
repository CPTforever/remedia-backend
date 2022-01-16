from cmath import pi
from turtle import color
from flask import Flask, request, jsonify, json
from flask_cors import CORS
import io
import os
import requests
from bs4 import BeautifulSoup
import re
import json
from requests.api import head

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

CLEANR = re.compile('<.*?>') 

def cleanhtml(raw_html):
    cleantext = re.sub(CLEANR, "", str(raw_html))  
    return cleantext

imprint = "G 12".replace(" ", "+")
color = "white"
shape = "oval"
pillURL = "https://www.drugs.com/imprints.php?imprint={}&color={}&shape={}".format(imprint, colorList[color], shapeList[shape])
print(pillURL)

# Searching for the drug
page = requests.get(pillURL)
soup = BeautifulSoup(page.content, "html.parser")
image = []
name = []
for x in soup.find_all('img'):
    a = x.get("src")
    if a[:5] == "https":
        image.append(a)
for x in soup.find('div', 'contentBox').findAll('div', class_="pid-details"):
    name.append(cleanhtml(x.li.a))

full = zip(name, image)
for x in full:
    print(x)
"""
page = requests.get(pillURL)
soup = BeautifulSoup(page.content, "html.parser")

# Finding the results
document = soup.find(id="document-list")
results = document.find("ol", class_="results")
drugURL = nlmsearch + results.div.a.get('href')

# Getting the page with drug info
"""