import sqlite3
import re
import os
from getpass import getpass
from datetime import datetime

connection = None
cursor = None

# Open up database for the program.
# ---path will be database 
def connect():

    # create global connection and cursor
    global connection, cursor

    try:
        path = input("Input a database: ")
        if (os.path.exists(path)):
            connection = sqlite3.connect(path)
            if (connection):
                print("Opened database successfully:")
            cursor = connection.cursor()
            cursor.execute(' PRAGMA foreign_keys=ON; ')
            connection.commit()
        else:
            print("not a valid database")
    except():
        connect()
    return

def latest_to_oldest(tweet):
    return tweet[2]

def tweets_stats(results, tid, user_id, hidden, shown):  # please fix this implementation
    validID = False
    while not validID:
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
            print("-"*30)
            # find the name of the user
            cursor.execute('''
                            SELECT users.name
                            FROM users 
                            WHERE users.usr == (SELECT DISTINCT tweets.writer
                                                FROM tweets
                                                WHERE tweets.tid = :tid)
                            ''', {"tid": tid})
            user = cursor.fetchall()
            user = clean_rows(user)
            print("Writer: ", user[0])

            cursor.execute('''
                            SELECT users.usr
                            FROM users
                            WHERE users.usr == (SELECT DISTINCT tweets.writer
                                                FROM tweets
                                                WHERE tweets.tid = :tid)
                            ''', {"tid": tid})
            usr = cursor.fetchall()
            usr = clean_rows(usr)

            current_tweet = result[3]
            print("Tweet: ", result[3])
            # Retrieve statistics about the selected tweet
            cursor.execute("SELECT COUNT(*) FROM retweets WHERE tid = ?", (tid,))
            num_retweets = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM tweets WHERE replyto = ?", (tid,))
            num_replies = cursor.fetchone()[0]

            # Display the statistics
            print(f"Number of retweets: {num_retweets}")
            print(f"Number of replies: {num_replies}")
            print("-"*30)
    
    # allow the user to write a reply
    while True:
        reply_yn =  input("Would you like to write a reply? (y/n): ")
        if reply_yn == 'y' or reply_yn == 'Y':
            compose_tweet(user_id, usr)
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
                cursor.execute("INSERT INTO retweets(usr, tid, rdate) VALUES (?, ?, ?);", (user_id, tid, current_date,))
            except Exception:
                print("You've already retweeted this tweet.")
            break
        elif retweet == 'n' or retweet == 'N':
            break
        else:
            print("Invalid input")
            continue

    connection.commit()
    
    end = False 
    while (end != True):
        print("q: Quit and see searched tweets"+"\n"+("-")*30)
        choice = (input("Input: ")).lower()
        if (choice == 'q'):
            display_current(hidden, shown)
            end = True
        else:
            print("-"*30)
            print("Writer: ", user[0])
            print("Tweet: ", current_tweet)
            print(f"Number of retweets: {num_retweets}")
            print(f"Number of replies: {num_replies}")
            print("-"*30)
            continue
    select_tweet(hidden, shown, user_id)

def search_tweets(user_ID):
    global connection, cursor
    
    keywords = input("Enter one or more keywords separated by spaces (press enter with no text to quit): ")
    text = keywords
    keywords = keywords.split()
    text = text.strip()
    end = text.find(' ', 0, len(text))
    if (end == -1): 
        text = "%" + text + "%"
    else:
        text = "%" + text[0:end] + "%"    
  
    if(text == '%%'): # when quit return to choosing functionalities
        print(("-")*30)
        menu(user_ID)

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
        select_tweet(hidden, shown, user_ID)

