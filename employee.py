# Employee parent class
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

    # dunder methods, which are overriding methods in the Object class (standard library)
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
        # useful syntax using for loops
        return '\n'.join(f'{key}: {val}' for key, val in cls.emp_registry.items())

    @classmethod
    def find_emp(cls, emp_id):
        return cls.emp_registry.get(emp_id)

    # Fires any employee, flags firing a manager if they have reports
    # Error handling functionality coming soon
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
        Employee.num_of_emps -= 1
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
        boss = self
        while boss is not None:
            if boss is emp:
                raise ValueError(f'{emp.fullname} cannot report to themselves or their own report')
            boss = boss.manager
        if emp.manager is not None and emp.manager is not self:
            emp.manager.remove_emp(emp)
        if emp not in self.employees:
            self.employees.append(emp)
            emp.manager = self

    def remove_emp(self, emp):
        if emp in self.employees:
            self.employees.remove(emp)
            emp.manager = None

    # Prints org charts with indentation under managers **APPENDING is useful here and in other functions**
    def org_chart(self, depth=0):
        indent = '  ' * depth
        lines = [f"{indent}{self.fullname}'s team"]
        for emp in self.employees:
            lines.append(f"{indent}--> {emp.fullname} [{emp.id}]")
            if isinstance(emp, Manager):
                lines.append(emp.org_chart(depth + 1))
        return '\n'.join(lines)

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