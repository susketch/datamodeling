# DROP TABLES 

songplay_table_drop = "DROP table IF EXISTS songplays"

user_table_drop = "DROP table IF EXISTS users"

song_table_drop = "DROP table IF EXISTS songs"

artist_table_drop = "DROP table IF EXISTS artists"

time_table_drop = "DROP table IF EXISTS time"

# CREATE TABLES



user_table_create = ("""CREATE TABLE IF NOT EXISTS users (user_id int CONSTRAINT user_id_pk PRIMARY KEY NOT NULL UNIQUE,
                                                          first_name varchar,
                                                          last_name varchar,
                                                          gender varchar,
                                                          level varchar );""")


song_table_create = ("""CREATE TABLE IF NOT EXISTS songs (song_id varchar CONSTRAINT song_id_pk PRIMARY KEY NOT NULL UNIQUE,
                                                          title varchar,
                                                          artist_id varchar,
                                                          year int,
                                                          duration decimal );""") 

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists (artist_id varchar CONSTRAINT artist_id_pk PRIMARY KEY NOT NULL UNIQUE,
                                                              name varchar,
                                                              location varchar,
                                                              latitude decimal,
                                                              longitude decimal);""") 

time_table_create = ("""CREATE TABLE IF NOT EXISTS time ( start_time timestamp CONSTRAINT start_time_pk PRIMARY KEY NOT NULL UNIQUE,
                                                          hour int,
                                                          day int,
                                                          week int,
                                                          month int,
                                                          year int,
                                                          weekday int);""") 

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays (songplay_id SERIAL CONSTRAINT songplay_id_pk PRIMARY KEY NOT NULL UNIQUE,
                                                                  start_time timestamp REFERENCES time NOT NULL UNIQUE,
                                                                  user_id int REFERENCES users NOT NULL,
                                                                  level varchar, 
                                                                  song_id varchar REFERENCES songs NOT NULL,
                                                                  artist_id varchar REFERENCES artists NOT NULL,
                                                                  session_id int,
                                                                  location varchar,
                                                                  user_agent varchar) ;""") 

# INSERT RECORDS
songplay_table_insert = ("""INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (start_time)
                            DO NOTHING;""")
                             


song_table_insert = ("""INSERT INTO songs (song_id, title, artist_id, year, duration) 
                        VALUES (%s, %s, %s, %s, %s) 
                        ON CONFLICT(song_id) 
                        DO NOTHING; """) 
                                                
                        
user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name, gender, level)
                        VALUES (%s, %s, %s, %s, %s) 
                        ON CONFLICT(user_id)
                        DO 
                          UPDATE SET level = EXCLUDED.level;""")

artist_table_insert = ("""INSERT INTO artists (artist_id, name, location, latitude, longitude)
                          VALUES (%s, %s, %s, %s, %s)
                          ON CONFLICT (artist_id)
                          DO
                            UPDATE SET name=EXCLUDED.name,
                                       location=EXCLUDED.location,   
                                       latitude=EXCLUDED.latitude,
                                       longitude=EXCLUDED.longitude;""") 


time_table_insert = ("""INSERT INTO time ( start_time, hour, day, week, month, year, weekday)
                        VALUES (%s, %s, %s, %s, %s, %s, %s) 
                        ON CONFLICT (start_time) 
                        DO NOTHING;""" ) 

# FIND SONGS
# get songid and artistid 
song_select = ("""SELECT s.song_id, a.artist_id
                  FROM ( songs s 
                         INNER JOIN artists a 
                         ON (s.artist_id = a.artist_id)) 
                         WHERE ( s.song_id IS NOT NULL
                         and a.artist_id IS NOT NULL
                         and s.title = %s
                         and a.name = %s
                         and s.duration = %s) ;""") 


#create all the tables listed
create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
#drop all the tables listed
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]