def select_tweet(hidden, shown, user_id):
    current_shown = len(shown) % 5 
    current_five = []
    tids = []
    if (current_shown == 0 and hidden != 0):
        for i in range(5):
            current_five.append(shown[i])
            tids.append(str(shown[i][0]))
        tids.reverse()
    else:
        for i in range(current_shown):
            current_five.append(shown[i])
            tids.append(str(shown[i][0]))
        tids.reverse()

    print("\n"+("-")*20+"\n"+"n: Next 5 tweets\np: Previous 5 tweets\nq: Quit"+"\n"+("-")*20)
    text = (input("Enter a tweet ID to see statistics: ")).lower()

    if (text.strip() == 'n'): # next page
        show_more(hidden, shown, user_id, 'tweets')
    elif (text.strip() == 'p'): # previous page
        show_previous(hidden, shown, user_id, 'tweets')
    elif (text.strip() == 'q'): # when quit, return to search_tweets()
        search_tweets(user_id)
    elif (text.strip() in tids and current_shown + 5 == 5): # a user is selected out of 5 choices
        selected_tid = 0
        for i in range(5):
            if text.strip() == tids[i]:
                selected_tid = tids[i]
        tweets_stats(current_five, selected_tid, user_id, hidden, shown)
    elif (text.strip() in tids and current_shown + 5 > 5): # a user is selected out of less than 5 choices
        for i in range(current_shown):
            if text.strip() == tids[i]:
                selected_tid = tids[i]
        tweets_stats(current_five, selected_tid, user_id, hidden, shown)
    else: # catch all invalid inputs
        print("------------------\nnot a valid input\n------------------")
        try:
            int(text)

        except:
            display_current(hidden, shown) 
            select_tweet(hidden, shown, user_id)
        else: 
            display_current(hidden, shown) 
            select_tweet(hidden, shown, user_id)

def list_followers(user):
    global connection, cursor

    cursor.execute("SELECT u.usr, u.name FROM users u INNER JOIN follows f ON u.usr = f.flwer WHERE f.flwee = ?", (user,))
    followers = cursor.fetchall()
    if len(followers) == 0:
        print("You currently have no followers.")
        print(("-")*30)
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
                print(("-")*30)
                return
            elif follow == 'n' or follow == 'N':
                print(("-")*30)
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
    
    end = False
    while (end != True):
        see_tweets = input("Would you like to see this user's tweets? (y/n): ")
        if see_tweets == 'y' or see_tweets == 'Y':
            while True:
                for i in range(max):
                    if i < len(tweets):
                        print("Tweet ID: %d   Tweet date: %s  Tweet: %s" % (tweets[i][0], tweets[i][1], tweets[i][2]))
                    else:
                        break

                if (len(tweets) > max):
                    see_more = input("See more (y/n): ")
                    if see_more == 'y' or see_more == 'Y':
                        max += 3
                    else:
                        break
                else:
                    print("-----End of user Tweets-----")
                    end = True
                    break
        elif see_tweets == 'n' or see_tweets == 'N':
            break
        else:
            continue

    connection.commit()
    print(("-")*30)
    return

def show_more(hidden, shown, user_id, search_type):
    current = len(shown) % 5
    count = 0
    if (current == 0 and len(hidden) == 0):
        display_current(hidden,shown)
        print("no next page")
        if (search_type == 'users'):
            select_user(hidden, shown, user_id)
        else:
            select_tweet(hidden, shown, user_id)
    else:
        if (len(hidden) == 0): # there are no more pages to access
            for i in range(current):
                print(i + 1, shown[current-(i+1)])
            print("no next page")
            if (search_type == 'users'):
                select_user(hidden, shown, user_id)
            else:
                select_tweet(hidden, shown, user_id)
        # shows the next page of users
        # if next page < 5 users shows # of users on that page
        while (count != 5):
            if (len(hidden) == 0):
                print("no more users")
                if (search_type == 'users'):
                    select_user(hidden, shown, user_id)
                else:
                    select_tweet(hidden, shown, user_id)
            else:
                # removes users from the hidden list, printing and placing them in shown
                print(count +1, hidden[0])
                shown.insert(0,hidden.pop(0))
                count = count +1
        if (search_type == 'users'):
            select_user(hidden, shown, user_id)
        else:
            select_tweet(hidden, shown, user_id)

def hide(hidden, shown, amount):
    # places the users shown back into hidden in order [1,2,3,4,5]
    if (amount == 0): # when 5 users were displayed
        for i in range(5):
            hidden.insert(0,shown.pop(0)) 
    else: # when < 5 users were displayed
        for i in range(amount):
            hidden.insert(0,shown.pop(0))
        
def show_previous(hidden, shown, user_id, search_type):
    # current is the amount of users currently displayed
    amount_displayed = len(shown) % 5
    count = 1
    try:
        if (len(shown) == 5):
            while (count <= 5):
                print(count, shown[5-count])
                count = count +1
            print("no prev. page")
            if (search_type == 'users'):
                select_user(hidden, shown, user_id)
            else:
                select_tweet(hidden, shown, user_id)
        else:
            # moves the users that were currently shown back into hidden
            # first set of [5,4,3,2,1] is the previous page
            hide(hidden, shown, amount_displayed)
            # prints the previous page of 5 users
            # shown populated [5,4,3,2,1,5,4,3,2,1] print starts at index 4 and decrements to 0 (5-count)
            while (count <= 5):
                print(count, shown[5-count])
                count = count +1
            if (search_type == 'users'):
                select_user(hidden, shown, user_id)
            else:
                select_tweet(hidden, shown, user_id)
    except:
        display_current(hidden, shown)
        print("no prev. page")
        if (search_type == 'users'):
            select_user(hidden, shown, user_id)
        else:
            select_tweet(hidden, shown, user_id)

