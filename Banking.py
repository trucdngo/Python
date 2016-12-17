#!/usr/bin/python
# Project: Banking System ver 1.0
# Student: Truc Ngo
# References
# https://docs.python.org/2/library/sqlite3.html

from random import randint
import sqlite3
import time
import re

key = "ravi"
bankingDb = "./bankingDb.sqlite"
tableName = "BankDatabase"


# Display menu
def display_menu():
    print
    print "MENU"
    print "1:  Open new account"
    print "2:  Check balance"
    print "3:  Deposit"
    print "4:  Withdraw"
    print "5:  Close an account"
    print "6:  Check Promotions"
    print "7:  Show active customer accounts (ADMIN)"
    print "8:  Show **ALL* customer accounts (ADMIN)"
    print "9:  List customers by joining date  (ADMIN)"
    print "10: Save customer list to text file (ADMIN)"
    print "11: Quit Program"
    print
    print "How may I help you?"


# Main menu
def main_menu():
    while True:
        display_menu()
        choice = raw_input("Please make a choice: ")
        print

        if choice == '1':
            customer_interface_new_account()
        elif choice == '2':
            customer_interface_check_balance()
        elif choice == '3':
            customer_interface_deposit()
        elif choice == '4':
            customer_interface_withdraw()
        elif choice == '5':
            customer_interface_close_account()
        elif choice == '6':
            check_promotions()
        elif choice == '7':
            get_all_active_customer_records_in_database()
        elif choice == '8':
            get_all_customer_records_in_database()
        elif choice == '9':
            list_customers_by_join_date()
        elif choice == '10':
            save_customer_list_to_csv()
        elif choice == '11':
            return


# Add a new record to database
def add_a_record_to_database(ssn_number, name, age, balance, join_date, account_status):
    conn = sqlite3.connect(bankingDb)
    c = conn.cursor()
    c.execute('INSERT INTO '+ tableName + ' VALUES(?,?,?,?,?,?)',(ssn_number, name, age, balance, join_date, account_status))
    conn.commit()
    conn.close()


# To return current date in format yyyy/mm/dd
def get_current_date():
    return time.strftime("%Y-%m-%d")


# Set balance of a record
# To deposit, withdraw
def set_balance_of_record(ssn_number, amount):
    conn = sqlite3.connect(bankingDb)
    c = conn.cursor()
    query = 'UPDATE {field1} SET {field2} = {field3} WHERE {field4} = '.\
            format(field1=tableName, field2='Balance', field3=amount, field4='SSN') + "'" + ssn_number + "'"
    c.execute(query)
    conn.commit()
    conn.close()


# Reactivate a previously closed account
# First delete the "closed" account
# Then open a new account
def reactive_account(ssn_number, name, age, balance, join_date, accountStatus):
    record = (ssn_number, name, age, balance, join_date, accountStatus)
    conn = sqlite3.connect(bankingDb)
    c = conn.cursor()
    query = 'DELETE FROM {field1} WHERE {field2} ='.\
            format(field1=tableName, field2='SSN') + "'" + ssn_number + "'"
    c.execute(query)
    conn.commit()
    conn.close()
    add_a_record_to_database(*record)


# Print out all records in database
# return a tuple
def get_all_records_in_database():
    conn = sqlite3.connect(bankingDb)
    c = conn.cursor()
    query = ('SELECT * FROM ' + tableName + '')
    c.execute(query)
    all_rows = c.fetchall()
    conn.commit()
    conn.close()
    return all_rows
    #return list(all_rows[0])[3])


# Print records in database in proper format
# records is a tuple
# if print_all == 0: print out all records
# if print_all == 1: print out only active records
def print_records_in_table(records, print_all=1):
    records_as_list = list(records)
    field1 = "SSN Num."
    field2 = "Name"
    field3 = "Age"
    field4 = "Balance"
    field5 = "JoinDate"
    field6 = "AccountActive(?)"
    print "List of Customers:"
    # If user wants to print active accounts only
    if print_all:
        print "%-15s %-20s %-5s %-13s %-13s" %(field1, field2, field3, field4, field5)
        for record in records_as_list:
            # print only active records
            # if AccountActive == 1
            if record[5]:
                print "%-15s %-20s %-5d %-13.2f %-13s" %(record[0],record[1],int(record[2]),float(record[3]),record[4])
    else:
        print "%-15s %-20s %-5s %-13s %-13s %-20s" %(field1, field2, field3, field4, field5, field6)
        for record in records_as_list:
            if record[5]:
                acct_active_status = 'Yes'
            else:
                acct_active_status = 'No'
            print "%-15s %-20s %-5d %-13.2f %-13s %-20s" %(record[0],record[1],int(record[2]),float(record[3]),\
                                                     record[4], acct_active_status)


