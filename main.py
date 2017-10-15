from flask import Flask, request, redirect, render_template, session, flash
from validators import blank_post
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(5000))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/', methods=['POST', 'GET'])
def index():

    return render_template('blog.html',title='Build a Blog')


@app.route('/blog', methods=['POST', 'GET'])
def blog():

    if request.method == 'POST':
        post_id = int(request.form['post-id'])
        post = Post.query.get(post_id)
        db.session.add(post)
        db.session.commit()
    
    posts = Post.query.all()

    return render_template('blog.html', title='Build a Blog', posts=posts) 


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if blank_post(title) or blank_post(body) == True:
            flash("Post is missing title and body")
            #return render_template('newpost.html', title=title
                                                # , body=body)
            #return "<h1>ERROR</h1>"
        else:
            new_post = Post(title, body)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/blog')

    return render_template('newpost.html') 


@app.route('/post', methods=['GET'])
def post():
    title = request.args.get('title')
    body = request.args.get('body')
    
    return render_template('post.html') 


'''@app.route("/", methods=["POST"])
def validate_post():

    username = request.form["username"]
    password = request.form["password"]

    title_error = validators.validate_title(title)
    body_error = validators.validate_body(body)

    if not title_error and not body_error: 
        return render_template('newpost.html', post=post)
    else:
        return render_template('blog.html', title=title, body=body) 
'''

if __name__ == '__main__':
    app.run()