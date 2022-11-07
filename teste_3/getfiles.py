import requests
from bs4 import BeautifulSoup
import re
import zipfile
import os
from datetime import datetime


url = 'http://ftp.dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/'


def get_documents():
    print('Buscando Arquivos...')
    year = datetime.now().year
    pages = []
    file_links = []
    for i in range(2):
        url_year = f"{url}{year - i}/"
        page = requests.get(url_year)
        pages.append(page)
        soup = BeautifulSoup(page.text, 'html.parser')
        links = soup.find_all('a', href=True)
        for link in (links):
            if re.match(r".+(.zip)", link.text):
                file_links.append(f"{url_year}{link.text}")

    download_documents(file_links)


def download_documents(link_list):
    for link in link_list:
        res = requests.get(link)
        file_name = re.search('.+/(\w+.zip)', link).group(1)
        os.makedirs('./files', exist_ok=True)
        with open(f"./files/{file_name}", 'wb') as f:
            f.write(res.content)
    for file in os.listdir('./files'):
        try:
            with zipfile.ZipFile(f"./files/{file}") as zip:
                zip.extractall('./files')
        except:
            continue

    delete_zipfiles('./files')
    print('Arquivos Baixados com Sucesso !!!')

def delete_zipfiles(path):
    zipfiles = os.listdir(path)
    for zipfile in zipfiles:
        if zipfile.endswith('.zip'):
            os.remove(f"{path}/{zipfile}")
    