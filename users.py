'''

By Terrance Liu 43267483 COMP249 2014


'''

import uuid
from http.cookies import SimpleCookie

# this variable MUST be used as the name for the cookie used by this application
COOKIE_NAME = 'sessionid'

# checks if the useremail is in the users database
def check_user(db, useremail):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email = (?)", (useremail,))
    result = False
    #if useremail is in table, returns true
    for row in cursor:
        result = True
    return result

# checks the sessions table if a user is logged in
def user_active(db, useremail):
    cursor = db.cursor()
    cursor.execute("SELECT sessionid FROM sessions WHERE useremail = (?)", (useremail,))
    result = cursor.fetchone()
    if result != None:
        return result[0]
    return None

# checks if the useremail and password are correct by querying the database
def check_login(db, useremail, password):
    """returns True if password matches stored"""
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE (email = (?) AND password = (?))", (useremail, db.crypt(password)))
    result = False
    for row in cursor:
        result = True
    return result

def generate_session(db, useremail):
    """create a new session, return a cookie obj with session key
    user must be a valid user in the database, if not, return None
    There should only be one session per user at any time, if there
    is already a session active, the cookie should use the existing
    sessionid
    """
    if check_user(db, useremail):
        cookie = SimpleCookie()
        old_key = user_active(db, useremail)
        if old_key != None:
            cookie[COOKIE_NAME] = old_key
        else:
            # use the uuid library to make the random key
            new_key = str(uuid.uuid4())
            cur = db.cursor()
            # store this new session key in the database with no likes in the value
            cur.execute("INSERT INTO sessions VALUES (?, ?)", (new_key, useremail,))
            db.commit()
        
            # store this new session key in the database with no likes in the value
            cookie[COOKIE_NAME] = new_key
            
        return (cookie)
    else:
        return None
    

def delete_session(db, useremail):
    """remove all session table entries for this user"""
    cursor = db.cursor()
    cursor.execute("DELETE FROM sessions WHERE useremail = (?)", (useremail,))
    return ""

def user_from_cookie(db, environ):
    """check whether HTTP_COOKIE set, if it is,
    and if our cookie is present, try to
    retrieve the user email from the sessions table
    return useremail or None if no valid session is present"""

    if 'HTTP_COOKIE' in environ:
        cookie = SimpleCookie(environ['HTTP_COOKIE'])
        if 'sessionid' in cookie:
            sessionkey = cookie['sessionid'].value
            cursor = db.cursor()
            cursor.execute("SELECT useremail FROM sessions WHERE sessionid = (?)", (sessionkey,))
            result = cursor.fetchone()
            if result != None:
                return result[0]
    return None    


