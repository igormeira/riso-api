# Recuperação de informações semânticas

## Desenvolvimento
Previamente a instalação do projeto é necessária a instalação do libmysql:

```
sudo apt-get install libmysqlclient-dev
sudo apt-get install python-numpy

```

Para instalar as dependencias necessárias é necessário executar o comando abaixo na pasta do projeto:


```
pip install -r requirements.txt
```

Também é necessário o arquivo de configuração do banco de dados que deve ser criado em `~/.my.cnf`. O conteúdo do arquivo é o seguinte:

```
[RISO]
user=usuarioDoBD
password=SenhaDoUsuario
host=hostDoUsuario
```


Para criar o Banco de dados e populá-lo inicialmente com os dados previamente baixados é necessário:

- executar na pasta script:
```
python inicial_script.py
```

Para executar a api na pasta raiz executar:

```
python run.py

```
