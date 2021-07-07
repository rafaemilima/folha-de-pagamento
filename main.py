from classes import Employee, Hourly, Commissioned, PointCard, Syindicate


def sindicato():
    pass


def adicionar_func():
    nome = input("Nome: ")
    endereco = input("Endereco: ")
    tipo = input("Tipo de funcionário (C - Comissionado; S - Assalariado; H - Horista): ")
    salario = float(input("Salario (valor float, 0 se Horista): "))
    salario_h = float(input("Sallario por hora (valor float, 0 se Comissionado ou Assalariado): "))
    comissao = float(input("Taxa de comissão (valor decimal):"))
    sindicado = bool(input("Afiliação sindical (True, False): "))
    e1 = None

    if(tipo == "H"):
        e1 = Hourly(nome, endereco, tipo, salario, sindicado, salario_h)
    elif(tipo == "C"):
        e1 = Commissioned(nome, endereco, tipo, salario, sindicado, comissao)
    elif(tipo == "S"):
        e1 = Employee(nome, endereco, tipo, salario, sindicado, salario_h, comissao)
    else:
        print("erro")

    return e1


def venda():
    while True:
        n = int(input("1 - Registrar uma nova venda\n2 - Ver total de vendas\n0 - Retornar\n"))
        if n == 0:
            return
        elif n == 1:
            identificador = str(input("ID do funcionário: "))
            e = Employee.get_employee_byid(identificador)
            if e and e.jobtype == "C":
                data = input("informe a data da venda: ")
                valor = float(input("informe o valor da venda: "))
                e.add_sale(data, valor)
                print("Resultado de venda lançado!")
        elif n == 2:
            identificador = str(input("ID do funcionário: "))
            e = Employee.get_employee_byid(identificador)
            if e and e.jobtype == "C":
                print(e.comission_amount)
                for i in e.sales:
                    print (i.value)





def cartao():
    while True:
        n = int(input("1 - Adicionar cartão de ponto\n2 - Bater ponto\n0 - Retornar\n"))

        if n == 0:
            return

        elif n == 1:
            identificador = str(input("ID do funcionário: "))
            card = PointCard()
            card.add_card(identificador)
            print(card.cardid)
            print(card.employee.name, card.employee.id)

        elif n == 2:
            identificador = str(input("ID do funcionário: "))
            e = Employee.get_employee_byid(identificador)
            h = int(input("1 - Início de expediente\n2 - Final de expediente\n"))
            if e and h == 1:
                inicio = int(input("Hora de início: "))
                e.punch_the_clock_in(inicio)
            elif e and h == 2:
                final = int(input("Hora de encerramento: "))
                e.punch_the_clock_out(final)
                print(e.salary_amount, e.hours_amount)


def funcionario():
    while True:
        n = int(input("1 - Adicionar um novo funcionário\n2 - Remover um funcionário registrado\n3 - Dados do "
                      "funcionário\n4 - Alterar informações de um funcionário\n0 - Retornar\n"))

        if n == 0:
            return

        elif n == 1:
            new = adicionar_func()
            print("Novo funcionario criado!")
            print(f"ID: {new.id}")

        elif n == 2:
            identificador = str(input("ID do funcionário: "))
            confirme = input("Realmente deseja remover esse funcionario? (s/n)")
            e = Employee.get_employee_byid(identificador)
            if confirme == "s" and e:
                Employee.remove(identificador)
                print("funcionario removido do sistema")
            else:
                print("ID inválido. Cerfique-se que o funcionário está no sistema.")


        elif n == 3:
            identificador = str(input("ID do funcionário: "))
            e = Employee.get_employee_byid(identificador)
            if e:
                e.info()
            else:
                print("ID inválido. Cerfique-se que o funcionário está no sistema.")

        elif n == 4:
            identificador = str(input("ID do funcionário: "))
            e = Employee.get_employee_byid(identificador)
            if e:
                print("digite o atributo que você deseja modificar")
                a = input("(name; salary; syndicate; comission; address; jobtype): ")
                valor = input("Digite o novo valor para o atributo especificado: ")
                e.update(a, valor)

            else:
                print("ID inválido. Cerfique-se que o funcionário está no sistema.")


def main():
    while True:
        n = int(input("1 - Funcionario\n2 - Cartão de ponto\n3 - Resultado de venda\n4 - Sindicato\n0 - Sair\n"))
        if n == 0:
            break
        elif n == 1:
            funcionario()
        elif n == 2:
            cartao()
        elif n == 3:
            venda()
        elif n == 4:
            sindicato()


main()