import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

from flask import Flask, render_template, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup
url = "https://www.cheogajip.com.tw/menu/"
Data = requests.get(url)
Data.endcoding = "utf-8"
sp = BeautifulSoup(Data.text, "html.parser")
meals=sp.select(".rightBox .Txt ")
for t in meals:
    name=t.find("a").get("title")
    say=t.find("p").text
    print(say)
    hyperlink=t.find("a").get("href")
    if "辣" in say:
        taste ="辣"
    else:
        taste = "不辣"
    doc = {
      "hyperlink": hyperlink,
      "name": name,
      "say": say,
      "taste":taste,
}
    doc_ref = db.collection("chicken1").document(name)
    doc_ref.set(doc)





@app.route("/")
def index():
    homepage = "<h1>起家雞 Python 網頁</h1>"
    homepage += "<a href=/search_GG target = _blank>起家雞查詢</a><br>"
    return homepage    
       
      
            





