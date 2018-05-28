from flask import Flask, render_template, request, redirect, url_for
from string import Template

import pymongo
client = pymongo.MongoClient('localhost', 27017)
db = client.enendb
co = db.enenco

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import re
import urllib.request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post', methods=['POST'])
def post():
    search = request.form['search']
    results = []
    for x in search.split():
      
      result = {}
      result["word"] = x
  
      url = 'https://ejje.weblio.jp/content/' + x.replace(' ','+')
      response = urllib.request.urlopen(url).read().decode('utf-8')

      repro = re.search(r'<span class=phoneticEjjeDesc>(.*?)<',response)
      if repro != None:
        result["pro"] = repro.group(1)
      else:
        result["pro"] = ''

      remean = re.search(r'<meta name="twitter:description" content="(.*?)"',response)
      if remean == None:
        continue
      result["mean"] = remean.group(1)

      url = 'https://dictionary.cambridge.org/dictionary/learner-english/' + x.replace(' ','-')
      response = urllib.request.urlopen(url).read().decode('utf-8')
      reenmean = re.search(r'<meta name="description" content="(.*?)Learn more."',response)
      if reenmean == None:
        continue
      result["enmean"] = reenmean.group(1)

      co.insert_one(result)
    
    return render_template('vocaview.html', contents=co.find())

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
