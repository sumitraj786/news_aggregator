# parser.py

import feedparser
from hashlib import md5
import logging
from bs4 import BeautifulSoup

def parse_rss_feeds(feeds):
    articles = []
    
    for feed_url in feeds:
        try:
            feed = feedparser.parse(feed_url)
        except Exception as e:
            logging.error(f"Error parsing feed {feed_url}: {str(e)}")
            continue

        for entry in feed.entries:
            title = entry.title
            content = get_clean_content(entry)
            pub_date = entry.published
            source_url = entry.link
            hash_id = md5(f"{title}{pub_date}".encode()).hexdigest()  # Unique identifier
            
            articles.append({
                'hash_id': hash_id,
                'title': title,
                'content': content,
                'pub_date': pub_date,
                'source_url': source_url,
                'category': None  # Will be assigned later
            })

    return articles

def get_clean_content(entry):
    content = entry.content[0].value if 'content' in entry and entry.content else entry.summary

    # Use BeautifulSoup to clean HTML tags
    soup = BeautifulSoup(content, 'html.parser')
    cleaned_content = soup.get_text(separator='\n', strip=True)

    return cleaned_content
