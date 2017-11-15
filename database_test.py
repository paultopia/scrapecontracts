
# coding: utf-8

# In[2]:

import sqlite3
import datetime
def now():
    return str(datetime.datetime.now())
def create_database(filename):
    conn = sqlite3.connect(filename)
    contracts_table = """ CREATE TABLE IF NOT EXISTS contracts (
                                        id integer PRIMARY KEY,
                                        added text NOT NULL,
                                        url text NOT NULL,
                                        contract text NOT NULL
                                    ); """
    c = conn.cursor()
    c.execute(contracts_table)
    return conn

def add_data(conn, url, text):
    insert_contract = """ INSERT INTO contracts(added,url,contract)
              VALUES(?,?,?) """
    c = conn.cursor()
    data = (now(), url, text)
    c.execute(insert_contract, data)
    conn.commit()
    return c.lastrowid

test_data = "this is some text"
test_url = "http://gowder.io"
test_database = "testing.db"

testconn = create_database(test_database)
result = add_data(testconn, test_url, test_data)
print(result)
testconn.close()
    


# In[3]:

import pandas as pd

conn = sqlite3.connect(test_database)
df = pd.read_sql_query("SELECT * from contracts", conn)
df.head()
conn.close()


# In[4]:

df.head()


# In[ ]:



