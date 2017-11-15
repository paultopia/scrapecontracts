
# coding: utf-8

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

# I need some exception handling in there.  what does sqlite3 throw or do if the write fails?  
# also are there memory based limits on how many transactions I can commit without closing the connection??
