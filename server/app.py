from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate
from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\ad|eQ\x80t \ca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

MAX_PAGE_VIEWS = 3

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    # Implement the logic for the /articles route
    pass

@app.route('/articles/<int:id>')
def show_article(id):
    # Initialize page_views if it doesn't exist in the session
    session['page_views'] = session.get('page_views', 0)

    # Increment the page_views counter
    session['page_views'] += 1

    # Check if the user has reached the maximum pageview limit
    if session['page_views'] <= MAX_PAGE_VIEWS:
        # Render the article data as a JSON response
        article = Article.query.get(id)
        if article:
            return jsonify({
                'id': article.id,
                'title': article.title,
                'content': article.content
            })
        else:
            return jsonify({'message': 'Article not found'}), 404
    else:
        # Render an error message as a JSON response with a 401 Unauthorized status code
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

if __name__ == '__main__':
    app.run(port=5555)
