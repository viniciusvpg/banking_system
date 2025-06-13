from datetime import datetime
import textwrap
from abc import ABC, abstractmethod

####################################
# Desenvolvedor: Vinicius Garcia   #
# Data: 06/06/2025                 #
# Atualizado: 12/06/2025           #
# Descrição: Sistema bancário      #
####################################

class Client:
    def __init__(self, andress):
        self.address = andress
        self.accounts = []

    def make_transaction(self, account, transaction):
        transaction.register(account)

    def add_account(self, account):
        self.accounts.append(account)

class NaturalPerson(Client):
    def __init__(self, name, cpf, date_of_birth, address):
        super().__init__(address)
        self.name = name
        self.cpf = cpf
        self.date_of_birth = date_of_birth

class Account():
    def __init__(self, account_number, client):
        self._account_number = account_number
        self._client = client
        self._balance = 0.0
        self._extract = History()
        self._agency = "0001"
    
    @classmethod
    def new_account(cls, client, account_number):
        return cls(account_number, client)
    
    @property
    def balance(self):
        return self._balance
    
    @property
    def account_number(self):
        return self._account_number
    
    @property
    def agency(self):
        return self._agency
    
    @property
    def client(self):   
        return self._client
    
    @property
    def extract(self):
        return self._extract
    
    def withdraw(self, amount):
        balance = self.balance
        max_withdraw = amount > balance
        if max_withdraw:
            print("Saldo insuficiente para saque.")

        elif balance > 0:
            self._balance -= amount
            print(f"Saque realizado com sucesso!")
            return True

        else:
            print("Informe um valor válido para saque.")

        return False 
    
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print(f"Depósito realizado com sucesso!")
        else:
            print("Informe um valor válido para depósito.")
            return False
        return True
      
class CurrentAccount(Account):
    def __init__(self, account_number,  client, max_withdraw_value=500, max_withdraw=3):
        super().__init__(account_number, client)
        self.max_withdraw_value = max_withdraw_value
        self.max_withdraw = max_withdraw
    
    def withdraw(self, amount):
        number_withdraws = len(
            [transition for transition in self.extract.transactions 
             if transition["tipo"] == "Saque"]) #Withdraw.__name__])
        
        exceeded_withdraw_value = amount >= self.max_withdraw_value
        exceeded_withdraw = number_withdraws >= self.max_withdraw


        if exceeded_withdraw_value:
            print("Valor de saque excedido.")
            return False
        if exceeded_withdraw:
            print("Número máximo de saques excedido.")
            return False
        
        else:
            return super().withdraw(amount)
        
        return False
    
    def __str__(self):
        return f"""
        Agência: {self.agency}
        Conta: {self.account_number}
        Titular: {self.client.name}
        """
    
class History():
    def __init__(self):
        self._transactions = []
    
    @property
    def transactions(self):
        return self._transactions
    
    def add_transaction(self, transaction):
        self._transactions.append(
            {
                "tipo": transaction.__class__.__name__,
                "valor": transaction.amount,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S") 
            }
        )

class Transaction(ABC):
    @property
    @abstractmethod
    def amount(self):
        pass

    @abstractmethod
    def register(self, account):
        pass

class Withdraw(Transaction):
    def __init__(self, amount):
        self._amount = amount

    @property  
    def amount(self):
        return self._amount

    def register(self, account):
        sucess_transaction = account.withdraw(self._amount)
        if sucess_transaction:
            account.extract.add_transaction(self)

class Deposit(Transaction):
    def __init__(self, amount):
        self._amount = amount

    @property
    def amount(self):
        return self._amount
    
    def register(self, account):
        sucess_transaction = account.deposit(self._amount)
        if sucess_transaction:
            account.extract.add_transaction(self)

def show_menu():
    menu = """\n
    Bem-vindo ao Sistema Bancário!
    
    [1]\tDepositar
    [2]\tSacar
    [3]\tConsultar Extrato
    [4]\tCriar Conta
    [5]\tAdicionar Cliente
    [6]\tConsultar Cliente

    [0]\tSair
    """
    return input(textwrap.dedent(menu))

