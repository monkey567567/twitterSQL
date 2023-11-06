import sqlite3
import time

connection = None
cursor = None

current_userID = 101

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

    cursor.execute(drop_includes)
    cursor.execute(drop_lists)
    cursor.execute(drop_retweets)
    cursor.execute(drop_mentions)
    cursor.execute(drop_hashtags)
    cursor.execute(drop_tweets)
    cursor.execute(drop_follows)
    cursor.execute(drop_users)
    connection.commit()

    return


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

# Cony Doe, Con Sam, Concord An, ARE TEST CASES
# Connor McDavid (14), Concord An (10), Cony Doe (8), Con Sam (7)
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

def connect(path):
    global connection, cursor
    
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')
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
        text = input("2: Search Users\n3: Compose a Tweet\n5: quit\nSelect functionality: ")
        if (text == '2'):
            # finds users where keyword searched is mentioned in the users name and city
            search_users() 
        elif (text == '3'):
            # current_user can create a new tweet
            compose_tweet(current_userID, None)
        elif (text == '5'):
            end = True
                    
            
    connection.close()
    return

if __name__ == "__main__":
    main()