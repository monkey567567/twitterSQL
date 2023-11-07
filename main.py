import sqlite3
import re
import getpass
from datetime import datetime

connection = None
cursor = None

# Open up database for the program.
# ---path will be database 
def connect(path):

    # create global connection and cursor
    global connection, cursor

    # Connect database, check if database is valid
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
                        (97,'1234','Connor McDavid','cm@nhl.com','Edmonton',-7),
                        (98,'1111','Cony Doe','cy@nhl.com','Edmonton',-7),
                        (99,'2222','Con Sam','cs@nhl.com','Edmonton',-7),
                        (100,'3333','Concord An','cc@nhl.com','Edmonton',-7),
                        (101,'4444','Jim Halpert','JH@nhl.com','PHILIDELPHIA',-7),
                        (102,'5555','PAM BEASLEY','PB@nhl.com','PHILLY',-7),
                        (103,'6666','DWIGHT SHRUTE','DS@nhl.com','PAR',-7),

                        (104,'7','Pat','DS@nhl.com','Edmonton',-7),
                        (105,'8','sam','DS@nhl.com','PAR',-7),
                        (106,'9','andrew','DS@nhl.com','PAR',-7),
                        (107,'10','steven','DS@nhl.com','PAR',-7),
                        (108,'11','Philip','DS@nhl.com','PAR',-7),
                        (109,'12','alex','DS@nhl.com','PAR',-7),
                        (110,'13','ben','DS@nhl.com','PARRR',-7),
                        (111,'14','khym','DS@nhl.com','PARR',-7),

                        (29,'5678','Leon Draisaitl','ld@nhl.com','Concord',-7),
                        (5,'0123','Davood Rafiei','dr@ualberta.ca','Calgary',-7);
                    '''

    insert_follows =  '''
                        INSERT INTO follows VALUES
                        (29,97,'2021-01-10'),
                        (97,29,'2021-09-01'),
                        (5,97,'2022-11-15'),
                        (108,111,'2021-09-01'),
                        (108,101,'2021-09-02'),
                        (108,102,'2021-09-03'),
                        (97,108,'2021-09-01'),
                        (111,108,'2021-09-01');

                    '''
    
    insert_tweets =  '''
                        INSERT INTO tweets VALUES
                        (1,5,'2023-06-01','Looking for a good book to read. Just finished lone #survivor', null),
                        (2,97,'2023-02-12','#Edmonton #Oilers had a good game last night.',null),
                        (3,5,'2023-03-01','Go oliers!',2),
                        (4,108,'2023-04-01','Hello',2),
                        (5,108,'2023-06-01','Hello World',2),
                        (6,108,'2023-05-01','SQL',2),
                        (7,108,'2023-07-01','SQLite!',2);
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


def latest_to_oldest(tweet):
    return tweet[2]

def tweets_stats(results):  # please fix this implementation
    validID = False
    while not validID:
        tid = input("Enter a tweet ID to see statistics: ")
        try:
            tid = int(tid)
        except ValueError:
            print('Invalid ID.')
            continue
        for r in results:
            if tid == r[0]:
                validID = True
                break
    for result in results:
        if tid == result[0]:
            # Retrieve statistics about the selected tweet
            cursor.execute("SELECT COUNT(*) FROM retweets WHERE tid = ?", (tid,))
            num_retweets = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM tweets WHERE replyto = ?", (tid,))
            num_replies = cursor.fetchone()[0]

            # Display the statistics
            print(f"Number of retweets: {num_retweets}")
            print(f"Number of replies: {num_replies}")
    return

