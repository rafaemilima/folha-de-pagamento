from random import randint


class Company:
    def __init__(self):
        self.employees = []


class Employee:
    def __init__(self, company, name = None, address = None, jobtype = None, salary = 0, issyndicate = False,
                 comission = None, salary_h = None, id = None):

        if id:
            self.id = id
        else:
            self.id = self.defineID(company)

        self.name = name
        self.address = address
        self.jobtype = jobtype
        self.salary = salary
        self.comission = comission
        self.payment = None
        self.salary_h = salary_h
        self.card = None
        self.aditional_taxes = 0
        if issyndicate == "y":
            self.issyndicate = True
        else:
            self.issyndicate = False
        company.employees.append(self)



    def add_employee(self, company, name, address, jobtype, salary, issyndicate, salary_h, comission, id = None):
        if self.id:
            self.id = id
        else:
            self.id = self.defineID(company)

        self.name = name
        self.address = address
        self.jobtype = jobtype
        self.salary = salary
        self.issyndicate = issyndicate
        self.salary_h = salary_h
        self.comission = comission
        company.employees.append(self)

    def info(self):
        print("###################################")
        print(f"ID do funcionário: {self.id}")
        print(f"Nome do funcionário: {self.name}")
        print(f"Endereço:{self.address}")
        print(f"Tipo de afiliação:{self.jobtype}")
        print(f"Salário fixo: {self.salary}")
        print(f"Salário Horário: {self.salary_h}")
        print(f"Taxa de Comissão: {self.comission}")
        print(f"Afiliação Sindical: {self.issyndicate}")
        if self.card:
            print(f"ID do cartão de ponto: {self.card.cardid}")
        print("###################################")

    def update(self, parameter, value):
        if parameter == "name":
            self.name = value
        elif parameter == "salary":
            self.salary = value
        elif parameter == "syndicate":
            self.issyndicate = value
        elif parameter == "comission":
            self.comission = value
        elif parameter == "address":
            self.address = value
        elif parameter == "jobtype":
            self.jobtype = value
        return


    @staticmethod
    def get_employee_byid(company, s_id):
        for i in company.employees:
            if i.id == int(s_id):
                return i
        return None

    @staticmethod
    def remove(company, s_id):
        for i in company.employees:
            if i.id == int(s_id):
                company.employees.remove(i)
                del(i)

        return

    def get_payment(self):
        if self.jobtype == "H":
            return self.payment

        elif self.jobtype == "C":
            return self.payment + self.salary

        elif self.jobtype == "S":
            return self.salary

        return -1


    @staticmethod
    def takeIDs(company):
        ids = []
        for i in company.employees:
            ids.append(i.id)
        return ids

    def defineID(self, company):
        id = randint(100000000, 999999999)  # return the id
        ids = self.takeIDs(company)
        while id in ids:
            id = randint(100000000, 999999999)
        return id



class Hourly(Employee):
    def __init__(self, company, name = None, address = None, jobtype = None, salary = None, issyndicate = False,
                 salary_h = None, day = 1):
        super().__init__(company, name, address, jobtype, salary, issyndicate, salary_h)
        self.card = PointCard(self.id, self)
        self.salary_h = salary_h
        self.salary_amount = 0
        self.hours_amount = 0
        self.day = day
        self.workstarthour = 0
        self.workendhour = 0

    def punch_the_clock_in(self, hour):
        self.workstarthour = hour

    def punch_the_clock_out(self, hour):
        self.workendhour = hour
        work_day = self.workendhour - self.workstarthour
        self.hours_amount = self.hours_amount + work_day
        self.salary_amount += self.calc_salary(work_day)
        self.payment = self.salary_amount

    def calc_salary(self, work_day):
        total = 0
        if work_day > 8:
            extra = work_day - 8
            total = 8 * self.salary_h + (extra * 1.5 * self.salary_h)
        else:
            total = work_day * self.salary_h

        return total


class Commissioned(Employee):
    def __init__(self, company, name = None, address = None, jobtype = None, salary = None, issyndicate = False,
                 comission_percent = None):
        super().__init__(company, name, address, jobtype, salary, issyndicate, comission_percent)
        self.comission_amount = 0
        self.sales = []
        self.comission_percent = comission_percent
        self.card = None

    def add_sale(self, date, value):
        self.sales.append(Sales(date, value))
        self.comission_amount = self.get_comission(value)
        self.payment = self.comission_amount

    def get_comission(self, value):
        self.comission_amount += value * self.comission_percent
        return self.comission_amount


class Sales:
    def __init__(self, date = None, value = None):
        self.date = date
        self.value = value


class Syindicate:
    def __init__(self, taxes = 0, syndicate_id = 1):
        self.syndicate_id = syndicate_id
        self.taxes = taxes

    def change_general_taxes(self, new_g_tax):
        self.taxes = new_g_tax


    @staticmethod
    def sign_syindicate(empresa, employee_id, aditional_taxes = 0):
        employee = Employee.get_employee_byid(empresa, employee_id)
        employee.aditional_taxes = aditional_taxes
        employee.issyndicate = True

    @staticmethod
    def plus_aditional_taxes(empresa, employee_id, aditional_taxes):
        employee = Employee.get_employee_byid(empresa, employee_id)
        employee.aditional_taxes += aditional_taxes




'''
class Payment:
    def __init__(self, payment = None, paymethod = None, type = None, taxes = None):
        self.payment = payment
        self.paymethod = paymethod
        self.taxes = self.calc_taxes()

    def make_payment(self):
        if

    def calc_taxes(self):
        return 1
'''


class PointCard:
    def __init__(self, employeeid = None, employee = None):
        if employeeid is None:
            self.cardid = None
        else:
            self.cardid = employeeid
        self.employee = employee

    @staticmethod
    def get_card_id():
        return randint(10000, 99999)

    def add_card(self, company, employeeid, salary_h):
        employee = Employee.get_employee_byid(company, employeeid)
        if employee.card is None:
            self.cardid = employeeid
            self.employee = employee
            employee.card = self
            employee.job_type = "H"
            employee.salary = 0
            employee.comission = 0
            employee.salary_h = salary_h

            return self
