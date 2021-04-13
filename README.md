# Data Moseling with sparkify database for a Music Streaming App  

## The Project Scope:

Music streaming app has records of songs and artists data stored in songs JSON files and the user activity logs are stored in log JSON files. It requires to process songs JSON files and logs JSON files and store the data in sparkify postgresql database tables like songs, artists, users, time and timeplay tables to use for data analytics purposes. 

## Schema description:   

### Fact Table   

1. songplays - records in log data associated with song plays i.e. records with page NextSong   

songplay_id SERIAL CONSTRAINT PRIMARY KEY   
start_time timestamp CONSTRAINT FOREIGN KEY  
user_id int CONSTRAINT FOREIGN KEY  
level varchar   
song_id varchar CONSTRAINT FOREIGN KEY 
artist_id varchar CONSTRAINT FOREIGN KEY  
session_id int   
location varchar   
user_agent varchar 

### Dimension Tables   

1. users - users in the app   

  user_id int CONSTRAINT PRIMARY KEY   
  first_name varchar   
  last_name varchar   
  gender varchar   
  level varchar 


2. songs - songs in music database   

  song_id varchar CONSTRAINT PRIMARY KEY   
  title varchar   
  artist_id varchar   
  year int   
  duration decimal   

3. artists - artists in music database   

  artist_id varchar CONSTRAINT PRIMARY KEY   
  name varchar   
  location varchar   
  latitude decimal   
  longitude decimal   

4. time - timestamps of records in songplays broken down into specific units

  start_time timestamp CONSTRAINT PRIMARY KEY,   
  hour int   
  day int   
  week int   
  month int   
  year int   
  weekday int 


## Project Details and scripts

I wrote  CREATE and DROP SQL statements in sql_queries.py to drop and create each table.   
if the table exists it will drop the table so that it will not get error trying to create the eisting table.
create_tables.py to create sparkify database and dimention and fact tables for star schema.
I build etl processes in the etl.ipynb to run etl processes for each table and ran test.ipynb to check if the table records are inserted correctly. I I used the create_tables.py from etl.py so I need not to run seperately before running the etl process to reset the tables. 
finally I used the main file etl.py to run entire etl processes. I processed the songs json files and stored the information in songs, artists dimention tables and processed all log files and stored the related data in user, time dimention tables and finally inserted some records which has page as 'NextSong' into songpays table using songs and artists fact tables and log json files based on song title, artist name and song duration. and finally ran test.ipynb to confirm that records in all the tables were successfully inserted into each table. 
 
 To run the project, shutdown all the kernels and 
1.Run etl.py which will process the song json files and log json files and select specific data and loads that data into all the five tables. etl.py will utilise the create_tables.py and sql_queries.py and we don't need to run create_tables.py seperately.
2.Next run the test.ipynb to test and see if the data is inserted or not


## Files in the repository:   

### create_tables.py  
This file allows us to drop and create the tables. You run this file to reset your tables before each time you run your ETL scripts.   
## sql_queries.py   
It contains all the sql queries required for ths project, and is imported into etl.py and create_tables.py.
## etl.ipynb   
This is useful to run the code on python notebook and check if that small portion of the code is working or not .
## etl.py   
This is the main file  where all the etl process happens. We need not to run create_tables.py seperately before running etl.py as I included a call from etl.py to create the database and tables. After debugging in python notebook, I added entire etl process into etl.py. I ran etl.py once and tested using test.ipynb once to see if all the records related to the tables are inserted or not.
## test.ipynb   
It is to test if the code in etl is really inserting into the tables or not. It displayes first few rows for testing purposes
## README.md   
This file explains about the project.

## Example queries with results of one record for each table

1. songs table   
   
   song_select = ("""SELECT s.song_id, a.artist_id
                  FROM ( songs s 
                         INNER JOIN artists a 
                         ON (s.artist_id = a.artist_id)) 
                         WHERE ( s.song_id IS NOT NULL
                         and a.artist_id IS NOT NULL
                         and s.title = %s
                         and a.name = %s
                         and s.duration = %s) ;""") 


song_table_insert = ('''INSERT INTO songs (song_id, title, artist_id, year, duration) VALUES (%s, %s, %s, %s, %s) ON CONFLICT ON CONSTRAINT song_id_pk 
                        DO NOTHING;''')

|song_id                |title                   |artist_id               |year      |duration    |   
|:----------------------|:-----------------------|:-----------------------|:---------|:-----------| 
|SOMZWCG12A8C13C480     |I Didn't Mean To        |ARD7TVE1187B99BFB1      |0         |218.93179   |

2. artist table   
    artist_table_insert = ('''INSERT INTO artists (artist_id, name, location, latitude, longitude) VALUES (%s, %s, %s, %s, %s) ON CONFLICT  
                              ON  CONSTRAINT artist_id_pk DO NOTHING;''')

|artist_id              |name                    |location                    |latitude           |longitude      |   
|:----------------------|:-----------------------|:-----------------------    |:---------         |:-----------   | 
|AR10USD1187B99F3F1     |Tweeterfriendly Music   |Burlington, Ontario, Canada |NaN                |NaN            |
        

3. users table   

    user_table_insert = ('''INSERT INTO users (user_id, first_name, last_name, gender, level) VALUES (%s, %s, %s, %s, %s) ON CONFLICT ON CONSTRAINT                                 user_id_pk DO NOTHING;''')

|user_id                | first_name              |last_name                |gender            |level          |
|:----------------------|:----------------------- |:----------------------- |:---------        |:-----------   | 
|86                     | Aiden                   |Hess                     |M                 |free           |   

4. Time table   

   time_table_insert = ('''INSERT INTO time ( start_time, hour, day, week, month, year, weekday) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT ON                                 CONSTRAINT start_time_pk 
                            DO NOTHING;''') 
   
|start_time                     |hour           |day            |week       |month      |year     |weekday    |
|:----------------------        |:--------------|:--------------|:---------  |:-------  |:--------|:----------|   
|1970-01-01 00:25:43.537328     |0              |1              |1           |1         |1970     |3          |   

5. Songplay table   


    songplay_table_insert = ('''INSERT INTO songplays (start_time, user_id, level, song_id,
                            artist_id, session_id, location, user_agent) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ''')
                            

|songplay_id|start_time                 |user_id|level |song_id            |artist_id         |session_id|location                |user_agent                          |
|:--------- |:--------------            |:------|:---- |:-------           |:--------         |:---------|------------            |-----------                         |   
|1          |1970-01-01 00:25:42.837408 |15     |paid  |SOZCTXZ12AB0182364 |AR5KOSW1187FB35FF4|818       |Chicago-Naperville-Elgin,<br> IL-IN-WI|"Mozilla/5.0 (X11; Linux x86_64)<br> AppleWebKit/537.36 (KHTML, like Gecko)<br> Ubuntu Chromium/36.0.1985.125 <br>Chrome/36.0.1985.125 Safari/537.36"