def search_tweets(user):
    global connection, cursor
    
    keywords = input("Enter one or more keywords separated by spaces: ").split()
    results = []
    for keyword in keywords:
        keyword = keyword.lower()
        if keyword.startswith("#"):
            keyword = keyword[1:]  # Removing the '#' symbol
            cursor.execute("SELECT t.tid, t.writer, t.tdate, t.text FROM tweets t LEFT JOIN mentions m ON t.tid = m.tid LEFT JOIN hashtags h ON m.term = h.term WHERE h.term = ? ORDER BY tdate DESC;", (keyword,))
        else:
            cursor.execute("SELECT tid, writer, tdate, text FROM tweets WHERE text LIKE ? ORDER BY tdate DESC;", (f"%{keyword}%",))
        results.extend(cursor.fetchall())
    results.sort(reverse = True, key = latest_to_oldest)
    clean_rows(results)
    
    hidden = results
    shown = []

    if len(hidden) == 0:
        print('No tweets contain that keyword')
        return
    else:
        count = 0
        while (count != 5 and len(hidden) != 0):
            print(count +1, hidden[0])
            count = count +1
            shown.insert(0, hidden.pop(0))
        select_user(hidden, shown, current_userID)
        
    # allow the user to write a reply
    while True:
        reply_yn =  input("Would you like to write a reply? (y/n): ")
        if reply_yn == 'y' or reply_yn == 'Y':
            compose_tweet(user, tid)
            break
        elif reply_yn == 'n' or reply_yn == 'N':
            break
        else:
            print("Invalid input")
            continue
    
    # allow the user to retweet
    while True:
        retweet = input("Would you like to retweet? (y/n): ")
        if retweet == 'y' or retweet == 'Y':
            current_date = datetime.today().strftime('%Y-%m-%d')
            try:
                cursor.execute("INSERT INTO retweets(usr, tid, rdate) VALUES (?, ?, ?);", (user, tid, current_date,))
            except Exception:
                print("You've already retweeted this tweet.")
            break
        elif retweet == 'n' or retweet == 'N':
            break
        else:
            print("Invalid input")
            continue

    connection.commit()
    return

def list_followers(user):
    global connection, cursor

    cursor.execute("SELECT u.usr, u.name FROM users u INNER JOIN follows f ON u.usr = f.flwer WHERE f.flwee = ?", (user,))
    followers = cursor.fetchall()
    if len(followers) == 0:
        print("You currently have no followers.")
        return
    for follower in followers:
        print("User ID: %d  Name: %s" % (follower[0], follower[1]))
    validID = False
    while not validID:
        select_flwer = input('Enter the ID of a user: ')
        if not select_flwer.isdigit():
            continue
        for f in followers:
            if int(select_flwer) == f[0]:
                validID = True
                break
    select_flwer = int(select_flwer)
    cursor.execute("SELECT COUNT(*) FROM tweets WHERE writer = ?", (select_flwer,))
    num_tweets = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM follows WHERE flwer = ?", (select_flwer,))
    num_followed = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM follows WHERE flwee = ?", (select_flwer,))
    num_following = cursor.fetchone()[0]

    cursor.execute("SELECT tid, tdate, text FROM tweets WHERE writer = ? ORDER BY tdate DESC", (select_flwer,))
    tweets = cursor.fetchall()

    print(f"Number of tweets: {num_tweets}")
    print(f"Number of followed accounts: {num_followed}")
    print(f"Number of followers: {num_following}")
    
    if len(tweets) == 0:
        print('This user has not posted any tweets')
        while True:
            follow = input("Would you like to follow this user? (y/n): ")
            if follow == 'y' or follow == 'Y':
                current_date = datetime.today().strftime('%Y-%m-%d')
                try:
                    cursor.execute("INSERT INTO follows(flwer, flwee, start_date) VALUES (%d, %d, %s);" % (user, select_flwer, current_date))
                except Exception:
                    print('You already follow this user')
                return
            elif follow == 'n' or follow == 'N':
                return
            else:
                continue
    i = 0
    max = 3
    while True:
        follow = input("Would you like to follow this user? (y/n): ")
        if follow == 'y' or follow == 'Y':
            current_date = datetime.today().strftime('%Y-%m-%d')
            try:
                cursor.execute("INSERT INTO follows(flwer, flwee, start_date) VALUES (%d, %d, %s);" % (user, select_flwer, current_date))
            except Exception:
                print('You already follow this user')
            break
        elif follow == 'n' or follow == 'N':
            break
        else:
            continue
    
    while True:
        see_tweets = input("Would you like to see this user's tweets? (y/n): ")
        if see_tweets == 'y' or see_tweets == 'Y':
            while True:
                while i < max and i < len(tweets):
                    print("Tweet ID: %d   Tweet date: %s  Tweet: %s" % (tweets[i][0], tweets[i][1], tweets[i][2]))
                    i += 1
                if len(tweets) > max:
                    see_more = input("See more (y/n): ")
                    if see_more == 'y' or see_more == 'Y':
                        max += 3
                        break
                    else:
                        break
                else:
                    break
        elif see_tweets == 'n' or see_tweets == 'N':
            break
        else:
            continue

    connection.commit()
    return

