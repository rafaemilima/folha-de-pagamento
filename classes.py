from random import randint
import calendar
import time
import datetime as dt


class Company:
    def __init__(self):
        self.employees = []
        self.payagendas = []
        self.standardPayagendas()

    def printEmployees(self):
        for employee in self.employees:
            print(f"Nome: {employee.name}\nID: {employee.id}")

    def standardPayagendas(self):
        date = time.localtime()
        month = int(time.strftime("%m", date))
        weekly = Payagenda()
        weekly.assumePayagenda("W", 4, month)
        bimonthly = Payagenda()
        bimonthly.assumePayagenda("B", 4, month)
        monthly = Payagenda()
        monthly.assumePayagenda("M", 100, month)
        self.payagendas.append(weekly)
        self.payagendas.append(bimonthly)
        self.payagendas.append(monthly)

    def printPayAgendas(self):
        for payagenda in self.payagendas:
            print(payagenda.nextpayday)

    def makePayments(self, today):
        for payagenda in self.payagendas:
            if today == payagenda.nextpayday:
                for employee in payagenda.employees:
                    employee.getSalary()
                    print("\n-------------NEW PAYMENT-------------")
                    print("Employee Informations")
                    print(f"ID:{employee.id}")
                    print(f"Name:{employee.name}")
                    print("Payment Details")
                    print(f"Value:{employee.payment.value}")
                    print(f"Pay Method:{employee.payment.paymethod}")
                    print(f"Data: {today[0]}/{today[1]}/{today[2]}")
                    print("--------------------------------------\n")
                    employee.resetPaymentS()
                    if employee.jobtype == "C":
                        employee.resetPaymentC()

                    elif employee.jobtype == "H":
                        employee.resetPaymentH()

                month = today[1]

                if payagenda.type == "M":
                    month = (month + 1) % 12
                    if month == 0:
                        month += 1

                payagenda.getNextPayday(month, today)



class Payagenda:
    def __init__(self):
        self.employees = []
        self.nextpayday = []
        self.type = None
        self.day = None

    def getNextPayday(self, month, today):
        d = dt.date(today[2], today[1], today[0])
        if self.type == "W":
            d += dt.timedelta(3)
            while d.weekday() != self.day:
                d += dt.timedelta(1)
            list = [d.day, d.month, d.year]
            self.nextpayday = list

        elif self.type == "M":
            list = []
            if self.day == 100:
                h = self.getLastBusinessDay(2021, month)
                list = [h, month, d.year]
            elif self.day == 50:
                list = [15, month, d.year]
            elif self.day == 0:
                list = [1, month, d.year]

            self.nextpayday = list

        elif self.type == "B":
            d += dt.timedelta(8)
            while d.weekday() != self.day:
                d += dt.timedelta(1)
            list = [d.day, d.month, d.year]
            self.nextpayday = list

    def assumePayagenda(self, type_pa, wday, month):
        d = dt.date.today()
        self.type = type_pa
        self.day = wday
        self.getNextPayday(month, [d.day, d.month, d.year])

    @staticmethod
    def getLastBusinessDay(year: int, month: int) -> int:
        return max(calendar.monthcalendar(year, month)[-1:][0][:5])


class Employee:
    def __init__(self, company, name = None, address = None, jobtype = None, salary = 0, issyndicate = False,
                 comission = None, salary_h = None, id = None, paymethod = None):

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
        self.payment = Payment(paymethod)

        if issyndicate == "y":
            self.issyndicate = True
        else:
            self.issyndicate = False
        company.employees.append(self)


    def addEmployee(self, company, name, address, jobtype, salary, issyndicate, salary_h, comission, id = None):
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

    def resetPaymentS(self):
        self.payment.value = 0

    def getSalary(self):
        if self.jobtype == "C":
            self.payment.value += (self.salary/2)
        else:
            self.payment.value += (self.salary)
        self.payment.value -= self.aditional_taxes


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
    def getEmployeeByID(company, s_id):
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
                 salary_h = None, day = 1, paymethod = None):
        super().__init__(company, name, address, jobtype, salary, issyndicate, salary_h, paymethod=paymethod)
        self.card = PointCard(self.id, self)
        self.salary_h = salary_h
        self.hours_amount = 0
        self.day = day
        self.workstarthour = 0
        self.workendhour = 0

    def resetPaymentH(self):
        self.hours_amount = 0
        self.workstarthour = 0
        self.workendhour = 0

    def punchTheClockIn(self, hour):
        self.workstarthour = hour

    def punchTheClockOut(self, hour):
        self.workendhour = hour
        work_day = self.workendhour - self.workstarthour
        self.hours_amount = self.hours_amount + work_day
        self.payment.value += self.calculateSalary(work_day)

    def calculateSalary(self, work_day):
        total = 0
        if work_day > 8:
            extra = work_day - 8
            total = 8 * self.salary_h + (extra * 1.5 * self.salary_h)
        else:
            total = work_day * self.salary_h

        return total


class Commissioned(Employee):
    def __init__(self, company, name = None, address = None, jobtype = None, salary = None, issyndicate = False,
                 comission_percent = 0, paymethod = None):
        super().__init__(company, name, address, jobtype, salary, issyndicate, comission_percent, paymethod=paymethod)
        self.comission_amount = 0
        self.sales = []
        self.comission_percent = comission_percent

    def addSale(self, date, value):
        self.sales.append(Sales(date, value))
        self.comission_amount = self.getComission(value)
        self.payment.value += self.comission_amount

    def getComission(self, value):
        self.comission_amount += (value * self.comission_percent)
        return self.comission_amount

    def resetPaymentC(self):
        self.payment.value = 0
        self.comission_amount = 0


class Sales:
    def __init__(self, date = None, value = None):
        self.date = date
        self.value = value


class Syindicate:
    def __init__(self, taxes = 0, syndicate_id = 1):
        self.syndicate_id = syndicate_id
        self.taxes = taxes

    def changeGeneralTaxes(self, new_g_tax):
        self.taxes = new_g_tax


    @staticmethod
    def signSyindicate(empresa, employee_id, aditional_taxes = 0):
        employee = Employee.getEmployeeByID(empresa, employee_id)
        employee.aditional_taxes = aditional_taxes
        employee.issyndicate = True

    @staticmethod
    def plusAditionalTaxes(empresa, employee_id, aditional_taxes):
        employee = Employee.getEmployeeByID(empresa, employee_id)
        employee.aditional_taxes += aditional_taxes


class Payment:
    def __init__(self, paymethod = None, value = 0):
        self.value = value
        self.paymethod = paymethod


class PointCard:
    def __init__(self, employeeid = None, employee = None):
        if employeeid is None:
            self.cardid = None
        else:
            self.cardid = employeeid
        self.employee = employee


    def addCard(self, company, employeeid, salary_h):
        employee = Employee.getEmployeeByID(company, employeeid)
        if employee.card is None:
            self.cardid = employeeid
            self.employee = employee
            employee.card = self
            employee.job_type = "H"
            employee.salary = 0
            employee.comission = 0
            employee.salary_h = salary_h

            return self
