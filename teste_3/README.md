# Banco de dados
Esse código primeiro faz a coleta dos dados de maneira automatizada. Em seguida lê os arquivos .CSV e os trata em DataFrame.

Com os dados devidamente tratados o código através das credenciais inseridas faz a comunicação com o bando de dados (MySQL) que por sua vez esta hospedado na AWS.

Após a leitura e o envio para o banco, o código esta pronto para receber as query.
## Instalação

Recomendavel ultilizar um ambiente virtual.

```
$ python -m venv .venv
```

Use este pip para instalar os requerimento nessesarios para o funcionamento.

```bash
$ pip install -r requirements.txt
```

## Uso

Webscraping para coleta dos arquivos do banco.
No terminal execute:
```bash
$ python getfiles.py
```
Load para o Banco.
No terminal execute:
```bash
$ python main.py
```