# Check if account is active in database
def account_is_active_in_database(ssn_number):
    ssn_field = "SSN";
    account_status_field = "ActiveAccount";
    conn = sqlite3.connect(bankingDb)
    c = conn.cursor()
    query = 'SELECT * FROM {table_name} WHERE {fieldName1} = '.format(table_name=tableName, fieldName1=ssn_field) +\
            "'" + ssn_number + "'" + ' AND {fieldName2} = 1'.format(fieldName2=account_status_field)
    c.execute(query)
    conn.commit()
    all_rows = c.fetchall()
    conn.close()
    # Count records in database
    record_counter = 0
    for item in all_rows:
        record_counter += 1

    if record_counter > 0:
        return True
    else:
        return False


# Check if account is in database and inactive
def account_is_inactive_in_database(ssn_number):
    ssn_field = "SSN";
    account_status_field = "ActiveAccount";
    conn = sqlite3.connect(bankingDb)
    c = conn.cursor()
    query = 'SELECT * FROM {table_name} WHERE {fieldName1} = '.format(table_name=tableName, fieldName1=ssn_field) +\
            "'" + ssn_number + "'" + ' AND {fieldName2} = 0'.format(fieldName2=account_status_field)
    c.execute(query)
    conn.commit()
    all_rows = c.fetchall()
    conn.close()
    # Count records in database
    record_counter = 0
    for item in all_rows:
        record_counter += 1
    if record_counter > 0:
        return True
    else:
        return False


# Return data on the account as a list = [ssn, name, age, balance, join_date, account status]
def get_account_information(ssn_number):
    ssn_field = "SSN";
    account_status_field = "ActiveAccount";
    conn = sqlite3.connect(bankingDb)
    c = conn.cursor()
    query = 'SELECT * FROM {table_name} WHERE {fieldName1} = '.format(table_name=tableName, fieldName1=ssn_field) +\
            "'" + ssn_number + "'" + ' AND {fieldName2} = 1'.format(fieldName2=account_status_field)
    c.execute(query)
    conn.commit()
    all_rows = c.fetchall()
    conn.close()
    return list(all_rows[0])


# Customer to delete his/her account
# It does not actually delete a record
# This method only marks the record as inactive - practically makes it invisible to UI
def delete_a_record_in_database(ssn_number):
    ssn_field = "SSN";
    account_status_field = "ActiveAccount";
    conn = sqlite3.connect(bankingDb)
    c = conn.cursor()
    query = 'UPDATE {table_name} SET {account_status} = 0 WHERE {fieldName} = '.\
            format(table_name=tableName, account_status=account_status_field, fieldName=ssn_field) +\
            "'" + ssn_number + "'"
    c.execute(query)
    conn.commit()
    conn.close()


# User wants to close his/her account
# First checks if account is currently active
# Issue a check for the value of the balance and close account
def customer_interface_close_account():
    print "Program to close your account"
    ssn_number = raw_input("Please enter your SSN ###-##-####: ")
    social_number_pattern = '(^\d{3})-(\d{2})-(\d{4})$';
    if re.match(social_number_pattern, ssn_number):
        if account_is_active_in_database(ssn_number):
            customer_data = get_account_information(ssn_number)
            this_customer = Customer(*customer_data)
            print "Your name is: " + this_customer.get_name()
            print "Here is a check for the amount of your current balance: $%.2f" %this_customer.get_balance()
            this_customer.set_balance(0.0)
            set_balance_of_record(ssn_number, this_customer.get_balance())
            delete_a_record_in_database(ssn_number)
            print "Account with SSN#: " + ssn_number + " has been closed."
        else:
            print "Account with SSN#: " + ssn_number + " is not found in database."
    else:
        print "Invalid SSN number!"


