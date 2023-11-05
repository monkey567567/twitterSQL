import sqlite3


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

    drop_includes = "DROP TABLE IF EXISTS includes; "
    drop_lists = "DROP TABLE IF EXISTS lists; "
    drop_retweets = "DROP TABLE IF EXISTS retweets; "
    drop_mentions = "DROP TABLE IF EXISTS mentions; "
    drop_hashtags = "DROP TABLE IF EXISTS hashtags; "
    drop_tweets = "DROP TABLE IF EXISTS tweets; "
    drop_follows = "DROP TABLE IF EXISTS follows; "
    drop_users = "DROP TABLE IF EXISTS users; "

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
                        CREATE TABLE users (
                                usr         INTEGER,
                                pwd	        TEXT,
                                name        TEXT,
                                email       TEXT,
                                city        TEXT,
                                timezone    FLOAT,
                                PRIMARY KEY (usr)
                            );
                    '''

    follows_query=  '''
                        CREATE TABLE follows (
                                flwer       INTEGER,
                                flwee       INTEGER,
                                start_date  DATE,
                                PRIMARY KEY (flwer,flwee),
                                FOREIGN KEY (flwer) REFERENCES users,
                                FOREIGN KEY (flwee) REFERENCES users
                                );
                    '''

    tweets_query= '''
                        CREATE TABLE tweets (
                                tid	        INTEGER,
                                writer      INTEGER,
                                tdate       DATE,
                                text        TEXT,
                                replyto     INTEGER,
                                PRIMARY KEY (tid),
                                FOREIGN KEY (writer) REFERENCES users,
                                FOREIGN KEY (replyto) REFERENCES tweets
                            );
                    '''
    
    hashtags_query = '''
                        CREATE TABLE hashtags (
                                term        TEXT,
                                PRIMARY KEY (term)
                            );
                    '''
    
    mentions_query= '''
                        CREATE TABLE mentions (
                                tid         INTEGER,
                                term        TEXT,
                                PRIMARY KEY (tid,term),
                                FOREIGN KEY (tid) REFERENCES tweets,
                                FOREIGN KEY (term) REFERENCES hashtags
                            );
                    '''
    
    retweets_query = '''
                        CREATE TABLE retweets (
                                usr         INTEGER,
                                tid         INTEGER,
                                rdate       DATE,
                                PRIMARY KEY (usr,tid),
                                FOREIGN KEY (usr) REFERENCES users,
                                FOREIGN KEY (tid) REFERENCES tweets
                            );
                    '''
    
    lists_query= '''
                        CREATE TABLE lists (
                                lname        TEXT,
                                owner        INTEGER,
                                PRIMARY KEY (lname),
                                FOREIGN KEY (owner) REFERENCES users
                            );
                    '''
    
    includes_query = '''
                        CREATE TABLE includes (
                                lname       TEXT,
                                member      INTEGER,
                                PRIMARY KEY (lname,member),
                                FOREIGN KEY (lname) REFERENCES lists,
                                FOREIGN KEY (member) REFERENCES users
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
                        INSERT INTO users VALUES 
                        (97, 'apple', 'Connor McDavid','cm@nhl.com','Edmonton',-7),
                        (29, 'pear', 'Leon Draisaitl','ld@nhl.com','Edmonton',-7),
                        (5, 'banana12', 'Davood Rafiei','dr@ualberta.ca','Edmonton',-7);
                    '''

    insert_follows =  '''
                        INSERT INTO follows VALUES 
                        (29, 97,'2021-01-10'),
                        (97, 29,'2021-09-01'),
                        (5, 97,'2022-11-15');
                    '''
    
    insert_tweets =  '''
                        INSERT INTO tweets VALUES 
                        (1, 5,'2023-06-01','Looking for a good book to read. Just finished lone #survivor', null),
                        (2, 97,'2023-02-12','#Edmonton #Oilers had a good game last night.', null),
                        (3, 5,'2023-03-01','Go oliers!', 2);
                    '''
    
    insert_hashtags =  '''
                        INSERT INTO hashtags VALUES 
                        ('survivor'),
                        ('oilers'),
                        ('edmonton');
                    '''
    
    insert_mentions =  '''
                        INSERT INTO mentions VALUES 
                        (1, 'survivor'),
                        (2, 'edmonton'),
                        (3, 'oilers');
                    '''
    insert_retweets =  '''
                        INSERT INTO retweets VALUES 
                        (29, 2, '2023-02-12');
                    '''
    
    insert_lists =  '''
                        INSERT INTO lists VALUES 
                        ('oilers players',5),
                        ('pc',5),
                        ('liberal',5),
                        ('ndp',5);
                    '''
    
    insert_includes =  '''
                        INSERT INTO includes VALUES 
                        ('oilers players', 97),
                        ('oilers players', 29);
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

def menu():

    user_action = input("")


    return

# def show_tweets(user_id):

#     cursor.execute('''
#         SELECT t.tid, t.text, t.tdate, u.writer
#         FROM tweets t
#         JOIN users u ON t.writer = u.usr
#         WHERE t.writer IN (SELECT followed_id FROM users_following WHERE follower_id = ?)
#         ORDER BY t.tdate DESC
#         LIMIT 5
#     ''', (writer,))
#     tweets = cursor.fetchall()

#     for tweet in tweets:
#         print(f"{tweet[3]} tweeted on {tweet[2]}:\n{tweet[1]}\n")
    

def generate_unique_usr():
    cursor.execute('SELECT COUNT(usr) FROM users')
    user_count = cursor.fetchone()[0]
    next_user_id = user_count + 1
    unique_usr = f'user_{next_user_id}'
    return unique_usr

def register_user():
    name_prompt = input("Please enter your name: ")
    email_prompt = input("Please enter your email: ")
    city_prompt = input("Please enter your city: ")
    time_zone_prompt = input("Please enter your timezone: ")
    pass_prompt = input("Please create your password: ")

    cursor.execute('SELECT COUNT(usr) FROM users')
    user_count = cursor.fetchone()[0]
    next_user_id = user_count + 1
    unique_usr = f'user_{next_user_id}'

    cursor.execute('INSERT INTO users (usr, pwd, name, email, city, timezone) VALUES (?, ?, ?, ?, ?, ?)',
                   (unique_usr, str(pass_prompt), str(name_prompt), str(email_prompt), str(city_prompt), float(time_zone_prompt)))
    
    cursor.commit()
    print("Registration successful.")

def main():
    global connection, cursor

    path = "./register.db"
    connect(path)
    drop_tables()
    define_tables()
    insert_data()

    cursor.execute("SELECT * FROM users")
    uid = cursor.fetchall()
    


    print(uid)
    for i in uid:
        print("user:", i[0])
        print(i)


    login_prompt = input("Please login or register: ")
    entry = False
    while entry == False:
        if login_prompt.lower() == "login":
            user_prompt = input("Please enter your user name: ")
            if user_prompt.lower() == 'exit':
                break
            pass_prompt = input("Please enter your password: ")
            if pass_prompt.lower() == 'exit':
                break
            
            

        if login_prompt.lower() == "register":
            register_user()
        
            

        elif login_prompt.lower() == 'exit':
            break

        else:
            print("Invalid entry.")
            login_prompt = input("Please login or register: ")
            


    drop_tables()
    
    connection.commit()
    connection.close()
    return


if __name__ == "__main__":
    main()
