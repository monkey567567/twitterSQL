import sqlite3
import time

connection = None
cursor = None

def connect(path):
    global connection, cursor
    
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')
    connection.commit()
    return

def drop_tables():
    global connection, cursor

    drop_users = "DROP TABLE IF EXISTS users;"
    drop_follows = "DROP TABLE IF EXISTS follows;"
    drop_tweets = "DROP TABLE IF EXISTS tweets;"
    drop_hashtags = "DROP TABLE IF EXISTS hashtags;"
    drop_mentions = "DROP TABLE IF EXISTS mentions;"
    drop_retweets = "DROP TABLE IF EXISTS retweets;"
    drop_lists = "DROP TABLE IF EXISTS lists;"
    drop_includes = "DROP TABLE IF EXISTS includes;"

    cursor.execute(drop_users)
    cursor.execute(drop_follows)
    cursor.execute(drop_tweets)
    cursor.execute(drop_hashtags)
    cursor.execute(drop_mentions)
    cursor.execute(drop_retweets)
    cursor.execute(drop_lists)
    cursor.execute(drop_includes)

def define_tables():
    global connection, cursor

    users_query = '''
    CREATE TABLE users (
  usr         int,
  pwd	      text,
  name        text,
  email       text,
  city        text,
  timezone    float,
  primary key (usr)
);
'''

    follows_query = '''
CREATE TABLE follows (
  flwer       int,
  flwee       int,
  start_date  date,
  primary key (flwer,flwee),
  foreign key (flwer) references users,
  foreign key (flwee) references users
);
'''
    tweets_query = '''
                    CREATE TABLE tweets (
                                tid	      int,
                                writer      int,
                                tdate       date,
                                text        text,
                                replyto     int,
                                primary key (tid),
                                foreign key (writer) references users,
                                foreign key (replyto) references tweets
                    );
'''
    hashtags_query = '''
CREATE TABLE hashtags (
  term        text,
  primary key (term)
);
'''

    mentions_query = '''
                        CREATE TABLE mentions (
                                    tid         int,
                                    term        text,
                                    primary key (tid,term),
                                    foreign key (tid) references tweets,
                                    foreign key (term) references hashtags
                        );
                    '''

    retweets_query = '''
CREATE TABLE retweets (
  usr         int,
  tid         int,
  rdate       date,
  primary key (usr,tid),
  foreign key (usr) references users,
  foreign key (tid) references tweets
);
'''

    lists_query = '''
CREATE TABLE lists (
  lname        text,
  owner        int,
  primary key (lname),
  foreign key (owner) references users
);'''


    includes_query = '''
CREATE TABLE includes (
  lname       text,
  member      int,
  primary key (lname,member),
  foreign key (lname) references lists,
  foreign key (member) references users
);'''

    cursor.execute(users_query)
    cursor.execute(follows_query)
    cursor.execute(tweets_query)
    cursor.execute(hashtags_query)
    cursor.execute(mentions_query)
    cursor.execute(retweets_query)
    cursor.execute(lists_query)
    cursor.execute(includes_query)
    connection.commit()

    return

def insert_data():
    global connection, cursor

    insert_users = '''
INSERT INTO users(usr, pwd, name, email, city, timezone) VALUES
    (97,'1234','Connor McDavid','cm@nhl.com','Edmonton',-7),
    (29,'5678','Leon Draisaitl','ld@nhl.com','Edmonton',-7),
    (5,'0123','Davood Rafiei','dr@ualberta.ca','Edmonton',-7);
'''

    insert_follows = '''
INSERT INTO follows(flwer, flwee, start_date) VALUES
    (29,97,'2021-01-10'),
    (97,29,'2021-09-01'),
    (5,97,'2022-11-15');
'''

    insert_tweets = '''
INSERT INTO tweets(tid, writer, tdate, text, replyto) VALUES
    (1,5,'2023-06-01','Looking for a good book to read. Just finished lone #survivor', null),
    (2,97,'2023-02-12','#Edmonton #Oilers had a good game last night.',null),
    (3,5,'2023-03-01','Go oliers!',2);
'''

    insert_hashtags = '''
INSERT INTO hashtags(term) VALUES
    ('survivor'),
    ('oilers'),
    ('edmonton');
'''
    insert_mentions = '''
INSERT INTO mentions(tid, term) VALUES
    (1, 'survivor'),
    (2, 'edmonton'),
    (3, 'oilers');
'''

    insert_retweets = '''
INSERT INTO retweets(usr, tid, rdate) VALUES
    (29,2,'2023-02-13');
'''

    insert_lists = '''
INSERT INTO lists(lname, owner) VALUES
    ('oilers players',5),
    ('pc',5),
    ('liberal',5),
    ('ndp',5);
'''

    insert_includes = '''
INSERT INTO includes(lname, member) VALUES
    ('oilers players',97),
    ('oilers players',29);
'''

    cursor.execute(insert_users)
    cursor.execute(insert_follows)
    cursor.execute(insert_tweets)
    cursor.execute(insert_hashtags)
    cursor.execute(insert_mentions)
    cursor.execute(insert_retweets)
    cursor.execute(insert_lists)
    cursor.execute(insert_includes)
    connection.commit()

    return


def main():
    global connection, cursor

    path = "./test.db"
    connect(path)
    drop_tables()
    define_tables()
    insert_data()

    return

if __name__ == "__main__":
    main()
