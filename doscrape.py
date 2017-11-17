import json
import sys
import sqlite3
import logging
import pandas as pd
from kscrape import findTOS
from kdatabase import create_database, add_data

logging.basicConfig(filename='scraping.log',level="INFO")

def scrape_sites(jsonfile, dbconn):
    for site in jsonfile:
        contracts = findTOS(site)
        if contracts:
            for contract in contracts:
                add_data(dbconn, contract["url"], contract["text"])
                logging.info("attempted to add: " + contract["url"]) # if these don't show up in db, I know it failed and I can go back and redo more aggressively.
    dbconn.close()

def save_sites_as_csv(dbfilename, csvfilename): # separate fx because may blow up memory.
    dbconnconn = sqlite3.connect(dbfilename)
    try:
        df = pd.read_sql_query("SELECT * from contracts", dbconn)
        df.write_csv("csvfilename")
    except Exception as e:
        logging.error("failed to load or write csv. here's the error: " + str(e))
    dbconn.close()


if __name__ == "__main__":
    if len(sys.argv) < 4:
        raise Exception("required arguments: JSONFILE with sites, DBFILENAME database to create, CSVFILENAME to attempt to create")
    jsonfile = sys.argv[1]
    dbfilename = sys.argv[2]
    csvfilename = sys.argv[3]
    dbconn = create_database(dbfilename)
    scrape_sites(jsonfile, dbconn)
    save_sites_as_csv(dbfilename, csvfilename)
    print("done executing scraping program!")
    logging.info("done executing scraping program!")
