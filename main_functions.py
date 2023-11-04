import sqlite3

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
    current = len(shown) % 5
    count = 1
    if (len(shown) - 5 == 0):
        while (count <= 5):
            print(count, shown[5-count][0])
            count = count +1
        print("no prev. page")
        select_user(hidden, shown)
    else:
        # moves the users that were currently shown back into hidden
        # first set of [5,4,3,2,1] is the previous page
        hide(hidden, shown, current)
        # prints the previous page of 5 users
        # shown populated [5,4,3,2,1,5,4,3,2,1] print starts at index 4 and decrements to 0 (5-count)
        while (count <= 5):
            print(count, shown[5-count][0])
            count = count +1
    select_user(hidden, shown)

def select_user(hidden, shown):
    text = (input("Select user to view (enter n to show next p to show previous): ")).lower()
    if (text == 'n'):
        show_more(hidden, shown)
    elif (text == 'p'):
        show_previous(hidden, shown)
        return
    else:
        select_user(hidden, shown)

def search_users(cursor):
    end = False
    while not end:
        text = "%"+(input("Search Users: "))+"%"
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