def main():
    clients = []
    accounts = []


    while True:
        option = show_menu()

        if option == "1":
            deposit(clients)

        elif option == "2":
            withdraw(clients)

        elif option == "3":
            show_extract(clients)

        elif option == "4":
            account_number = len(accounts) + 1
            create_account(account_number, clients, accounts)

        elif option == "5":
            add_client(clients)

        elif option == "6":
            show_client(clients)

        elif option == "0":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def deposit(clients):
    cpf = input("Informe o CPF do cliente: ")
    client = filter_client(cpf, clients)

    if not client:
        print("Cliente não encontrado.")
        return
    
    amount = float(input("Informe o valor do depósito: "))
    transition = Deposit(amount)

    account = client_recover_account(client)
    if not account:
        return

    client.make_transaction(account, transition)

def withdraw(clients):
    cpf = input("Informe o CPF do cliente: ")
    client = filter_client(cpf, clients)

    if not client:
        print("Cliente não encontrado.")
        return
    
    amount = float(input("Informe o valor do saque: "))
    transition = Withdraw(amount)

    account = client_recover_account(client)
    if not account:
        return

    client.make_transaction(account, transition)

def filter_client(cpf, clients):
    client_found = [client for client in clients if getattr(client, 'cpf', None) == cpf]
    return client_found[0] if client_found else None

def client_recover_account(client):
    if not client.accounts:
        print("Cliente não possui conta.")
        return None
    
    return client.accounts[0]

def show_extract(clients):
    cpf = input("Informe o CPF do cliente: ")
    client = filter_client(cpf, clients)

    if not client:
        print("Cliente não encontrado.")
        return
    
    account = client_recover_account(client)
    if not account:
        return

    print(f"\n============= Extrato da conta ============= ")
    transitions = account.extract.transactions
    extract = ''

    if not transitions:
        extract = "Nenhuma transação realizada."
    else:
        for transition in transitions:
            extract += f"\n{str(transition['tipo']).replace('Deposit', 'Depósito').replace('Withdraw', 'Saque')}: R$ {transition['valor']:.2f}"

    print(extract)
    print(f"\nSaldo atual: \tR$ {account.balance:.2f}") 
    print(f"=============================================")

def create_account(account_number, clients, accounts):
    cpf = input("Informe o CPF do cliente: ")
    client = filter_client(cpf, clients)

    if not client:
        print("Cliente não encontrado.")
        return
    
    account = CurrentAccount.new_account(client, account_number)
    accounts.append(account)
    client.add_account(account)

    print(f"=== Conta criada com sucesso! ===")

def list_accounts(accounts):
    for accont in accounts:
        print("=" * 50)
        print(textwrap.dedent(str(accont)))

def add_client(clients):
    cpf = input("Informe o CPF do cliente: ")
    client = filter_client(cpf, clients)

    if client:
        print("Cliente já cadastrado.")
        return

    name = input("Informe o nome do cliente: ")
    date_of_birth = input("Informe a data de nascimento do cliente (DD/MM/AAAA): ")
    address = input("Informe o endereço do cliente: ")

    new_client = NaturalPerson(name=name, cpf=cpf, date_of_birth=date_of_birth, address=address)

    clients.append(new_client)
    print(f"=== Cliente {new_client.name} adicionado com sucesso!===")

def show_client(clients):
    cpf = input("Informe o CPF do cliente: ")
    client = filter_client(cpf, clients)

    if not client:
        print("Cliente não encontrado.")
        return
    
    print(f"\n=== Cliente: {client.name} ===")
    print(f"CPF: {client.cpf}")
    print(f"Data de Nascimento: {client.date_of_birth}")
    print(f"Endereço: {client.address}")
    
    if client.accounts:
        print("Contas:")
        for account in client.accounts:
            print(f" - Conta {account.account_number} (Agência: {account.agency})")
    else:
        print("Nenhuma conta associada ao cliente.")

if __name__ == "__main__":
    main()
