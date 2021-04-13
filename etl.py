import os
import glob
import psycopg2
import os
import glob
import psycopg2
import pandas as pd
import json
from sql_queries import *
from create_tables import *
from datetime import date
import calendar
#process each song file and insert into song and artist table
def process_song_file(cur, filepath):
    '''
    Processes song files and inserts data into songs and artists tables in sparkify postgres database

            Parameters:
                    cur: A cursor
                    filepath: filepath

            Returns:
                    none
    '''
    
    # open song file
    df = pd.read_json(filepath, lines=True)
    
    # insert song record into songs table
    df[['song_id','title','artist_id']] = df[['song_id','title','artist_id']].astype(str) 
    df['year'] =  df['year'].astype(int)
    df['duration'] = df['duration'].astype(float)
    song_data = df[['song_id','title','artist_id','year','duration']]
    song_data = song_data.values.tolist()
    song_data = song_data[0]
    cur.execute(song_table_insert, song_data)
    
    # insert artist record into artists table
    df[['artist_id','artist_name', 'artist_location']] = df[['artist_id','artist_name', 'artist_location']].astype(str)
    df[['artist_latitude', 'artist_longitude']]=df[['artist_latitude', 'artist_longitude']].astype(float)
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']]
    artist_data = artist_data.values.tolist()
    artist_data=artist_data[0]
    cur.execute(artist_table_insert, artist_data)

# process log file and insert into time, user and songplays tables
def process_log_file(cur, filepath):
    '''
    Process log files and inserts data into time, user and songplaytables in sparkify postgres database.

            Parameters:
                    cur (cursor): A database cursor
                    filepath: filepath of the files to be processed

            Returns:
                    None
    '''

    
    # open log file
    df = pd.read_json(filepath, lines=True)
    
    # filter by NextSong action
    df = df[df['page']=='NextSong']
    
    # convert timestamp column to datetime
    df['ts'] = pd.to_datetime(df['ts'])

  
    # insert time data records into time table
    time_data = [df.ts, df.ts.dt.hour, df.ts.dt.day, df.ts.dt.weekofyear, df.ts.dt.month, df.ts.dt.year, df.ts.dt.weekday]
    column_labels = ['timestamp', 'hour', 'day', 'weekofyear', 'month', 'year', 'weekday']

    # Create DataFrame
    time_df = pd.DataFrame.from_dict(dict(zip(column_labels, time_data)))
    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))
 
        
    # load user table
    column_labels = ['user_id', 'first_name', 'last_name', 'gender', 'level']
    user_data = [df.userId, df.firstName, df.lastName, df.gender, df.level]
 
    # Create DataFrame
    user_df = pd.DataFrame.from_dict(dict(zip(column_labels, user_data)))
  
    # insert user records into user table
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    songplays_data=[]
    ctr=0
    # insert songplay records into songplays table
    column_labels = ['timestamp', 'user_ID', 'level', 'song_ID', 'artist_ID', 'session_ID', 'location', 'user_agent']
    for index, row in df.iterrows():
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()   
        if results:
            songid, artistid = results
            songplay_data = [row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent]
            cur.execute(songplay_table_insert, list(songplay_data))
            print(songplay_data)
        else:
            songid, artistid = None, None
        
# process all the files in the filepath using the function given
def process_data(cur, conn, filepath, func):
    '''
    Gets all the files in the absolute path given.

            Parameters:
                    cur : cursor
                    conn : connection to the sparkify postgres database
                    filepath: filepath of the files to be processed
                    func(function): any function 
            Returns:
                    none
    '''

    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        print(files)
        for f in files :
            print(f)
            print("_____________file ")
            all_files.append(os.path.abspath(f))
            print(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))
# process all the songs and logs files using process_song file and process_log file functions
def main():
    try:
        cur, conn = create_database()
        drop_tables(cur,conn)
        create_tables(cur,conn)
        process_data(cur, conn, filepath='data/song_data', func=process_song_file)
        process_data(cur, conn, filepath='data/log_data', func=process_log_file)
        conn.close()
    except psycopg2.Error as e: 
         print(e)
if __name__ == "__main__":
    main()

