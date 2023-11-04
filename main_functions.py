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

def show_more(hidden, shown):
    current = len(shown) % 5
    count = 0
    # there are no more pages to access
    if (len(hidden) == 0):
        for i in range(current):
            print(i + 1, shown[current-(i+1)][0])
        print("no next page")
        select_user(hidden, shown)
    # shows the next page of users
    # if next page < 5 users shows # of users on that page
    while (count != 5):
        if (len(hidden) == 0):
            print("no more users")
            select_user(hidden, shown)
        else:
            # removes users from the hidden list, printing and placing them in shown
            print(count +1, hidden[0][0])
            shown.insert(0,hidden.pop(0))
            count = count +1
    select_user(hidden, shown)

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
            print(count, shown[5-count][0])
            count = count +1
        print("no prev. page")
        select_user(hidden, shown)
    else:
        # moves the users that were currently shown back into hidden
        # first set of [5,4,3,2,1] is the previous page
        hide(hidden, shown, amount_displayed)
        # prints the previous page of 5 users
        # shown populated [5,4,3,2,1,5,4,3,2,1] print starts at index 4 and decrements to 0 (5-count)
        while (count <= 5):
            print(count, shown[5-count][0])
            count = count +1
    select_user(hidden, shown)

def select_user(hidden, shown):
    end = False
    while(end != True):
        text = (input("Input list number to view user (enter n to show next, p to show previous, q to quit current search): ")).lower()
        if (text == 'n'):
            show_more(hidden, shown)
        elif (text == 'p'):
            show_previous(hidden, shown)
        elif (text == 'q'): # when quit, return to search_users()
            end = True
        elif (text in ['1','2','3','4','5']): # a user is selected
            display_current(hidden, shown, text)
            follow_user(hidden, shown, shown[5-int(text)][0], current_userID)
        else: # catch all invalid inputs
            for count in range(1,6):
                print(count, shown[5-count][0])   

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
                    ORDER BY julianday('now') - julianday(tweets.tdate) DESC
                   ''' %(user))
    user_tweets = cursor.fetchall()
    print("Tweets: ")
    if (len(user_tweets) != 0):
        for i in range(3):
            print(user_tweets[i][0])
    
    print("--------------------------------------------------------")

def follow_user(hidden, shown, flwee, current_userID):
    text = (input("Enter 0 to follow or view other user (enter n to show next, p to show previous, q to quit current search) : ")).lower()
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

        # inserts the follower and followee and the start_date as a new row in the follows table
        cursor.execute('''
                        INSERT INTO follows(flwer, flwee, start_date) VALUES
                            (%d, %d, julianday('now'))
                        ''' %(int(current_userID), int(flweeID[0][0])))
        connection.commit()
        select_user(hidden, shown)
    elif (text in ['1','2','3','4','5']): # a user is selected
        display_current(hidden, shown, text)
        follow_user(hidden, shown, shown[5-int(text)][0], current_userID)
    else:
        display_current(hidden, shown, text)
        select_user(hidden, shown)

def display_current(hidden, shown, text):
    # displays the current list of users and the selected user data
    amount_displayed = len(shown) % 5
    if (amount_displayed == 0): # there are 5 users displayed
        for count in range(1,6):
            print(count, shown[5-count][0])
            if (count == int(text)):
                print("--------------------------------------------------------")
                print("user: ", shown[5-int(text)][0])
                display_data(shown[5-int(text)][0])
    else: # there are less than 5 users displayed
        for count in range(1,amount_displayed+1):
            print(count, shown[amount_displayed-count][0])
            if (count == int(text)):
                print("--------------------------------------------------------")
                print("user: ", shown[amount_displayed-int(text)][0])
                display_data(shown[amount_displayed-int(text)][0])

def search_users():
    end = False
    while not end:
        text = "%"+(input("Search Users (q to quit): "))+"%"
        if(text == "%"+'q'+"%"): # when quit return to chossing functionalities
            end = True
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
            # users being displayed (populated [5,4,3,2,1,5,4,3,2,1])
            shown = []

            if (len(hidden) == 0):
                search_users()
            else:
                # shows only 5 users and prompts the user to see more users or search again
                count = 0
                while (count != 5 and len(hidden) != 0):
                    # removes users from the hidden list, printing and placing them in shown
                    print(count +1, hidden[0][0])
                    count = count +1
                    shown.insert(0,hidden.pop(0))
            select_user(hidden, shown)