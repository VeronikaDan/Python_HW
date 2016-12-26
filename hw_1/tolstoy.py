import re
import json

def getTranslit():
    translit = {}
    kirlat = open('kir_to_lat.tsv', 'r', encoding = 'utf-8')
    for stroka in kirlat:
        stroka = stroka.split()
        translit[stroka[0]] = stroka[1]
    kirlat.close()
    return translit

def getText(fileName):
    f = open(fileName, 'r', encoding = 'utf-8')
    alltext = f.readlines()
    f.close()
    return alltext

def writeInFile(text):
    f = open('1.json', 'w', encoding = 'utf-8')
    json.dump(text, f, indent = 2, ensure_ascii = False)
    f.close()

def searchInStroka(stroka):
    symbols = list(stroka)
    i = len(symbols) - 1
    kir = '[А-Яа-я]'
    lat = '[A-Za-z]'
    wrong = []
    translit = getTranslit()
    for k in range(i):
        if re.search(lat, symbols[k]):
            if re.search(kir, symbols[k+1]):
                wrong.append(k)
    return wrong

def errorsInText(m):
    i = 0
    errors = {}
    for stroka in m:
        wrong = searchInStroka(stroka)
        if len(wrong) != 0:
            errors[i] = wrong        
        i += 1
    return errors

def searchErrors():
    text = getText('Полное собрание сочинений. Том 23..xhtml')
    errors = errorsInText(text)
    return errors

def correctStroka(s, num):
    transl = getTranslit()
    newStroka = ''
    chars = list(s)
    k = len(chars)
    for m in range(k):
        if m in num:
            if chars[m] in transl:
                newStroka += transl[chars[m]]
            else:
                newStroka += chars[m]
        else:
            newStroka += chars[m]
    return newStroka

def correct(file):
    fileCorr = file[:-6] + '-corr.xhtml'
    f = open(fileCorr, 'w', encoding = 'utf-8')
    errors = searchErrors()
    text = getText(file)
    i = 0
    for s in text:
        if i in errors:
            f.write(correctStroka(s, errors[i]))
        else:
            f.write(s)
        i += 1
    f.close()

if __name__ == '__main__':
    writeInFile(searchErrors())
    correct('Полное собрание сочинений. Том 23..xhtml')
