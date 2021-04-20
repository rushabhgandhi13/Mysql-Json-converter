import mysql.connector
import datetime
import json
from json import JSONEncoder
import getpass


# fetching the database
print("\n\n\n\t\t ******* Welcome to our system :)********\n\n\n")
password1 = getpass.getpass(prompt='Please enter your mysql password :')

conn = mysql.connector.connect(user='root', password=password1,host='127.0.0.1', buffered=True)

if conn:
    print("Connected Successfully")
else:
    print("Connection Not Established")


cursor = conn.cursor()
data = ("show databases")
cursor.execute(data)
list1 = list()
print("Please select a number to corresponding database")
a = 1
for (data) in cursor:
    list1.append(data[0])
    print(f"{a} : {data[0]}")
    a += 1

b = int(input("input :"))
if b > a-1 or b < 1:
    print("please enter correct value")
    b = int(input())
c = list1[b-1]

Current_database = c


# fetching all the tables from the database selected


conn = mysql.connector.connect(user='root', password=password1,host='127.0.0.1', database=c,auth_plugin='mysql_native_password')

if conn:
    print("Connected Successfully")
else:
    print("Connection Not Established")


class create_dict(dict):

    # __init__ function
    def __init__(self):
        self = dict()

    # Function to add key:value
    def add(self, key, value):
        self[key] = value




# for handling date field in mysql database
class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


mydict = create_dict()

cursor = conn.cursor()

# fetching all the tables
list1 = list()
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

print("Please select a number to corresponding table")
a = 1
for (row,) in tables:
    list1.append(row)
    print(f"{a} : {row}")
    a += 1

b = int(input("input :"))
if b > a-1 or b < 1:
    print("please enter correct value")
    b = int(input())
c = list1[b-1]

# fetching the data from the corresponding tables
cursor.execute(
    f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema ='{Current_database}' AND table_name = '{c}'")


count1 = cursor.fetchall()
for (row,) in count1:
    count2 = row

# now fetching the columns for the selected table for making a json object

cursor.execute(
    f"SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='{Current_database}' AND `TABLE_NAME`='{c}';")
count3 = cursor.fetchall()

list_name = list()
for (row,) in count3:
    list_name.append(row)

# making a single string from the columns fetched to further add to the dictionary

string1 = '''({'''
r = 0
for i in range(0, int(count2)):

    string1 = string1+"""'"""+list_name[r]+"""'"""+": row["+str(i)+"]"
    r += 1
    if r < (int(count2)):
        string1 += ","

string1 += '''})'''

# example output-->({'Aadhar_Number': row[0],'Contact_Number': row[1],'Flat_Number': row[2],'OName': row[3]})


# finaly fetching the objects of the table

select_flat = f"SELECT * FROM {Current_database}." + c + ";"
cursor.execute(select_flat)
result = cursor.fetchall()

# adding each object to dictionary along with the corresponding name of the column
a = 1
for row in result:
    mydict.add(a, eval(string1))
    a += 1
# Example output of the dictionary created -->
# {1: {'Aadhar_Number': 4444444, 'Contact_Number': 777, 'Flat_Number': 502, 'OName': 'harsh'}, 2: {'Aadhar_Number': 11111111, 'Contact_Number': 555, 'Flat_Number': 802, 'OName': 'pathik Ghugare'}, 3: {'Aadhar_Number': 222222222, 'Contact_Number': 333, 'Flat_Number': 702, 'OName': 'Ram'}, 4: {'Aadhar_Number': 333333333, 'Contact_Number': 444, 'Flat_Number': 602, 'OName': 'Raju'}}


# converting the dictionary extracted to json object
# example-->"1": {
    #     "Amount": 500.0,
    #     "Amount_paid": 50.0,
    #     "Flat_Number": 502,
    #     "Payment_date": "2021-02-01",
    #     "Penalty_charges": 100,
    #     "Pending_amount": 50.0
    #   },


stud_json = json.dumps(mydict, indent=2, sort_keys=True, cls=DateTimeEncoder)

print(stud_json)

# Storing the json objects in a json file
# overwriting the previous file and writing the updated data
f = open("demo.json", "w")
f.write(stud_json)
f.close()

print("\n\t\t *******File is stored in demo.json in current folder********")
print("\n\t\t ******* Thank You for using our system :)********")
