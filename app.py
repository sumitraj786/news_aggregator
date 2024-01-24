from flask import Flask, request, jsonify, send_file
from models import db, NewsArticle
import tasks
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sumitraj:12345@localhost/news_aggregator'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

class NewsArticle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)
    source_url = db.Column(db.String(255))
    category = db.Column(db.String(255))
    feed_title = db.Column(db.String(255))
    feed_description = db.Column(db.Text)
    feed_link = db.Column(db.String(255))

db.create_all()

@app.route('/parse_feeds', methods=['POST'])
def parse_feeds():
    try:
        feeds = request.json.get('feeds')
        if not feeds:
            return jsonify({'error': 'No feeds provided in the request.'}), 400

        for feed_data in feeds:
            feed_title = feed_data.get('title', '')
            feed_description = feed_data.get('description', '')
            feed_link = feed_data.get('link', '')

            tasks.parse_feeds.delay(feed_data)

        return jsonify({'message': 'Tasks submitted for processing.'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export_data', methods=['GET'])
def export_data():
    try:
        articles = NewsArticle.query.all()
        articles_data = []
        for article in articles:
            articles_data.append({
                'title': article.title,
                'content': article.content,
                'pub_date': str(article.pub_date),
                'source_url': article.source_url,
                'category': article.category,
                'feed': {
                    'title': article.feed_title,
                    'description': article.feed_description,
                    'link': article.feed_link,
                }
            })

        export_format = request.args.get('format', 'json')
        if export_format == 'csv':
            return jsonify({'error': 'CSV export not implemented yet!'}), 501
        elif export_format == 'sql':
            sql_dump = db.session.execute('SELECT * FROM news_articles;')
            return send_file(sql_dump, as_attachment=True, download_name='news_articles.sql')
        else:
            with open('output.json', 'a') as json_file:
            json.dump(articles_data, json_file)
            json_file.write('\n')
            return send_file('output.json', as_attachment=True, download_name='output.json')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
