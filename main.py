#Main = Controller

@app.route('/', methods = ['POST','GET'])
def index():
    return redirect('/blog')

@app.route('/newpost', methods = ['POST','GET'])
def create_post():
    if request.method == 'POST':
        blog_title = request.form['blog-title']
        blog_body = request.form['blog-body']
        blog_author = user.query('username')
        title_error = ''
        body_error = ''
        author_error = ''

        if not blog_title:
            title_error = "All posts need titles, give it one!"
        
        if not blog_body:
            body_error = "You can't have a blog post without a post, get writing!"

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

@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(username = username).first()
        if not existing_user:

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
            if password == user.password:
                session['user'] = user.username
                flash('Welcome back, ' + user.username)
                return redirect("/")
        flash('Incorrect username or password')
        return redirect('/login')
            
    

if __name__ == "__main__":
    app.run()