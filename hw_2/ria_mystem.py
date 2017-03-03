import os
from subprocess import call
dirs = os.walk('C:/Users/Вероника/Documents/ВШЭ/RIA/plaintexts')
for dir in dirs:
    #дублируем каталог текстов
    morph_dir = 'morph_' + dir[0] + '/'
    os.makedirs(os.path.dirname(new_dir), exist_ok = True)
    files = dir[2]
    for file in files:
        input_f = dir[0] + '/' + file
        output_f = morph_dir + file
        #передаем команду запуска mystem в командную строку
        mystem_call = 'mystem.exe -id ' + input_f + output_f
        call(mystem_call)
