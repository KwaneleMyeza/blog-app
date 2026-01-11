from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from app.models import Post
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('home.html', posts=posts)

@main_bp.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get(post_id)

    if post is None:
        abort(404)

    return render_template('post_detail.html', post=post)

@main_bp.route("/post/new", methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        if not title or not content:
            flash("Title and content are required.", "danger")
            return redirect(url_for("main.create_post"))

        post = Post(title=title, content=content)
        db.session.add(post)
        db.session.commit()

        flash("Post created successfully!", "success")
        return redirect(url_for("main.home"))

    return render_template("create_post.html")