def select_user(hidden, shown, user_id):
    print("\n"+("-")*20+"\n"+"n: Next 5 users\np: Previous 5 users\nq: Quit"+"\n"+("-")*20)
    text = (input("Input list number to view user: ")).lower()
    current_shown = len(shown) % 5 
    if (text.strip() == 'n'): # next page
        show_more(hidden, shown, user_id, 'users')
    elif (text.strip() == 'p'): # previous page
        show_previous(hidden, shown, user_id, 'users')
    elif (text.strip() == 'q'): # when quit, return to search_users()
        search_users(user_id)
    elif (text.strip() in ['1','2','3','4','5'] and current_shown + 5 == 5): # a user is selected out of 5 choices
        follow_page(hidden, shown, shown[5-int(text)], user_id)
    elif (text.strip() in ['1','2','3','4','5'] and current_shown + 5 > 5): # a user is selected out of less than 5 choices
        if (int(text) <= current_shown):
            if (len(shown) % 5 < 3): # less than 3 users shown
                follow_page(hidden, shown, shown[(len(shown) % 5) - int(text)], user_id)
            else: # more than 3 users are shown
                follow_page(hidden, shown, shown[5-int(text)], user_id)
            print("------------------\nnot a valid input\n------------------")
            display_current(hidden, shown)
            select_user(hidden, shown, user_id)
    else: # catch all invalid inputs
        print("------------------\nnot a valid input\n------------------")
        try:
            int(text)
        except:
            display_current(hidden, shown) 
            select_user(hidden, shown, user_id)
        else: 
            display_current(hidden, shown) 
            select_user(hidden, shown, user_id)

def display_data(user):
    print("--------------------------------------------------------")
    print("User: ", user)
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
    print("Follows: ",nbr_flwee[0][0],"users")

    # number of people the user is following
    cursor.execute('''
                    SELECT COUNT(DISTINCT follows.flwer)
                    FROM follows
                    WHERE follows.flwee = (SELECT users.usr
                                            FROM users
                                            WHERE users.name = '%s')
                   ''' %(user))
    nbr_followers = cursor.fetchall()
    print("Followers: ",nbr_followers[0][0],"users")

