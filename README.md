# backend
```
virtualenv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
python webscraper.py
```

Use postman to send a request to localhost:8081/multi
with brand: drugName

## Drug List generator 
This just creates a json with every drug name in Medline and a link to it in Medline
```
python listgen.py
```
