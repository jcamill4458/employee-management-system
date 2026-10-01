# Employee management system
# Allows for basic employee management functions including:
# hiring/firing, salary management, org hierarchy

from employee import Employee, Manager, Developer

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

    print("File ", filename, " loaded.\n")

# input checker
def input_check(u):
    if ' ' in u:
        u, arg = u.split(' ')

    match u:
        case 'help':
            return help_menu()
        case 'print_all':
            return Employee.print_all()
        case 'print_org':
            return Manager.find_mgr(arg).print_org_chart()
        case 'print':
            return Employee.find_emp(arg)
        case 'print_data':
            return repr(Employee.find_emp(arg))
        case 'exit':
            return 'Exiting...'
        case _:
            return 'Unknown command'

# help function
def help_menu():
    return ("help: Bring up help menu\n"
            "print_all: Print all employees\n"
            "print_org {mgr_id}: Print a manager's org hierarchy\n"
            "print {emp_id}: Print a singular employee's basic information\n"
            "print_data {emp_id}: Print a singular employee's data\n"
            "")

# tests
if __name__ == '__main__':
    # load in all employees and managers from txt file
    load_from_file('example-employees.txt')
    print("Type 'exit' to exit.\n")

    u = ""
    while u != 'exit':
        u = input("Enter employee function ('help' for function list): ")
        print(input_check(u), "\n")

# TO DO:
# Find way to error handle (ex. print_org used on employee)
# Make sure input_check is doing things properly