def follow_page(hidden, shown, user, user_id):

    display_data(user)

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
    
    end = False
    more = 0
    while(end != True):
        print("Tweets: ")
        if (len(user_tweets) < 3): # user has less that 3 tweets
            if (len(user_tweets) == 0):
                print("User has no tweets")
                print("--------------------------------------------------------")
            else:
                for i in range(len(user_tweets)):
                    print(user_tweets[i][0])
                print("--------------------------------------------------------")
        else: # user has more than 3 tweets
            if (len(user_tweets) % 3) == 0: # user has tweets that are divisible by 3
                for i in range(3+(3*more)):
                    print(user_tweets[i][0])
                if (3 + 3*more == len(user_tweets)): # the last set of tweets have been printed
                    print("-----End of user Tweets-----")
                    break
                print("--------------------------------------------------------")
            else:
                for i in range(3+more): # user has tweets that are not divisible by 3
                  print(user_tweets[i][0])
                if (3 + more == len(user_tweets)):
                    print("-----End of user Tweets-----")
                print("--------------------------------------------------------")  
        
        print(("-")*30+"\n"+"0: Follow user\nm: View more tweets from user\nq: Quit and see searched users"+"\n"+("-")*30)
        choice = (input("Input: ")).lower()
        
        if (choice == 'm'):
            if (3+more < len(user_tweets)): # user can view more tweets
                if (len(user_tweets) % 3) == 0: # amount of tweets is divisible by 3
                    more = more + 1
                    display_data(user)
                else: # amount of tweets not divisible by 3
                    more = more + (len(user_tweets) % 3) 
                    display_data(user)
            else: # user can not view more tweets
                display_data(user)
        elif (choice == 'q'): # when quit, return to select_user()
            display_current(hidden, shown)
            select_user(hidden, shown, user_id)
            end = True
        elif (choice == '0'): # current_user has chosen to follow selected user
            # finds the user.usr of the selected user
            cursor.execute('''
                            SELECT users.usr
                            FROM users
                            WHERE users.name = '%s'  
                            ''' %(user))
            flweeID = cursor.fetchall()
            # finds all the people following the selected user
            cursor.execute('''
                            SELECT follows.flwer
                            FROM follows
                            WHERE follows.flwee = '%d'
                        ''' %(flweeID[0][0]))
            all_flwers = cursor.fetchall()
            all_flwers = clean_rows(all_flwers)
            if (flweeID[0][0] == user_id): # user can not follow themselves
                print("User can not follow themselves")
            elif (user_id in all_flwers): # user can not follow a user they're already following 
                print("----------\nAlready following user\n----------")
                display_data(user)
            else:
                # inserts the follower and followee and the start_date as a new row in the follows table
                cursor.execute('''
                                INSERT INTO follows(flwer, flwee, start_date) VALUES
                                    ('%d', '%d', julianday('now'))
                                ''' %(int(user_id), int(flweeID[0][0])))
                connection.commit()
                display_data(user) 
        else:
            print("------------------\nnot a valid input\n------------------")
            try:
                int(choice)
            except:
                display_data(user) 
            else: 
                display_data(user) 
    
    end = False
    already_displayed = 1
    while (end != True):

        if (already_displayed == 0):
            display_data(user)
            for i in range(3+(3*more)):
                print(user_tweets[i][0])
            print("-----End of user Tweets-----")
            print("--------------------------------------------------------")
        already_displayed == 0

        print(("-")*30+"\n"+"0: Follow user\nm: View more tweets from user\nq: Quit and see searched users"+"\n"+("-")*30)
        choice = (input("Input: ")).lower()
        if (choice == 'm'):
                display_data(user)
                for i in range(3+(3*more)):
                    print(user_tweets[i][0])
                print("-----End of user Tweets-----")
        elif (choice == 'q'): # when quit, return to select_user()
            display_current(hidden, shown)
            select_user(hidden, shown, user_id)
            end = True
        elif (choice == '0'): # current_user has chosen to follow selected user
            # finds the user.usr of the selected user
            cursor.execute('''
                            SELECT users.usr
                            FROM users
                            WHERE users.name = '%s'  
                            ''' %(user))
            flweeID = cursor.fetchall()
            # finds all the people following the selected user
            cursor.execute('''
                            SELECT follows.flwer
                            FROM follows
                            WHERE follows.flwee = '%d'
                        ''' %(flweeID[0][0]))
            all_flwers = cursor.fetchall()
            all_flwers = clean_rows(all_flwers)
            if (flweeID[0][0] == user_id): # user can not follow themselves
                print("User can not follow themselves")
            elif (user_id in all_flwers): # user can not follow a user they're already following 
                print("----------\nAlready following user\n----------")
                already_displayed = 0
            else:
                # inserts the follower and followee and the start_date as a new row in the follows table
                cursor.execute('''
                                INSERT INTO follows(flwer, flwee, start_date) VALUES
                                    ('%d', '%d', julianday('now'))
                                ''' %(int(user_id), int(flweeID[0][0])))
                connection.commit()
                already_displayed = 0 
        else:
            print("------------------\nnot a valid input\n------------------")
            try:
                int(choice)
            except:
                display_data(user) 
            else: 
                display_data(user)

def display_current(hidden, shown):
    # when test == 0 no user data can be displayed (important for follow_user count never == int(text))
    # displays remaining amount of users after displaying selected user data
    amount_displayed = len(shown) % 5
    if (amount_displayed == 0 and len(shown) != 0): # there are 5 users displayed
        for count in range(1,6):
            print(count, shown[5-count])
    elif (amount_displayed == 0 and len(hidden) != 0): # there were less than 5 users queried
        amount_displayed = len(hidden) % 5
        for count in range(1,amount_displayed+1):
            print(count, hidden[(amount_displayed-1)-count])
            shown.insert(0,hidden.pop(0))
    else: # there are less than 5 users displayed
        for count in range(1,amount_displayed+1):
            print(count, shown[amount_displayed-count])

