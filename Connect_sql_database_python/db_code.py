# wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/INSTRUCTOR.csv
import sqlite3
import pandas as pd
conn = sqlite3.connect('STAFF.db')

# create and load the table
table_name = 'INSTRUCTOR'
attribute_list = ['ID', 'FNAME', 'LNAME', 'CITY', 'CCODE']

# Reading the csv file
file_path = '/home/etud/Documents/python_for_data_engineering/sql_database_python/INSTRUCTOR.csv'
df = pd.read_csv(file_path, names = attribute_list)

# loading the data to a table
df.to_sql(table_name, conn, if_exists = 'replace', index =False)
print('Table is ready')

# running basic queries on data
    # viewing all the data in the table

query_statement = f"SELECT * FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

    # viewing only FNAME column of data
query_statement = f"SELECT FNAME FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

    # viewing the total number of entries in the table
query_statement = f"SELECT COUNT(*) FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

# create dataframe of the new data
data_dict = {'ID' : [100],
            'FNAME' : ['John'],
            'LNAME' : ['Doe'],
            'CITY' : ['Paris'],
            'CCODE' : ['FR']}
data_append = pd.DataFrame(data_dict)

# append data on the instructor table
data_append.to_sql(table_name, conn, if_exists = 'append', index =False)
print('Data appended successfully')

# close connectioo the database
conn.close()