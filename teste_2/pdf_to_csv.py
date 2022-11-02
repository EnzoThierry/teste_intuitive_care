import camelot
import pandas as pd
import zipfile
import os


print('Convertendo PDF para tabelas CSV...')
tables = camelot.read_pdf('./Anexo_1.pdf', process_background=True, pages='3-100')
tables[0].to_csv('./convertido.csv', sep=";")





def zip_file(name, path): #ultima def zip
    print('Comprimindo dados...')
    handle = zipfile.ZipFile(name, 'w')
    os.chdir(path)

    for x in os.listdir(path):
        if x.endswith('.csv'):
            handle.write(x, compress_type= zipfile.ZIP_DEFLATED)
    print('Dados comprimidos!')
    handle.close()
    #os.makedirs('./files', exist_ok=True)


zip_file('Teste_Enzo_Thierry.zip', './files') #'Teste_Intuitive_Care_Enzo_Thierry.zip'
