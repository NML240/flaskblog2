from flask import flash, Blueprint, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from app import db
from app.models import User, Posts
from app.postinfo.forms import (Postform)


# make @postinfo work from postinfo folder
postinfo = Blueprint('postinfo', __name__)


@postinfo.route("/post/new", methods = ['POST', 'GET'])
@login_required
# why do I need to link to the name of the function in the html? Ex new_post 
def new_post(): 
    form = Postform()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        # This works because I am using the user.id for the foreign key in the Post database.                 
        posts = Posts(title=title, content=content, user_id=current_user.id)
        db.session.add(posts)  
        db.session.commit()

        flash('You have posted successfully')
        return redirect(url_for('userinfo.home'))

    
    return render_template('new_post.html',title='new post', form=form)



# The reason you have post_id is because you only want to edit 1 post at a time. 
# If you leave out post_id you would edit every posts. 
@postinfo.route("/post/edit/<int:post_id>", methods = ['POST', 'GET'])
# edit/update posts
@login_required
def edit_post(post_id): 
    form = Postform() 
    if form.validate_on_submit(): 
        title = form.title.data
        content = form.content.data 
        posts = Posts(title=title, content=content, user_id=current_user.id)
        db.session.add(posts)  
        # date_posted = form.content.data
        db.session.commit()
        flash('You have edited your post successfully')
        return redirect(url_for('userinfo.home'))
        # todo I need to add so you can see the title and the post when editing it.  How?
    return render_template('new_post.html', title='edit post', post_id=post_id, form=form) 


# Can I go ("/post/<int:post_id>/delete") instead of below? 
@postinfo.route("/post/delete/<int:post_id>", methods = ['POST', 'GET'])
@login_required
def delete_post(post_id): 
    form = Postform()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data 
        db_post_info = Posts(title=title, content=content)
        db.session.delete(db_post_info)
        db.session.commit()
        flash('You have deleted your post')
    # where should this link to?
    return render_template('home.html', title='delete post', post_id=post_id, form=form)

# gives you ability to click on posts from home route and see the posts
# create the post/number route
# gets the posts number
@postinfo.route("/post/<int:post_id>", methods = ['POST', 'GET'])
def post(post_id):
    # Pass on the Posts database to the post_number variable. If the post doesn't exist get 404 error
    # The reason I don't use Posts.id is because I want a certain "Posts database id". 
    post = Posts.query.get_or_404(post_id)
    # Do I need to pass on post_id 
    return render_template('post.html', post=post, post_id=post_id, title='post')





















