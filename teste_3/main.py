import sqlite3
import os
import pandas as pd
import re
from getfiles import get_documents

connection = sqlite3.connect("sqlite.db")
cursor = connection.cursor()
get_documents()

def sanitize_csv(file_csv , file_name):
    f = re.sub("^.+\n+\s", "", file_csv)
    sanitized_file = open(f"./files/{file_name}", "w")
    sanitized_file.write(f)
    sanitized_file.close()

def fixed_df(df):
    if 'VL_SALDO_INICIAL' not in df.columns:
        df['VL_SALDO_INICIAL'] = ''

def load_files(file_list):
    print('Fazendo LOAD dos Arquivos...')
    for file_name in file_list:
        file_csv = open(f'./files/{file_name}', 'r' ,encoding=  "ISO-8859-1").read()
        if re.match('^.+\n+\s', file_csv):
            sanitize_csv(file_csv, file_name)
           
        df = pd.read_csv(f'./files/{file_name}', on_bad_lines="skip", sep = ';' , encoding=  "ISO-8859-1")
        if 'cadop' in file_name:
            df.to_sql('cadop', connection, if_exists='append', index = False)
        else:
            fixed_df(df)
            df.to_sql('demo_cont', connection, if_exists='append', index = False)
    print('LOAD Finalizado !!!')

file_list = os.listdir('./files')
load_files(file_list)
