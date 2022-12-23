import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

from flask import Flask, render_template, request, make_response, jsonify

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


@app.route("/webhook", methods=["POST"])
def webhook():
    # build a request object
    req = request.get_json(force=True)
    # fetch queryResult from json
    action =  req.get("queryResult").get("action")
    #msg =  req.get("queryResult").get("queryText")
    #info = "動作：" + action + "； 查詢內容：" + msg
    if(action   ==  "tasteChoice"):
        taste   = req.get("queryResult").get("parameters").get("taste")
        if(taste=="辣"):
            taste = "可能會辣，怕辣的人要小心"
        elif(taste=="不辣"):
            taste = "本產品是不含辣的"

    info    ="您選擇的辣度是:"  +   taste

    collection_ref = db.collection("chicken1")
    docs = collection_ref.get()
    result = ""
    for doc in docs:
        dict=doc.to_dict()
        result += "您可以選擇的品名為："  + dict["name"] +"產品的介紹:"+ dict["say"]
        info +=result


    return make_response(jsonify({"fulfillmentText": info}))





@app.route("/")
def index():
    homepage = "<h1>起家雞 Python 網頁</h1>"
    homepage += "<a href=/search_GG target = _blank>起家雞查詢</a><br>"
    return homepage    
       
      
            





