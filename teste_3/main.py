import os
import pandas as pd
import re
from getfiles import get_documents
import sqlalchemy
from datetime import datetime
from dotenv import load_dotenv
from display_querys import display_tables

load_dotenv()

USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
NAME = os.getenv('NAME')

connection = sqlalchemy.create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{NAME}')   
get_documents()

def sanitize_csv(file_csv , file_name):
    # Remove linhas acima do cabeçalho do CSV.
    f = re.sub("^.+\n+\s", "", file_csv)
    sanitized_file = open(f"./files/{file_name}", "w")
    sanitized_file.write(f)
    sanitized_file.close()

def arrange_dates(df):
    # Trata datas com formatos distintos.
    if len(df['DATA'][df['DATA'].str.match('\d{4}\/\d{2}\/\d{2}')]) > 0:
        df['DATA'] = df['DATA'][df['DATA'].str.match('\d{4}\/\d{2}\/\d{2}')].apply(lambda x: datetime.strptime(x, "%Y/%m/%d"))
    elif len(df['DATA'][df['DATA'].str.match('\d{2}\/\d{2}\/\d{4}')]) > 0:
        df['DATA'] = df['DATA'][df['DATA'].str.match('\d{2}\/\d{2}\/\d{4}')].apply(lambda x: datetime.strptime(x, "%d/%m/%Y"))
    return df

def fixed_df(df):
    arrange_dates(df)
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
            df.columns = ['reg_ans', 'cnpj', 'razao_social', 'nome_fantasia', 'modalidade', 'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'uf', 'cep', 'ddd', 'telefone', 'fax', 'email', 'representante', 'cargo_representante', 'data_reg_ans']
            df["data_reg_ans"] = pd.to_datetime(df["data_reg_ans"], format="%d/%m/%Y")
            df.to_sql('cadop', connection, if_exists='append', index = False)
        else:
            fixed_df(df) 
            df['VL_SALDO_FINAL'].astype
            df.to_sql('demo_cont', connection, if_exists='append', index = False)
    print('LOAD Finalizado !!!')
    display_tables()

file_list = os.listdir('./files')
load_files(file_list)
