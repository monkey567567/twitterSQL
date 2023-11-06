import sqlite3
import re

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

def menu(user_id):

    while True:
        print("---------------------\nMain Menu:")
        print("1. View and interact with tweets from users you follow")
    
        choice = input("What would you like to do? ")

        if choice == "1":
            show_tweets(user_id)
        elif choice.lower() == "logout":
            print("Logging out. See you next time.")
            break
        else:
            print("Invalid input. Please try again.")

def show_tweets(user_id):

    while True:
        
        # Fetch the latest 5 tweets or retweets from users being followed
        cursor.execute('''
            SELECT t.tid, t.text, t.tdate, u.name
            FROM tweets t
            JOIN users u ON t.writer = u.usr
            WHERE t.writer IN (SELECT flwee FROM follows WHERE flwer = ?)
            ORDER BY t.tdate DESC
            LIMIT 5
        ''', (user_id,))
        tweets = cursor.fetchall()

        # If no tweets exist from users being followed exit show_tweets
        if not tweets:
            print("No tweets from users you follow.")
            break

        # List latest tweets from users being followed
        print("Latest tweets from users you follow:")
        for idx, tweet in enumerate(tweets, start=1):
            print(f"{idx}. {tweet[3]} tweeted on {tweet[2]}:\n{tweet[1]}\n")

        # Interact with tweets
        tweet_choice = input("Enter the id of the tweet you want to interact with (or 'more' to see more, or 'exit'): ")

        if tweet_choice.lower() == 'exit':
            break
        elif tweet_choice.lower() == 'more':
            continue
        elif tweet_choice.isdigit():
            tweet_idx = int(tweet_choice) - 1
            if 0 <= tweet_idx < len(tweets):
                selected_tweet = tweets[tweet_idx]
                tweet_id = selected_tweet[0]

                # Display statistics about the selected tweet
                cursor.execute('''
                    SELECT COUNT(*) FROM retweets WHERE tid = ?
                ''', (tweet_id,))
                retweet_count = cursor.fetchone()[0]

                cursor.execute('''
                    SELECT COUNT(*) FROM tweets WHERE replyto = ?
                ''', (tweet_id,))
                reply_count = cursor.fetchone()[0]

                print(f"Tweet by {selected_tweet[3]} on {selected_tweet[2]}:\n{selected_tweet[1]}")
                print(f"Retweets: {retweet_count} | Replies: {reply_count}")

                # Allow the user to compose a reply or retweet
                interaction_choice = input("Enter 'reply' to compose a reply, 'retweet' to retweet, or 'back' to return: ")

                if interaction_choice.lower() == 'reply':
                    reply_text = input("Enter your reply: ")
                    # Insert the reply into the database with appropriate details
                    cursor.execute('''
                        INSERT INTO tweets (writer, tdate, text, replyto)
                        VALUES (?, DATE('now'), ?, ?)
                    ''', (user_id, reply_text, tweet_id))
                    connection.commit()
                    print("Reply posted successfully!")

                elif interaction_choice.lower() == 'retweet':
                    # Insert the retweet into the database
                    cursor.execute('''
                        INSERT OR IGNORE INTO retweets (usr, tid, rdate)
                        VALUES (?, ?, DATE('now'))
                    ''', (user_id, tweet_id))
                    connection.commit()
                    print("Retweet posted successfully!")

            else:
                print("Invalid tweet number.")
        else:
            print("Invalid input. Please enter 'more', 'exit', or a valid tweet number.")
    
def login_user():
    usr = input("Enter your user ID: ")
    pwd = input("Enter your password: ")
    
    valid = True

    cursor.execute('SELECT usr, name FROM users WHERE usr = ? AND pwd = ?', (usr, pwd))
    user = cursor.fetchone()

    if user:
        print(f"Welcome, {user[1]}!")
        return user[0]

    else:
        print("Invalid username or password.")
        return None

def register_user():

    #Valiedate user name
    
    # Validate and input user name
    while True:
        name_prompt = input("Please enter your name: ")
        if re.match(r"^[A-Za-z\s]+$", name_prompt):
            break
        else:
            print("Invalid name. Please use only letters and spaces.")
    
    # Validate and input user email
    while True:
        email_prompt = input("Please enter your email: ")
        if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email_prompt):
            break
        else:
            print("Invalid email address. Please use a valid email format.")
    
    # Input user city
    city_prompt = input("Please enter your city: ")
    
    # Validate and input user timezone
    while True:
        time_zone_prompt = input("Please enter your timezone (e.g., -7.0 or 3.5): ")
        try:
            time_zone = float(time_zone_prompt)
            break
        except ValueError:
            print("Invalid timezone. Please enter a numeric value.")
    pass_prompt = input("Please create your password: ")

    cursor.execute('SELECT COUNT(usr) FROM users')
    user_count = cursor.fetchone()[0]
    next_user_id = user_count + 1
    unique_usr = next_user_id

    cursor.execute('INSERT OR IGNORE INTO users (usr, pwd, name, email, city, timezone) VALUES (?, ?, ?, ?, ?, ?)',
                   (unique_usr, str(pass_prompt), str(name_prompt), str(email_prompt), str(city_prompt), float(time_zone_prompt)))
    
    connection.commit()
    print("Registration successful.")
    return unique_usr




def main():
    global connection, cursor

    path = "./register.db"
    connect(path)
    drop_tables()
    define_tables()
    insert_data()

    # cursor.execute("SELECT * FROM users")
    # uid = cursor.fetchall()
    
    # print(uid)
    # for i in uid:
    #     print("user:", i[0])
    #     print(i)


    
    entry = False

    while True:
        login_prompt = input("Please login or register (or 'exit' to quit): ")

        if login_prompt.lower() == "login":
            user_id = login_user()
            if user_id is not None:
                menu(user_id)
                entry = True

        if login_prompt.lower() == "register":
            new_user = register_user()

            cursor.execute("SELECT * FROM users")
            uid = cursor.fetchall()
            print(uid)

            menu(new_user)
            

        elif login_prompt.lower() == 'exit':
            break
        elif entry:
            pass

        else:
            print("Invalid input. Please try again.")

    drop_tables()
    
    connection.commit()
    connection.close()
    return


if __name__ == "__main__":
    main()
