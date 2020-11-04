# -*- coding: utf-8 -*-
# Master script for the plagiarism-checker
# Coded by: Shashank S Rao

#import other modules
from cosineSim import *
from htmlstrip import *
from extractdocx import *

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
        "x-rapidapi-key": "cef4531821mshdd00775dfb4fa11p120050jsn333223957d0a",
        "x-rapidapi-host" :"google-search3.p.rapidapi.com"
    }
    query = {
        "q": text,
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
    

# Use the main function to scrutinize a file for
# plagiarism
def main():
    # n-grams N VALUE SET HERE
    n=9

    t = docxExtract('testdocx.docx')
    queries = getQueries(t,n)
    q = [' '.join(d) for d in queries]
    #using 2 dictionaries: c and output
    #output is used to store the url as key and number of occurences of that url in different searches as value
    #c is used to store url as key and sum of all the cosine similarities of all matches as value	
    output = {}
    c = {}
    i=1
    count = len(q)
    if count>25:
        count=25
    f = open("sampleOut.txt","w")

    for s in q[:count]:
        searchWeb(s,output,c)
        msg = "\r"+str(i)+"/"+str(count)+"completed..."
        sys.stdout.write(msg)
        sys.stdout.flush()
        i=i+1
    

    # Line --> Search --> Most Related (cosine 60-70%+)-- Highlight <url> 

    f.write("URL Count\t URL \t\t\t\t\t\t\t\t Match Percentage\n")
    for ele in sorted(output.items(),key=operator.itemgetter(1),reverse=True):
        if c[ele[0]]*100 > 20 and ele[1]>1:
            f.write(str(ele[1])+"\t\t"+str(ele[0])+" "+str(c[ele[0]]*100.00))
            f.write("\n")

    f.close()
    print("\nDone!")


if __name__ == "__main__":
    try:
        main()
    except:
        #writing the error to stdout for better error detection
        error = traceback.format_exc()
        print("\nUh Oh!\n"+"Plagiarism-Checker encountered an error!:\n"+error)