# User checks for any on-going promotion
def check_promotions():
    random_number = randint(0,9)
    print "PROMOTION!"
    if random_number == 0:
        print "5% cash back on all credit card spending up to $10,000"
    elif random_number == 1:
        print "No annual fee for all new checking and saving accounts"
    elif random_number == 2:
        print "No fee when you open a new home credit line"
    elif random_number == 3:
        print "3% cash back on all credit card spending up to $5,000"
    elif random_number == 4:
        print "$200 cash back for all new checking account with balance > $10,000"
    elif random_number == 5:
        print "3% rate on all 6-month CDs"
    elif random_number == 6:
        print "No fee no cost for all home loans"
    elif random_number == 7:
        print "300 free trades for new brokerage account"
    elif random_number == 8:
        print "4.5% APR on all loans over $20,000"
    elif random_number == 9:
        print "Free $300 for new saving account over $20,000"


# User wants to create new account
# Check SSN # if record already exists in database
def customer_interface_new_account():
    print "Program to open new account"
    answer = raw_input("Do you want to create a new account (y,n)?")
    if answer.lower() == 'y':
        ssn = raw_input("Your SSN is ###-##-####: ")
        social_number_pattern = '(^\d{3})-(\d{2})-(\d{4})$';
        if re.match(social_number_pattern, ssn):
            name = raw_input("Your name is: ")
            name_pattern = '[a-zA-Z\s]';
            if re.match(name_pattern, name):
                age = raw_input("Your age is: ")
                if age.isdigit():
                    initial_deposit = raw_input("How much do you want to deposit: ")
                    deposit_pattern = '[0-9\.0-9]';
                    if re.match(deposit_pattern, initial_deposit) and initial_deposit != '.':
                        activate_account = 1
                        join_date = get_current_date()
                    else:
                        print "invalid format for deposit amount.  Must be a number!"
                        return
                else:
                    print "invalid format for age!"
                    return
            else:
                print "invalid name!"
                return
        else:
            print "invalid SSN number!"
            return

        customer_data = (ssn, name, age, initial_deposit, join_date, activate_account)
        if account_is_active_in_database(ssn):
            print "There is already an active account with SSN# " + ssn + " in database."
            print "Please check your SSN# (!)"
        elif account_is_inactive_in_database(ssn):
            print "There was a (closed) account with SSN # " + ssn + " in database."
            answer = raw_input("Do you want to re-open that account (y,n)?")
            if answer.lower() == 'y':
                new_customer = Customer(*customer_data)
                reactive_account(*customer_data)
                print "Your account has been created."
            elif answer.lower() == 'n':
                print "Please check with credit agency for potential identity theft"
        else:
            new_customer = Customer(*customer_data)
            new_customer.save_to_database()
            print "Your account has been created in database."
        print
    else:
        print "Hope to have you as our customer next time!"
        print


# User wants to check his/her account
# First checks if account is active
# Return the balance
def customer_interface_check_balance():
    print "Program to check your account-balance"
    ssn_number = raw_input("What is your ssn ###-##-####: ")
    social_number_pattern = '(^\d{3})-(\d{2})-(\d{4})$';
    if re.match(social_number_pattern, ssn_number):
        if account_is_active_in_database(ssn_number):
            customer_data = get_account_information(ssn_number)
            current_customer = Customer(*customer_data)
            print
            print "Your name is: %s" %(current_customer.get_name())
            print "Your account balance is: $%.2f" %(current_customer.get_balance())
            print
        else:
            print "Invalid SSN number!"
    else:
        print "Invalid format of SSN number!"


def __isDigitNumberToDeposit():
    counter = 2
    while counter > 0:
        amount = raw_input("How much do you want to deposit? ")
        amount_pattern = '[0-9\.0-9]';
        if re.match(amount_pattern, amount) and amount != '.':
            return amount
            counter -=2
        else:
            counter -= 1
            print "Invalid Input Data!"
            if counter > 0:
                print "You can try %d more time." % counter
            if counter == 0:
                return False


# Customer to deposit
def customer_interface_deposit():
    print "Program to make a deposit"
    ssn_number = raw_input("What is your ssn ###-##-####: ")
    social_number_pattern = '(^\d{3})-(\d{2})-(\d{4})$';
    if re.match(social_number_pattern, ssn_number):
        if account_is_active_in_database(ssn_number):
            customer_data = get_account_information(ssn_number)
            current_customer = Customer(*customer_data)
            print
            print "Your name is: %s" %(current_customer.get_name())
            print "Your account balance is: $%.2f" %(current_customer.get_balance())
            amount = __isDigitNumberToDeposit()
            if amount:
                current_customer.deposit(float(amount))
                set_balance_of_record(ssn_number, current_customer.get_balance())
                print "Your account new balance is: $%.2f" %(current_customer.get_balance())
        else:
            print "Invalid SSN number!"
    else:
        print "Invalid format of SSN number!"