def show_more(hidden, shown, current_userID):
    current = len(shown) % 5
    count = 0
    # there are no more pages to access
    if (len(hidden) == 0):
        for i in range(current):
            print(i + 1, shown[current-(i+1)])
        print("no next page")
        select_user(hidden, shown, current_userID)
    # shows the next page of users
    # if next page < 5 users shows # of users on that page
    while (count != 5):
        if (len(hidden) == 0):
            print("no more users")
            select_user(hidden, shown, current_userID)
        else:
            # removes users from the hidden list, printing and placing them in shown
            print(count +1, hidden[0])
            shown.insert(0,hidden.pop(0))
            count = count +1
    select_user(hidden, shown, current_userID)

def hide(hidden, shown, amount):
    # places the users shown back into hidden in order [1,2,3,4,5]
    if (amount == 0): # when 5 users were displayed
        for i in range(5):
            hidden.insert(0,shown.pop(0)) 
    else: # when < 5 users were displayed
        for i in range(amount):
            hidden.insert(0,shown.pop(0))
        
def show_previous(hidden, shown, current_userID):
    # current is the amount of users currently displayed
    amount_displayed = len(shown) % 5
    count = 1
    if (len(shown) == 5):
        while (count <= 5):
            print(count, shown[5-count])
            count = count +1
        print("no prev. page")
        select_user(hidden, shown, current_userID)
    else:
        # moves the users that were currently shown back into hidden
        # first set of [5,4,3,2,1] is the previous page
        hide(hidden, shown, amount_displayed)
        # prints the previous page of 5 users
        # shown populated [5,4,3,2,1,5,4,3,2,1] print starts at index 4 and decrements to 0 (5-count)
        while (count <= 5):
            print(count, shown[5-count])
            count = count +1
    select_user(hidden, shown, current_userID)

def select_user(hidden, shown, current_userID):
    text = (input("Input list number to view user (enter n to show next, p to show previous, q to quit current search): ")).lower()
    current_shown = len(shown) % 5 
    if (text == 'n'):
        show_more(hidden, shown, current_userID)
    elif (text == 'p'):
        show_previous(hidden, shown, current_userID)
    elif (text == 'q'): # when quit, return to search_users()
        search_users(current_userID)
    elif (text in ['1','2','3','4','5'] and current_shown + 5 == 5): # a user is selected out of 5 choices
        display_current(hidden, shown, text, True)
        follow_user(hidden, shown, shown[5-int(text)], current_userID)
    elif (text in ['1','2','3','4','5'] and current_shown + 5 > 5): # a user is selected out of less than 5 choices
        display_current(hidden, shown, text, True)
        if (int(text) <= current_shown):
            if (len(shown) % 5 < 3): # less than 3 users shown
                follow_user(hidden, shown, shown[int(text)-1], current_userID)
            else: # more than 3 users are shown
                follow_user(hidden, shown, shown[5-int(text)], current_userID)
        else:
            print("------------------\nnot a valid input\n------------------")
            display_current(hidden, shown, text, True)
            select_user(hidden, shown, current_userID)
    else: # catch all invalid inputs
        print("------------------\nnot a valid input\n------------------")
        try:
            int(text)
        except:
            if (current_shown + 5 == 5):
                display_current(hidden, shown, current_shown, False) 
                select_user(hidden, shown, current_userID) 
            else:
                display_current(hidden, shown, current_shown, False) 
                select_user(hidden, shown, current_userID)
        else: 
            display_current(hidden, shown, text, False) 
            select_user(hidden, shown, current_userID)

def display_data(user):
    # number of tweets
    cursor.execute('''
                    SELECT COUNT(tweets.writer) 
                    FROM tweets 
                    WHERE tweets.writer = (SELECT users.usr
                                            FROM users
                                            WHERE users.name = '%s') 
                    ''' %(user))
    nbr_tweets = cursor.fetchall()
    print("Number of tweets: ",nbr_tweets[0][0])

    # number of people following the user
    cursor.execute('''
                    SELECT COUNT(DISTINCT follows.flwee)
                    FROM follows
                    WHERE follows.flwer = (SELECT users.usr
                                            FROM users
                                            WHERE users.name = '%s')  
                   ''' %(user))
    nbr_flwee = cursor.fetchall()
    print("follows: ",nbr_flwee[0][0],"users")

    # number of people the user is following
    cursor.execute('''
                    SELECT COUNT(DISTINCT follows.flwer)
                    FROM follows
                    WHERE follows.flwee = (SELECT users.usr
                                            FROM users
                                            WHERE users.name = '%s')
                   ''' %(user))
    nbr_followers = cursor.fetchall()
    print("followers: ",nbr_followers[0][0],"users")

    # users tweets from newest to oldest
    cursor.execute('''
                    SELECT tweets.text
                    FROM tweets
                    WHERE tweets.writer = (SELECT users.usr
                                            FROM users
                                            WHERE users.name = '%s')
                    ORDER BY julianday('now') - julianday(tweets.tdate) ASC
                   ''' %(user))
    user_tweets = cursor.fetchall()
    print("Tweets: ")
    if (len(user_tweets) < 3):
        for i in range(len(user_tweets)):
            print(user_tweets[i][0])
    else:
        for i in range(3):
            print(user_tweets[i][0])
    
    print("--------------------------------------------------------")

