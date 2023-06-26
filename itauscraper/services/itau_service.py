import requests
from typing import Tuple
from services.itau_scraper_service import ItauScraper
from models.auth_model import AuthCredentials, Operation
from models.bank_model import CreditCard, OpenCreditCardInvoice, AccountStatement, Statement
from helpers.formatter_helper import format_account_credentials

itau_scrapper = ItauScraper()

def generate_credentials(agency: str, account: str, password: str) -> AuthCredentials:
    return itau_scrapper.authentication(
        format_account_credentials(agency),
        format_account_credentials(account),
        password
    )

def account_statement(credentials: AuthCredentials) -> AccountStatement:
    response = itau_scrapper.account_statement(credentials)
    if response.status_code != requests.codes.ok:
        return None
    response_body = response.json()
    invoice_statements = response_body['lancamentos']
    account_statements: list[Statement] = []
    for statement in invoice_statements:
        date = statement['dataLancamento']
        amount = statement['valorLancamento']
        description = statement['descricaoLancamento']
        if date is None or amount is None or description == 'SALDO DO DIA':
            continue
        account_statements.append(
            Statement(
                date=date,
                description=description if description is not None else '###',
                value=amount,
            )
        )
    
    balance = response_body['saldoResumido']["saldoContaCorrente"]["valor"]
    return AccountStatement(
        available_balance=float(balance.replace('.', '').replace(',', '.')),
        transactions=account_statements
    )
    
    

def account_balance(credentials: AuthCredentials) -> float:
    statement = account_statement(credentials)
    if statement is None:
        return None
    return statement.available_balance

def list_credit_cards(credentials: AuthCredentials) -> list[CreditCard]:
    response_cards_list = itau_scrapper.credit_cards_list(credentials)
    if response_cards_list.status_code != requests.codes.ok:
        return None

    credit_card_ids = [card['id']
                       for card in response_cards_list.json()['object']['data']]
    response_cards_statement = itau_scrapper.credit_card_details(
        credentials, credit_card_ids)

    if response_cards_statement.status_code != requests.codes.ok:
        return None

    credit_cards: list[CreditCard] = []
    for card in response_cards_statement.json()['object']:
        credit_card = CreditCard(
            id=card['id'],
            name=card['nome'],
            last_digits=card['numero'],
            expiration_date=card['vencimento'],
        )

        limites = card['limites']
        if limites is not None and len(limites) > 0:
            credit_card.total_limit = limites['limiteCreditoValor'],
            credit_card.used_limit = limites['limiteCreditoUtilizadoValor'],
            credit_card.available_limit = limites['limiteCreditoDisponivelValor'],

        faturas = card['faturas']
        if faturas is not None and len(faturas) > 0:
            faturas_abertas = [
                fatura for fatura in faturas if fatura['status'] == 'aberta']
            if len(faturas_abertas) == 0:
                continue

            credit_card.open_invoice = OpenCreditCardInvoice(
                total=faturas_abertas[0]['valorAberto'],
                due_date=faturas_abertas[0]['dataVencimento'],
                close_date=faturas_abertas[0]['dataFechamentoFatura']
            )

        credit_cards.append(credit_card)
    return credit_cards