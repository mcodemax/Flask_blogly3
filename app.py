"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, PostTag, Tag


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:myPassword@localhost:5433/blogly' #@ people looking at this code; you may need to change on your own computer for code to work
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True #prints in ipython the queries being run

app.config["SECRET_KEY"] = "maxcode1"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

@app.route('/')
def show_title_get():

    #psql query the db and get a list of users


    return redirect("/users")



@app.route('/users')
def list_users():
    """Show all users.

    Make these links to view the detail page for the user.

    Have a link here to the add-user form.
    """
    
    users = User.query.all()

    
    
    return render_template("userlist.html", users=users)
#in ipython do db.session.execute('SELECt*from blah') and set to 
# a vars and put in a list to see the data


@app.route('/users/new')#method is get by default?
def add_user_form():
    """Show an add form for users"""


    return render_template('makeuser.html')

    

@app.route('/users/new', methods=["POST"])
def post_user():
    """Process the add form, adding a new user and going back to /users"""
    
    #get user data from post request from HTML form; ref forex project for refresher
    #user = User(name='input', first_name='see notes from above getting user data')
            #make sure to seperate logic n stuff above
    #then db.session.add(the above stuff)
    #then db.session.commit()

    #notes: you don't have to re add() a whole user once you commit it
        #you only have to commit() changes; you can call upon the user later again

    
    first_name = request.form.get("first-name")
    last_name = request.form.get("last-name")
    imglink = request.form.get("imglink")

    
    #seperate web interface from logic
    if '' in [first_name]:
        return redirect("/users/new")

    if '' in [imglink]:
        user = User(first_name=first_name, last_name=last_name)
    else:
        user = User(first_name=first_name, last_name=last_name, image_url=imglink)

    
    db.session.add(user)
    db.session.commit()

    return redirect("/users")



@app.route('/users/<int:user_num>', methods=["GET"])
def show_question(user_num):
    """Show information about the given user.

    Have a button to get to their edit page, and to delete the user.
    """
        
    user = User.query.get_or_404(user_num)
    
    return render_template('details.html',user=user)



@app.route('/users/<int:user_num>/edit', methods=["GET"])
def edit_user(user_num):
    """
    Show the edit page for a user.

    Have a cancel button that returns to the detail page for 
    a user, and a save button that updates the user.
    """
    # https://stackoverflow.com/questions/547821/two-submit-buttons-in-one-form

    user = User.query.get(user_num)

    return render_template('edituser.html',user_num=user_num, user=user)


@app.route('/users/<int:user_num>/edit', methods=["POST"])
def store_edits(user_num):
    """
    Process the edit form, returning the user to the /users page.
    """
    user = User.query.get_or_404(user_num)
    
    first_name = request.form.get("first-name")
    last_name = request.form.get("last-name")
    imglink = request.form.get("imglink")

    if len(first_name) > 50 or len(last_name) > 50 or len(imglink) > 5000:
        redir_txt = '/users/' + str(user_num) + "/edit"
        return redirect(redir_txt)

    if '' not in [first_name]:
        user.first_name = first_name

    if '' not in [last_name]:
        user.last_name = last_name

    if '' not in [imglink]:
        user.image_url = imglink   
    
    db.session.commit()

    return redirect('/users')



@app.route('/users/<int:user_num>/delete', methods=["POST"])
def delete_user(user_num):
    """
    Process the edit form, returning the user to the /users page.
    """
    user = User.query.get_or_404(user_num)

    db.session.delete(user)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_num>/posts/new')
def new_post_form(user_num):

    user = User.query.get_or_404(user_num)
    tags = Tag.query.all()

    return render_template('makepost.html',user=user,user_num=user_num,tags=tags)


@app.route('/users/<int:user_num>/posts/new', methods=["POST"])
def add_new_post(user_num):
    """Handle add form; add post and redirect to the user detail page."""

    user = User.query.get_or_404(user_num)
    tag_list = request.form.getlist("tags")
    

    title = request.form.get("title")
    content = request.form.get("content")
    
    #logic, error checking
    if '' in [title, content] or len(title) > 50 or len(content) > 5000: #bad to hardcore numbers; refactor possibly
        redir_route = '/users/' + str(user_num) + '/posts/new'
        return redirect(redir_route)

    new_post = Post(title=title, content=content, user_id=user_num)#idk if text needs to be paren or not


    for tag in tag_list:
        
        tag = Tag.query.filter(Tag.name == tag).first()
        
        new_post.tags.append(tag)    

        
    db.session.add(new_post)    
    db.session.commit()
    
    return render_template('details.html',user=user)


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show a post. Show buttons to edit and delete the post."""
    post = Post.query.get_or_404(post_id)
    

    # show al the tags for this post
    return render_template('viewpost.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """Show form to edit a post, and to cancel (back to user page)."""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template('editpost.html', post=post,tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """Handle editing of a post. Redirect back to the post view."""
    post = Post.query.get_or_404(post_id)

    title = request.form.get("title")
    content = request.form.get("content")
    tag_list = request.form.getlist("tags")
    tags = Tag.query.all()

    #query and search for checked tags, add if check marked, delete if not

    if len(title) > 50 or len(content) > 5000: #bad to hardcode numbers; refactor possibly
        redir_route = '/posts/' + str(post_id) + '/edit'
        return redirect(redir_route)
    
    if '' != title:
        post.title = title
        
    if '' != content:
        post.content = content

    
    
    # empty out all the tags in a post
    # select all PostTag where post = the one im editing, then delete them
    post_tags = PostTag.query.filter(PostTag.post_id == post.id).all()
    for tag in post_tags:
        db.session.delete(tag)
    

    # add back in all tags the user wants back in, via the app
    for tag in tag_list:
        tag = Tag.query.filter(Tag.name == tag).first()
        
        post.tags.append(tag)    
    

    db.session.commit()

    return redirect(f"/posts/{post_id}")
    


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):

    #make queries to do this
    post = Post.query.get_or_404(post_id)
    user = post.user

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user.id}")

@app.route('/tags')
def list_tags():
    """List all tags w/ links to tag detail page"""
    tag_list = Tag.query.all()
    
    return render_template('taglist.html', tag_list=tag_list)


@app.route('/tags/<int:tag_id>') #delete route not working yet cause cascade
def show_tag_details(tag_id):
    """show a tag's details
    Have links to edit form and to delete.
    """
    tag = Tag.query.get(tag_id)

    return render_template('tagdetails.html',tag=tag)

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    tag = Tag.query.get(tag_id)

    return render_template(f"edittag.html", tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def change_tag(tag_id):
    tag = Tag.query.get(tag_id)

    name = request.form.get("tag")

    if '' != name and len(name) <= 50:
        tag.name = name
        db.session.commit()
    else:
        flash(f"invalid tag change")
        redirect(f"/tags/{tag_id}/edit")

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete',methods=["POST"]) #delete route not working yet cause cascade
def delete_tag(tag_id):
    """delete a tag
    """
    tag = Tag.query.get(tag_id)

    try:
        db.session.delete(tag)
        db.session.commit()
    except:
        flash(f"Tag unable to be deleted")
        return redirect('/tags')
        
    return redirect('/tags')

@app.route('/tags/new')
def show_new_tag_form():

    return render_template('maketag.html')

@app.route('/tags/new', methods=["POST"])
def create_new_tag():
    
    name = request.form.get("tag")
    tag = Tag(name=name)

    if '' != name and len(name) <= 50:
        db.session.add(tag)
        db.session.commit()
    else:
        flash(f"invalid tag name add")
        redirect(f"/tags/new")
    
    return redirect('/tags')