def search_users(user_id):
    text = input("Search Users (press enter with no text to quit): ")
    text = text.strip()
    end = text.find(' ', 0, len(text))
    if (end == -1): 
        text = "%" + text + "%"
    else:
        text = "%" + text[0:end] + "%"    
  
    if(text == '%%'): # when quit return to choosing functionalities
        print(("-")*30)
        menu(user_id)
    else:
        try:
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
        except:
            search_users(user_id)
        else:
            # all rows are "hidden" since no users are being displayed (populated [1,2,3,4,5])
            hidden = rows1 + rows2
            hidden = clean_rows(hidden)
            # users being displayed (populated [5,4,3,2,1,5,4,3,2,1])
            shown = []

            if (len(hidden) == 0): # no result for search
                search_users(user_id)
            else:
                # shows only 5 users and prompts the user to see more users or search again
                count = 0
                while (count != 5 and len(hidden) != 0):
                    # removes users from the hidden list, printing and placing them in shown
                    print(count +1, hidden[0])
                    count = count +1
                    shown.insert(0,hidden.pop(0))
                select_user(hidden, shown, user_id)

def compose_tweet(user_id, replyto):
    tweet_text = input("Tweet text (press enter with no text to quit): ")

    if (tweet_text.strip() == ' '): # quits the function
        menu(user_id)
    else:
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
                        ''', {"tid":(total_tid[0][0]) + 1, "writer":user_id, "text":tweet_text, "replyto":replyto})
        connection.commit()

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
    print(("-")*30)

def clean_rows(rows):
    # removes the data from the queried row into a list where each indiviual elemnt is a string 
    all_elements = []
    for i in range(len(rows)):
        all_elements.append(rows[i][0])
    return(all_elements)

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

def menu(user_id):

    while True:
        print("Main Menu:")
        print("1. View and interact with tweets from users you follow")
        print("2. Search Tweets")
        print("3. Search Users")
        print("4. Compose a tweet")
        print("5. List followers")
        print("6. Logout")
        print(("-")*30)
    
        choice = input("What would you like to do? ")

        if choice == "1":
            show_tweets(user_id)
        elif choice == "2":
            search_tweets(user_id)
        elif choice == "3":
            search_users(user_id)
        elif choice == "4":
            compose_tweet(user_id, None)
        elif choice == "5":
            list_followers(user_id)
        elif choice == "6":
            print("Logging out. See you next time.")
            login_page()
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
        ''', (user_id,))
        tweets = cursor.fetchall()

        # If no tweets exist from users being followed exit show_tweets
        if not tweets:
            print(("-")*30)
            print("No tweets from users you follow.")

        # List latest tweets from users being followed
        stop = False
        more = 0

        while (stop != True):
            print(("-")*30)
            print("Latest tweets from users you follow:")
            if (len(tweets) < 5): # user has less than 5 tweets
                if (len(tweets) == 0):
                    print("No tweets found")
                else: # no tweets are found
                    for index in range(len(tweets)):
                        print((index+1),".",tweets[index][0],tweets[index][3]," tweeted on ",tweets[index][2],tweets[index][1])
            else: # user has more than 5 tweets
                if (len(tweets) %5) == 0: # user has tweets that are divisible by 5
                    for i in range (5+(5*more)):
                        print((index+1),".",tweets[index][0],tweets[index][3]," tweeted on ",tweets[index][2],tweets[index][1])
                    if (5 + 5*more == len(tweets)): # the last set of tweets have been printed
                        print("-----End of user Tweets-----")
                        break
                    print("--------------------------------------------------------")
                else:
                    for index in range(5 + more): #user has tweets that are not divisible by 5
                        print((index+1),".",tweets[index][0],tweets[index][3]," tweeted on ",tweets[index][2],tweets[index][1])
                    if (5 + more == len(tweets)):
                        print("-----End of user Tweets-----")
                print("--------------------------------------------------------")  
                
            # Interact with tweets
            tweet_choice = input("Enter the list number of the tweet you want to interact with (or 'm' to see more, or '0' to see menu): ")

            if tweet_choice.lower() == '0':
                print(("-")*30)
                menu(user_id)
                break
            elif tweet_choice.lower() == 'm':
                if (5+more < len(tweets)): # user can view more tweets
                    if (len(tweets) % 5) == 0: # amount of tweets is divisible by 5
                        more = more + 1
                    else: # amount of tweets not divisible by 5
                        more = more + (len(tweets) % 5) 
                else: # user can not view more tweets
                    print("no more tweets")
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

                    print(("-")*30+"\n")
                    print(f"Tweet by {selected_tweet[3]} on {selected_tweet[2]}:\n{selected_tweet[1]}")
                    print(f"Retweets: {retweet_count} | Replies: {reply_count}")
                    print("\n"+("-")*30)

                    # Allow the user to compose a reply or retweet
                    print(("-")*30+"\n"+"1: reply\n2: retweet\n3: to return"+"\n"+("-")*30)
                    interaction_choice = input("Input: ")

                    if interaction_choice.lower() == '1': # reply
                        reply_text = input("Enter your reply: ")
                        # Insert the reply into the database with appropriate details
                        cursor.execute('''
                            INSERT INTO tweets (writer, tdate, text, replyto)
                            VALUES (?, DATE('now'), ?, ?)
                        ''', (user_id, reply_text, tweet_id))
                        connection.commit()
                        print("Reply posted successfully!")

                    elif interaction_choice.lower() == '2': # retweet
                        # Insert the retweet into the database
                        cursor.execute('''
                            INSERT OR IGNORE INTO retweets (usr, tid, rdate)
                            VALUES (?, ?, DATE('now'))
                        ''', (user_id, tweet_id))
                        connection.commit()
                        print("Retweet posted successfully!")
                    
                    elif interaction_choice.lower() == '3':
                        break

                    else:
                        end = False
                        while(end != True):
                            print(("-")*30+"\n"+"Invalid Input"+"\n"+("-")*30)

                            print(("-")*30+"\n")
                            print(f"Tweet by {selected_tweet[3]} on {selected_tweet[2]}:\n{selected_tweet[1]}")
                            print(f"Retweets: {retweet_count} | Replies: {reply_count}")
                            print("\n"+("-")*30)   

                            print(("-")*30+"\n"+"1: reply\n2: retweet\n3: to return"+"\n"+("-")*30)
                            interaction_choice = input("Input: ")

                            if interaction_choice.lower() == '1': # reply
                                reply_text = input("Enter your reply: ")
                                # Insert the reply into the database with appropriate details
                                cursor.execute('''
                                    INSERT INTO tweets (writer, tdate, text, replyto)
                                    VALUES (?, DATE('now'), ?, ?)
                                ''', (user_id, reply_text, tweet_id))
                                connection.commit()
                                print("Reply posted successfully!")

                            elif interaction_choice.lower() == '2': # retweet
                                # Insert the retweet into the database
                                cursor.execute('''
                                    INSERT OR IGNORE INTO retweets (usr, tid, rdate)
                                    VALUES (?, ?, DATE('now'))
                                ''', (user_id, tweet_id))
                                connection.commit()
                                print("Retweet posted successfully!")
                            
                            elif interaction_choice.lower() == '3':
                                end = True
                else:
                    print("Invalid tweet number.")
            else:
                print("Invalid input. Please enter 'more', 'exit', or a valid tweet number.")
    
