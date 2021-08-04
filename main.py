from classes import Company, Employee, Hourly, Commissioned, PointCard, Syindicate


def sindicato_func(empresa, sindicato):
    while True:
        n = int(input("1 - Definir taxa sindical geral\n2 - Definir taxa sindical adicional\n0 - Retornar"))
        if n == 0:
            return
        elif n == 1:
            taxa_geral = float(input("Informe o valor que deseja adicionar para a taxa geral: "))
            sindicato.changeGeneralTaxes(taxa_geral)
            print(sindicato.taxes)

        elif n == 2:
            identificador = input("Informe o identificador do funcionário: ")
            taxa_ad = float(input("Informe a taxa adicional de serviço: "))
            sindicato.plusAditionalTaxes(empresa, identificador, taxa_ad)


def adicionar_func(empresa):
    nome = input("Nome: ")
    endereco = input("Endereco: ")
    tipo = input("Tipo de funcionário (C - Comissionado; S - Assalariado; H - Horista): ")
    tipo.upper()
    while tipo != "C" or tipo != "S" or tipo != "H":
        print("Valor inválido para o atributo!")
        tipo = input("Tipo de funcionário (C - Comissionado; S - Assalariado; H - Horista): ")
        tipo.upper()
    salario = float(input("Salario fixo mensal (0 se Horista): "))
    sindicado = str(input("Afiliação sindical (y, n): "))
    sindicado.lower()
    while sindicado != "y" or sindicado != "n":
        print("Valor inválido para o atributo!")
        sindicado = str(input("Afiliação sindical (y, n): "))
        sindicado.lower()
    e1 = None

    if(tipo == "H"):
        salario_h = float(input("Salario por hora (valor float, 0 se Comissionado ou Assalariado): "))
        e1 = Hourly(empresa, nome, endereco, tipo, 0, sindicado, salario_h)
    elif(tipo == "C"):
        comissao = float(input("Taxa de comissão (valor decimal):"))
        e1 = Commissioned(empresa, nome, endereco, tipo, salario, sindicado, comissao)
    elif(tipo == "S"):
        e1 = Employee(empresa, nome, endereco, tipo, salario, sindicado, 0, 0)
    else:
        print("erro")

    return e1


def venda(empresa):
    while True:
        n = int(input("1 - Registrar uma nova venda\n2 - Ver total de vendas\n0 - Retornar\n"))
        if n == 0:
            return
        elif n == 1:
            identificador = str(input("ID do funcionário: "))
            e = Employee.getEmployeeByID(empresa, identificador)
            if e and e.jobtype == "C":
                data = input("informe a data da venda: ")
                valor = float(input("informe o valor da venda: "))
                e.addSale(data, valor)
                print("Resultado de venda lançado!")
        elif n == 2:
            identificador = str(input("ID do funcionário: "))
            e = Employee.getEmployeeByID(empresa, identificador)
            if e and e.jobtype == "C":
                print(f"Comissão total: {e.comission_amount}")
                print("Vendas efetuadas:")
                for i in e.sales:
                    print (i.value)


def cartao(empresa):
    while True:
        n = int(input("1 - Adicionar cartão de ponto\n2 - Bater ponto\n0 - Retornar\n"))

        if n == 0:
            return

        elif n == 1:
            identificador = str(input("ID do funcionário: "))
            card = PointCard()
            salario = float(input("Salário horário"))
            card.addCard(empresa, identificador, salario)
            print(card.cardid)
            print(card.employee.name, card.employee.id)

        elif n == 2:
            identificador = str(input("ID do funcionário: "))
            e = Employee.getEmployeeByID(empresa, identificador)
            h = int(input("1 - Início de expediente\n2 - Final de expediente\n"))
            if e and h == 1:
                inicio = int(input("Hora de início: "))
                e.punchTheClockIn(inicio)
            elif e and h == 2:
                final = int(input("Hora de encerramento: "))
                e.punchTheClockOut(final)
                print(e.salary_amount, e.hours_amount)


def funcionario(empresa):
    while True:
        n = int(input("1 - Adicionar um novo funcionário\n2 - Remover um funcionário registrado\n3 - Dados do "
                      "funcionário\n4 - Alterar informações de um funcionário\n0 - Retornar\n"))

        if n == 0:
            return

        elif n == 1:
            new = adicionar_func(empresa)
            print("Novo funcionario criado!")
            print(f"ID: {new.id}")

        elif n == 2:
            identificador = str(input("ID do funcionário: "))
            confirme = input("Realmente deseja remover esse funcionario? (s/n)")
            e = Employee.getEmployeeByID(empresa, identificador)
            if confirme == "s" and e:
                Employee.remove(empresa, identificador)
                print("funcionario removido do sistema")
            else:
                print("ID inválido. Cerfique-se que o funcionário está no sistema.")


        elif n == 3:
            identificador = str(input("ID do funcionário: "))
            e = Employee.getEmployeeByID(empresa, identificador)
            if e:
                e.info()
            else:
                print("ID inválido. Cerfique-se que o funcionário está no sistema.")

        elif n == 4:
            identificador = str(input("ID do funcionário: "))
            e = Employee.getEmployeeByID(empresa, identificador)
            if e:
                print("digite o atributo que você deseja modificar")
                a = input("(name; salary; syndicate; comission; address; jobtype): ")
                valor = input("Digite o novo valor para o atributo especificado: ")
                e.update(a, valor)

            else:
                print("ID inválido. Cerfique-se que o funcionário está no sistema.")


def main(empresa, sindicato):
    while True:
        n = int(input("1 - Funcionario\n2 - Cartão de ponto\n3 - Resultado de venda\n4 - Sindicato\n0 - Sair\n"))
        if n == 0:
            break
        elif n == 1:
            funcionario(empresa)
        elif n == 2:
            cartao(empresa)
        elif n == 3:
            venda(empresa)
        elif n == 4:
            sindicato_func(empresa, sindicato)


s = Syindicate(100,  1)
c = Company()
main(c, s)
