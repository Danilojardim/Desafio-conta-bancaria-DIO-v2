# 🏦 Desafio: Sistema Bancário em Python — Versão POO

Projeto desenvolvido como parte do **Bootcamp Luizalabs na [DIO (Digital Innovation One)](https://www.dio.me/)**.  
O objetivo é criar um **sistema bancário completo**, agora utilizando **Programação Orientada a Objetos (POO)**, aplicando os princípios de **herança, encapsulamento, abstração e polimorfismo**.

---

## 💡 Contexto do Projeto

Nesta versão aprimorada, o sistema foi totalmente reestruturado em **classes e objetos**, simulando o funcionamento de um banco real.  
Cada cliente, conta e transação é representado como uma **entidade independente**, o que torna o código mais modular, escalável e fiel a sistemas reais do mercado financeiro.

O foco está em:
- Uso de **classes, herança e abstração**;
- **Separação de responsabilidades** entre as entidades;
- **Leitura e manutenção facilitadas**;
- **Boas práticas de código (PEP8)** e **documentação linha a linha**.

---

## ⚙️ Funcionalidades

✅ Criar novos **usuários** (`PessoaFisica`) com:
- Nome completo  
- CPF  
- Data de nascimento  
- Endereço  

✅ Criar **contas bancárias** (`ContaCorrente`) associadas a um cliente existente  
✅ Realizar **depósitos**  
✅ Efetuar **saques** com controle de limite de valor e quantidade de operações  
✅ Exibir o **extrato completo** com histórico detalhado de transações  
✅ Sistema **interativo via menu**, com mensagens claras de sucesso e erro  
✅ **Controle de histórico** de transações (`Historico`)  
✅ **Tratamento de erros e validações de entrada**  

---

## 🧱 Estrutura de Classes

| Classe | Descrição |
|--------|------------|
| **PessoaFisica** | Representa o cliente, herda de `Cliente`. Possui nome, CPF, data de nascimento e endereço. |
| **Cliente** | Classe base que gerencia as contas e realiza transações. |
| **Conta** | Classe base que define saldo, agência, número e cliente. Implementa métodos para saque e depósito. |
| **ContaCorrente** | Especialização de `Conta`, com controle de limite de valor e número máximo de saques. |
| **Transacao (interface)** | Classe abstrata que define o método `registrar()`, base para `Saque` e `Deposito`. |
| **Saque** | Implementa o método `registrar()`, executando a lógica de retirada de valores. |
| **Deposito** | Implementa o método `registrar()`, executando a lógica de adição de valores. |
| **Historico** | Armazena todas as transações de uma conta, com data, tipo e valor. |

---
