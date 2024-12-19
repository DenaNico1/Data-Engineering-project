#wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/exchange_rate.csv
import requests
import sqlite3
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime

# Code for ETL operations on Country-GDP data
# initialisation of known entities
url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'
db_name = 'Banks.db'
table_name = 'Largest_banks'
csv_path = '/home/etud/Documents/python_for_data_engineering/bank_project/exchange_rate.csv'
output_path = '/home/etud/Documents/python_for_data_engineering/bank_project/Bank_data.csv'
table_attribs=["Rank","Bank_name","Market_cap"]

# Importing the required libraries


def extract(url, table_attribs):
    page = requests.get(url).text
    data = BeautifulSoup(page,'html.parser')
    df = pd.DataFrame(columns=table_attribs)
    tables = data.find_all('tbody')
    rows = tables[0].find_all('tr')
    for row in rows:
        col = row.find_all('td')
        if len(col)!=0:
            data_dict = {"Rank": col[0].contents[0].strip(),
                         "Bank_name": col[1].contents[2],
                         "Market_cap": col[2].contents[0].strip()}
            df1 = pd.DataFrame(data_dict, index=[0])
            df = pd.concat([df,df1], ignore_index=True)
    
    df['Market_cap'] = (
        df['Market_cap']
        .str.replace(',', '', regex=False)  # Suppression des virgules si présentes
        .str.rstrip()  # Suppression des espaces ou '\n'
        .astype(float)  # Conversion en float
    )
    return df
    

def transform(df, csv_path):
    exchange_rate = pd.read_csv(csv_path)
    exchange_rate = exchange_rate.set_index('Currency').to_dict()['Rate']
    
    # Calcul des nouvelles colonnes en fonction des taux de change
    df['MC_GBP_Billion'] = [np.round(x * exchange_rate['GBP'], 2) for x in df['Market_cap']]
    df['MC_EUR_Billion'] = [np.round(x * exchange_rate['EUR'], 2) for x in df['Market_cap']]
    df['MC_INR_Billion'] = [np.round(x * exchange_rate['INR'], 2) for x in df['Market_cap']]
    
    return df

def load_to_csv(df, output_path):
    df.to_csv(output_path)

def load_to_db(df, sql_connection, table_name):
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)


def run_query(query_statement, sql_connection):
    print(f"Executing query: {query_statement}")
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output)
    return query_output

''' Here, you define the required entities and call the relevant
functions in the correct order to complete the project. Note that this
portion is not inside any function.'''
def log_progress(message):
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    now = datetime.now() # get current timestamp 
    timestamp = now.strftime(timestamp_format) 
    with open("/home/etud/Documents/python_for_data_engineering/bank_project/code_log.txt","a") as f: 
        f.write(timestamp + ' : ' + message + '\n')
log_progress('Preliminaries complete. Initiating ETL process')

df = extract(url, table_attribs)

log_progress('Data extraction complete. Initiating Transformation process')
print(df)

df = transform(df, csv_path)
log_progress('Data transformation complete. Initiating loading process')
print(df)

load_to_csv(df, output_path)

log_progress('Data saved to CSV file')

sql_connection = sqlite3.connect(db_name)

log_progress('SQL Connection initiated.')

load_to_db(df, sql_connection, table_name)

log_progress('Data loaded to Database as table. Running the query')

# Définition des requêtes
query1 = "SELECT * FROM Largest_banks"
query2 = "SELECT AVG(MC_GBP_Billion) FROM Largest_banks"
query3 = "SELECT Bank_name FROM Largest_banks LIMIT 5"

# Exécution des trois requêtes
result1 = run_query(query1, sql_connection)
result2 = run_query(query2, sql_connection)
result3 = run_query(query3, sql_connection)

# Optionnel : organiser les résultats dans un dictionnaire si vous souhaitez les conserver ensemble
results = {
    'all_banks': result1,
    'avg_mc_gbp': result2,
    'top_5_banks': result3
}
print("Results Summary:")
print(f"All Banks: \n{results['all_banks']}")
print(f"Average Market Cap in GBP: \n{results['avg_mc_gbp']}")
print(f"Top 5 Banks by Name: \n{results['top_5_banks']}")

log_progress('Process Complete.')

sql_connection.close() 
