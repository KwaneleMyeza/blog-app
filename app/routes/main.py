from flask import Blueprint, render_template, abort
from app.models import Post

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
