from fastapi import FastAPI
import sqlalchemy
from dotenv import load_dotenv
import os
import pandas as pd
import uvicorn
import json

load_dotenv()

USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
NAME = os.getenv('NAME')

connection = sqlalchemy.create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{NAME}')

app = FastAPI()

@app.get('/test_api')
def get_infos(
    reg_ans: str = "",
    cnpj: str = "",
    razao_social: str = "",
    nome_fantasia: str = "",
    modalidade: str = "",
    logradouro: str = "",
    numero: str = "",
    complemento: str = "",
    bairro: str = "",
    cidade: str = "",
    uf: str = "",
    cep: str = "",
    ddd: str = "",
    telefone: str = "",
    fax: str = "",
    email: str = "",
    representante: str = "",
    cargo_representante: str = "",
    data_reg_ans: str = ""
    ):
    query = f"""
        SELECT * FROM cadop WHERE reg_ans like '%{reg_ans}%'
        and cnpj like '%{cnpj}%'
        and razao_social LIKE '%{razao_social}%'
        AND nome_fantasia LIKE '%{nome_fantasia}%'
        AND modalidade LIKE '%{modalidade}%'
        AND logradouro LIKE '%{logradouro}%'
        AND numero LIKE '%{numero}%'
        AND complemento LIKE '%{complemento}%'
        AND bairro LIKE '%{bairro}%'
        AND cidade LIKE '%{cidade}%'
        AND uf LIKE '%{uf}%'
        AND cep LIKE '%{cep}%'
        AND ddd LIKE '%{ddd}%'
        AND telefone LIKE '%{telefone}%'
        AND fax LIKE '%{fax}%'
        AND email LIKE '%{email}%'
        AND representante LIKE '%{representante}%'
        AND cargo_representante LIKE '%{cargo_representante}%'
        AND data_reg_ans LIKE '%{data_reg_ans}%';
    """
    df = pd.read_sql(sqlalchemy.text(query), connection)
    return json.loads(df.to_json(orient='records', force_ascii=False, date_format="%d/%m/%Y"))



if __name__ == '__main__':

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
