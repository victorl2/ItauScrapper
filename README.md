# Itaú Scraper

Scraper para obter dados do banco [Itaú](itau.com.br):  **extrato, cartões de crédito e investimentos**.

## Motivação
Como a maioria dos bancos, o Itaú não disponibiliza APIs para consultas de dados bancários a seus clientes. Antigas implementações disponíveis online, como [bankscraper](https://github.com/kamushadenes/bankscraper), estão em sua maioria defasadas. Desta forma foi necessário a criação deste repositório para interagir com o banco Itaú, a fim de obter os dados desejados.

## Funcionamento
Com o objetivo de obter as credenciais necessárias, um navegador é utilizado através com [playwright](https://playwright.dev/python/) para realizar o **login** no [banco Itaú](itau.com.br). Após o login, de posse das informações/credenciais necessárias, é possível realizar as consultas desejadas diretamente via **requisições HTTP**.


## Instalação
É necessário possuir [Python 3.9.6](https://www.python.org/downloads/) (ou superior) instalado.

Adicione as dependências do projeto 
```bash
pip install -r requirements.txt
```

## Utilização
Vá até a raiz do projeto e execute o comando:
```python
python src/main.py
```

