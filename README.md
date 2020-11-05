# Sparkify Database

Sparkify database is a Postgres database that stores the user activity and songs metadata on Sparkify's new streaming application. Previously this information was available in JSON files. ETL pipeline is built using python scripts to transfer the data from JSON files to Sparkify Postgres database.

## Purpose

- The database provides Sparkify's analytical team with easy access to the data on their new streaming application.
- The design of the database tables is optimized for queries on song play analysis.

## Database Schema Design

Sparkify database tables form a star schema. This database design separates facts and dimensions yielding a subject-oriented design where data is stored according to logical relationships, not according to how the data was entered. 

- Fact And Dimension Tables

    The database includes:
    - Fact table:
        
        1. **songplays** - records in log data associated with song plays i.e. records with page NextSong
            - songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
            
    - Dimension tables:
        
        2. **users** - users in the app
            - user_id, first_name, last_name, gender, level
        3. **songs** - songs in music database
            - song_id, title, artist_id, year, duration
        4. **artists** - artists in music database
            - artist_id, name, location, latitude, longitude
        5. **time** - timestamps of records in songplays broken down into specific units
            - start_time, hour, day, week, month, year, weekday

## ETL Pipeline

An ETL pipeline is built using python. The python script reads and processes files from song_data and log_data and loads them into the Sparkify database tables.
    
## Running Python Scripts
    
The following python scripts are used to create database tables and read and process files from song_data and log_data and to insert the records into the database tables:

1. **create_tables.py** 
This script drops and creates database tables. This script imports and uses drop and create statements from *sql_queries.py* script. Run this file to reset the database tables before running ETL scripts.
*Run below command in terminal to execute this script:*
    `python create_tables.py`

2. **etl.py**
This script reads and processes files from song_data and log_data and loads them into the database tables. 
*Run below command in terminal to execute this script:*
        `python etl.py`






    

