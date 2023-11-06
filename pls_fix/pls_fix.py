import sqlite3
from datetime import datetime
import random

connection = None
cursor = None

current_userID = 101

def connect(path):
    global connection, cursor
    
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys = ON; ')
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

    insert_follows = '''
INSERT INTO follows(flwer, flwee, start_date) VALUES
    (29,97,'2021-01-10'),
    (97,29,'2021-09-01'),
    (5,97,'2022-11-15'),
    (108,111,'2021-09-01'),
    (108,101,'2021-09-02'),
    (108,102,'2021-09-03'),
    (97,108,'2021-09-01'),
    (111,108,'2021-09-01');
'''

    insert_tweets = '''
INSERT INTO tweets(tid, writer, tdate, text, replyto) VALUES
    (1,5,'2023-06-01','Looking for a good book to read. Just finished lone #survivor', null),
    (2,97,'2023-02-12','#Edmonton #Oilers had a good game last night.',null),
    (3,5,'2023-03-01','Go oliers!',2),
    (4,108,'2023-04-01','Hello',2),
    (5,108,'2023-06-01','Hello World',2),
    (6,108,'2023-05-01','SQL',2),
    (7,108,'2023-07-01','SQLite!',2);
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

def latest_to_oldest(tweet):
    return tweet[2]

def tweets_stats(results):
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

def show_more(hidden, shown):
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
        
def show_previous(hidden, shown):
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
        show_more(hidden, shown)
    elif (text == 'p'):
        show_previous(hidden, shown)
    elif (text == 'q'): # when quit, return to search_users()
        search_users()
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
        show_more(hidden, shown)
    elif (text == 'p'):
        show_previous(hidden, shown)
    elif (text == 'q'): # when quit, return to search_users()
        search_users()
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
                        SELECT DISTINCT follows.flwer
                        FROM follows
                        WHERE follows.flwee = '%s'
                       ''' %(flwee))
        all_flwers = cursor.fetchall()
        all_flwers = clean_rows(all_flwers)
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

def search_users():
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
            search_users()
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
    if (replyto == None): # not a retweet
        cursor.execute('''
                        INSERT INTO tweets(tid, writer, tdate, text, replyto) VALUES
                            (:tid, :writer, date(), :text, :replyto)
                        ''', {"tid":(total_tid[0][0]) + 1, "writer":current_userID, "text":tweet_text, "replyto":replyto})
        connection.commit()
    else: # retweet
        cursor.execute('''
                        INSERT INTO tweets(tid, writer, tdate, text, replyto) VALUES
                            (%d, %d, date(), '%s', '%s')
                        ''' %((total_tid[0][0]) + 1, current_userID, tweet_text, replyto))
        connection.commit()
        cursor.execute('''
                        INSERT INTO retweets(usr, tid, rdate) VALUES
                            (:usr, :tid, date())
                        ''', {"usr":current_userID, "tid":(total_tid[0][0]) + 1})
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
    
    see_tweets = input("Would you like to see this user's tweets? (y/n): ")
    while see_tweets != 'y' and see_tweets != 'Y' and see_tweets != 'N' and see_tweets != 'n':
        see_tweets = input("would you like to see this user's tweets? (y/n): ")
    if see_tweets == 'y' or see_tweets == 'Y':
        while True:
            while i < max and i < len(tweets):
                print("Tweet ID: %d   Tweet date: %s  Tweet: %s" % (tweets[i][0], tweets[i][1], tweets[i][2]))
                i += 1
            if len(tweets) > max:
                see_more = input("See more (y/n): ")
                while see_more != 'y' and see_more != 'Y' and see_more != 'n' and see_more != 'N':
                    see_more = input('See more (y/n)')
                if see_more == 'y' or see_more == 'Y':
                    max += 3
                else:
                    break
            else:
                break

    connection.commit()
    return

def logout():
    print("Succesfully logged out")
    exit()

def main():
    global connection, cursor

    path = "./test.db"
    connection = sqlite3.connect(path)
    cursor = connection.cursor()

    drop_tables()
    define_tables()
    insert_data()

    
    end = False
    while(end != True):
        text = input("1: Search Tweets\n2: Search Users\n3: Compose a Tweet\n4: List followers\n5: quit\nSelect functionality: ")
        if (text == '1'):
            search_tweets(current_userID)
        if (text == '2'):
            # finds users where keyword searched is mentioned in the users name and city
            search_users() 
        elif (text == '3'):
            # current_user can create a new tweet
            compose_tweet(current_userID, None)
        elif text == '4':
            list_followers(current_userID)
        elif (text == '5'):
            logout()
                    
            
    connection.close()
    return

if __name__ == "__main__":
    main()
