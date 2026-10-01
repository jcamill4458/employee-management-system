# Employee management system
# Allows for basic employee management functions including:
# hiring/firing, salary management, org hierarchy

from employee import Employee
from employee import Manager
from employee import Developer

# File reader
# In place of future SQL database
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

# tests
if __name__ == '__main__':
    # load in all employees and managers from txt file
    load_from_file('example-employees.txt')

    Employee.print_all()
    print()
    Manager.find_mgr('24').print_org_chart()
    print()
    Manager.find_mgr('25').print_org_chart()
    print()
    Manager.find_mgr('26').print_org_chart()
    print()
    Manager.find_mgr('27').print_org_chart()