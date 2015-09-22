'''

By Terrance Liu 43267483 COMP249 2014


'''

import os
import cgi
from templating import render
import database
import interface
import users

# global variable
STATIC_URL_PREFIX = '/static/'

# dictionary of file extensions
MIME_TABLE = {'.txt': 'text/plain',
              '.html': 'text/html',
              '.css': 'text/css',
              '.jpg': 'image/jpeg',
              '.png': 'image/png',
              '.js': 'application/javascript',
             }    

# gets images, dates, names, comments and image location for index page 
def get_content():
    image_list = interface.list_images(db, 3)
    item =''
    # constructs html for each image div
    for index in range(len(image_list)):
        comments = '<ul>'
        item += '<div class="flowtow">'
        item += '<span class="date"> '+ image_list[index][1] + '</span>'
        item += '<span class="name"> '+ image_list[index][2] + '</span>'
        item += '<img src="/static/images/' + image_list[index][0] + '">'
        # loop to show comments
        for comment in range(len(image_list[index][3])):
            comments = comments + '<li>' + image_list[index][3][comment] + '</li>'
        item += '<div class="comments">'+ comments + '</ul></div>'
        # creates a form for commenting
        item += """<form method="post" action="/add_comment"> 
                        <input type="hidden" name="image" value="""+image_list[index][0]+""">
                        <input type="text" class="form-control" name="comment" id="comment" placeholder="Enter your comment here"><br>
                        <input type="submit" class="btn btn-primary" value="Submit">
                        </form></div>"""
    return item

# function for displaying images only uploaded by the logged in/current user
def my_content(environ):
    # gets current logged in user
    current_user = users.user_from_cookie(db, environ)    
    image_list = interface.list_images_for_user(db, current_user)
    result = []
    for index in range(len(image_list)):
        comments = interface.list_comments(db, image_list[index][0])
        new_row = image_list[index] + (comments,)
        result.append(new_row)
    image_list = result
    # html form for image upload
    item ="""<div class="well uploadform">
    <form id="uploadform" method="post" action="/upload" enctype="multipart/form-data">
    <fieldset class="form-group">
      <legend>Upload New Image</legend>
       <input class="form-control" type="file" name="file">
       <input type="hidden" name="user" value="""+ current_user +""">
       <br><div class="text-center"><input class="btn btn-primary" type="submit" value="Upload File"></div>
      </fieldset>
    </form>  
    </div> 
    """
    # constructs html for each image div
    for index in range(len(image_list)):
        comments = '<ul>'
        item += '<div class="flowtow">'
        item += '<span class="date"> '+ image_list[index][1] + '</span>'
        item += '<span class="name"> '+ image_list[index][2] + '</span>'
        item += '<img src="/static/images/' + image_list[index][0] + '">'
        for comment in range(len(image_list[index][3])):
            comments = comments + '<li>' + image_list[index][3][comment] + '</li>'
        item += '<div class="comments">'+ comments + '</ul></div>'
        # creates a form for commenting
        item += """<form method="post" action="/add_comment"> 
                        <input type="hidden" name="image" value="""+image_list[index][0]+""">
                        <input type="text" class="form-control" name="comment" id="comment" placeholder="Enter your comment here"><br>
                        <input type="submit" class="btn btn-primary" value="Submit">
                        </form></div>"""
    return item

# login_page = """<html><h1>LOGGED IN</h1><p>
#                 asdugasdualuslkgbak <a href="/">Home</a>
#                 </p></html>"""

# the navbar is separated into sections
# When a user is not logged in, it will not display the "My Images" link
# login form is displayed  
def get_navbar(environ):
    current_user = users.user_from_cookie(db, environ) 
    navbar_1 =  """<div class="collapse navbar-collapse">
                <ul class="nav navbar-nav">
            <li><a href="/">Home</a></li><li><a href="/about.html">About</a></li>"""
    if current_user == None:
        my_images = """ """
        form = """<form id='loginform' class="navbar-form navbar-right" role="login" method='post' action='/login'>
                <div class="form-group">
                  <input type="text" name='email' class="form-control" placeholder="Email">
                </div>
                <div class="form-group">
                  <input type="password" name='password' class="form-control" placeholder="Password">
                </div>                
                <input type="submit" class="btn btn-default" value='Login' >
        </form>"""
    # if user is logged in, logged in user is shown, my image link and logout button
    else:
        my_images = """<li><a href="/my">My Images</a></li>""" 
        form = """<form id='logoutform' class="navbar-form navbar-right pull-right" role="logout" method='post' action='/logout'>
            <input type="submit" class="btn btn-default" name='logout' value='Logout' >
        </form>
     
        <div class='navbar-text pull-right'>Logged in as """  + current_user + """</div>"""   
    navbar_2 = """</ul>"""
    return navbar_1 + my_images + navbar_2 + form + """</div>"""


def not_found(environ, start_response):
    start_response('404 Not Found', [('content-type','text/html')])
    # contents of 'Page not Found'
    not_found_page = """<html><h1>Page not Found</h1><p>
                That page is unknown. Return to the <a href="/">Home</a>
                </p></html>"""
    return [not_found_page.encode(),]  

def index(environ, start_response):
    content = "<p>Hello World!</p>"
    mapping = {
               'title': 'Welcome to FlowTow',
                 'content': get_content(),
                'navbar': get_navbar(environ),}
    start_response("200 OK", [('content-type', 'text/html')])
    return render('index.html', mapping)

def about(environ, start_response):
    content = "<p>About this </p>"
    mapping = {
               'title': 'About',
                'content': content,
                'navbar': get_navbar(environ),}
    start_response("200 OK", [('content-type', 'text/html')])
    return render('about.html', mapping)

