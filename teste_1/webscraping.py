import requests
from bs4 import BeautifulSoup
import re
import zipfile
import os


# Essa função recebe o link e os parametros para baixar arquivos
def get_attachments(): 
    attachments_list = {}
    page = requests.get(
        f'https://www.gov.br/ans/pt-br/assuntos/consumidor/o-que-o-seu-plano-de-saude-deve-cobrir-1/o-que-e-o-rol-de-procedimentos-e-evento-em-saude')
    soup = BeautifulSoup(page.text, 'html.parser')
    attachments = soup.findAll("p", class_="callout")
    for attachment in attachments:
        if "Anexo" in attachment.text:
            href = attachment.contents[0]['href']
            extesion = re.findall("\.\w+$", href)[0]
            anexo = re.findall("^Anexo\s+\w+", attachment.text)[0]
            attachments_list[anexo + extesion] = href
    return attachments_list

# Função para download. ela mostra o caminho/local para armazenar
def download_files():
    attachments_list = get_attachments()
    for attachment in attachments_list:
        res = requests.get(attachments_list[attachment])
        filename = (attachment).replace(" ", "_")
        os.makedirs('./files', exist_ok=True)
        with open(f"./files/{filename}", 'wb') as f:
            f.write(res.content)

# Função converte os arquivos baixados em determinada pasta
def zip_file(name):
    print('Comprimindo dados...')
    handle = zipfile.ZipFile(f"./{name}", 'w')
    for x in os.listdir("./files"):
        handle.write(f"./files/{x}", compress_type=zipfile.ZIP_DEFLATED)
    print('Dados comprimidos!')
    handle.close()

# Por fim chama as funções executando-as
download_files()
zip_file("files.rar")
