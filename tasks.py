
from celery import Celery
from models import Session, NewsArticle
from parser import parse_rss_feeds, get_clean_content
from nltk import classify
import logging
import nltk

# Load the trained classifier
with open('nlp_classifier.pickle', 'rb') as file:
    classifier = nltk.load(file)

app = Celery('tasks', broker='pyamqp://guest@localhost//')
# Configure logging
logging.basicConfig(filename='tasks.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.task
def process_news_articles(feeds):
    try:
        articles = parse_rss_feeds(feeds)

        for article in articles:
            session = Session()
            existing_article = session.query(NewsArticle).filter_by(hash_id=article['hash_id']).first()

            if not existing_article:
                new_article = NewsArticle(**article)
                session.add(new_article)
                session.commit()

                categorize_article.delay(new_article.hash_id)

            session.close()

        logging.info("News articles processed successfully")
    except Exception as e:
        logging.error(f"Error processing news articles: {str(e)}")

@app.task
def categorize_article(hash_id):
    try:
        session = Session()
        article = session.query(NewsArticle).filter_by(hash_id=hash_id).first()

        # Use the trained classifier to predict the category
        article.category = classifier.classify(preprocess_text(article.content))

        session.commit()
        session.close()

        logging.info(f"Article categorized successfully: {hash_id}")
    except Exception as e:
        logging.error(f"Error categorizing article {hash_id}: {str(e)}")
