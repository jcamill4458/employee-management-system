# Python OOP practice file

# File reader
def load_from_file(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f if line.strip()]

    manager_lines = []

    for line in lines:
        kind, rest = line.split(',', 1)
        if kind == 'emp':
            Employee.from_string(rest)
        elif kind == 'dev':
            Developer.from_string(rest)
        elif kind == 'mgr':
            manager_lines.append(rest)

    for line in manager_lines:
        Manager.from_string(line)

class Employee:

    # class variables
    num_of_emps = 0
    raise_amt = 1.04
    next_id = 0
    emp_registry = {}

    def __init__(self, first, last, salary):
        # instance variables
        self.first = first.capitalize()
        self.last = last.capitalize()
        self.salary = salary
        self.manager = None

        self.id = f'{Employee.next_id:02d}'
        Employee.next_id += 1

        Employee.emp_registry[self.id] = self
        Employee.num_of_emps += 1

    # dunder methods, which are overring methods in the Object class (standard library)
    def __repr__(self):
        return f'Employee({self.first!r}, {self.last!r}, {self.email!r}, {self.salary})'

    def __str__(self):
        return f'{self.fullname} - {self.email}'

    # normal method(s)
    def apply_raise(self):
        self.salary = int(self.salary * self.raise_amt)

    @property
    def email(self):
        return f'{self.first}.{self.last}@company.com'

    @property
    def fullname(self):
        return f'{self.first} {self.last}'

    @fullname.setter
    def fullname(self, name):
        self.first, self.last = name.split(' ')
        self.first = self.first.capitalize()
        self.last = self.last.capitalize()

    # class methods
    @classmethod
    def set_raise_amt(cls, amount):
        cls.raise_amt = amount

    @classmethod
    def print_all(cls):
        for key, value in cls.emp_registry.items():
            print(f'{key}: {value}')

    @classmethod
    def find_emp(cls, emp_id):
        emp = Employee.emp_registry.get(emp_id)
        if emp is None:
            return f'Employee with ID {emp_id} not found.'
        return emp


    @classmethod
    def fire(cls, emp_id):
        emp = cls.find_emp(emp_id)
        if emp is None:
            return f'Employee with ID {emp_id} not found.'

        if isinstance(emp, Manager) and emp.employees:
            return f'Cannot fire {emp.fullname} — they still have {len(emp.employees)} direct report(s). Reassign them first.'

        if emp.manager:
            emp.manager.remove_emp(emp)
        del cls.emp_registry[emp_id]
        return f'{emp.fullname} has been fired.'

    @classmethod
    def from_string(cls, emp_str):
        first, last, salary = emp_str.split(',')
        return cls(first, last, int(salary))

# Developer subclass
class Developer(Employee):
    raise_amt = 1.1

    def __init__(self, first, last, salary, prog_lang):
        super().__init__(first, last, salary)
        self.prog_lang = prog_lang

    @classmethod
    def from_string(cls, emp_str):
        first, last, salary, prog_lang = emp_str.split(',')
        return cls(first, last, int(salary), prog_lang)

# Manager subclass
class Manager(Employee):
    # pass employees=None instead of Employees=[] for our list so that we aren't passing a mutable object
    def __init__(self, first, last, salary, employees=None):
        super().__init__(first, last, salary)
        self.employees = []
        if employees is not None:
            for emp in employees:
                self.add_emp(emp)


    def add_emp(self, emp):
        if emp not in self.employees:
            self.employees.append(emp)
            emp.manager = self

    def remove_emp(self, emp):
        if emp in self.employees:
            self.employees.remove(emp)
            emp.manager = None

    def print_org_chart(self, depth=0):
        print('  ' * depth + self.fullname + "'s team")
        for emp in self.employees:
            print('  ' * depth + '-->', emp.fullname)
            if isinstance(emp, Manager):
                emp.print_org_chart(depth + 1)

    @classmethod
    def find_mgr(cls, emp_id):
        emp = cls.find_emp(emp_id)
        if not isinstance(emp, Manager):
            return None
        return emp

    @classmethod
    def from_string(cls, emp_str):
        first, last, salary, emp_ids = emp_str.split(',', 3)
        mgr = cls(first, last, int(salary))
        for emp_id in emp_ids.split('|'):
            emp = cls.find_emp(emp_id)
            if emp:
                mgr.add_emp(emp)
        return mgr

# tests
if __name__ == '__main__':
    # load in all employees and managers from txt file
    load_from_file('example-employees.txt')

    Employee.print_all()
    print()
    Manager.find_mgr('05').print_org_chart()
