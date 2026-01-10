from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

# Placeholder posts
posts = [
    {"title": "First Post", "snippet": "This is the first post snippet."},
    {"title": "Second Post", "snippet": "This is the second post snippet."}
]

@main_bp.route('/')
def home():
    return render_template('post_list.html', posts=posts)
