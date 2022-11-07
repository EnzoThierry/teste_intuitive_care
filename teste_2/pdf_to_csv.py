import camelot
import pandas as pd
import zipfile

# O código começa a lê o PDF.
print('Convertendo PDF para tabelas CSV...')
tables = camelot.read_pdf('./Anexo_1.pdf', process_background=True, pages='3-180')
# Tratando os dataframe com Pandas
table_list = [] 
for i in range(len(tables)):
    table_list.append(tables[i].df)
df = pd.concat(table_list)
#df.columns = ["PROCEDIMENTO","RN","VIGÊNCIA","OD","AMB","HCO","HSO","REF","PAC","DUT","SUBGRUPO","GRUPO","CAPÍTULO"]
# Deixa a tabulação das colunas de forma autônoma.
df.columns = tables[0].df.iloc[0].tolist() 
# Correção de legendas "OD" "AMB".
df['OD'].replace("OD" , "Seg. Odontológica" , inplace=True)
df['AMB'].replace("AMB" , "Seg. Ambulatorial" , inplace=True)
df.to_csv('convertido.csv', sep=";" , index=False)

# Converte o CSV para .ZIP
handle = zipfile.ZipFile('./Teste_Enzo_Thierry.zip' , 'w')
handle.write(f"./convertido.csv", compress_type=zipfile.ZIP_DEFLATED)
handle.close()
