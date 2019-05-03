#Main = Controller
from flask import request, redirect, render_template, session
import cgi
from app import app, db
from model import User, Blog
from hashutils import make_password_hash, check_password_hash

app.secret_key = 'supersecretunknownkeythatkeepseverythingsafebutnotreally'

@app.route('/')
def index():
    usernames = User.query.all()
    return render_template('index.html', usernames = usernames)

@app.route('/newpost', methods = ['POST','GET'])
def create_post():
    if request.method == 'POST':
        author = User.query.filter_by(username = session['user']).first()
        blog_title = request.form['blog-title']
        blog_body = request.form['blog-body']
        title_error = ''
        body_error = ''

        if not blog_title:
            title_error = "All posts need titles, give it one!"
        
        if not blog_body:
            body_error = "You can't have a blog post without a post, get writing!"

        if not title_error and not body_error:
            new_post = Blog(blog_title, blog_body, logged_in_user())
            db.session.add(new_post)
            db.session.commit()
            return redirect('/blog?id={}'.format(new_post.id))
        else:
            return render_template('newpost.html', title = "New Post", title_error = title_error, body_error = body_error, blog_title = blog_title, blog_body = blog_body)
    return render_template('newpost.html', title = 'New Post')

@app.route('/blog', methods = ['POST','GET'])
def blog():
    blogs = Blog.query.all()
    blog_id = request.args.get('id')
    user_id = request.args.get('user')
    user = User.query.get('username')

    if blog_id:
        blogpost = Blog.query.get(blog_id)
        return render_template('post.html', post = blogpost)

    if user_id:
        posts = Blog.query.filter_by(owner_id = user_id)
        username = User.query.get(user_id)
        return render_template('singleUser.html', user = username, posts = posts)

    return render_template('blog.html', posts = blogs, user = user)

@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    username_error = ''
    password_error = ''
    verify_password_error = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        username_exists = User.query.filter_by(username=username).first()

        if not username:
            username_error = 'Aw come on, put in a username!'
        if username_exists:
            username_error = 'Uh Oh! That name is already taken!'

        if password == '':
            password_error = 'You need to type in a password!'
        elif ' ' in password:
            password_error = 'Passwords may not contain spaces!'
        elif len(password) < 3:
            password_error = 'Passwords must be at least 3 characters long! At LEAST!'
        
        if password != verify:
            verify_password_error = 'Passwords did not match. They have to match!'
        elif verify == '':
            verify_password_error = 'Passwords did not match. They have to match!'

        if not username_exists and not username_error and not password_error and not verify_password_error:
            user = User(username = username, hashword = password)
            db.session.add(user)
            db.session.commit()
            session['user'] = user.username
            return redirect("/newpost")
    
        else:
            return render_template('signup.html', username_error = username_error, password_error = password_error, verify_password_error = verify_password_error, username = username, password = password, verify = verify)
    
    return render_template('signup.html')


@app.route('/login', methods = ['POST', 'GET'])
def login():
    login_error = ''
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = User.query.filter_by(username=username)
        if users.count() == 1:
            user = users.first()
            if check_password_hash(password, user.hashword):
                session['user'] = user.username
                return redirect("/")
            else:
                login_error = 'Incorrect username or password'
                return render_template('login.html', login_error = login_error)
    
@app.route('/logout', methods = ['POST', 'GET'])
def logout():
    del session['user']
    return redirect('/')

def logged_in_user():
    owner = User.query.filter_by(username=session['user']).first()
    return owner

@app.before_request
def require_login():
    allowed_routes = ['login','blog','index','signup']
    if request.endpoint not in allowed_routes and 'user' not in session:
        return redirect('/login')


if __name__ == "__main__":
    app.run()