def __isDigitNumberToWithdraw():
    counter = 2
    while counter > 0:
        amount = raw_input("How much do you want to withdraw? ")
        amount_pattern = '[0-9\.0-9]';
        if re.match(amount_pattern, amount) and amount != '.':
            return amount
            counter -=2
        else:
            counter -= 1
            print "Invalid Input Data!"
            if counter > 0:
                print "You can try %d more time." % counter
            if counter == 0:
                return False


# Customer to withdraw
def customer_interface_withdraw():
    print "Program to make a withdrawal"
    ssn_number = raw_input("What is your ssn ###-##-####: ")
    social_number_pattern = '(^\d{3})-(\d{2})-(\d{4})$';
    if re.match(social_number_pattern, ssn_number):
        if account_is_active_in_database(ssn_number):
            customer_data = get_account_information(ssn_number)
            current_customer = Customer(*customer_data)
            print
            print "Your name is: %s" %(current_customer.get_name())
            balance = current_customer.get_balance()
            print "Your account balance is: $%.2f" %balance
            amount = __isDigitNumberToWithdraw()
            if amount:
                amount = float(amount)
                while (amount - balance) > 0.0:
                    print "Your withdrawal amount should be less than your balance."
                    amount = __isDigitNumberToWithdraw()
                    amount = float(amount)
                current_customer.withdraw(amount)
                print "Here is your $ for amount of $%.2f" %amount
                set_balance_of_record(ssn_number, current_customer.get_balance())
                print "Your account's balance is now: $%.2f" %current_customer.get_balance()
        else:
            print "Invalid SSN number!"
    else:
        print "Invalid format of SSN number!"


# Bank manager wants to list all *ACTIVE* customer in database
def get_all_active_customer_records_in_database():
    counter = 3
    while counter > 0:
        keyword = raw_input("Please enter password (Hint = your name): ");
        if keyword.lower() == key:
            records = get_all_records_in_database()
            print_records_in_table(records)
            counter -=3
        else:
            counter -= 1
            if counter > 0:
                print "You can try %d more time(s)." % counter


# Bank manager wants to list *ALL* (active and inactive) customer in database
def get_all_customer_records_in_database():
    counter = 3
    while counter > 0:
        keyword = raw_input("Please enter password (Hint = your name): ");
        if keyword.lower() == key:
            records = get_all_records_in_database()
            print_records_in_table(records, 0)
            counter -=3
        else:
            counter -= 1
            if counter > 0:
                print "You can try %d more time(s)." % counter


# List customers by join date
# Will ask for a range of join_date in which customers will be located
def list_customers_by_join_date():
    counter = 3
    while counter > 0:
        keyword = raw_input("Please enter password (Hint = your name): ");
        if keyword.lower() == key:
            print "Please enter two join dates in which customers will be located"
            from_date = raw_input("From (yyyy-mm-dd): ")
            to_date = raw_input("To (yyyy-mm-dd): ")
            date_pattern = '(^\d{4})-(\d{2})-(\d{2})$';
            if re.match(date_pattern, from_date) and re.match(date_pattern, to_date):
                join_date_field = "JoinDate"
                conn = sqlite3.connect(bankingDb)
                c = conn.cursor()
                query = 'SELECT * FROM {table_name} WHERE {fieldName1} BETWEEN '.\
                    format(table_name=tableName, fieldName1=join_date_field) +\
                    "'" + from_date + "'" + " AND " + "'" + to_date + "'" + " ORDER BY {fieldname2}".format(fieldname2=join_date_field)
                c.execute(query)
                conn.commit()
                all_rows = c.fetchall()
                conn.close()
                print_records_in_table(all_rows)
                counter -=3
            else:
                counter -= 1
                print "Invalid input data for date!"
                if counter > 0:
                    print "You can try %d more time(s)." % counter
        else:
            counter -= 1
            if counter > 0:
                print "You can try %d more time(s)." % counter