def follow_user(hidden, shown, flwee, current_userID):
    text = (input("Enter 0 to follow or view other user (enter n to show next, p to show previous, q to quit current search) : ")).lower()
    current_shown = len(shown) % 5
    if (text == 'n'):
        show_more(hidden, shown, current_userID)
    elif (text == 'p'):
        show_previous(hidden, shown, current_userID)
    elif (text == 'q'): # when quit, return to search_users()
        search_users(current_userID)
    elif (text == '0'): # current_user has chosen to follow selected user
        # finds the user.usr of the selected user
        cursor.execute('''
                        SELECT users.usr
                        FROM users
                        WHERE users.name = '%s'  
                        ''' %(flwee))
        flweeID = cursor.fetchall()
        # finds all the people following the selected user
        cursor.execute('''
                        SELECT follows.flwer
                        FROM follows
                        WHERE follows.flwee = '%d'
                       ''' %(flweeID[0][0]))
        all_flwers = cursor.fetchall()
        print("all_flwers: ", all_flwers)
        all_flwers = clean_rows(all_flwers)
        print("all_flwers: ", all_flwers)
        if (flweeID[0][0] == current_userID): # user can not follow themselves
            print("User can not follow themselves")
        elif (current_userID in all_flwers): # user can not follow a user they're already following 
            print("Already following user")
        else:
            # inserts the follower and followee and the start_date as a new row in the follows table
            cursor.execute('''
                            INSERT INTO follows(flwer, flwee, start_date) VALUES
                                ('%d', '%d', julianday('now'))
                            ''' %(int(current_userID), int(flweeID[0][0])))
            connection.commit()
            display_follows()
        display_current(hidden, shown, text, False)
        select_user(hidden, shown, current_userID)
    elif (text in ['1','2','3','4','5'] and current_shown + 5 == 5): # a user is selected out of 5 choices
        display_current(hidden, shown, text, True)
        follow_user(hidden, shown, shown[5-int(text)], current_userID)
    elif (text in ['1','2','3','4','5'] and current_shown + 5 > 5): # a user is selected out of less than 5 choices
        display_current(hidden, shown, text, True)
        if (int(text) <= current_shown):
            if (len(shown) % 5 < 3): # less than 3 users shown
                follow_user(hidden, shown, shown[int(text)-1], current_userID)
            else: # more than 3 users are shown
                follow_user(hidden, shown, shown[5-int(text)], current_userID)
        else:
            select_user(hidden, shown, current_userID)
    else:
        print("------------------\nnot a valid input\n------------------")
        try:
            int(text)
        except:
            if (current_shown + 5 == 5):
                display_current(hidden, shown, current_shown, False) 
                select_user(hidden, shown, current_userID) 
            else:
                display_current(hidden, shown, current_shown, False) 
                select_user(hidden, shown, current_userID)
        else: 
            display_current(hidden, shown, text, False) 
            select_user(hidden, shown, current_userID)

def display_current(hidden, shown, text, display):
    # when test == 0 no user data can be displayed (important for follow_user count never == int(text))
    # displays remaining amount of users after displaying selected user data
    amount_displayed = len(shown) % 5
    if (amount_displayed == 0): # there are 5 users displayed
        for count in range(1,6):
            print(count, shown[5-count])
            if (display == True and count == int(text)):
                print("--------------------------------------------------------")
                print("user: ", shown[5-int(text)])
                display_data(shown[5-int(text)])
    else: # there are less than 5 users displayed
        for count in range(1,amount_displayed+1):
            print(count, shown[amount_displayed-count])
            if (display == True and count == int(text)):
                print("--------------------------------------------------------")
                print("user: ", shown[amount_displayed-int(text)])
                display_data(shown[amount_displayed-int(text)])

