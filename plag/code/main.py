
from .cosineSim import *
from .htmlstrip import *

#import required modules
import codecs
import traceback
import sys
import operator
import urllib
import simplejson as json
import urllib.request
import urllib.parse
import json
import requests

# Given a text string, remove all non-alphanumeric
# characters (using Unicode definition of alphanumeric).
tags = ''

def getQueries(text,n):
    import re
    sentenceEnders = re.compile('[.!?]')
    sentenceList = sentenceEnders.split(text)
    sentencesplits = []
    for sentence in sentenceList:
        x = re.compile(r'\W+', re.UNICODE).split(sentence)
        x = [ele for ele in x if ele != '']
        sentencesplits.append(x)
    finalq = []
    for sentence in sentencesplits:
        l = len(sentence)
        l=l//n
        index = 0
        for i in range(0,l):
            finalq.append(sentence[index:index+n])
            index = index + n-1
        if index !=len(sentence):
            finalq.append(sentence[len(sentence)-index:len(sentence)])
    return finalq

# Search the web for the plagiarised text
# Calculate the cosineSimilarity of the given query vs matched content on google
# This is returned as 2 dictionaries 

def searchWeb(text,output,c):
    headers = {
        "x-rapidapi-key": "a11b2cd662mshab360b5a103343cp1269d6jsnf45d439ef002",
        "x-rapidapi-host" :"google-search3.p.rapidapi.com"
    }
    query = {
        "q": text+' '+tags,
        "num": 5,
        "lr":"lang_en"
    }
    base_url = f'https://rapidapi.p.rapidapi.com/api/v1/search/'
    url = base_url 
    resp = requests.get("https://rapidapi.p.rapidapi.com/api/v1/search/" + urllib.parse.urlencode(query), headers=headers)


    results = resp.json()
    from collections import defaultdict
    try:
        new_dict = defaultdict(int)
        if ( len(results['results'])):
            for ele in results['results']:
                url = ele['link']
                title = ele['title']
                snippet = ele['description'] 	
                new_dict[url]+=1
                if url in output:
                    output[url] = output[url] + 1
                    c[url] = (c[url]*(output[url] - 1) + cosineSim(text,strip_tags(snippet)))/(output[url])
                else:
                    output[url] = 1
                    c[url] = cosineSim(text,strip_tags(snippet))
    except:
        return
    return 


import threading
def task(count,q,output,c):
    i = 0
    for s in q[:count]:
        searchWeb(s,output,c)
        msg = "\r"+str(i)+"/"+str(count)+"completed..."
        sys.stdout.write(msg)
        sys.stdout.flush()
        i=i+1

def task2(count,q,output,c):
    i = 0
    for s in q[count:2*count]:
        searchWeb(s,output,c)
        msg = "\r"+str(i)+"/"+str(count)+"completed..."
        sys.stdout.write(msg)
        sys.stdout.flush()
        i=i+1

def task3(count,q,output,c):
    i = 0
    for s in q[2*count:3*count]:
        searchWeb(s,output,c)
        msg = "\r"+str(i)+"/"+str(count)+"completed..."
        sys.stdout.write(msg)
        sys.stdout.flush()
        i=i+1
def task4(count,q,output,c):
    i = 0
    for s in q[3*count:4*count]:
        searchWeb(s,output,c)
        msg = "\r"+str(i)+"/"+str(count)+"completed..."
        sys.stdout.write(msg)
        sys.stdout.flush()
        i=i+1
def task5(count,q,output,c):
    i = 0
    for s in q[4*count:5*count]:
        searchWeb(s,output,c)
        msg = "\r"+str(i)+"/"+str(count)+"completed..."
        sys.stdout.write(msg)
        sys.stdout.flush()
        i=i+1
def task6(count,q,output,c):
    i = 0
    for s in q[5*count:6*count]:
        searchWeb(s,output,c)
        msg = "\r"+str(i)+"/"+str(count)+"completed..."
        sys.stdout.write(msg)
        sys.stdout.flush()
        i=i+1

# Use the main function to scrutinize a file for
# plagiarism
def process(data,tag):
    # n-grams N VALUE SET HERE
    global tags 
    tags = tag 
    n=7

    queries = getQueries(data,n)
    q = [' '.join(d) for d in queries]
    #using 2 dictionaries: c and output
    #output is used to store the url as key and number of occurences of that url in different searches as value
    #c is used to store url as key and sum of all the cosine similarities of all matches as value	
    output = {}
    c = {}
    i=1
    count = len(q)
    if count>5:
        count=5
    import time 
    start = time.time()
    t1 = threading.Thread(target=task, args=(count,q,output,c)) 
    t2 = threading.Thread(target=task2, args=(count,q,output,c)) 
    t3 = threading.Thread(target=task3, args=(count,q,output,c)) 
    t4 = threading.Thread(target=task4, args=(count,q,output,c)) 
    t5 = threading.Thread(target=task5, args=(count,q,output,c))
    t6 = threading.Thread(target=task6, args=(count,q,output,c))    
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    end = time.time()
    print(end-start)


    

    # Line --> Search --> Most Related (cosine 60-70%+)-- Highlight <url> 

    print("URL Count\t URL \t\t\t\t\t\t\t\t Match Percentage\n")
    for ele in sorted(output.items(),key=operator.itemgetter(1),reverse=True):
        if c[ele[0]]*100 > 20 and ele[1]>1:
            print(str(ele[1])+"\t\t"+str(ele[0])+" "+str(c[ele[0]]*100.00))
            print("\n")
    print("\nDone!")
    return c,output


if __name__ == "__main__":
    try:
        process()
    except:
        #writing the error to stdout for better error detection
        error = traceback.format_exc()
        print("\nUh Oh!\n"+"Plagiarism-Checker encountered an error!:\n"+error)

