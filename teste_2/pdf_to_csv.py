import camelot
import pandas as pd
import zipfile
import os


tables = camelot.read_pdf('./Anexo_1.pdf', pages='4', process_background=True) #Anexo_I > pdf
tables.export('Anexo_1.csv', f='csv', compress=True)
tables[0].to_csv('./Anexo_1.csv')


#tabelas = [] #pandas formatar legenda
#for i in range(1, 7):
#    tabelas.append(tables[i].df)
#tabelas = pd.concat(tabelas)
#tabelas.to_csv('C:/Users/Enzo Thierry/Documents/Atari/DOCS/csv/', index=False)


#def post_process_table(full_table): #incerir legendas
#    full_table["OD"].replace({ "OD": "Seg. Odontológica" }, inplace=True)
#    full_table["AMB"].replace({ "AMB": "Seg. Ambulatorial" }, inplace=True)



def zip_file(name, path): #ultima def
    print('Comprimindo dados...')
    handle = zipfile.ZipFile(name, 'w')
    os.chdir(path)

    for x in os.listdir(path):
        if x.endswith('.csv'):
            handle.write(x, compress_type= zipfile.ZIP_DEFLATED)
    print('Dados comprimidos!')
    handle.close()
    os.makedirs('./files', exist_ok=True)


zip_file('Teste_Enzo_Thierry.zip', './files') #'Teste_Intuitive_Care_Enzo_Thierry.zip'