def search_users(current_userID):
    # TODO: handle test case for when user inputs two key words 
    text = input("Search Users (' ' to quit): ")
    # only takes in the first key word entry TODO: is this needed?
    end = text.find(' ', 0, len(text))
    if (end == -1): 
        text = "%" + text + "%"
    else:
        text = "%" + text[0:end] + "%"    
  
    if(text == '%%'): # when quit return to choosing functionalities
        return
    else:
        # users name matches keyword
        cursor.execute('''
                        SELECT users.name 
                        FROM users 
                        WHERE users.name LIKE '%s' 
                        ORDER BY length(users.name)
                        ''' %(text))
        rows1 = cursor.fetchall()
                
        # users city but not name match the keyword
        cursor.execute('''
                        SELECT users.name, users.city
                        FROM users 
                        WHERE users.name NOT LIKE '%s' 
                        AND users.city LIKE '%s' 
                        ORDER BY length(users.city)
                        ''' %(text,text))
        rows2 = cursor.fetchall()

        # all rows are "hidden" since no users are being displayed (populated [1,2,3,4,5])
        hidden = rows1 + rows2
        hidden = clean_rows(hidden)
        # users being displayed (populated [5,4,3,2,1,5,4,3,2,1])
        shown = []

        if (len(hidden) == 0): # no result for search
            search_users(current_userID)
        else:
            # shows only 5 users and prompts the user to see more users or search again
            count = 0
            while (count != 5 and len(hidden) != 0):
                # removes users from the hidden list, printing and placing them in shown
                print(count +1, hidden[0])
                count = count +1
                shown.insert(0,hidden.pop(0))
            select_user(hidden, shown, current_userID)

def compose_tweet(current_userID, replyto):
    # TODO: compose tweet needs to work for retweets i.e. replyto != None
    tweet_text = input("Tweet text: ")

    # creates a new tid for the tweet 
    cursor.execute('''
                    SELECT COUNT(tweets.tid)
                    FROM tweets
    ''')
    total_tid = cursor.fetchall()

    # inserts the new tweet into the tweets table
    cursor.execute('''
                    INSERT INTO tweets(tid, writer, tdate, text, replyto) VALUES
                        (:tid, :writer, date(), :text, :replyto)
                    ''', {"tid":(total_tid[0][0]) + 1, "writer":current_userID, "text":tweet_text, "replyto":replyto})
    connection.commit()
    display_tweets()
    display_retweets()

    # determines the hashtags in the tweet_text
    if ('#' in tweet_text):
        tweet_hashtags = find_hashtags(tweet_text)
        # determines if hashtags in tweet_text in table hashtags and updates hashtags and mentions
        cursor.execute('''
                        SELECT DISTINCT hashtags.term
                        FROM hashtags
                    ''')
        rows = cursor.fetchall()
        all_hashtags = clean_rows(rows)
        # updates hashtags and mentions tables
        for index in range(len(tweet_hashtags)):
            if (tweet_hashtags[index] not in all_hashtags): # hashtag in tweet_text not in hashtags table, updates mentions 
                cursor.execute('''
                                INSERT INTO hashtags(term) VALUES
                                    ('%s')
                                ''' %(tweet_hashtags[index]))
                cursor.execute('''
                                INSERT INTO mentions(tid, term) VALUES
                                    ('%d', '%s')
                                ''' %((total_tid[0][0]) + 1, tweet_hashtags[index]))
                connection.commit()
            else: # hashtag already in the hashtags table, updates mentions
                cursor.execute('''
                                INSERT INTO mentions(tid, term) VALUES
                                    ('%d', '%s')
                                ''' %((total_tid[0][0]) + 1, tweet_hashtags[index]))
                connection.commit()
    display_hashtags()

def clean_rows(rows):
    # removes the data from the queried row into a list where each indiviual elemnt is a string 
    all_elements = []
    for i in range(len(rows)):
        all_elements.append(rows[i][0])
    return(all_elements)

def display_mentions(): # TODO: remove, only used for testing
    cursor.execute('''
                    SELECT *
                    FROM MENTIONS
                   ''')
    mentions = cursor.fetchall()
    print(mentions)

def display_tweets(): # TODO: remove, only used for testing
    cursor.execute('''
                    SELECT *
                    FROM tweets
                    ''')
    tweets = cursor.fetchall()
    print(tweets)

def display_retweets(): # TODO: remove, only used for testing
    cursor.execute('''
                    SELECT *
                    FROM retweets
                    ''')
    retweets = cursor.fetchall()
    print(retweets)

def display_follows(): # TODO: remove, only used for testing
    cursor.execute('''
                    SELECT *
                    FROM follows
                    ''')
    follows = cursor.fetchall()
    print(follows)