# save customer data to a CSV file
# This file can be imported to Excel for display
# using Excel's text-to-column feature
def save_customer_list_to_csv():
    counter = 3
    while counter > 0:
        keyword = raw_input("Please enter password (Hint = your name): ");
        if keyword.lower() == key:
            records = get_all_records_in_database()
            print_records_in_table(records)
            '''save to file '''
            file_object = open("CustomerData.txt", "w")
            title = ["ssn_number", "name", "age", "balance", "join_date", "account_status"]
            field_counter = 0
            # write title
            for i in title:
                field_counter += 1
                file_object.write(i)
                if field_counter < len(title):
                    file_object.write(",")
            file_object.write("\n")
            # write fields in each record
            for record in records:
                field_counter = 0
                for field in record:
                    field_counter += 1
                    file_object.write(str(field))
                    if field_counter < len(record):
                        file_object.write(",")
                file_object.write("\n")
            file_object.close()
            print
            print "Attention!"
            print "Customer data has been saved to current directory: CustomerData.txt"
            counter -=3
        else:
            counter -= 1
            if counter > 0:
                print "You can try %d more time(s)." % counter


class Customer:
    # flag is for "active" account (flag = 1)
    # for non-active account or deleted account, (flag = 0)
    def __init__(self, ssn, name, age, initial_deposit, join_date, flag):
        self.__SSN = ssn
        self.__name = name
        self.__age = int(age)
        self.__balance = float(initial_deposit)
        self.__join_date = join_date
        self.__flag = flag

    def withdraw(self, amount):
        self.__balance -= amount

    def deposit(self, amount):
        self.__balance += amount

    def get_balance(self):
        return self.__balance

    def set_balance(self, amount):
        self.__balance = amount

    def get_name(self):
        return self.__name

    def save_to_database(self):
        record = (self.__SSN,
                  self.__name,
                  self.__age,
                  self.__balance,
                  self.__join_date,
                  self.__flag)
        add_a_record_to_database(*record)


# Run only once to initialize this project
# Create a database
def create_database():
    conn = sqlite3.connect(bankingDb)
    field1 = "SSN"
    field2 = "Name"
    field3 = "Age"
    field4 = "Balance"
    field5 = "JoinDate"
    field6 = "ActiveAccount"
    c = conn.cursor()
    c.execute('CREATE TABLE {tn} ({f1} PRIMARY KEY,{f2},{f3},{f4},{f5},{f6})'.\
              format(tn=tableName, f1=field1, f2=field2, f3=field3, f4=field4, f5=field5, f6=field6))
    conn.commit()
    conn.close()


# Run only once to initialize project
def set_up_project():
    add_a_record_to_database("156-45-0781","Michael Jackson", 50, 0, "1990-02-12", 0)
    add_a_record_to_database("873-01-1782","William Elliot", 73, 0, "1991-03-14", 0)
    add_a_record_to_database("123-26-7783","John Grisham", 53, 0, "1982-04-30", 0)

    add_a_record_to_database("123-55-6784","Truc Ngo", 23, 10000, "2012-04-09", 1)
    add_a_record_to_database("463-01-1785","John Borg", 53, 20000, "2015-03-02", 1)
    add_a_record_to_database("193-46-6886","Bill Gates", 33, 11000.45, "2010-07-09", 1)
    add_a_record_to_database("728-85-2387","Larry Ellison", 23, 610000, "2011-06-23", 1)
    add_a_record_to_database("863-15-6588","Mark Zunck", 18, 900000, "2009-05-15", 1)
    add_a_record_to_database("935-49-7989","Steven Harrison", 54, 10000000, "2013-12-12",1)
    add_a_record_to_database("386-48-1281","Elton John", 44, 1000.34, "2012-11-01",1)
    add_a_record_to_database("365-35-6492","Richard Marx", 37, 90000.34, "1993-02-13",1)
    add_a_record_to_database("725-12-1473","Albert Einstein", 73, 23000.99, "1994-01-15",1)
    add_a_record_to_database("336-43-9824","Bill Clinton", 36, 510000, "2000-12-01",1)
    add_a_record_to_database("125-39-7295","Mel Gibson", 45, 880000.20, "1992-05-14",1)
    add_a_record_to_database("793-16-1376","Harrison Ford", 53, 153400.84, "1995-07-11",1)
    add_a_record_to_database("746-93-9327","Bruce Willis", 56, 1210000.12, "1999-09-12",1)
    add_a_record_to_database("123-45-6789","Taylor Swift", 27, 700000, "2016-07-12",1)


if __name__=='__main__':
    #setup database
    #create_database()

    #setup accounts
    #set_up_project()
    main_menu()