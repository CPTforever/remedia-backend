# backend
This was for the Hackathon CruzHacks 2022!

Here is our dev post: https://devpost.com/software/cruzhacks-2022-9suva2

## Setup
```
virtualenv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
python webscraper.py
```

## Usage
There are two requests you can make both of which are post requests. 

It webscrapes https://www.drugs.com/imprints.php to find the pill information. https://www.drugs.com/ for the drug informations.

localhost:port/multi

BRAND: DRUG

localhost:port/pill

IMPRINT: STRING

SHAPE: SHAPE OF PILL

COLOR: COLOR OF PILL

## Drug List generator 
This just creates a json with every drug name in Medline and a link to it in Medline
```
python listgen.py
```

## Attributions
https://www.drugs.com/ For pill information
https://medlineplus.gov/druginformation.html For drug information
