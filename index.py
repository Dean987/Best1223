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
    if (action == "tasteChoice"):
        taste   = req.get("queryResult").get("parameters").get("taste")
        info="您選擇的辣度是:" + taste + "，相關資訊：" + "\n"

        collection_ref = db.collection("chicken1")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict=doc.to_dict()
            if taste  == "全部" :
                result += "品名：" + dict["name"] + "\n"
                result += "介紹：" + dict["say"] +"\n\n"
                result += "網址：" + dict["hyperlink"] +"\n\n"
            elif taste == dict["taste"]:
                result += "品名：" + dict["name"] + "\n"
                result += "介紹：" + dict["say"] +"\n\n"
        info += result

        #info = "動作：" + action + "； 查詢內容：" + msg
    elif (action == "searchMeal"):
        name = req.get("queryResult").get("parameters").get("searchMeal")
        info = "您選擇的餐點是：" + name  + "，相關資訊：" + "\n"

        collection_ref = db.collection("chicken1")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict=doc.to_dict()
            if name in dict["name"]:
                result += "品名：" + dict["name"] + "\n"
                result += "介紹：" + dict["say"] +"\n\n"
                result += "辣度：" + dict["taste"] + "\n"
                result += "網址：" + dict["hyperlink"] +"\n\n" 
        if result == "":
            result += "抱歉，查無相關條件的產品資訊</a>" 
            return result      
        info += result
       
        


    




    return make_response(jsonify({"fulfillmentText": info}))






@app.route("/")
def index():
    homepage = "<h1>起家雞 Python 網頁</h1>"
    homepage += "<a href=/search_GG target = _blank>起家雞查詢</a><br>"
    return homepage    
       
      
            





