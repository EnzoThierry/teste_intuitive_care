import camelot
import pandas as pd
import zipfile

# O codigo le o PDF
print('Convertendo PDF para tabelas CSV...')
tables = camelot.read_pdf('./Anexo_1.pdf', process_background=True, pages='3-180') #Anexo_1 > pages= 3-180 diz quais as paginas 
#Tratando os dataframe com Pandas
table_list = [] 
for i in range(len(tables)):
    table_list.append(tables[i].df)
df = pd.concat(table_list)
#df.columns = ["PROCEDIMENTO","RN","VIGÊNCIA","OD","AMB","HCO","HSO","REF","PAC","DUT","SUBGRUPO","GRUPO","CAPÍTULO"]
df.columns = tables[0].df.iloc[0].tolist() #deixa a tabulacao de forma autonoma
# correcao de legendas
df['OD'].replace("OD" , "Seg. Odontológica" , inplace=True)
df['AMB'].replace("AMB" , "Seg. Ambulatorial" , inplace=True)
df.to_csv('convertido.csv', sep=";" , index=False)

#converte o CSV para .ZIP
handle = zipfile.ZipFile('./Teste_Enzo_Thierry.zip' , 'w')
handle.write(f"./convertido.csv", compress_type=zipfile.ZIP_DEFLATED)
handle.close()
#tables.export('Teste_Enzo_Thierry.csv', f='csv', compress=True)

#requirements
