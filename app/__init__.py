from flask import Flask
from flask import render_template   
from flask_sqlalchemy import SQLAlchemy
from flask import request


from app.config.options import SQLALCHEMY_DATABASE_URI
from . import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config[config.options.DEBUG]

db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    body = db.Column(db.String(), unique=True)

    def __init__(self, title, body):
        self.title = title
        self.body = body

db.create_all()

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@app.route('/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get(post_id)
    return  render_template('post.html', post=post)

@app.route('/posts', methods=['POST'])
def create_post():
    if request.method == 'POST':
        title = request.args.get('title')
        body = request.args.get('body')
        post = Post(title, body)
        db.session.add(post)
        db.session.commit()
        return  'OK'
    return 'NOT OK'
