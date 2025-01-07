# Twitter Replica Using Python and SQL

## General Overview
This project replicates a mini social media platform where users can follow others and interact with tweets. Users can log in or register to access a main menu, which provides functionalities such as viewing tweets, searching for tweets or users, composing tweets, and managing followers.

### Key Features:
1. **Login and Registration**: Secure user authentication and account creation.
2. **View and Interact with Tweets**: Display tweets from followed users and allow interactions.
3. **Search for Tweets and Users**: Search functionality with advanced filtering and navigation.
4. **Compose Tweets**: Users can create tweets with hashtags.
5. **List Followers**: View followers and interact with their profiles.
6. **Logout**: Securely log out of the system.

---

## User Guide

### Functionalities:
1. **View and Interact with Tweets**:  
   - Access the latest tweets from users you follow.  
   - Options: Reply, Retweet, or Show More Tweets.

2. **Search for Tweets**:  
   - Enter keywords to find matching tweets.  
   - Navigate through results, reply to, or retweet tweets.

3. **Search for Users**:  
   - Search by name or city.  
   - View user details and follow/unfollow them.

4. **Compose a Tweet**:  
   - Create a tweet, optionally including hashtags.  
   - Hashtags are automatically linked to relevant mentions.

5. **List Followers**:  
   - View and interact with your followers.  
   - Follow/unfollow users or view their tweets.

6. **Logout**:  
   - Securely exit the system.

---

## Design

### Workflow:
1. **Login/Registration**:
   - New users can register by providing their name, email, city, timezone, and password.
   - Existing users can log in with their user ID and password.

2. **Tweet Interaction**:
   - Displays the latest tweets with options to interact or navigate.

3. **Menu Options**:
   - Provides access to the six core functionalities listed above.

### Main Functions:
- `def login_page()`: Handles login/registration menu.
- `def show_tweets(user_id)`: Displays tweets for interaction.
- `def menu(user_id)`: Main functionalities menu.
- `def search_tweets(user_id)`: Searches for tweets by keyword.
- `def search_users(user_id)`: Searches for users by name or city.
- `def compose_tweet(user_id, replyto)`: Allows composing tweets with hashtags.
- `def list_followers(user)`: Lists and manages followers.

---

## Testing Strategy

### Common Bugs:
1. **Input Validation**:
   - Tested various character types to ensure proper input handling.

2. **Pre-existing Data**:
   - Used SQL `OR IGNORE` to prevent duplicate entries.

3. **Function Calls**:
   - Ensured proper return paths between functions.

4. **Index Errors**:
   - Fixed bugs in navigation (e.g., viewing more or previous tweets).

5. **Foreign Key Constraints**:
   - Resolved mismatches in SQL queries for consistent key relationships.

6. **SQL Commits**:
   - Verified all database commits were executed correctly.

7. **Integration Bugs**:
   - Aligned variable names and fixed compatibility issues during code consolidation.

---

## Group Work Strategy

### Team Members:
- **Khym Nad**:
  - Responsibilities: Search for users, Compose tweets.
  - Time Allocated: 20 hours.

- **Samuel Chan**:
  - Responsibilities: Login menu, Search for tweets.
  - Time Allocated: 20 hours.

- **Andrew Zhang**:
  - Responsibilities: Search for tweets, List followers.
  - Time Allocated: 20 hours.

### Collaboration:
- Regular in-person meetings on campus to review and integrate work.
- Peer reviews to ensure compatibility between functionalities.

---

## Conclusion
This project provides a simplified social media experience with robust features for user interaction and management. Its modular design and rigorous testing ensure smooth functionality, making it an excellent prototype for a larger application.