# function to get My images
def my(environ, start_response):
    current_user = users.user_from_cookie(db, environ) 
    if current_user != None:
        content = "<p>Hello World!</p>"
        mapping = {
                   'title': 'Welcome to FlowTow',
                     'content': my_content(environ),
                    'navbar': get_navbar(environ),}
        start_response("200 OK", [('content-type', 'text/html')])
        return render('index.html', mapping)
    else:
        return index(environ, start_response)

def add_comment(environ, start_response):
    formdata = cgi.FieldStorage(environ=environ, fp=environ['wsgi.input'])
    if 'comment' in formdata:
        image = formdata.getvalue("image","")
        comment = formdata.getvalue("comment","")
        interface.add_comment(db, image, cgi.escape(comment))
    start_response("301 Redirect", [('content-type', 'text/html')])
    return [redirect_page.encode(),] 

# refresh page
redirect_page = """<html><head><meta http-equiv="refresh" content="0; url=/" />
                </head></html>"""

def upload(environ, start_response):
    current_user = users.user_from_cookie(db, environ) 
    formdata = cgi.FieldStorage(environ=environ, fp=environ['wsgi.input'])
    if 'file' in formdata and formdata['file'].filename != '':
        file_data = formdata['file'].file.read()
        filename = formdata['file'].filename
        # write the content of the uploaded file to the static image directory
        target = os.path.join('static/images', filename)
        f = open(target, 'wb')
        f.write(file_data)
        f.close()        
        interface.add_image(db, filename, current_user)
    start_response("301 Redirect", [('content-type', 'text/html')])
    # refresh my_page
    redirect_my_page = """<html><head><meta http-equiv="refresh" content="0; url=/my" />
                </head></html>"""
    return [redirect_my_page.encode(),] 

def login(environ, start_response):
    success = False
    headers = [('content-type', 'text/html')]
    formdata = cgi.FieldStorage(environ=environ, fp=environ['wsgi.input'])
    if 'password' in formdata:
        email = formdata.getvalue("email","")
        password = formdata.getvalue("password","")
        success = users.check_login(db, email, password)
    # login is successful, creates a cookie
    if success:
        cookie = users.generate_session(db, email)
        headers.append(('Set-Cookie', cookie['sessionid'].OutputString()))
        headers.append(("Location", "/"))
        start_response('303 See Other', headers)
        return [redirect_page.encode(),]
    else:
        content = "Login problem"
        mapping = {
                   'title': 'Login',
                     'content': content,
                    'navbar': get_navbar(environ),}
    start_response('200 OK', headers)
    return render('login.html', mapping)

def logout(environ, start_response):
#     success = False
    current_user = users.user_from_cookie(db, environ) 
    headers = [('content-type', 'text/html')]
#     formdata = cgi.FieldStorage(environ=environ, fp=environ['wsgi.input'])
#     if 'password' in formdata:
#         email = formdata.getvalue("email","")
#         password = formdata.getvalue("password","")
#         success = users.check_login(db, email, password)
#     if success:
#         cookie = users.generate_session(db, email)
#         headers.append(('Set-Cookie', cookie['sessionid'].OutputString()))
#         headers.append(("Location", "/"))
    users.delete_session(db, current_user)
    start_response('303 See Other', headers)
    return [redirect_page.encode(),]
#     else:
#         content = "Login problem"
#         mapping = {
#                    'title': 'Login',
#                      'content': content,
#                     'navbar': get_navbar(environ),}
#     start_response('200 OK', headers)
#     return render('login.html', mapping)

def static_app(environ, start_response):
    """Serve static files from the directory named
    in STATIC_FILES"""
    
    path = environ['PATH_INFO']

    path = path[len(STATIC_URL_PREFIX):]
    path = os.path.join('static', path) 

    if os.path.exists(path):
        h = open(path, 'rb')
        content = h.read()
        h.close()
        
        headers = [('content-type', content_type(path))]
        start_response('200 OK', headers)
        return [content]
    else:
        return not_found(environ, start_response)


def content_type(path):
    """Return a guess at the mime type for this path
    based on the file extension"""
    
    name, ext = os.path.splitext(path)
    
    if ext in MIME_TABLE:
        return MIME_TABLE[ext]
    else:
        return "application/octet-stream"
    
    
def application(environ, start_response):
    """A simple application to return one of two pages
    based on the PATH_INFO environment setting"""   

    # based on PATH_INFO, choose which page to display
    if environ['PATH_INFO'] == '/':
        return index(environ, start_response)
    elif environ['PATH_INFO'] == '/add_comment':
        return add_comment(environ, start_response)
    elif environ['PATH_INFO'] == '/upload':
        return upload(environ, start_response)
    elif environ['PATH_INFO'] == '/login':
        return login(environ, start_response)
    elif environ['PATH_INFO'] == '/logout':
        return logout(environ, start_response)
    elif environ['PATH_INFO'] == '/my':
        return my(environ, start_response)
    elif environ['PATH_INFO'] == '/about.html':
        return about(environ, start_response)
    elif environ['PATH_INFO'].startswith(STATIC_URL_PREFIX):
        return static_app(environ, start_response)
    else:
        return not_found(environ, start_response)
   
    
if __name__ == '__main__':
    
    from wsgiref import simple_server
    
    # creates database, setups tables and inserts sample data
    db = database.COMP249Db()
    db.create_tables()
    db.sample_data()
    
    #starts server
    server = simple_server.make_server('localhost', 8000, application)
    print("listening on http://localhost:8000/ ...")
    server.serve_forever()
    
    