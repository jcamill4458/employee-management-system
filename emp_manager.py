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
def input_check(user_input):
    cmd, _, arg = user_input.strip().partition(' ')
    cmd, arg = cmd.lower(), arg.strip()

    if cmd in ('print', 'print_data', 'print_org'):
        if not arg:
            return f'Usage: {cmd} {{id}}'
        emp = Employee.find_emp(arg)
        if emp is None:
            return f"No employee with id '{arg}'"
        if cmd == 'print':
            return str(emp)
        if cmd == 'print_data':
            return repr(emp)
        if not isinstance(emp, Manager):
            return f'{emp.fullname} is not a manager'
        return emp.org_chart()

    match cmd:
        case 'help':
            return help_menu()
        case 'print_all':
            return Employee.print_all()
        case 'exit':
            return 'Exiting...'
        case '':
            return ''
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