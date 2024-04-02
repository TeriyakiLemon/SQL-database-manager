import mysql.connector

############################################

def back_to_main_menu():
    print("Going back to main menu")
    main()

###  Employee table  ####
def add_employee():
    fname = input("Enter first name: ")
    minit = input("Enter middle initial: ")
    lname = input("Enter last name: ")
    ssn = input("Enter SSN: ")
    bdate = input("Enter birth date (YYYY-MM-DD): ")
    address = input("Enter address: ")
    sex = input("Enter sex (M/F): ")
    salary = input("Enter salary: ")
    super_ssn = input("Enter supervisor SSN: ")
    dno = input("Enter department number: ")

    connection = mysql.connector.connect(
        host='localhost',
        user='JASON',  
        passwd='takoyaki-06902', 
        database='company_database'
    )
    cursor = connection.cursor()

    sql = """INSERT INTO employee (Fname, Minit, Lname, Ssn, Bdate, Address, Sex, Salary, Super_ssn, Dno)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    val = (fname, minit, lname, ssn, bdate, address, sex, salary, super_ssn, dno)
    
    try:
        cursor.execute(sql, val)
        connection.commit()
        print("Employee added successfully.")
    except mysql.connector.Error as e:
        print(f"Error occurred: {e}")
    finally:
        cursor.close()
        connection.close()

def view_employee():
    ssn = input("Enter employee's SSN to view: ")

    connection = mysql.connector.connect(
        host='localhost',
        user='JASON',  
        passwd='takoyaki-06902', 
        database='company_database'
    )
    cursor = connection.cursor()

    sql = "SELECT * FROM employee WHERE Ssn = %s"
    val = (ssn,)

    try:
        cursor.execute(sql, val)
        result = cursor.fetchone()
        if result:
            print("Employee Details: ", result)
        else:
            print("No employee found with SSN:", ssn)
    except mysql.connector.Error as e:
        print(f"Error occurred: {e}")
    finally:
        cursor.close()
        connection.close()

def modify_employee():
    ssn = input("Enter the employee's SSN to modify: ")

    connection = mysql.connector.connect(
        host='localhost',
        user='JASON',
        passwd='takoyaki-06902',
        database='company_database',
        autocommit=False  
    )
    cursor = connection.cursor(buffered=True)
    try:
        connection.start_transaction()

        cursor.execute("SELECT * FROM employee WHERE Ssn = %s FOR UPDATE", (ssn,))
        employee = cursor.fetchone()
        if employee:
            print("Current employee details:", employee)
        else:
            print("No employee found with SSN:", ssn)
            return

        new_address = input("Enter new address (leave blank to keep current): ")
        new_sex = input("Enter new sex (M/F) (leave blank to keep current): ")
        new_salary = input("Enter new salary (leave blank to keep current): ")
        new_super_ssn = input("Enter new supervisor SSN (leave blank to keep current): ")
        new_dno = input("Enter new department number (leave blank to keep current): ")

        update_sql = "UPDATE employee SET "
        update_params = []
    
        if new_address:
            update_sql += "Address = %s, "
            update_params.append(new_address)
        if new_sex:
            update_sql += "Sex = %s, "
            update_params.append(new_sex)
        if new_salary:
            update_sql += "Salary = %s, "
            update_params.append(new_salary)
        if new_super_ssn:
            update_sql += "Super_ssn = %s, "
            update_params.append(new_super_ssn)
        if new_dno:
            update_sql += "Dno = %s, "
            update_params.append(new_dno)

        if update_params:
            update_sql = update_sql.rstrip(", ")  
            update_sql += " WHERE Ssn = %s"
            update_params.append(ssn)
            
            
            cursor.execute(update_sql, tuple(update_params))
            connection.commit() 
            print("Employee updated successfully.")
        else:
            print("No updates made.")
            connection.rollback()  

    except mysql.connector.Error as e:
        print(f"Error occurred: {e}")
        connection.rollback() 
    finally:
        cursor.close()
        connection.close()

def remove_employees():
    ssn = input("Enter the employee's SSN to remove: ")

    connection = mysql.connector.connect(
        host='localhost',
        user='JASON',
        passwd='takoyaki-06902',
        database='company_database',
        autocommit=False
    )
    cursor = connection.cursor(buffered=True)

    try:
        cursor.execute("SELECT * FROM employee WHERE Ssn = %s FOR UPDATE", (ssn,))
        employee = cursor.fetchone()
        if employee:
            print("Employee to be removed:", employee)
        else:
            print("No employee found with SSN:", ssn)
            return

        confirm = input("Are you sure you want to delete this employee? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Operation cancelled.")
            return

        
        cursor.execute("SELECT * FROM department WHERE Mgr_ssn = %s", (ssn,))
        if cursor.fetchone():
            print("Cannot remove employee: Employee is a department manager. Please update department information first.")
            return

        cursor.execute("DELETE FROM employee WHERE Ssn = %s", (ssn,))
        connection.commit()
        print("Employee removed successfully.")
    except mysql.connector.Error as e:
        print(f"Error occurred: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()


###  Department table  ####
def add_department():
    dname = input("Enter the department name: ")
    dnumber = input("Enter the department number: ")
    mgr_ssn = input("Enter the manager's SSN: ")
    mgr_start_date = input("Enter the manager's start date (YYYY-MM-DD): ")

    connection = mysql.connector.connect(
        host='localhost',
        user='JASON',
        passwd='takoyaki-06902',
        database='company_database'
    )
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM department WHERE Dnumber = %s", (dnumber,))
    if cursor.fetchone():
        print("Error: Department number already exists.")
        return
    
    cursor.execute("SELECT * FROM employee WHERE Ssn = %s", (mgr_ssn,))
    if not cursor.fetchone():
        print("Error: Manager's SSN does not exist in employee records.")
        return

    try:
        sql = """INSERT INTO department (Dname, Dnumber, Mgr_ssn, Mgr_start_date)
                 VALUES (%s, %s, %s, %s)"""
        val = (dname, dnumber, mgr_ssn, mgr_start_date)
        
        cursor.execute(sql, val)
        connection.commit()
        print("New department added successfully.")
    except mysql.connector.Error as e:
        print(f"Error occurred: {e}")
    finally:
        cursor.close()
        connection.close()


def view_department():
    dnumber = input("Enter the department number: ")

    connection = mysql.connector.connect(
        host='localhost',
        user='JASON',
        passwd='takoyaki-06902',
        database='company_database'
    )
    cursor = connection.cursor()

    cursor.execute("SELECT Dname, Mgr_ssn FROM department WHERE Dnumber = %s", (dnumber,))
    department = cursor.fetchone()
    if department:
        dname, mgr_ssn = department

        cursor.execute("SELECT Fname, Lname FROM employee WHERE Ssn = %s", (mgr_ssn,))
        manager = cursor.fetchone()
        mgr_name = f"{manager[0]} {manager[1]}" if manager else "No manager found"
        
        cursor.execute("SELECT Dlocation FROM dept_locations WHERE Dnumber = %s", (dnumber,))
        locations = cursor.fetchall()
        locations_str = ", ".join(location[0] for location in locations)

        print(f"Department Name: {dname}")
        print(f"Manager Name: {mgr_name}")
        print(f"Locations: {locations_str}")
    else:
        print("No department found with the given number.")

    cursor.close()
    connection.close()


def remove_department():
    dnumber = input("Enter the department number: ")

    connection = mysql.connector.connect(
        host='localhost',
        user='JASON',
        passwd='takoyaki-06902',
        database='company_database',
        autocommit=False
    )
    cursor = connection.cursor(buffered=True)

    try:
        cursor.execute("SELECT * FROM department WHERE Dnumber = %s FOR UPDATE", (dnumber,))
        department = cursor.fetchone()
        if not department:
            print("No department found with the given number.")
            return
        
        print("Department to be removed:", department)

        confirm = input("Are you sure you want to delete this department? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Operation cancelled.")
            return

        cursor.execute("SELECT * FROM employee WHERE Dno = %s", (dnumber,))
        if cursor.fetchone():
            print("Cannot remove department: There are employees associated with this department. Please reassign or remove them first.")
            return

        cursor.execute("SELECT * FROM dept_locations WHERE Dnumber = %s", (dnumber,))
        if cursor.fetchone():
            print("Cannot remove department: There are department locations associated with this department. Please remove them first.")
            return

        cursor.execute("DELETE FROM department WHERE Dnumber = %s", (dnumber,))
        connection.commit()
        print("Department removed successfully.")
    except mysql.connector.Error as e:
        print(f"Error occurred: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()


###  Location table  ####
def add_location():
    dnumber = input("Enter the department number: ")

    connection = mysql.connector.connect(
        host='localhost',
        user='JASON',
        passwd='takoyaki-06902',
        database='company_database',
        autocommit=False  
    )
    cursor = connection.cursor(buffered=True)

    try:
        cursor.execute("SELECT Dname FROM department WHERE Dnumber = %s FOR UPDATE", (dnumber,))
        department = cursor.fetchone()
        if not department:
            print("No department found with the given number.")
            return
        else:
            print(f"Department {department[0]} locked for update.")
        
        cursor.execute("SELECT Dlocation FROM dept_locations WHERE Dnumber = %s", (dnumber,))
        locations = cursor.fetchall()
        if locations:
            print("Current locations:")
            for location in locations:
                print(location[0])
        else:
            print("This department currently has no locations.")

        new_location = input("Enter new location: ")
        cursor.execute("INSERT INTO dept_locations (Dnumber, Dlocation) VALUES (%s, %s)", (dnumber, new_location))
        connection.commit()
        print("New location added successfully.")
    except mysql.connector.Error as e:
        print(f"Error occurred: {e}")
        connection.rollback()  
    finally:
        cursor.close()
        connection.close()


def remove_location():
    dnumber = input("Enter the department number: ")

    connection = mysql.connector.connect(
        host='localhost',
        user='JASON',
        passwd='takoyaki-06902',
        database='company_database',
        autocommit=False  
    )
    cursor = connection.cursor(buffered=True)

    try:
        cursor.execute("SELECT Dname FROM department WHERE Dnumber = %s FOR UPDATE", (dnumber,))
        department = cursor.fetchone()
        if not department:
            print("No department found with the given number.")
            return
        else:
            print(f"Department {department[0]} locked for update.")
        
    
        cursor.execute("SELECT Dlocation FROM dept_locations WHERE Dnumber = %s", (dnumber,))
        locations = cursor.fetchall()
        if locations:
            print("Current locations:")
            for location in locations:
                print(location[0])
        else:
            print("This department currently has no locations.")
            return

        
        location_to_remove = input("Enter the location to be removed: ")
        cursor.execute("DELETE FROM dept_locations WHERE Dnumber = %s AND Dlocation = %s", (dnumber, location_to_remove))
        
        if cursor.rowcount == 0:
            print("No location found with the given name for this department.")
        else:
            connection.commit()
            print("Location removed successfully.")
    except mysql.connector.Error as e:
        print(f"Error occurred: {e}")
        connection.rollback()  
    finally:
        cursor.close()
        connection.close()


###  Dependent table  ####
def add_dependent():
    ssn = input("Enter the employee's SSN: ")

    connection = mysql.connector.connect(
        host='localhost',
        user='JASON',
        passwd='takoyaki-06902',
        database='company_database',
        autocommit=False
    )
    cursor = connection.cursor(buffered=True)

    try:
        cursor.execute("SELECT * FROM employee WHERE Ssn = %s FOR UPDATE", (ssn,))
        employee = cursor.fetchone()
        if not employee:
            print("No employee found with SSN:", ssn)
            return

        cursor.execute("SELECT * FROM dependent WHERE Essn = %s", (ssn,))
        dependents = cursor.fetchall()
        print("Current dependents:")
        for dep in dependents:
            print(dep)

        dep_name = input("Enter dependent's name: ")
        sex = input("Enter dependent's sex (M/F): ")
        bdate = input("Enter dependent's birth date (YYYY-MM-DD): ")
        relationship = input("Enter relationship to employee: ")

        cursor.execute("INSERT INTO dependent (Essn, Dependent_name, Sex, Bdate, Relationship) VALUES (%s, %s, %s, %s, %s)",
                       (ssn, dep_name, sex, bdate, relationship))
        connection.commit()
        print("New dependent added successfully.")
    except mysql.connector.Error as e:
        print(f"Error occurred: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()


def remove_dependent():
    ssn = input("Enter the employee's SSN: ")

    connection = mysql.connector.connect(
        host='localhost',
        user='JASON',
        passwd='takoyaki-06902',
        database='company_database',
        autocommit=False
    )
    cursor = connection.cursor(buffered=True)

    try:
        cursor.execute("SELECT * FROM employee WHERE Ssn = %s FOR UPDATE", (ssn,))
        employee = cursor.fetchone()
        if not employee:
            print("No employee found with SSN:", ssn)
            return
        
        cursor.execute("SELECT * FROM dependent WHERE Essn = %s", (ssn,))
        dependents = cursor.fetchall()
        if not dependents:
            print("This employee has no dependents.")
            return
        else:
            print("Current dependents:")
            for dep in dependents:
                print(dep[1])  

        dep_name = input("Enter the name of the dependent to be removed: ")

        cursor.execute("DELETE FROM dependent WHERE Essn = %s AND Dependent_name = %s", (ssn, dep_name))
        if cursor.rowcount == 0:
            print("No dependent found with the given name for this employee.")
        else:
            connection.commit()
            print("Dependent removed successfully.")
    except mysql.connector.Error as e:
        print(f"Error occurred: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()


########################################
### employee table  menu ####
def manage_employees():
    print ("Choose which operation you want to perform on the Employees table:")
    print ("0. Back to main menu")
    print("1. add employee")
    print("2. view employee")
    print("3. modify employee")
    print("4. remove employee")

    choice = input("Enter your choice: ")
    if choice == '0':
        back_to_main_menu()
    elif choice == '1':
        add_employee()
    elif choice == '2':
        view_employee()
    elif choice == '3':
        modify_employee()
    elif choice == '4':
        remove_employees()
    else:
        print("Invalid choice")

### department table  menu ####
def manage_departments():
    print ("Choose which operation you want to perform on the Departments table:")
    print ("0. Back to main menu")
    print ("1. add department")
    print ("2. view department")
    print ("3. remove department")

    choice = input("Enter your choice: ")
    if choice == '0':
        back_to_main_menu()
    elif choice == '1':
        add_department()
    elif choice == '2':
        view_department()
    elif choice == '3':
        remove_department()
    else:
        print("Invalid choice")

### location table  menu ####

def manage_locations():
    print ("Choose which operation you want to perform on the Locations table:")
    print ("0. Back to main menu")
    print ("1. add location")
    print ("2. remove location")
   

    choice = input("Enter your choice: ")
    if choice == '0':
       back_to_main_menu()
    elif choice == '1':
        add_location()
    elif choice == '2':
        remove_location()
    else:
        print("Invalid choice")

### dependent table  menu ####
def manage_dependents():
    print ("Choose which operation you want to perform on the Dependents table:")
    print ("0. Back to main menu")
    print ("1. add dependent")
    print ("2. remove dependent")

    choice = input("Enter your choice: ")
    if choice == '0':
       back_to_main_menu()
    elif choice == '1':
        add_dependent()
    elif choice == '2':
        remove_dependent()
  
    else:
        print("Invalid choice")


def main():
    print("\nChoose which table you want to manage or exit:")
    print("0. Exit")
    print("1. Employees")
    print("2. Departments")
    print("3. Department locations")
    print("4. Dependent")
    choice = input("Enter your choice: ")
    running = True
    while running:
        if choice == '0':
            running = False
            exit(0)
        elif choice == '1':
            manage_employees()
        elif choice == '2':
            manage_departments()
        elif choice == '3':
            manage_locations()
        elif choice == '4':
            manage_dependents()
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()