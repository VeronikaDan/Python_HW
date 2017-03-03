import urllib.request
import re
import lxml.html
import os
import requests
import time

def getTree(url):    
    try:
        req = urllib.request.urlopen(url)
        html = req.read().decode('utf-8')
        tree = lxml.html.fromstring(html)
        return tree
    except:        
        return False

def dates():
    year = ['2015','2016']
    month = ['01','02','03','04','05','06','07','08','09','10','11','12']
    day = ['01','02','03','04','05','06','07','08','09','10','11','12',
             '13','14','15','16','17','18','19','20','21','22','23','24',
             '25','26','27','28','29','30','31']    
    #нельзя обратиться к дате, не указав тематику
    themes = ['politics','defense_safety', 'society', 'media', 'health',
              'education', 'beauty_medicine', 'economy', 'company', 'world',
              'incidents', 'sport', 'science', 'technology', 'culture', 'religion']
    print('dates are ready')
    return themes, year, month, day

def getUrls(themes, year, month, day):
    #строим все возможные урлы из архива
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
                for t in themes:
                    ref = 'https://ria.ru/' + t + '/' + y + m + d + '/'
                    print('try ' + ref)
                    getArticles(ref)

def getArticles(d):        
    try:
        req = urllib.request.urlopen(d)
        html = req.read().decode('utf-8')
        #ищем в архиве ссылки на конкретные статьи
        pat = d[14:] + '[0-9]+\.html'
        ref = re.findall(pat,html)
        print('got references')
        for r in ref:
            rdn = ['https://ria.ru/' + r, d[-9:-1], r[-15:-5]]
            tree = getTree(rdn[0])
            if tree != False:
                #достаем текст статьи
                text = getText(tree)
                p = writeText(text, rdn[1], rdn[2])
                if p != '0':
                    count = countWords(text)
                    dt = getMeta(tree)
                    writeMeta(p, dt[0], dt[1], rdn[0], str(count))
            else:
                print("can't reach article " + rdn[0])
            time.sleep(0.3)
        print('got articles')
    except:
        print("can't reach url " + d)

def getMeta(tree):
    title = tree.xpath('.//title/text()')[0]
    #убираем лишнее в названии
    if ' - РИА Новости, ' in title:
        title = title[:-26]
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
    #создаем промежуточные папки
    os.makedirs(pa, exist_ok=True)
    p = pa + name + '.txt'
    #проверяем наличие такой статьи у нас
    if os.path.exists(p):
        return '0'
    else:
        f = open(p, 'w', encoding = 'utf-8')
        f.write(text)
        f.close()
        #возвращаем путь к ней
        return p[32:]    

def writeMeta(path, date, title, url, wordcount):
    #дописываем инф-ию о статье в файл meta.tcv (авторов у статей нет)
    path_meta = 'C:/Users/Вероника/Documents/ВШЭ/RIA/meta.tsv'
    if os.path.exists(path_meta):
        f = open(path_meta, 'a', encoding = 'utf-8')
    else:
        f = open(path_meta, 'w', encoding = 'utf-8')    
    f.write(path + '\t-\t' + date + '\tRIA-News\t' + title + '\t' + url + '\t' + wordcount + '\n')  
    f.close()   
    
def doAll():
    d = dates()
    getUrls(d[0], d[1], d[2], d[3])    
        
if __name__ == '__main__':
    doAll()
