import time
import textwrap

####################################
# Desenvolvedor: Vinicius Garcia   #
# Data: 06/06/2025                 #
# Atualizado: 09/06/2025           #
# Descrição: Sistema bancário      #
####################################

class BankSystem():
    def __init__(self):
        self.accounts = []
        self.users_names = {}
        self.agency = '0001'
        self.initial_balance = 0
        self.max_account_number = 100  #simulado busca da maior conta
        self.login_name = ''
        self.login_account_number = ''
        self.max_withdrawal = 1000  
        self.count_withdrawals = 0 
        self.extract = ""
        self.show_menu()

    def show_menu(self):
        menu = f"""\n
        ____________________________________\n
        Bem-vindo ao Sistema Bancário {self.login_name}!

        1. \tCriar conta
        2. \tCriar usuário
        3. \tAcessar conta
        4. \tDepositar
        5. \tSacar
        6. \tConsultar saldo
        7. \tExibir contas cadastradas
        8. \tSair

        Escolha uma opção: """

        print(textwrap.dedent(menu))

        while True:
            choice = input().strip()
            if choice == '1':
                account = self.create_account(self.agency, self.max_account_number, self.users_names)
                if account:
                    self.accounts.append(account)
                self.show_menu()

            elif choice == '2':
                self.create_user(self.users_names)

            elif choice == '3':
                self.login(self.accounts)

            elif choice == '4':
                values = self.deposit(self.login_account_number, self.accounts, self.extract)
                if values:
                    for account in self.accounts:
                        if account['numero_conta'] == self.login_account_number:
                            account['saldo'] = values[0]
                            print(f"\nDepósito realizado com sucesso! Saldo atual: R$ {account['saldo']:.2f}")
                self.show_menu()
                
            elif choice == '5':
                value = input("\nDigite o valor a ser sacado: ").strip()
                values = self.withdraw(value, self.extract, self.login_account_number, self.accounts, self.max_withdrawal, self.count_withdrawals)
                if values:
                    for account in self.accounts:
                        if account['numero_conta'] == self.login_account_number:
                            account['saldo'] -= values[0]
                            self.count_withdrawals += 1
                            print(f"\nSaque realizado com sucesso! Saldo atual: R$ {account['saldo']:.2f}")
                self.show_menu()

            elif choice == '6':
                for account in self.accounts:
                    if account['numero_conta'] == self.login_account_number:
                        balance = account['saldo']
                        break
                self.get_balance(balance, extract=self.extract)

            elif choice == '7':
                self.show_accounts(self.accounts)

            elif choice == '8':
                print("\nSaindo do sistema. Até logo!")
                break
            
            else:
                print("\nOpção inválida. Tente novamente.")
                time.sleep(2)
                self.show_menu()

    def create_user(self, users):
        cpf = input("\nDigite o CPF(sem pontos) do usuário: ").strip()
        usuario_existe = self.filter_user(cpf, users)
        if not usuario_existe:
            name = input("Digite o nome do usuário: ").strip()
            date_of_birth = input("Digite a data de nascimento do usuário (DD-MM-AAAA): ").strip()
            andress = input("Digite o endereço (logradouro, numero - bairro - cidade/estado abreviado): ").strip()

            if name and date_of_birth and andress:
                self.users_names[cpf] = {
                    'name': name,
                    'date_of_birth': date_of_birth,
                    'cpf': cpf,
                    'andress': andress
                }
                print(f"Usuário {name} criado com sucesso! CPF: {cpf}")
                time.sleep(3)  
                self.show_menu()
            else:
                print("Verifique os campos e tente novamente.")
                time.sleep(3)
                self.show_menu()
        
        else:
            print(f"Usuário com CPF {cpf} já existe.")
            time.sleep(3)
            self.show_menu()

    def filter_user(self, cpf, users):
        if cpf in users:
            return True
        else:
            return False

    def create_account(self, agency, account_number, users):
        cpf = input("\nDigite o CPF(sem pontos) do titular da conta: ").strip()
        user = self.filter_user(cpf, users)
        if user:
            new_account_number = account_number + 1
            self.max_account_number = new_account_number
            print(f"Conta criada com sucesso! Número da conta: {new_account_number}, CPF: {cpf}")
            return {"agencia:": agency, "numero_conta": new_account_number, "cpf": cpf, "nome": users[cpf]['name'], "saldo": self.initial_balance}
        else:
            print("Usuário não encontrado. Por favor, crie um usuário primeiro.")
            time.sleep(3)
            self.show_menu()

    def login(self, accounts):
        data = None
        account_number = int(input("\nDigite o Numero da Conta: ").strip())

        for account in accounts:
            if account['numero_conta'] == account_number:
                data = account
                break
            
            print("Conta não encontrada. Verifique o número da conta.")
            time.sleep(3)
            self.show_menu()

        if data:
            print(f"\nBem-vindo {data['nome']}, você está logado na conta {account_number}.")
            self.login_name = data['nome']
            self.login_account_number = account_number 
            time.sleep(2)
            self.show_menu()
        else:
            print("Conta não encontrada. Verifique o número da conta.")
            time.sleep(3)
            self.show_menu()

    def deposit(self, login_account_number, accounts, extract, /):
        if login_account_number == '':
            print("\nVocê precisa estar logado para realizar um depósito.")
            time.sleep(3)
            self.show_menu()
        
        else:
            amount = float(input("\nDigite o valor a ser depositado: ").strip())
            if amount <= 0:
                print("Não é possível depositar um valor negativo ou zero.")
            
            else:
                for account in accounts:
                    if account['numero_conta'] == login_account_number:
                        self.login_account_number = account['numero_conta']
                        balance = account['saldo']
                        balance += amount
                        self.extract += f"Depósito: R$ {amount:.2f}\n"
                        return balance, extract

    def withdraw(self, value, extract, account_number, accounts, max_withdrawal, count_withdrawals):
        if count_withdrawals == 3:
            print("Você atingiu o limite de saques diários. Tente novamente amanhã.")
            time.sleep(3)
            self.show_menu()
            return
        
        if account_number == '':
            print("\nVocê precisa estar logado para realizar um saque.")
            time.sleep(3)
            self.show_menu()
            return
        
        else:
            if int(value) <= 0:
                print("\nNão é possível sacar um valor negativo ou zero.")
                time.sleep(3)
                self.show_menu()

            elif int(value) > max_withdrawal:
                print(f"\nO valor máximo para saque é R$ {max_withdrawal:.2f}.")
                time.sleep(3)
                self.show_menu()

            else:
                for account in accounts:
                    if account['numero_conta'] == account_number:
                        if account['saldo'] < int(value):
                            print("\nSaldo insuficiente para realizar o saque.")
                            time.sleep(3)
                            self.show_menu()
                            return

                        self.extract += f"Saque: R$ {int(value):.2f}\n"
                        return int(value), extract

                time.sleep(3)
                self.show_menu()

    def get_balance(self, balance, /, *, extract=''):
        if self.login_account_number == '':
            print("\nVocê precisa estar logado para consultar o saldo.")
            time.sleep(3)
            self.show_menu()
        
        else:
            print(f"\nExtrato da conta:\n {extract}")
            print(f"\nSaldo Total: R$ {balance:.2f}")
            print("Pressione Enter para ver o extrato.")
            input()
            self.show_menu()

    def show_accounts(self, accounts):
        if not accounts:
            print("\nNenhuma conta cadastrada.")
        else:
            print("\nContas cadastradas:")
            for account in accounts:
                print(f"Agência: {account['agencia:']}, Número da Conta: {account['numero_conta']}, Nome: {account['nome']}")
        
        print("\nPressione Enter para voltar ao menu principal.")
        input()
        self.show_menu()

if __name__ == "__main__":
    bank = BankSystem()
    
