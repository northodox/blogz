from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:terriblepassword@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    owner_id = db.Column(db.Integer, foreign_key = True)

    def __init__(self, title, body):
        self.title = title
        self.body = body

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(60))
    blogs = db.Column(db.Integer, foreign_key = True)

@app.route('/', methods = ['POST','GET'])
def index():
    return redirect('/blog')

@app.route('/newpost', methods = ['POST','GET'])
def create_post():
    if request.method == 'POST':
        blog_title = request.form['blog-title']
        blog_body = request.form['blog-body']
        blog_author = request.form['blog-author']
        title_error = ''
        body_error = ''
        author_error = ''

        if not blog_title:
            title_error = "All posts need titles, give it one!"
        
        if not blog_body:
            body_error = "You can't have a blog post without a post, get writing!"

        if not blog_author:
            author_error = "A person has a name. Write yours here!"

        if not title_error and not body_error and not author_error:
            new_post = Blog(blog_title, blog_body)
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

if __name__ == "__main__":
    app.run()