def display_hashtags(): # TODO: remove, only used for testing
    cursor.execute('''
                    SELECT *
                    FROM hashtags
                    ''')
    hashtags = cursor.fetchall()
    print(hashtags)

def find_hashtags(tweet_text):
    hashtags = []
    # finds the first instance the '#' occurs
    text_start = tweet_text.find('#',0,len(tweet_text))
    hashtag_index = text_start
    # finds the string that follows after '#'
    while (hashtag_index < len(tweet_text)):
        if (tweet_text[hashtag_index] == ' '): # hashtags in the middle of tweet_text 
            text_end = hashtag_index
            hashtags.append(tweet_text[text_start+1:text_end])
            text_start = tweet_text.find('#',text_end,len(tweet_text))
            if (text_start == -1): # the remaining sting has no hashtags
                break
            hashtag_index = text_start
        elif (hashtag_index == len(tweet_text)-1): # hashtag at the end of tweet_text
            text_end = hashtag_index
            hashtags.append(tweet_text[text_start+1:text_end+1])
        hashtag_index += 1 
    return(hashtags)

# define a menu for the user to interact with
# - user_id is the current user's id (usr)
def menu(user_id):

    # loop the menu until the user puts in a valid action or logs out
    while True:
        print("---------------------\nMain Menu:")
        print("1. View and interact with tweets from users you follow")
        print("2. Search Users")
        print("3. Compose a tweet")
        print("4. List followers")
        print("5. Logout")
    
        # User action
        choice = input("What would you like to do? ")
        if choice == "1":
            show_tweets(user_id)
        elif choice == "2":
            search_users(user_id)
        elif choice == "3":
            compose_tweet(user_id, None)
        elif choice == "4":
            list_followers(user_id)
        elif choice == "5":
            print("Logging out. See you next time.")
            break
        else:
            print("Invalid input. Please try again.")

# View the tweets from users being followed by current user. Allow user to see 'more', 'select tweet', 'reply', and 'retweet'
# - user_id is the current user's id (usr) 
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

        # Interact with tweets, 'select' or see 'more'
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

                # Allow the user to compose a 'reply' or 'retweet'
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
    
# Validate the login of the user, return user id on successful login, return None on unsucessful login
def login_user():

    usr = input("Enter your user ID: ")
    pwd = getpass.getpass("Enter your password: ")

    # fetch usr id from database
    cursor.execute('SELECT usr, name FROM users WHERE usr = ? AND pwd = ?', (usr, pwd))
    user = cursor.fetchone()

    # if usr exists return usr id, if user doesn't exist return None 
    if user:
        print(f"Welcome, {user[1]}!")
        return user[0]

    else:
        print("Invalid username or password.")
        return None

# Input new register into database, return the usr of the new user
def register_user():
    
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
        time_zone_prompt = input("Please enter your timezone (e.g., -2.0 or 1.5): ")
        try:
            time_zone = float(time_zone_prompt)
            break
        except ValueError:
            print("Invalid timezone. Please enter a numeric value.")

    # Input user password
    pass_prompt = input("Please create your password: ")

    # Find the number of users in the data base, have the new user id be the number of users + 1
    cursor.execute('SELECT COUNT(usr) FROM users')
    user_count = cursor.fetchone()[0]
    next_user_id = user_count + 1
    unique_usr = next_user_id

    # Insert new user into database
    cursor.execute('INSERT OR IGNORE INTO users (usr, pwd, name, email, city, timezone) VALUES (?, ?, ?, ?, ?, ?)',
                   (unique_usr, str(pass_prompt), str(name_prompt), str(email_prompt), str(city_prompt), float(time_zone_prompt)))
    
    connection.commit()
    print("Registration successful.")
    return unique_usr


def main():
    global connection, cursor

    # find database and connect to it
    path = "./register.db"
    connect(path)
    drop_tables()
    define_tables()
    insert_data()
    
    entry = False

    # loop login and register for user
    # if current user logs out, return them to this menu
    while True:
        login_prompt = input("Please login or register (or 'exit' to quit): ")

        # user login, if login is successful set entry to True and go to main menu
        if login_prompt.lower() == "login":
            user_id = login_user()
            if user_id is not None:
                menu(user_id)
                entry = True

        # register user, if registration is successful go to main menu as the new user
        if login_prompt.lower() == "register":
            new_user = register_user()

            cursor.execute("SELECT * FROM users")
            uid = cursor.fetchall()
            print(uid)

            menu(new_user)
            
        # break loop if exit 
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
