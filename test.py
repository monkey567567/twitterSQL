import sqlite3
import time

connection = None
cursor = None

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    if (connection):
        print("Opened database successfully:")
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return


def drop_tables():
    global connection, cursor

    drop_includes = "drop table if exists includes; "
    drop_lists = "drop table if exists lists; "
    drop_retweets = "drop table if exists retweets; "
    drop_mentions = "drop table if exists mentions; "
    drop_hashtags = "drop table if exists hashtags; "
    drop_tweets = "drop table if exists tweets; "
    drop_follows = "drop table if exists follows; "
    drop_users = "drop table if exists users; "

    cursor.execute(drop_includes)
    cursor.execute(drop_lists)
    cursor.execute(drop_retweets)
    cursor.execute(drop_mentions)
    cursor.execute(drop_hashtags)
    cursor.execute(drop_tweets)
    cursor.execute(drop_follows)
    cursor.execute(drop_users)


def define_tables():
    global connection, cursor

    users_query=   '''
                        create table users (
                                usr         int,
                                pwd	      text,
                                name        text,
                                email       text,
                                city        text,
                                timezone    float,
                                primary key (usr)
                            );
                    '''

    follows_query=  '''
                        create table follows (
                                flwer       int,
                                flwee       int,
                                start_date  date,
                                primary key (flwer,flwee),
                                foreign key (flwer) references users,
                                foreign key (flwee) references users
                                );
                    '''

    tweets_query= '''
                        create table tweets (
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
                        create table hashtags (
                                term        text,
                                primary key (term)
                            );
                    '''
    
    mentions_query= '''
                        create table mentions (
                                tid         int,
                                term        text,
                                primary key (tid,term),
                                foreign key (tid) references tweets,
                                foreign key (term) references hashtags
                            );
                    '''
    
    retweets_query = '''
                        create table retweets (
                                usr         int,
                                tid         int,
                                rdate       date,
                                primary key (usr,tid),
                                foreign key (usr) references users,
                                foreign key (tid) references tweets
                            );
                    '''
    
    lists_query= '''
                        create table lists (
                                lname        text,
                                owner        int,
                                primary key (lname),
                                foreign key (owner) references users
                            );
                    '''
    
    includes_query = '''
                        create table includes (
                                lname       text,
                                member      int,
                                primary key (lname,member),
                                foreign key (lname) references lists,
                                foreign key (member) references users
                            );
                    '''


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
                        insert into users values (97, apple, 'Connor McDavid','cm@nhl.com','Edmonton',-7);
                        insert into users values (29,pear, 'Leon Draisaitl','ld@nhl.com','Edmonton',-7);
                        insert into users values (5, banana12, 'Davood Rafiei','dr@ualberta.ca','Edmonton',-7);
                    '''

    insert_follows =  '''
                        insert into follows values (29,97,'2021-01-10');
                        insert into follows values (97,29,'2021-09-01');
                        insert into follows values (5,97,'2022-11-15');
                    '''
    
    insert_tweets =  '''
                        insert into tweets values (4324, 5,'2023-06-01','Looking for a good book to read. Just finished lone #survivor', 97);
                        insert into tweets values (23, 97,'2023-02-12','#Edmonton #Oilers had a good game last night.', NULL);
                        insert into tweets values (3245, 5,'2023-03-01','Go oliers!',97,'2023-02-12', 5);
                    '''
    
    insert_hashtags =  '''
                        insert into hashtags values ('survivor');
                        insert into hashtags values ('oilers');
                        insert into hashtags values ('edmonton');
                    '''
    
    insert_mentions =  '''
                        insert into mentions values (23, 'survivor');
                        insert into mentions values (3245, 'edmonton');
                        insert into mentions values (4324, 'oilers');
                    '''
    insert_retweets =  '''
                        insert into retweets values (97, 23, '2023-02-12');
                    '''
    
    insert_lists =  '''
                        insert into lists values ('oilers players',5);
                        insert into lists values ('pc',5);
                        insert into lists values ('liberal',5);
                        insert into lists values ('ndp',5);
                    '''
    
    insert_includes =  '''
                        insert into includes values ('oilers players',97);
                        insert into includes values ('oilers players',29);
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

    path = "./register.db"
    connect(path)
    drop_tables()
    define_tables()

    prompt = input("Please login or register: ")
    entry = False
    while entry == False:
        if prompt.lower() != "login" and prompt.lower() != "register":
            print("Invalid entry.")
            prompt = input("Please login or register: ")
        elif prompt.lower() == 'q':
            break
        else:
            entry = True
            


    drop_tables()
    
    connection.commit()
    connection.close()
    return


if __name__ == "__main__":
    main()
