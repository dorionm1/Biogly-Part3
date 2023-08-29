"""Blogly application."""
from flask import Flask, render_template, request, redirect, jsonify
from models import db, connect_db, User, Post
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///biogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/user-create')
def show_create_form():
    user = User
    return render_template('user-create.html', user=user)

@app.route('/post-create/<int:id>')
def show_post_form(id):
    user = User.query.get(id)
    return render_template('post-create.html', user=user)

@app.route('/user-edit/<int:id>')
def edit_user_page(id):
    user = User.query.get(id)
    return render_template('user-edit.html', user=user)

@app.route('/post-edit/<int:id>')
def edit_user_post(id):
    post = Post.query.get(id)
    return render_template('post-edit.html', post=post)

@app.route('/edit-complete/<int:id>', methods=['POST'])
def edit_user_task(id):
    user = User.query.get(id)
    new_first = request.form.get('first_name')
    new_last = request.form.get('last_name')
    new_url = request.form.get('image_url')

    user.first_name = new_first
    user.last_name = new_last
    user.image_url = new_url

    db.session.commit()

    return redirect(f'/{id}')

@app.route('/edit-post-complete/<int:id>', methods=['POST'])
def edit_post_task(id):
    post = Post.query.get(id)
    new_title = request.form.get('title')
    new_content = request.form.get('content')

    post.title = new_title
    post.content = new_content

    db.session.commit()

    return redirect(f'/post/{id}')

@app.route('/user-list')
def show_list():
    """Shows list of all users in db"""
    users = User.query.all()
    return render_template('user-list.html', users=users)

@app.route('/<int:id>')
def show_user_detail(id):
    """Show details of a single user"""
    user = User.query.get(id)
    posts = Post.query.filter_by(user_id=id)

    return render_template('user-detail.html', user=user, posts=posts)

@app.route('/post/<int:id>')
def show_post_detail(id):
    post = Post.query.get(id)

    return render_template('post-detail.html', post=post)  

@app.route('/user-detail', methods=['POST'])
def create_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    users = User.query.all()    
    latest_id= users[-1].id

    return redirect(f'/{latest_id}')

@app.route('/create-post/<int:id>', methods=['POST'])
def create_post(id):
    user = User.query.get(id)
    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(user=user,title=title, content=content)
    db.session.add(new_post)
    db.session.commit()

    return redirect("/user-list")

@app.route('/remove-user/<int:id>')
def remove_user(id):
    User.query.filter_by(id=id).delete()

    db.session.commit()

    return redirect('/user-list')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

