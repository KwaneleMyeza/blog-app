from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Post
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('home.html', posts=posts)

@main_bp.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@main_bp.route("/post/new", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        if not title or not content:
            flash("Title and content are required.", "danger")
            return redirect(url_for("main.create_post"))

        post = Post(title=title, content=content, author=current_user)
        db.session.add(post)
        db.session.commit()

        flash("Post created successfully!", "success")
        return redirect(url_for("main.home"))

    return render_template("create_post.html")

@main_bp.route('/posts/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('main.home'))

@main_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not title or not content:
            flash('Title and content are required.', 'danger')
            return redirect(url_for('main.edit_post', post_id=post.id))

        post.title = title
        post.content = content
        db.session.commit()

        flash('Post updated successfully!', 'success')
        return redirect(url_for('main.post_detail', post_id=post.id))

    return render_template('create_post.html', post=post)
