'''

By Terrance Liu 43267483 COMP249 2014


'''

import time

def list_comments(db, filename):
    """Return a list of the comments stored for this image filename"""
    cursor = db.cursor()
    cursor.execute("SELECT comment FROM comments where filename = (?)", (filename,))
    result = []
    for row in cursor:
        result.append(row[0])
    return result

def add_comment(db, filename, comment):
    """Add this comment to the database for this image filename"""
    cursor = db.cursor()
    cursor.execute("INSERT INTO comments ( filename, comment ) Values ( ?, ?)", (filename, comment))
    db.commit()
    
def list_images(db, n):
    """Return a list of tuples for the first 'n' images in 
    order of date.  Tuples should contain (filename, date, useremail, comments)."""
    cursor = db.cursor()
    cursor.execute("SELECT filename, date, useremail FROM images ORDER BY date desc limit (?)", (n,))
    result = []
    # adds comments as 4th element
    for row in cursor:
        comments = list_comments(db, row[0])
        new_row = row + (comments,)
        result.append(new_row)
    return result

def list_images_for_user(db, useremail):
    """Return a list of tuples for the images belonging to this user.
    Tuples should contain (filename, date, useremail)."""
    cursor = db.cursor()
    cursor.execute("SELECT filename, date, useremail FROM images WHERE useremail = (?) ORDER BY date desc", (useremail,))
    result = []
    # adds comments as 4th element
    for row in cursor:
        result.append(row)
    return result

def list_only_images(db, n):
    """Return a list of tuples for the first 'n' images in 
    order of date.  Tuples should contain (filename, date, useremail)."""
    cursor = db.cursor()
    cursor.execute("SELECT filename, date, useremail FROM images ORDER BY date desc limit (?)", (n,))
    result = []
    for row in cursor:
        result.append(row)
    return result

def add_image(db, filename, useremail):
    today = time.strftime("%Y-%m-%d")
    cursor = db.cursor()
    cursor.execute("INSERT INTO images ( filename, date, useremail) Values ( ?, ?, ?)", (filename, today, useremail))
    db.commit()


    
