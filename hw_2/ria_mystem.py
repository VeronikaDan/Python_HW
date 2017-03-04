import os
from subprocess import call

dirs = os.walk('plaintexts')
for dir in dirs:
    #дублируем каталог текстов
    m_dir = dir[0] + '/'
    m_dir = m_dir.replace('plaintexts','mystem')
    os.makedirs(os.path.dirname(m_dir), exist_ok=True)
    files = dir[2]
    for file in files:
        input_f = dir[0] + '/' + file
        output_f = m_dir + file
        #передаем команду запуска mystem в командную строку
        mystem_call = 'mystem.exe -id ' + input_f + ' ' + output_f
        call(mystem_call)
