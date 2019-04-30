#Main = Controller
from flask import request, redirect, render_template, session, flash
import cgi
from app import app, db
from model import User, Blog
from hashutils import make_password_hash, check_password_hash


@app.route('/', methods = ['POST','GET'])
def index():
    return redirect('/blog')

@app.route('/newpost', methods = ['POST','GET'])
def create_post():
    if request.method == 'POST':
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

@app.route('/blog')
def blog():
    blog_id = request.args.get('id')
    
    if not blog_id:
        posts = Blog.query.all()
        return render_template('blog.html', posts = posts, title = "Blog Yo' Self!")
    else:
        post = Blog.query.get(blog_id)
        return render_template('post.html', post = post, title = 'Blog post')

@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        username_db_count = User.query.filter_by(username=username).count()
        if not username:
            flash('Aw come on, put in a username!')
            return redirect('/signup')
        if username_db_count > 0:
            flash('Uh Oh! That ' + username + ' is already taken!')
            return redirect('/signup')
        if password != verify:
            flash('Passwords did not match. They have to match!')
            return redirect('/signup')
        user = User(username=username, hashword=password)
        db.session.add(user)
        db.session.commit()
        session['user'] = user.username
        return redirect("/")
    else:
        return render_template('signup.html')


@app.route('/login', methods = ['POST', 'GET'])
def login():
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
                flash('Welcome back, ' + user.username)
                return redirect("/")
        flash('Incorrect username or password')
        return redirect('/login')
    
@app.route('/logout', methods = ['POST', 'GET'])
def logout():
    del session['user']
    return redirect('/')

def logged_in_user():
    owner = User.query.filter_by(username=session['user']).first()
    return owner

app.secret_key = 'supersecretunknownkeythatkeepseverythingsafebutnotreally'

if __name__ == "__main__":
    app.run()