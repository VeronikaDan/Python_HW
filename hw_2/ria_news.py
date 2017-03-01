import urllib.request
import re
import json
import lxml.html
import os
import requests
import time

def getTree(url):    
    response = requests.get(url)
    if response.status_code < 400:
        req = urllib.request.urlopen(url)
        html = req.read().decode('utf-8')
        tree = lxml.html.fromstring(html)
        return tree
    else:
        return False

def dates():
    year = ['2016']
    month = ['09']
    day = ['01','02','03','04','05','06','07','08','09','10','11','12',
           '13','14','15','16','17','18','19','20','21','22','23','24',
           '25','26','27','28','29','30','31']
    themes = ['technology']
    return themes, year, month, day

def getDates(themes, year, month, day):
    refs = []
    for t in themes:
        for y in year:
            if y == '2015':
                mon = month[6:]
            else:
                mon = month
            for m in mon:
                if m in ['04', '06', '09', '11']:
                    da = day[:-1]
                elif m == '02':
                    da = day[:29]
                else:
                    da = day
                for d in da:
                    ref = 'https://ria.ru/' + t + '/' + y + m + d + '/'
                    refs.append(ref)      
    return refs

def getRefDateName(dates):
    refs = []
    for d in dates:        
        response = requests.get(d)
        if response.status_code < 400:
            req = urllib.request.urlopen(d)
            html = req.read().decode('utf-8')
            pat = d[14:] + '[0-9]+\.html'
            ref = re.findall(pat,html)
            for r in ref:
                rdn = ['https://ria.ru/' + r, d[-9:-1], r[-15:-5]]
                refs.append(rdn)
        time.sleep(0.5)
    return refs    

def getMeta(tree):
    title = tree.xpath('.//title/text()')[0]
    ria = re.search('\s-\sРИА\sНовости,\s[0-9.]+', title).group(0)
    l = -len(ria)
    title = title[:l]
    date = tree.xpath('.//head/meta[@property="article:published_time"]')[0].get('content')
    return date, title

def getText(tree):
    ps = tree.xpath('.//div[@itemprop="articleBody"]/p/text()')
    text = ''
    for sent in ps:
        sent = sent.replace('/ха0',' ')
        text = text + sent + ' '
    return text

def countWords(text):
    for i in '.,:;?!()—"':
        text = text.replace(i, '')
    t = text.split()
    count = len(t)
    return count

def writeText(text, date, name):
    d = date[:4] + '/' + date[4:6] + '/' + date[6:8] + '/'
    pa = 'C:/Users/Вероника/Documents/ВШЭ/RIA/plaintexts/' + d
    os.makedirs(pa, exist_ok=True)
    path = pa + name + '.txt'
    f = open(path, 'w', encoding = 'utf-8')
    f.write(text)
    f.close()
    return path[32:]

def writeMeta(path, date, title, url, wordcount):
    path_meta = 'C:/Users/Вероника/Documents/ВШЭ/RIA/meta.tsv'
    if os.path.exists(path_meta):
        f = open(path_meta, 'a', encoding = 'utf-8')
    else:
        f = open(path_meta, 'w', encoding = 'utf-8')    
    f.write(path + '\t-\t' + date + '\tRIA-News\t' + title + '\t' + url + '\t' + wordcount + '\n')  
    f.close()

def writeInJson(d, name):
    f = open(name + '.json', 'w', encoding = 'utf-8')
    json.dump(d, f, indent = 2, ensure_ascii = False)
    f.close()    
    
def doAll():
    d = dates()
    date = getDates(d[0], d[1], d[2], d[3])
    refs = getRefDateName(date)
    for rdn in refs:
        tree = getTree(rdn[0])
        if tree != False:
            text = getText(tree)
            path = writeText(text, rdn[1], rdn[2])
            count = countWords(text)
            dt = getMeta(tree)
            print(dt[1])
            writeMeta(path, dt[0], dt[1], rdn[0], str(count))
        time.sleep(0.5)

if __name__ == '__main__':
    doAll()