def login_user():
    usr = input("Enter your user ID: ")
    pwd = getpass("Enter your password: ")
    
    valid = True

    cursor.execute('SELECT usr, name FROM users WHERE usr = ? AND pwd = ?', (usr, pwd))
    user = cursor.fetchone()

    if user:
        print(("-")*30)
        print(f"Welcome, {user[1]}!")
        return user[0]

    else:
        print("Invalid username or password.")
        return None

#Validate and input user name
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
    pass_prompt = getpass("Please create your password: ")

    cursor.execute('SELECT COUNT(usr) FROM users')
    user_count = cursor.fetchone()[0]
    next_user_id = user_count + 1
    unique_usr = next_user_id

    cursor.execute('INSERT OR IGNORE INTO users (usr, pwd, name, email, city, timezone) VALUES (?, ?, ?, ?, ?, ?)',
                   (unique_usr, str(pass_prompt), str(name_prompt), str(email_prompt), str(city_prompt), float(time_zone_prompt)))
    
    connection.commit()
    print("Registration successful.")
    return unique_usr

def login_page():
    entry = False

    while True:
        print(("-")*30+"\n"+"1: login\n2: register\n3: Quit"+"\n"+("-")*30)
        login_prompt = input("Input: ")

        if login_prompt.lower() == "1": # login
            print(("-")*30+"\n"+"Login"+"\n"+("-")*30)
            user_id = login_user()
            if user_id is not None:
                show_tweets(user_id)
                entry = True

        if login_prompt.lower() == "2": # register
            print(("-")*30+"\n"+"Register"+"\n"+("-")*30)
            new_user = register_user()

            cursor.execute("SELECT * FROM users")
            uid = cursor.fetchall()

            menu(new_user)
            
        elif login_prompt.lower() == '3': # Quit
            connection.close()  
            quit()
        elif entry:
            pass

        else:
            print("Invalid input. Please try again.")
