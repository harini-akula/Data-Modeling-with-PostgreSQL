import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Description: This function can be used to read the file in the filepath (data/song_data)
    to get the song and artist information and used to populate the songs and artists dimension tables.

    Arguments:
        cur: the cursor object. 
        filepath: song data file path. 

    Returns:
        None 
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id','title','artist_id','year','duration']].values[0].tolist()
    try:
        cur.execute(song_table_insert, song_data)
    except psycopg2.Error as e: 
        print("Error: Issue inserting in songs table")
        print (e)  
    
    # insert artist record
    artist_data = df[['artist_id','artist_name','artist_location', 'artist_latitude', 'artist_longitude']].values[0].tolist()
    try:
        cur.execute(artist_table_insert, artist_data)
    except psycopg2.Error as e: 
        print("Error: Issue inserting in artists table") 
        print (e)


def process_log_file(cur, filepath):
    """
    Description: This function can be used to read the file in the filepath (data/log_data)
    to get the user and time information and used to populate the users and time dimension tables.

    Arguments:
        cur: the cursor object. 
        filepath: log data file path. 

    Returns:
        None
    """
    # open log file
    df =  pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = [t, t.dt.hour, t.dt.day, t.dt.weekofyear, t.dt.month, t.dt.year, t.dt.weekday]
    column_labels = ['timestamp', 'hour', 'day', 'weekofyear', 'month', 'year', 'weekday']
    time_df = pd.DataFrame({column_labels[0]: time_data[0], column_labels[1]: time_data[1],
                       column_labels[2]: time_data[2], column_labels[3]: time_data[3],
                       column_labels[4]: time_data[4], column_labels[5]: time_data[5],
                       column_labels[6]: time_data[6]})
    for i, row in time_df.iterrows():
        try:
            cur.execute(time_table_insert, list(row))
        except psycopg2.Error as e: 
            print("Error: Issue inserting in time table") 
            print (e)

    # load user table    
    user_df = df[['userId','firstName','lastName','gender','level']]

    # insert user records
    for i, row in user_df.iterrows():
        try:
            cur.execute(user_table_insert, row)
        except psycopg2.Error as e:
            print("Error: Issue inserting in users table")
            print (e)            

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        try:
            cur.execute(song_select, (row.song, row.artist, row.length))
            results = cur.fetchone()
        
            if results:
                songid, artistid = results
            else:
                songid, artistid = None, None

            # insert songplay record
            songplay_data = (pd.to_datetime(row.ts, unit='ms'), row.userId, row.level, songid, artistid,
                             row.sessionId, row.location, row.userAgent)
            try:
                cur.execute(songplay_table_insert, songplay_data)
            except psycopg2.Error as e: 
                print("Error: Issue inserting in songplay table") 
                print (e)
        except psycopg2.Error as e: 
            print("Error: Issue inserting in song_select table") 
            print (e)
           


def process_data(cur, conn, filepath, func):
    """
    Description: This function can be used to get all files matching extension from all directories
    in any filepath and iterate over these files and process them.

    Arguments:
        cur: the cursor object. 
        conn: the connection object.
        filepath: any file path including 'data/song_data' or 'data/log_data'. 
        func: the function to be called.

    Returns:
        None
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))



def main():
    """
    Description: This function can be used to connect to the Sparkify database and process data 
    in filepaths 'data/song_data' and 'data/log_data'.

    Arguments:
        None.

    Returns:
        None.
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()