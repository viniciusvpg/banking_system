import time

####################################
# Desenvolvedor: Vinicius Garcia   #
# Data: 06/06/2025                 #
# Descrição: Sistema bancário      #
####################################

class BankSystem():
    def __init__(self):
        self.accounts = {}
        self.initial_balance = 0
        self.max_account_number = 10049  #simulado busca da maior conta
        self.login_name = ''
        self.login_account_number = ''
        self.max_withdrawal = 1000  
        self.count_withdrawals = 0 
        self.show_menu()

    def show_menu(self):
        menu = f"""\n
        ____________________________________\n
        Bem-vindo ao Sistema Bancário {self.login_name}!

        1. Criar conta
        2. Acessar conta
        3. Depositar
        4. Sacar
        5. Consultar saldo
        6. Sair

        Escolha uma opção: """

        print(menu, end="")

        while True:
            choice = input().strip()
            if choice == '1':
                self.create_account()

            elif choice == '2':
                self.login()

            elif choice == '3':
                self.deposit()

            elif choice == '4':
                self.withdraw()

            elif choice == '5':
                self.get_balance()

            elif choice == '6':
                print("\nSaindo do sistema. Até logo!")
                break
            else:
                print("\nOpção inválida. Tente novamente.")
                time.sleep(2)
                self.show_menu()

    def create_account(self):
        name = input("\nDigite o nome do titular da conta: ").strip()
        if name:
            account_number = self.max_account_number + 1
            self.accounts[account_number] = [name, self.initial_balance]
            self.max_account_number = account_number
            print(f"Conta criada com sucesso! Número da conta: {account_number}, Titular: {name}, Saldo inicial: {self.initial_balance}")
            time.sleep(3)  
            self.show_menu()
        else:
            print("Nome inválido. Tente novamente.")
            time.sleep(3)
            self.show_menu()

    def login(self):
        account_number = int(input("\nDigite o número da conta: ").strip())
        name = input("Digite o nome do titular da conta: ").strip()

        if account_number in self.accounts and self.accounts[account_number][0] == name:
            print(f"\nBem-vindo, {name}! Você está logado na conta {account_number}.")
            self.login_name = name
            self.login_account_number = account_number 
            time.sleep(2)
            self.show_menu()
        else:
            print("Conta não encontrada. Verifique o número da conta e o nome do titular.")
            time.sleep(3)
            self.show_menu()

    def deposit(self):
        if self.login_account_number == '':
            print("\nVocê precisa estar logado para realizar um depósito.")
            time.sleep(3)
            self.show_menu()
        
        else:
            amount = float(input("\nDigite o valor a ser depositado: ").strip())
            if amount <= 0:
                print("Não é possível depositar um valor negativo ou zero.")
            
            else:
                self.accounts[self.login_account_number][1] += amount
                print(f"Depósito de R$ {amount:.2f} realizado com sucesso! Saldo atual: R$ {self.accounts[self.login_account_number][1]:.2f}")
                time.sleep(3)
                self.show_menu()

    def withdraw(self):
        if self.count_withdrawals == 3:
            print("Você atingiu o limite de saques diários. Tente novamente amanhã.")
            time.sleep(3)
            self.show_menu()
            return
        
        if self.login_account_number == '':
            print("\nVocê precisa estar logado para realizar um saque.")
            time.sleep(3)
            self.show_menu()
            return
        
        else:
            amount = float(input("\nDigite o valor a ser sacado: ").strip())
            if amount <= 0:
                print("\nNão é possível sacar um valor negativo ou zero.")
                time.sleep(3)
                self.show_menu()

            elif amount > self.max_withdrawal:
                print(f"\nO valor máximo para saque é R$ {self.max_withdrawal:.2f}.")
                time.sleep(3)
                self.show_menu()
            
            elif self.accounts[self.login_account_number][1] < amount:
                print("\nSaldo insuficiente para realizar o saque.")
                time.sleep(3)
                self.show_menu()

            else:
                self.accounts[self.login_account_number][1] -= amount
                self.count_withdrawals += 1
                print(f"Saque de R$ {amount:.2f} realizado com sucesso! Saldo atual: R$ {self.accounts[self.login_account_number][1]:.2f}")
                time.sleep(3)
                self.show_menu()

    def get_balance(self):
        if self.login_account_number == '':
            print("\nVocê precisa estar logado para consultar o saldo.")
            time.sleep(3)
            self.show_menu()
        
        else:
            balance = self.accounts[self.login_account_number][1]
            print(f"\nSaldo atual da conta {self.login_account_number}: R$ {balance:.2f}")
            time.sleep(3)
            self.show_menu()

if __name__ == "__main__":
    bank = BankSystem()
    
