#!/usr/bin/env python
# coding: utf-8

# Tutorial: ETL-like Operations with Meteo Data using Python

# In this tutorial, we will perform the following steps:
# 1. Scrape the past 12 months of data in 30-day windows using the '
#    api_scraper(start, end)' function.
# 2. Convert the results into Pandas DataFrames.
# 3. Create an SQLite database and idempotently insert the data into it.
# 4. Perform basic querying on the data.
#
# There are some ugly bugs in the scraper and insertion logic!
# Can you AI assistant fix them? And... can your AI assistant help you write
# some basic SQL queries to answer questions about the data?


# Step 1: Import necessary libraries and define the API scraper function

import pandas as pd
import sqlite3


# Step 1: import api scraper.
# You can open the python and have Codeium explain you what is happening!
# For example, try deleting the docstrings from the conversion functions, and have
# Codeium tell you what the (now undocumented) code does!

from knmi import api_scraper


# Step 2: Define a function to scrape past year data in 30-day windows

import datetime


def scrape_past_year_data(api_scraper_func):
    # Get today's date
    today = datetime.date.today()

    # Set the number of days in each window
    window_size = 30

    # Initialize lists to store the data
    data_frames = []
    start_date = today - datetime.timedelta(days=365)
    end_date = start_date + datetime.timedelta(days=window_size - 1)

    while end_date < today:
        # Scrape data for the current window
        meteo_data = api_scraper_func(start_date, end_date - datetime.timedelta(days=1))

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(meteo_data)

        # Append the DataFrame to the list
        data_frames.append(df)

        # Move the window forward for the next iteration
        start_date = end_date + datetime.timedelta(days=1)
        end_date = start_date + datetime.timedelta(days=window_size + 1)

    return data_frames


# Step 3: Create SQLite database and insert data


def create_database_and_insert_data(data_frames, db_file):
    # Establish a connection to the database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Iterate through each DataFrame and insert its data into the database
    for i, df in enumerate(data_frames):
        # Use the DataFrame's 'to_sql' method to insert data into the database
        # If the table already exists, 'if_exists' will ensure records are inserted if they don't already exist.
        # Here, 'YYYYMMDD' is assumed to be a unique key for each record.
        df.to_sql(name=f"meteo_data", con=conn, if_exists="append", index=False)
        print(f"Inserted {len(df)} records into table {i + 1} of {len(data_frames)}")

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()


# Step 4: Perform basic querying on the data


def perform_basic_querying(db_file):
    # Establish a connection to the database
    conn = sqlite3.connect(db_file)

    # Query 1: Get the number of records in the table
    query1 = "SELECT COUNT(*) as num_records FROM meteo_data;"

    # Execute the query and fetch the results into a DataFrame
    result_df = pd.read_sql_query(query1, conn)

    # Print the query result
    print("Number of records in the table:")
    print(result_df)

    # Query 2: Get the average temperature for each month
    # works by getting the 5th and 6th character of the YYYMMDD string
    query2 = """
        SELECT AVG(TEMP_GEM) as avg_temperature, SUBSTR(YYYYMMDD, 5, 2) as month 
        FROM meteo_data 
        GROUP BY month;
        """

    # Execute the query and fetch the results into a DataFrame
    result_df = pd.read_sql_query(query2, conn)

    # Print the query results
    print("\nAverage temperature for each month:")
    print(result_df)

    # Close the database connection
    conn.close()


if __name__ == "__main__":
    # Let's run the code!
    # Do you think this nicely fetches EACH day in the year?
    data_frames = scrape_past_year_data(api_scraper)

    db_file = "meteo_data.db"

    # Is this insertion code really idempotent? What happens when you run the code twice?
    create_database_and_insert_data(data_frames, db_file)
    perform_basic_querying(db_file)
