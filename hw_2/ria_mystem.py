import os
from subprocess import call

dirs = os.walk('C:/Users/Вероника/Documents/ВШЭ/RIA/plaintexts')
for dir in dirs:
    #дублируем каталог текстов
    d = os.path.dirname(dir[0])
    d = d.replace('plaintexts','mystem')
    os.makedirs(d, exist_ok = True)
    files = dir[2]
    for file in files:
        input_f = dir[0] + '/' + file
        output_f = d + '/' + file
        #передаем команду запуска mystem в командную строку
        mystem_call = 'mystem.exe -id ' + input_f + output_f
        call(mystem_call)
