import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

# initialisation of known entities
url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
db_name = 'Movies_pratical.db'
table_name = 'Top_100'
csv_path = '/home/etud/Documents/python_for_data_engineering/websraping/top_100_films.csv'
df = pd.DataFrame(columns=["Film","Year","Rotten_Tomatoes_Top_100"])
count = 0

# load the webpage for webscraping
html_page = requests.get(url).text
data = BeautifulSoup(html_page, 'html.parser')

# Scraping of required information
tables = data.find_all('tbody')
rows = tables[0].find_all('tr')

for row in rows:
    if count<100:
        col = row.find_all('td')
        if len(col)!=0:
            data_dict = {"Film": col[1].contents[0],
                         "Year": col[2].contents[0],
                         "Rotten_Tomatoes_Top_100": col[3].contents[0]}
            df1 = pd.DataFrame(data_dict, index=[0])
            df = pd.concat([df,df1], ignore_index=True)
            count+=1
    else:
        break

df = df[df['Rotten_Tomatoes_Top_100'] != "unranked"]
df['Rotten_Tomatoes_Top_100'] = pd.to_numeric(df['Rotten_Tomatoes_Top_100'])
final_df = df.sort_values(by=['Rotten_Tomatoes_Top_100'], ascending=True)
final_df = final_df.head(25)
final_df['Year'] = pd.to_numeric(final_df['Year'])
final_df = final_df[final_df['Year'] >= 2000]
print(final_df) 

# storing the data
final_df.to_csv(csv_path)

conn = sqlite3.connect(db_name)
final_df.to_sql(table_name, conn, if_exists='replace', index=False)
conn.close()
