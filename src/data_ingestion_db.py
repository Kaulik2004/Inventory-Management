import pandas as pd 
import os
from sqlalchemy import create_engine
import time
from src.logger import logging

# SQLAlchemy is essentially the gold standard database toolkit for Python. It bridges the gap between your Python code and your relational database (like PostgreSQL, MySQL, SQLite, or SQL Server).

# Instead of writing raw SQL strings everywhere, SQLAlchemy lets you interact with your database using Python objects and functions.

engine=create_engine('sqlite:///inventory.db')

def ingest_db(df,table_name,engine):
    # this function converts the dataframe(csv) to tables in SQL
    df.to_sql(table_name, engine, if_exists='replace', index=False, chunksize=10000)
   #  df.to_sql(table_name,engine,if_exists='replace',index=False)


def load_raw_data():
   """
   This function loads all the raw data from the data folder into the database.
   Each file is read into a pandas dataframe and then sent to the ingest_db function to create a table in the database.
   The table name is the file name without the .csv extension.
   """
   start = time.time()
   for file in os.listdir('data'):
      if file.endswith('.csv'):
         print(f'Ingesting file: {file}')
         df = pd.read_csv('data/' + file)
         logging.info(f'Ingesting {file} in db')
         # print(df.shape)
         ingest_db(df, file[:-4], engine)
         # each table is sent to this function to create a table in the sql database. The table name is the file name without the .csv extension.
   end = time.time()
   total_time = (end - start)/60
   logging.info(f'Total time taken to ingest all files: {total_time} minutes')

if __name__ == '__main__':
   load_raw_data()
