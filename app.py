"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post, PostTag, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False



@app.route('/')
def list_users():
    '''Lists users and shows add form'''

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/add_user')
def show_add_form():
    return render_template("add_user.html")


@app.route('/add_user', methods=['POST'])
def add_user():
    '''Add a profile'''
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url']

    if first_name or last_name != "":
       user = User(first_name=first_name, last_name=last_name, img_url=img_url)
       db.session.add(user)
       db.session.commit()
 
    else:
        
        flash("Please enter a valid full name")
        return redirect("/")

    return redirect("/")


@app.route('/<int:user_id>')
def show_user_profile(user_id):
    '''Show user profile'''
    user = User.query.get_or_404(user_id)
    return render_template("profile.html", user=user)


@app.route('/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    '''Delete user'''
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')


@app.route('/edit_profile/<int:user_id>')
def show_edit_form(user_id):
    '''Show edit profile form'''
    user = User.query.get_or_404(user_id)
    return render_template("edit_profile.html", user=user)


@app.route('/edit_profile/<int:user_id>', methods=['POST'])
def edit_profile(user_id):
    '''Edit profile'''
    user = User.query.get_or_404(user_id)

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    img_url = request.form.get('img_url')

    if first_name != "":
        user.first_name = first_name
    if last_name != "":
        user.last_name = last_name
    if img_url != "":
        user.img_url = img_url

    db.session.add(user)
    db.session.commit()
    return redirect('/')


@app.route("/post-page/<int:user_id>")
def show_post_page(user_id):
    '''Show post page'''
    user = User.query.get_or_404(user_id)
    return render_template("post_page.html", user=user)


@app.route("/post-page/<int:user_id>", methods=['POST'])
def add_post(user_id):
    user = User.query.get_or_404(user_id)
    
    title = request.form['title']
    content = request.form['content']

    if title or content != "":
       post = Post(title=title, content=content)
       db.session.add(post)
       db.session.commit()
    #    db.session.add(user)
    #    db.session.commit()
       flash("New post added")
       return redirect(f"/{user.id}")
 
    else:
        
        flash("Please enter a valid post")
        return redirect(f"/{user.id}")


@app.route("/<int:post_id>")
def show_post(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template("post.html", post=post)

@app.route("/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/{post.user_id}')

@app.route('/edit_post/<int:post_id>')
def get_edit_post_page(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("edit_post.html", post=post)

@app.route('/edit_post/<int:post_id>', methods=['POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    title = request.form.get('title')
    content = request.form.get('content')

    if title != "":
        post.title = title
    if content != "":
        post.content = content

    db.session.add(post)
    db.session.commit()

    return redirect("/<int:post_id>")


@app.route('/tags')
def tags_index():
    """Show a page with info on all tags"""

    tags = Tag.query.all()
    return render_template('tag_list.html', tags=tags)


@app.route('/tags/new')
def tags_new_form():
    """Show a form to create a new tag"""

    posts = Post.query.all()
    return render_template('make_tag.html', posts=posts)


@app.route("/tags/new", methods=["POST"])
def tags_new():
    """Handle form submission for creating a new tag"""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}' added.")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>')
def tags_show(tag_id):
    """Show a page with info on a specific tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):
    """Show a form to edit an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('edit_tag.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tags_edit(tag_id):
    """Handle form submission for updating an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited.")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tags_destroy(tag_id):
    """Handle form submission for deleting an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' deleted.")

    return redirect("/tags")