from flask import Flask, request, redirect, render_template, session, flash
from validators import validate_title, validate_body, validate_verify_pw, validate_gen
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:root@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_title = db.Column(db.String(120))
    post_body = db.Column(db.String(5000))

    def __init__(self, post_title, post_body, owner):
        self.post_title = post_title
        self.post_body = post_body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    posts = db.relationship('Post', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'post', 'index', 'blog']
    if request.endpoint not in allowed_routes and 'username' not in session:
        flash("Must be logged in")
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session["username"] = username
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist')

    return render_template('login.html')


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_pw = request.form['verify_pw']

        username_error = validate_gen(username)
        password_error = validate_gen(password)
        verify_pw_error = validate_verify_pw(password, verify_pw)

        if username_error or password_error:
            flash(username_error)
            return render_template("signup.html", username=username)

        if verify_pw_error:
            flash(verify_pw_error)
            return render_template("signup.html", username=username)

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            flash("Don't be a copycat, try a different username")

    return render_template('signup.html')


@app.route('/', methods=['POST', 'GET'])
def index():

    users = User.query.all()

    return render_template("index.html", users=users)


@app.route('/blog', methods=['POST', 'GET'])
def blog():
    
    #posts = Post.query.all()
    #return render_template('blog.html', title="build a blog", posts=posts) 

    post_id = request.args.get("postid")
    user_id = request.args.get("userid")

    posts = []
    title = "Blog!"

    # if query string, find single post; else, display all non-removed posts
    if post_id:
        posts = Post.query.filter_by(id=int(post_id)).all()
    elif user_id:
        posts = Post.query.filter_by(owner_id=int(user_id)).all()
    else:
        posts = Post.query.order_by(Post.id.desc()).all()

    return render_template('blog.html', title=title, posts=posts)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    owner = User.query.filter_by(username=session["username"]).first()

    if request.method == 'POST':
        post_title = request.form['post_title']
        post_body = request.form['post_body']

        title_error = validate_title(post_title)
        body_error = validate_body(post_body)       

        if title_error or body_error:
            if title_error:
                flash(title_error)
            if body_error:
                flash(body_error)
            return render_template('newpost.html', title="New Post!"
                                                 , post_title=post_title
                                                 , post_body=post_body)        
        else:
            new_post = Post(post_title, post_body, owner)
            db.session.add(new_post)
            db.session.commit()

            post_ids = db.session.query(Post.id).order_by(Post.id).all()
            post_id = post_ids[len(post_ids)-1][0]
            return redirect('/post?id=' + str(post_id))

    return render_template('newpost.html') 


@app.route('/post', methods=['GET'])
def post():
    post_id = request.args.get('id')

    posts = []

    if post_id:
        posts = Post.query.filter_by(id=int(post_id)).all()

    return render_template('post.html', title='Posty Post', posts=posts) 


if __name__ == '__main__':
    app.run()