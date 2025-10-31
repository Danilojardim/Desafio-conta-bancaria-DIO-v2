from abc import ABC, abstractmethod
from datetime import datetime, date

# ===================== MENU =====================
def menu(): 
    menu = """ 
    ================ MENU ================
    +\t[1] Novo Usuário                 +
    +\t[2] Criar Conta                  +
    +\t[3] Depositar                    +
    +\t[4] Sacar                        + 
    +\t[5] Extrato                      +
    +\t[0] Sair                         +
    ======================================
    """
    return input(menu)

# ===================== CLASSES BASE =====================

class Cliente:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco
        self.contas = []  # cada cliente pode ter várias contas

    def adicionar_conta(self, conta):
        """Associa uma nova conta ao cliente"""
        self.contas.append(conta)
        print(f"✅ Conta {conta._numero} adicionada ao cliente {self.nome}.")

    def realizar_transacao(self, conta, transacao):
        """Permite que o cliente realize uma transação (depósito/saque)"""
        transacao.registrar(conta)

# ===================== CONTA =====================

class Conta:
    def __init__(self, cliente, numero, agencia):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @classmethod
    def nova_conta(cls, cliente, numero):
        """Cria uma nova conta associada a um cliente"""
        return cls(cliente=cliente, numero=numero, agencia="0001")

    def sacar(self, valor):
        """Realiza o saque da conta"""
        if valor <= 0:
            print("❌ Operação inválida! Valor precisa ser positivo.")
            return False

        if valor > self._saldo:
            print("❌ Saldo insuficiente para saque!")
            return False

        self._saldo -= valor
        print(f"✅ Saque de R$ {valor:.2f} realizado com sucesso!")
        return True

    def depositar(self, valor):
        """Realiza o depósito na conta"""
        if valor <= 0:
            print("❌ Operação inválida! Valor precisa ser positivo.")
            return False

        self._saldo += valor
        print(f"✅ Depósito de R$ {valor:.2f} realizado com sucesso!")
        return True

# ===================== INTERFACE TRANSAÇÃO =====================

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

# ===================== DEPÓSITO =====================

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta._historico.adicionar_transacao(self)
            print(f"✅ Depósito de R$ {self.valor:.2f} registrado com sucesso!")

# ===================== SAQUE =====================

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta._historico.adicionar_transacao(self)
            print(f"✅ Saque de R$ {self.valor:.2f} registrado com sucesso!")

# ===================== HISTÓRICO =====================

class Historico:
    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, transacao):
        registro = {
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        self._transacoes.append(registro)

    def exibir(self):
        print("\n📜 Extrato da conta:")
        if not self._transacoes:
            print("Nenhuma movimentação registrada.")
        else:
            for t in self._transacoes:
                print(f"{t['data']} - {t['tipo']}: R$ {t['valor']:.2f}")

# ===================== CONTA CORRENTE =====================

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, agencia, limite=500, limite_saques=3):
        super().__init__(cliente, numero, agencia)
        self._limite = limite
        self._limite_saques = limite_saques
        self._saques_realizados = 0

    def sacar(self, valor):
        if valor <= 0:
            print("❌ Operação inválida! Valor deve ser positivo.")
            return False

        if valor > self._limite:
            print(f"⚠️ O limite por saque é de R$ {self._limite:.2f}.")
            return False

        if self._saques_realizados >= self._limite_saques:
            print(f"⚠️ Limite diário de {self._limite_saques} saques atingido.")
            return False

        if valor > self._saldo:
            print("❌ Saldo insuficiente para saque.")
            return False

        self._saldo -= valor
        self._saques_realizados += 1
        self._historico.adicionar_transacao(Saque(valor))
        print(f"✅ Saque de R$ {valor:.2f} realizado com sucesso!")
        return True

    def __str__(self):
        return (f"Agência: {self._agencia} | Conta: {self._numero} | "
                f"Titular: {self._cliente.nome} | Saldo: R$ {self._saldo:.2f}")

# ===================== PESSOA FÍSICA =====================

class PessoaFisica(Cliente):
    def __init__(self, nome: str, data_nascimento: date, cpf: str, endereco: str):
        super().__init__(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

# ===================== FUNÇÃO PRINCIPAL =====================

def main():
    AGENCIA = "0001"
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            print("\n=== Criar novo cliente ===")
            nome = input("Nome completo: ")
            cpf = input("CPF (somente números): ")
            while True:
                data_nascimento = input("Data de nascimento (AAAA-MM-DD): ")
                try:
                    ata_nascimento = date.fromisoformat(data_nascimento)
                    break
                except ValueError:
                    print("⚠️  Formato inválido! Digite no formato correto: AAAA-MM-DD (ex: 1994-06-10)")
            endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")

            cliente = PessoaFisica(
                nome=nome,
                data_nascimento=date.fromisoformat(data_nascimento),
                cpf=cpf,
                endereco=endereco
            )
            clientes.append(cliente)
            print(f"✅ Cliente {nome} criado com sucesso!")

        elif opcao == "2":
            print("\n=== Criar nova conta ===")
            cpf = input("Informe o CPF do cliente: ")

            cliente = next((c for c in clientes if c.cpf == cpf), None)
            if cliente:
                numero_conta = len(contas) + 1
                conta = ContaCorrente(cliente=cliente, numero=numero_conta, agencia=AGENCIA)
                cliente.adicionar_conta(conta)
                contas.append(conta)
                print(f"✅ Conta criada com sucesso para {cliente.nome}!")
            else:
                print("❌ Cliente não encontrado. Cadastre o cliente primeiro.")

        elif opcao == "3":
            print("\n=== Depósito ===")
            cpf = input("Informe o CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)

            if not cliente:
                print("❌ Cliente não encontrado.")
                continue

            valor = float(input("Informe o valor do depósito: "))
            conta = cliente.contas[0]
            transacao = Deposito(valor)
            cliente.realizar_transacao(conta, transacao)

        elif opcao == "4":
            print("\n=== Saque ===")
            cpf = input("Informe o CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)

            if not cliente:
                print("❌ Cliente não encontrado.")
                continue

            valor = float(input("Informe o valor do saque: "))
            conta = cliente.contas[0]
            transacao = Saque(valor)
            cliente.realizar_transacao(conta, transacao)

        elif opcao == "5":
            print("\n=== Extrato ===")
            cpf = input("Informe o CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)

            if not cliente:
                print("❌ Cliente não encontrado.")
                continue

            conta = cliente.contas[0]
            conta._historico.exibir()

        elif opcao == "0":
            print("\n👋 Encerrando o sistema. Até logo!")
            break

        else:
            print("⚠️ Opção inválida, tente novamente.")

# ===================== EXECUÇÃO =====================
if __name__ == "__main__":
    main()
