# Short Url

Essa aplicação apresenta um serviço de encurtamento de URL. Quando uma URL encurtada é acessada, o cliente é redirecionado para a URL original. O sistema também contém uma tela simples para visualizar todas as URLs ativas.

O sistema foi construído em Python com a biblioteca **[Flask](https://flask.palletsprojects.com/)** e **[SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)**. 

## 1. Instalação
### 1.1 Pré-requisitos
Você precisa ter o **[Python 3.8](https://www.python.org/)** instalado, além do gerenciador de pacotes do Python, o **[Python Package Index](https://pypi.org/)**, para instalar as dependências.

Você deve clonar o repositório para um diretório local. Para saber mais sobre o *Git* e seus comandos, siga esse [link](https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository).

### 1.2 Requirements
Após clonar o repositório, entre no diretório da aplicação e instale suas dependências, listadas no arquivo `requirements.txt`:
```bash
$ pip3 install -m requirements.txt
```
Se preferir instalar as dependências em um ambiente virtual para proteger seu sistema de bibliotecas não desejadas e não se confundir com versionamentos de bibliotecas entre projetos, você pode criar um diretório chamado `venv` para instalar as bibliotecas necessárias:
```bash
$ python3 -m venv venv
```
Esse comando vai utilizar o módulo *venv* do Python para criar um diretório que permite iniciar um ambiênte seguro para o desenvolvimento.

Ative o ambiente e instale os requisitos como abaixo:
```bash
# Ativando o ambiente virtual 
$ source venv/bin/activate
# Instalando os requisitos dentro do ambiente
(venv) $ pip install -m requirements.txt
```

### 1.3 Banco de Dados
O sistema utilza o banco de dados MySQL/MariaDB. Crie um banco de dados para a utilização do sistema.

Para configurar o acesso do sistema ao banco é necessário alterar o arquivo `config.py`. No exemplo abaixo o banco será acessado com o usuário *username* e com a senha *password*, modifique esses valores para ambientes de produção. 

```python
ENV = 'production'
DEBUG = False
SQLALCHEMY_ECHO = False
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/db_name'
SQLALCHEMY_TRACK_MODIFICATIONS = False
DOMAIN_BASE_URL = 'http://dns.io/'
JWT_SECRET_KEY = 'change-this-key'
```
Como indicado, o banco está foi configurado para funcionar no mesmo servidor (*localhost*) que o sistema e com o nome de `db_name`. Modifique esses valores com o endereço e o nome do banco, respectivamente, para os valores utilizados por você.

Se quiser utilizar o sistema em modo *debug* você pode criar um outro arquivo `config.py` e colocá-lo em uma pasta chamada `instance` na raiz da aplicação. O sistema vai identificar o arquivo de configuração e utilizá-lo preferencialmente. Segue abaixo uma sugestão do arquivo `config.py` para o modo de desenvolvimento ou *debug*. Note que você deve modificar as credenciais de acesso ao banco da mesma maneira que descrito acima.
```python
ENV = 'develop'
DEBUG = True
SQLALCHEMY_ECHO = True
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/db_name'
SQLALCHEMY_TRACK_MODIFICATIONS = False
DOMAIN_BASE_URL = 'http://127.0.0.1:5000/'
JWT_SECRET_KEY = 'change-this-key'
```
Após as configurações do banco de dados serem realizadas, você pode executar as migrações com o comando abaixo:
```bash
(venv) $ flask db upgrade
```

### 1.4 Running
Para iniciar a aplicação é necessário executar o arquivo `run.py` que vai iniciar um servidor web com o Flask.
```bash
(venv) $ python run.py
 * Serving Flask app "app" (lazy loading)
 * Environment: develop
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 123-456-789
```
Neste exemplo a aplicação está funcionando com o arquivo de configuração de *debug*, assim as rotas e as telas já estão acessíveis como um serviço local.

## 2. Utilização
### 2.1 Criação e leitura de URLs encurtadas
#### POST `/short-urls`
Para criar uma url encurtada é utilizado a rota `/short-urls` com o método *POST* e os seguintes parâmetros enviados como JSON:

| Parâmetro     | Tipo      | Obrigatório | Valor padrão        |
|---------------|-----------|-------------|---------------------|
| original_url  | string    | sim         | -                   |
| shorted_key   | string    | não         | aleatório           |
| expires_at    | datetime  | não         | data atual + 7 dias |

Essa rota retorna um JSON com os mesmos parâmetros mas com a data de expiração calculada se necessário (`expires_at`) e a URL encurtada completa.

#### GET `/<shorted_key>`
Para acessar uma URL encurtada a aplicação deve ser acionada na rota raiz seguida da chave de refência (`shorted_key`) retornada na rota de criação. A aplicação vai redirecionar o acesso para a rota original.

#### GET `/short-urls`
Essa rota retorna uma lista de URLs encurtadas juntamente com os valores de paginação.

### 2.2 Testando a aplicação
Os testes da aplicação são realizados com a utilização da biblioteca **[pytest](https://docs.pytest.org/)**. Para executar os testes é necessário ativar o ambiente virtual e executar o comando `pytest` na raiz da aplicação:
```bash
# Ativando o ambiente virtual 
$ source venv/bin/activate
# Instalando os requisitos dentro do ambiente
(venv) $ pytest
==================================== test session starts ====================================
platform linux -- Python 3.8.2, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: /path/to/short_url
collected 1 item                                                                                                                                                                                     

test/test_app.py .                                                                     [100%]

===================================== 1 passed in 0.65s =====================================
```
