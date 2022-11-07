import sqlalchemy
from dotenv import load_dotenv
import os
from tabulate import tabulate
import pandas as pd

load_dotenv()

USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
NAME = os.getenv('NAME')

connection = sqlalchemy.create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{NAME}')   

def display_tables():
    print("Quais as 10 operadoras que mais tiveram despesas com EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR no último trimestre?")
    df = pd.read_sql(sqlalchemy.text("""
        SELECT cp.nome_fantasia, cp.razao_social,
        dc.VL_SALDO_INICIAL - dc.VL_SALDO_FINAL as valor_gasto
        FROM cadop cp JOIN demo_cont dc
        ON cp.reg_ans = dc.REG_ANS 
        WHERE dc.DESCRICAO LIKE "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%" 
        AND dc.`DATA` BETWEEN DATE_SUB(NOW(), INTERVAL 3 MONTH) AND NOW()
        ORDER BY dc.VL_SALDO_FINAL DESC
        LIMIT 10;
"""), connection)
    df['valor_gasto'] = df['valor_gasto'].astype(int)
    print(tabulate(df, headers = 'keys', tablefmt = 'psql'))
    print("Quais as 10 operadoras que mais tiveram despesas com EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR no último ano?")
    df = pd.read_sql(sqlalchemy.text("""
        SELECT cp.nome_fantasia, cp.razao_social,
        dc.VL_SALDO_INICIAL - dc.VL_SALDO_FINAL as valor_gasto
        FROM cadop cp JOIN demo_cont dc
        ON cp.reg_ans = dc.REG_ANS 
        WHERE dc.DESCRICAO LIKE "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%" 
        AND dc.`DATA` BETWEEN DATE_SUB(NOW(), INTERVAL 1 YEAR) AND NOW()
        ORDER BY valor_gasto DESC
        LIMIT 10;
    """), connection)
    df['valor_gasto'] = df['valor_gasto'].astype(int)
    print(tabulate(df, headers = 'keys', tablefmt = 'psql'))

display_tables()
